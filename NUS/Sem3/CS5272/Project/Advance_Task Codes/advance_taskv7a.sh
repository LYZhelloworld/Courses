#!/bin/bash
CPUFREQ=/sys/devices/system/cpu/cpufreq
PID=$(pidof -s DisplayImage)

echo 'userspace' > $CPUFREQ/policy0/scaling_governor
echo 'userspace' > $CPUFREQ/policy2/scaling_governor

while true; do

		fcount=$(cat FCount.txt) #obtain first count value from object_detection
		sleep 1s                 #give period of 1s delay
		fcount2=$(cat FCount.txt) #obtain second count value from object_detection
		result=$(expr $fcount2 - $fcount) #calculate actual FPS
        target=$(cat target.txt) #obtain user defined target FPS
               
       if [ "$result" != "$target" ]; then #if actual FPS != target, 
           taskset -p 0x1 "$PID"          #set both CPU to lowest freq 
                                           #and set to A53
           echo 667000 > $CPUFREQ/policy0/scaling_setspeed
            echo 667000 > $CPUFREQ/policy2/scaling_setspeed
		    fcount=$(cat FCount.txt) 
		    sleep 1s                 
		    fcount2=$(cat FCount.txt) 
            result=$(expr $fcount2 - $fcount) 
            target=$(cat target.txt) 
       fi

            if [ $result -lt $target -o "$result" != "$target" ]; then
               echo 1000000 > $CPUFREQ/policy0/scaling_setspeed
               echo 667000 > $CPUFREQ/policy2/scaling_setspeed
		       fcount=$(cat FCount.txt) 
		       sleep 1s                 
		       fcount2=$(cat FCount.txt) 
               result=$(expr $fcount2 - $fcount) 
            fi 

            if [ $result -lt $target -o "$result" != "$target" ]; then
               echo 1200000 > $CPUFREQ/policy0/scaling_setspeed
               echo 667000 > $CPUFREQ/policy2/scaling_setspeed
		       fcount=$(cat FCount.txt) 
		       sleep 1s                 
		       fcount2=$(cat FCount.txt) 
               result=$(expr $fcount2 - $fcount) 
            fi

            if [ $result -lt $target -o "$result" != "$target" ]; then
               echo 1398000 > $CPUFREQ/policy0/scaling_setspeed
               echo 667000 > $CPUFREQ/policy2/scaling_setspeed
		       fcount=$(cat FCount.txt) 
		       sleep 1s                 
		       fcount2=$(cat FCount.txt) 
               result=$(expr $fcount2 - $fcount) 
            fi

            if [ $result -lt $target -o "$result" != "$target" ]; then
               echo 1512000 > $CPUFREQ/policy0/scaling_setspeed
               echo 667000 > $CPUFREQ/policy2/scaling_setspeed                 
		       fcount=$(cat FCount.txt) 
		       sleep 1s                 
		       fcount2=$(cat FCount.txt) 
               result=$(expr $fcount2 - $fcount) 
            fi

            if [ $result -lt $target -o "$result" != "$target" ]; then
               echo 1608000 > $CPUFREQ/policy0/scaling_setspeed
               echo 667000 > $CPUFREQ/policy2/scaling_setspeed 
		       fcount=$(cat FCount.txt) 
		       sleep 1s                 
		       fcount2=$(cat FCount.txt) 
               result=$(expr $fcount2 - $fcount) 
            fi

            if [ $result -lt $target -o "$result" != "$target" ]; then
               echo 1704000 > $CPUFREQ/policy0/scaling_setspeed
                echo 667000 > $CPUFREQ/policy2/scaling_setspeed 
		        fcount=$(cat FCount.txt) 
		        sleep 1s                 
		        fcount2=$(cat FCount.txt) 
                result=$(expr $fcount2 - $fcount) 
            fi

            if [ $result -lt $target -o "$result" != "$target" ]; then
               echo 1896000 > $CPUFREQ/policy0/scaling_setspeed
               echo 667000 > $CPUFREQ/policy2/scaling_setspeed 
            fi

       		    fcount=$(cat FCount.txt)
		        sleep 1s                 
		       fcount2=$(cat FCount.txt) 
               result=$(expr $fcount2 - $fcount) 
               target=$(cat target.txt) 

            if [ $result -lt $target ]; then
               taskset -p 0x4 "$PID"  #if max CPU freq reached, change to A73
                echo 667000 > $CPUFREQ/policy2/scaling_setspeed
                echo 667000 > $CPUFREQ/policy0/scaling_setspeed
               echo "Target FPS still not achieved. Migrating to A73"
            fi	

		        fcount=$(cat FCount.txt) 
		        sleep 1s                 
		        fcount2=$(cat FCount.txt) 
                result=$(expr $fcount2 - $fcount) 

            if [ "$result" != "$target" ]; then
               echo 1000000 > $CPUFREQ/policy2/scaling_setspeed
                echo 667000 > $CPUFREQ/policy0/scaling_setspeed
		        fcount=$(cat FCount.txt) 
		        sleep 1s                 
		        fcount2=$(cat FCount.txt) 
                result=$(expr $fcount2 - $fcount) 
            fi

            if [ "$result" != "$target" ]; then
               echo 1398000 > $CPUFREQ/policy2/scaling_setspeed
               echo 667000 > $CPUFREQ/policy0/scaling_setspeed
		        fcount=$(cat FCount.txt) 
		        sleep 1s                 
		        fcount2=$(cat FCount.txt) 
                result=$(expr $fcount2 - $fcount) 
            fi

            if [ "$result" != "$target" ]; then
               echo 1512000 > $CPUFREQ/policy2/scaling_setspeed
               echo 667000 > $CPUFREQ/policy0/scaling_setspeed
		        fcount=$(cat FCount.txt) 
		        sleep 1s                 
		        fcount2=$(cat FCount.txt) 
                result=$(expr $fcount2 - $fcount) 
            fi

            if [ "$result" != "$target" ]; then
               echo 1608000 > $CPUFREQ/policy2/scaling_setspeed
               echo 667000 > $CPUFREQ/policy0/scaling_setspeed
		        fcount=$(cat FCount.txt) 
		        sleep 1s                 
		        fcount2=$(cat FCount.txt) 
                result=$(expr $fcount2 - $fcount) 
            fi

            if [ "$result" != "$target" ]; then
               echo 1704000 > $CPUFREQ/policy2/scaling_setspeed
               echo 667000 > $CPUFREQ/policy0/scaling_setspeed
		        fcount=$(cat FCount.txt) 
		        sleep 1s                 
		        fcount2=$(cat FCount.txt) 
                result=$(expr $fcount2 - $fcount) 
            fi

            if [ "$result" != "$target" ]; then
               echo 1800000 > $CPUFREQ/policy2/scaling_setspeed
               echo 667000 > $CPUFREQ/policy0/scaling_setspeed
            fi

       		    fcount=$(cat FCount.txt)
		        sleep 1s                 
		       fcount2=$(cat FCount.txt) 
               result=$(expr $fcount2 - $fcount) 
               target=$(cat target.txt) 

            if [ "$result" == "$target"  ]; then #when target FPS achieved,  
               echo "Target FPS ACHIEVED!"  #next check scheduled 5s later
               echo "..."

               taskset -p "$PID"
               echo "Target FPS=$target"
			   echo "Actual FPS Achieved=$result"
               sleep 5
            fi
            
            taskset -p "$PID"
            echo "Target FPS=$target"
			echo "Actual FPS Achieved=$result"

	     echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
         echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
              
             sleep 1
done
