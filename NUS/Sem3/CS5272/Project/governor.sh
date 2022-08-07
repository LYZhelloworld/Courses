#!/bin/bash
CPUFREQ=/sys/devices/system/cpu/cpufreq
PID=$(pgrep -f run\.sh)

echo 'userspace' > $CPUFREQ/policy0/scaling_governor
echo 'userspace' > $CPUFREQ/policy2/scaling_governor

cpu0_ismax () {
	freqs=($(cat $CPUFREQ/policy0/scaling_available_frequencies))
	current_freq=$(cat $CPUFREQ/policy0/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -ge $current_freq ]; then
			if [ $i = 10 ]; then
				echo 1
			else
				echo 0
			fi
			break
		fi
	done
}
cpu0_ismin () {
	freqs=($(cat $CPUFREQ/policy0/scaling_available_frequencies))
	current_freq=$(cat $CPUFREQ/policy0/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -le $current_freq ]; then
			if [ $i = 0 ]; then
				echo 1
			else
				echo 0
			fi
			break
		fi
	done
}
cpu2_ismax () {
	freqs=($(cat $CPUFREQ/policy2/scaling_available_frequencies))
	current_freq=$(cat $CPUFREQ/policy2/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -ge $current_freq ]; then
			if [ $i = 0 ]; then
				echo 1
			else
				echo 0
			fi
			break
		fi
	done
}
cpu2_ismin () {
	freqs=($(cat $CPUFREQ/policy2/scaling_available_frequencies))
	current_freq=$(cat $CPUFREQ/policy2/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -le $current_freq ]; then
			if [ $i = 0 ]; then
				echo 1
			else
				echo 0
			fi
			break
		fi
	done
}
increase_freq_0 () {
	freqs=($(cat $CPUFREQ/policy0/scaling_available_frequencies))
	#echo 'freqs='"${freqs[*]}"
	current_freq=$(cat $CPUFREQ/policy0/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -ge $current_freq ]; then
			echo "i=$i"
	       		current_freq="${freqs[$(expr $i + 1)]}"       
			break
		fi
	done
	echo "Increase CPU 0: $current_freq"
	echo $current_freq > $CPUFREQ/policy0/scaling_setspeed
}
increase_freq_2 () {
	freqs=($(cat $CPUFREQ/policy2/scaling_available_frequencies))
	#echo 'freqs='"${freqs[*]}"
	current_freq=$(cat $CPUFREQ/policy2/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -ge $current_freq ]; then
			echo "i=$i"
	       		current_freq="${freqs[$(expr $i + 1)]}"       
			break
		fi
	done
	echo "Increase CPU 2: $current_freq"
	echo $current_freq > $CPUFREQ/policy2/scaling_setspeed
}
decrease_freq_0 () {
	freqs=($(cat $CPUFREQ/policy0/scaling_available_frequencies))
	#echo 'freqs='"${freqs[*]}"
	current_freq=$(cat $CPUFREQ/policy0/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -le $current_freq ]; then
			#echo "i=$i"
	       		current_freq="${freqs[$(expr $i - 1)]}"       
			break
		fi
	done
	echo "Decrease CPU 0: $current_freq"
	echo $current_freq > $CPUFREQ/policy0/scaling_setspeed
}
decrease_freq_2 () {
	freqs=($(cat $CPUFREQ/policy2/scaling_available_frequencies))
	#echo 'freqs='"${freqs[*]}"
	current_freq=$(cat $CPUFREQ/policy2/cpuinfo_cur_freq)
	for i in "${!freqs[@]}"; do
		if [ "${freqs[$i]}" -le $current_freq ]; then
			#echo "i=$i"
	       		current_freq="${freqs[$(expr $i - 1)]}"       
			break
		fi
	done
	echo "Decrease CPU 2: $current_freq"
	echo $current_freq > $CPUFREQ/policy2/scaling_setspeed
}

while true; do
	if [ -e FCount.txt ]; then
		fcount=$(cat FCount.txt)
		sleep 1s
		fcount2=$(cat FCount.txt)
		result=$(expr $fcount2 - $fcount)
		echo $result
		echo $result > governor.txt

		if [ -e target.txt ]; then
			target=$(cat target.txt)
			if [ $result -lt $target ]; then
				if [ "$(cpu0_ismax)" = "0" ]; then
					increase_freq_0
				else
					taskset -p 0x2 "$PID"
				fi
			fi
			if [ $result -lt $target ]; then
				if [ "$(cpu2_ismax)" = "0" ]; then
					increase_freq_2
				fi
			fi
			if [ $result -gt $target ]; then
				if [ "$(cpu0_ismin)" = "0" ]; then
					decrease_freq_0
				fi
			fi
			if [ $result -gt $target ]; then
				if [ "$(cpu2_ismin)" = "0" ]; then
					decrease_freq_2
				else
					taskset -p 0x1 "$PID"
				fi
			fi
		fi
	fi
done
