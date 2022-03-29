import threading
import types

def synchronized(func):
	
    func.__lock__ = threading.Lock()
		
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)


    return synced_func

def synchronized_method(method):
    
    outer_lock = threading.Lock()
    lock_name = "__"+method.__name__+"_lock"+"__"
    
    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)  

    return sync_method

def synchronized_with_attr(lock_name):
    
    def decorator(method):
			
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)
                
        return synced_method
		
    return decorator


def synchronized_with(lock):
    def decorator(func):
        def sync_func(*args, **kws):
            with lock:
                return func(*args, **kws)
        return sync_func
		
    return decorator


def synchronized_class(sync_class):
	
    lock = threading.RLock()
	
    orig_init = sync_class.__init__
    def __init__(self, *args, **kws):
        self.__lock__ = lock
        orig_init(self, *args, **kws)
    sync_class.__init__ = __init__
	
    for key in sync_class.__dict__:
        val = sync_class.__dict__[key]
        if type(val) is types.FunctionType:
            decorator = synchronized_with(lock)
            sync_class.__dict__[key] = decorator(val)
    
    return sync_class
