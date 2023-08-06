from collections import Iterable
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def w_stat_update(src, dst):
    for i in dst:
        src[i] = src.get(i, 0) + dst[i]
    return src

def w_stat(lst, parallel=1, words=None):
    """
    a word times stat.
    @parallel : set processer's number
    @words: only stat [words] 's stat from lst.
    """
    cl = {}
    if parallel == 1:
        if words:
            for i in lst:
                if i in words:
                    cl[i] = cl.get(i, 0) + 1

        else:
            for i in lst:
                cl[i] = cl.get(i, 0) + 1

        return cl
    elif parallel>1:
        pro = ProcessPoolExecutor(parallel)
        l = len(lst)
        c = round(l / parallel)
        last = lst[parallel * c:]
        w = words
        # update callback function 
        callback  = lambda x: w_stat_update(cl, x.result())
        
        for i in range(parallel):
            f = pro.submit(w_stat, lst[i * c: (i+1) *c], words=w)
            f.add_done_callback(callback)

        if last:
            f = pro.submit(w_stat, last, words=w)
            f.add_done_callback(callback)
        
        pro.shutdown()
            
        return cl


