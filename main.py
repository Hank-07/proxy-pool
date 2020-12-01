import crawler
import requests
import threading
import time
from queue import Queue


def use_proxy_ip(url, host, port, q):
    proxies = {
    "http": f"http://{host}:{port}",
    "https": f"http://{host}:{port}",
    }

    try:
        r=requests.get(url, proxies=proxies, timeout=5)
        if r.status_code == 200:
            print('success', f'url={url}', proxies)
            q.put({url:1})
        else:
            q.put({url:0})
    except Exception as e:
        q.put({url:0})
        print('fail', e)

def calculate_result(q, result, url_list):
    while not q.empty():
        item = q.get()
        for url in item.keys():
            result[url] = result[url] + item[url]
            # result[url]: 達成次數
            if result[url] == 20:
                if url in url_list:
                    try:
                        url_list.remove(url)
                    except:
                        url_list = []
    
    return url_list, result

# url.txt 取得目標的ip
def get_url_list():
    file = open('url.txt', 'r', encoding='utf-8')
    url_list = file.readlines()
    file.close()
    for count in range(len(url_list)):
        url_list[count] = url_list[count].strip()
        if '險：' in url_list[count]:
            url_list[count] = url_list[count].split('險：')[1]

    return url_list

if __name__ == '__main__':
    url_list = get_url_list()
    result = {}
    q = Queue()
    for url in url_list:
        result[url] = 0
    proxy_pool = crawler.main()
    count = 0
    tasks = []
    for host in proxy_pool.keys():
        if not url_list:
            print('任務完成')
            break
        else:
            for url in url_list:
                port = proxy_pool[host]
                # 線程執行 限制一次100條
                action = threading.Thread(target=use_proxy_ip, args=[url, host, port, q])
                action.start()
                tasks.append(action)
                count += 1
                if count == 100:
                    for task in tasks:
                        task.join()
                    count = 0
                    url_list, result = calculate_result(q, result, url_list)