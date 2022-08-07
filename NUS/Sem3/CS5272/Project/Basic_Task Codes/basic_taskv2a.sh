#!/bin/bash
CPUFREQ=/sys/devices/system/cpu/cpufreq
PID=$(pidof -s DisplayImage)

echo 'userspace' > $CPUFREQ/policy0/scaling_governor
echo 'userspace' > $CPUFREQ/policy2/scaling_governor

while true; do
	
	    cpu_type=$(cat cpu_type.txt)  #obtain user selected cpu type 0 or 2
        cpu_freq=$(cat cpu_freq.txt)  #obtain user selected cpu frequency   

	    if [ $cpu_type == 0 ]; then
           echo "Frequency Selected=$cpu_freq"
           echo "CPU Type Selected=$cpu_type"
           taskset -p 0x1 "$PID"   #set CPU to A53 Dual Core   
           echo $cpu_freq > $CPUFREQ/policy0/scaling_setspeed   #set CPU frequency
           echo "A53 CPU Frequency=$(cat $CPUFREQ/policy0/cpuinfo_cur_freq)"
		   fcount=$(cat FCount.txt)   #obtain first count value from    
                                      #object_detection
		   sleep 1s                   #give period of 1s delay
		   fcount2=$(cat FCount.txt)  #obtain second count value from
                                      #object_detection
		   result=$(expr $fcount2 - $fcount)  #calculate actual FPS
           echo "Actual FPS=$result"      
         fi    
	    
         if [ $cpu_type == 2 ]; then
            echo "Frequency Selected=$cpu_freq"
            echo "CPU Type Selected=$cpu_type"
            taskset -p 0x4 "$PID"   #set CPU to A73 Quad Core  
            echo $cpu_freq > $CPUFREQ/policy2/scaling_setspeed   #set CPU frequency
            echo "A73 CPU Frequency=$(cat $CPUFREQ/policy2/cpuinfo_cur_freq)"
		    fcount=$(cat FCount.txt)   #obtain first count value from 
                                       #object_detection
		sleep 1s                   #give period of 1s delay
		    fcount2=$(cat FCount.txt)  #obtain second count value from
                                       #object_detection
		    result=$(expr $fcount2 - $fcount)  #calculate actual FPS
            echo "Actual FPS=$result"      
         fi 
	     
         echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
         echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
         echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 

done
