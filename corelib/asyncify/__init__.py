from concurrent.futures import ThreadPoolExecutor
import psutil


cpu_executor = ThreadPoolExecutor(psutil.cpu_count())

io_executor = ThreadPoolExecutor(128)

rpc_service_executor = ThreadPoolExecutor(1)