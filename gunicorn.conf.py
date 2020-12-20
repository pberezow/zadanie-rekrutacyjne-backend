import multiprocessing
import os

port = os.environ.get('PORT', '8000')

bind = f'0.0.0.0:{port}'
workers = multiprocessing.cpu_count() * 2 + 1
proc_name = 'user_service'
max_requests = 0  # num of request after which worker will restart (prevent memory leaks)
