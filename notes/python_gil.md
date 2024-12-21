# Python Global Interpreter Lock, Multi processing and Multhreading

## Why GIL? 
Python uses reference counting for memory management. So this means that python will keep track of the amount of references to an object. When the amount of references to the object reach 0, that memory is released. 

So the problem is that this reference count needs protection from being controlled by more than one thread. If two threads start contributing to this ref count, you run into race conditions. 
One way you could fix it is adding locks to data structs, so a thread needs to unlock access to the count. But this can lead to deadlocks(if multiple locks), because you now start 



## Multithreading & Multiprocessing 

### What is multiprocessing 

### What is multithreading 

### When would you pick one over the other? 


## Async 

## why is async needed 

## 