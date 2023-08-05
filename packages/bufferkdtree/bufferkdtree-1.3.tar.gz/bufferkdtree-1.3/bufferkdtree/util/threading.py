#
# Copyright (C) 2013-2016 Fabian Gieseke <fabian.gieseke@di.ku.dk>
# License: GPL v2
#

import multiprocessing

def _wrapped_task(proc_num, task, args, kwargs, return_dict):

    return_dict[proc_num] = task(*args, **kwargs)
            
def start_via_single_process(task, args, kwargs):
    
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    proc_num = 0
    proc = multiprocessing.Process(target=_wrapped_task, args=(proc_num, task, args, kwargs, return_dict))
            
    proc.daemon = False
    proc.start()

    proc.join()

    return return_dict[proc_num]   