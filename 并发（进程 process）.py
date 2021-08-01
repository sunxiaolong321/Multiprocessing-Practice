from multiprocessing import Pool, cpu_count, Process
from threading import Thread
from time import time

import requests
from matplotlib import pyplot as plt


class ProcessTest(Process):
    def __init__(self, target, args=()):
        super(ProcessTest, self).__init__()
        self.func = target
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_end_time(self):
        return self.result


def baidu():
    rep = requests.get('https://www.baidu.com')
    code = rep.status_code
    return time()


def highConcurrent(count):
    mult = []

    start_time = time()

    for _ in range(count):
        t = ProcessTest(target=baidu)
        t.start()
        mult.append(t)

    for t in mult:
        t.join()

    time_li = []
    for t in mult:
        time_li.append(t.get_end_time() - start_time)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    fig, ax = plt.subplots()
    ax.plot([i for i in range(1, len(time_li) + 1)], time_li)
    ax.set(xlabel='请求', ylabel='时间（s）',
           title='线程（并发）')
    ax.grid()
    fig.savefig('并发（进程 process）.png')


if __name__ == '__main__':
    highConcurrent(100)
