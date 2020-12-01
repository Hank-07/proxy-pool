import requests
import base64
import os
from pyquery import PyQuery as pq
from fake_useragent import UserAgent


def us_proxy_crawler(proxy_ip, headers):
    count = 0
    response = requests.get('https://www.us-proxy.org/', headers=headers).text
    doc = pq(response)
    rows = doc('tr')
    for row in rows:
        name = pq(row).find('td').eq(0).text()
        value = pq(row).find('td').eq(1).text()

        if name and value:
            count += 1
            print(f'{count}, {name}, {value}')
            proxy_ip[name] = value
            if count == 200:
                return proxy_ip


def free_proxy_crawler(proxy_ip, headers):
    count = 0
    for index in range(1, 6):
        response = requests.get(f'http://free-proxy.cz/zh/proxylist/country/all/all/ping/all/{index}',
                                headers=headers).text
        doc = pq(response)
        rows = doc('tbody > tr')
        for row in rows:
            name = pq(row).find('td').eq(0).text()
            try:
                name = name[name.find("\"") + 1:name.find(")") - 1]
                ip = base64.b64decode(name).decode()
            except:
                continue
            value = pq(row).find('td').eq(1).text()

            if ip and value:
                count += 1
                print(f'{count}, {ip}, {value}')
                proxy_ip[ip] = value
                if count == 200:
                    return proxy_ip

    return proxy_ip


def open_proxy_crawler(proxy_ip, headers):

    """
    原始網站: https://openproxy.space/list
    """
    ip_list = None
    count = 0
    # 直接從原始網站下載，可以有好幾千個免費ip proxy
    with open('open_proxy_ip.txt', 'r') as f:
        ip_list = f.readlines()
        f.close()

    for ip_info in ip_list:
        try:
            name, port = ip_info.strip().split(':')
            proxy_ip[name] = port
            count += 1
            print(f'{count}, {name}, {port}')
        except:
            continue

    return proxy_ip


def crawl_kuaidaili(proxy_ip, headers):
    """
    快代理：https://www.kuaidaili.com
    """
    url = "https://www.kuaidaili.com/free/{}"
    count = 0
    items = ["inha/1/"]
    for proxy_type in items:
        try:
            html = requests.get(url.format(proxy_type), headers=headers, timeout=5).text
            if html:
                doc = pq(html)
                for proxy in doc(".table-bordered tr").items():
                    ip = proxy("[data-title=IP]").text()
                    port = proxy("[data-title=PORT]").text()
                    if ip and port:
                        proxy_ip[ip] = port
                        count += 1
                        print(f"{count}, http://{ip}:{port}")
        except:
            continue

    return proxy_ip


def crawl_data5u(proxy_ip, headers):
    """
    无忧代理：http://www.data5u.com/
    """
    url = "http://www.data5u.com/"
    count = 0
    try:
        html = requests.get(url, headers=headers).text
        if html:
            doc = pq(html)
            for index, item in enumerate(doc("li ul").items()):
                if index > 0:
                    ip = item("span:nth-child(1)").text()
                    port = item("span:nth-child(2)").text()
                    schema = item("span:nth-child(4)").text()
                    if ip and port and schema:
                        proxy_ip[ip] = port
                        count += 1
                        print(f"{count}, {schema}://{ip}:{port}")
    except:
        pass

    return proxy_ip


def main():
    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    user_agent = UserAgent(fallback=default_user_agent)
    proxy_ip = {}

    headers = {"User-Agent": user_agent.random}
    proxy_ip = open_proxy_crawler(proxy_ip, headers)
    proxy_ip = crawl_kuaidaili(proxy_ip, headers)
    proxy_ip = crawl_data5u(proxy_ip, headers)
    proxy_ip = us_proxy_crawler(proxy_ip, headers)
    proxy_ip = free_proxy_crawler(proxy_ip, headers)

    return proxy_ip


if __name__ == '__main__':
    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    user_agent = UserAgent(fallback=default_user_agent)
    proxy_ip = {}
    headers = {"User-Agent": user_agent.random}
    proxy_ip = crawl_data5u(proxy_ip, headers)
