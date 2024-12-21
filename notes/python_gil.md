# Python Global Interpreter Lock, Multi processing and Multhreading

## Why GIL and what is it? 
Python uses reference counting for memory management. So this means that python will keep track of the amount of references to an object. When the amount of references to the object reach 0, that memory is released. When a variable goes out of scope, or is reassigned, we decrement the refence value. Once its 0, CPython runs the deallocator, and memory is freed

So the problem is that this reference count needs protection from being controlled by more than one thread. If two threads start contributing to this ref count, you run into race conditions. 
One way you could fix it is adding locks to data structs, so a thread needs to unlock access to the count. But this can lead to deadlocks(if multiple locks). 

The GIL acts as a *single* lock on the interpreter itself, so that any execution of python bytecode requires having control of this interpreter lock. This obviously stops deadlocks, but makes any CPU bound code single threaded. 

## (Cyclic)Garbage Collector 
The issue with reference counting by itself, is that you might end up with variables that have cyclic references. So if you end up even deleting the objects, they still maintin a reference to each other, leading to a cyclic ref. 
The GC detects this, and checks if variables are accessible from externalreferences and which ones are solely reachable by each other. 
So calling the GC is only really necessary if you end up in a space that you've cyclically referenced variables. 


## Multithreading & Multiprocessing 

### What is multiprocessing 

### What is multithreading 

### When would you pick one over the other? 


## Async 

## why is async needed 

## 