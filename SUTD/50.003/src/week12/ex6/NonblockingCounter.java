package week12.ex6;

import java.util.concurrent.atomic.AtomicStampedReference;

public class NonblockingCounter {
    private AtomicStampedReference<NonblockingCounter> value = new AtomicStampedReference<NonblockingCounter>(this, 0); 
    
    public int getValue() {
        return value.getStamp();
    }

    public int increment() {
        int oldValue; 
        do{
          oldValue = value.getStamp();
        } while (!value.compareAndSet(this, this, oldValue, oldValue + 1)); 
        return oldValue + 1;
    }
    
    public boolean isChanged(int lastValue) {
    	int oldValue = value.getStamp();
    	return !value.compareAndSet(this, this, lastValue, oldValue);
    }
}
