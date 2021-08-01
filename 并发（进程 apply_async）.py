from multiprocessing import Pool, cpu_count
from time import time

import requests
from matplotlib import pyplot as plt


def baidu(_):
    rep = requests.get('https://www.baidu.com')
    code = rep.status_code
    return time()


def highConcurrent(count):

    pool = Pool(cpu_count())
    tl = []
    start_time = time()

    for i in range(count):
        p = pool.apply_async(baidu, args=(i, ))
        tl.append(p)

    tl = [t.get() for t in tl]
    pool.close()
    pool.join()

    time_li = []
    for t in tl:
        time_li.append(t - start_time)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    fig, ax = plt.subplots()
    ax.plot([i for i in range(1, len(time_li) + 1)], time_li)
    ax.set(xlabel='请求', ylabel='时间（s）',
           title='线程（并发）')
    ax.grid()
    fig.savefig('并发（进程 apply_async）.png')


if __name__ == '__main__':
    highConcurrent(100)