import asyncio
from multiprocessing import Pool, cpu_count
from time import time

import aiohttp as aiohttp
import requests
from matplotlib import pyplot as plt


async def baidu(_):
    async with aiohttp.ClientSession() as sn:
        async with sn.get('https://www.baidu.com') as rep:
            pass
    return time()

def highConcurrent(count):
    start_time = time()

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(baidu(_)) for _ in range(count)]
    loop.run_until_complete(asyncio.wait(tasks))

    time_li = []
    for t in tasks:
        time_li.append(t.result()-start_time)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    fig, ax = plt.subplots()
    ax.plot([i for i in range(1, len(time_li)+1)], time_li)
    ax.set(xlabel='请求', ylabel='时间（s）',
           title='线程（并发）')
    ax.grid()
    fig.savefig('并发（协程）.png')


if __name__ == '__main__':
    highConcurrent(100)