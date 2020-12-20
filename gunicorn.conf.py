import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
proc_name = 'user_service'
max_requests = 0  # num of request after which worker will restart (prevent memory leaks)
