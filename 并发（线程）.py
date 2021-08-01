from threading import Thread
from time import time

import requests
from matplotlib import pyplot as plt


class ThreadTest(Thread):
    def __init__(self, func, args=()):
        '''
      :param func: 被测试的函数
      :param args: 被测试的函数的返回值
            '''

        super(ThreadTest, self).__init__()
        self.func = func
        self.args = args
        self.start_time = time()

    def run(self):
        self.result = self.func(*self.args)
        self.end_time = time()

    def getResult(self):
        try:
            return self.result
        except BaseException as e:
            return e.args[0]

    def getTotalTime(self):
        return self.end_time


def baidu():
    rep = requests.get('https://www.baidu.com')
    code = rep.status_code
    time = rep.elapsed.total_seconds()
    return code, time

def highConcurrent(count):
    bad_req = []
    tasks = []
    results = []
    code_ls = []
    time_ls = []
    list_count = []
    req_time = []

    start_time = time()
    for i in range(count):
        t = ThreadTest(func=baidu)
        t.start()
        tasks.append(t)

    for t in tasks:
        t.join()
        if t.getResult()[0] != 200:
            bad_req.append(t.getResult())
        results.append(t.getResult())
        req_time.append(t.getTotalTime() - start_time)

    # for res in results:
    #     code_ls.append(res[0])
    #     time_ls.append(res[1])
    for req in req_time:
        time_ls.append(req)

    for i in range(len(time_ls)):
        list_count.append(i)

    print(time_ls)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    fig, ax = plt.subplots()
    ax.plot(list_count, time_ls)
    ax.set(xlabel='请求', ylabel='时间（s）',
           title='线程（并发）')
    ax.grid()
    fig.savefig('并发（线程 threading）.png')



if __name__ == '__main__':
    highConcurrent(100)