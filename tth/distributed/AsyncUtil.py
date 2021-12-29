import threading

def threaded(f):
    import Queue

    def wrapped_f(q, *args, **kwargs):
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        q = Queue.Queue()

        t = threading.Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = True
        t.start()
        t.result_queue = q        
        return t

    return wrap
    
def locked(f):
    def wrap(*args, **kwargs):
        with threading.Lock():
            return f(*args,**kwargs)
            
    return wrap 
