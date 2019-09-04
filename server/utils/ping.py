import threading
import subprocess
import time
from queue import Queue

# 定义工作线程
WORD_THREAD = 50

# 将需要 ping 的 ip 加入队列
IP_QUEUE = Queue()
for i in range(1,255):
    IP_QUEUE.put('192.168.150.'+str(i))
# # 定义一个执行 ping 的函数
def ping_ip():
    while not IP_QUEUE.empty():
        ip = IP_QUEUE.get()
        res = subprocess.call('ping -n 2 -w 5 %s' % ip,stdout=subprocess.PIPE)  # linux 系统将 '-n' 替换成 '-c'
        # 打印运行结果
        print(ip,True if res == 0 else False)

def get_id(os):
    # 将需要 ping 的 ip 加入队列
    IP_QUEUE = Queue()
    result=[]
    for i in os:
        IP_QUEUE.put(i.ip)
    # 定义一个执行 ping 的函数
    def ping_ip():
        while not IP_QUEUE.empty():
            ip = IP_QUEUE.get()
            res = subprocess.call('ping -n 2 -w 5 %s' % ip, stdout=subprocess.PIPE)  # linux 系统将 '-n' 替换成 '-c'
            # 打印运行结果
            # print(ip, True if res == 0 else False,type(ip))
            result.append({"ip": ip, "result": str(True if res == 0 else False)})
    threads = []
    start_time = time.time()
    for i in range(WORD_THREAD):  # WORD_THREAD定义工作线程
        thread = threading.Thread(target=ping_ip)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('程序运行耗时：%s' % (time.time() - start_time))
    return result


if __name__ == '__main__':
    threads = []
    start_time = time.time()
    for i in range(WORD_THREAD):# WORD_THREAD定义工作线程
        thread = threading.Thread(target=ping_ip)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('程序运行耗时：%s' % (time.time() - start_time))