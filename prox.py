import requests
from bs4 import BeautifulSoup
from threading import Thread
import time
from util import log, print
import re

class Proxy:
    def __init__(self):
        self.urls = [
            "https://www.sslproxies.org/",
            "https://free-proxy-list.net/en/",
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text",
        ]
       

        self.proxy_list = []
        self.used_proxies = []
        self.invalid_proxy = []


        self.test_url = "https://mahadevadity8080.pythonanywhere.com/ipaddr"
        self.child = []
        self.at_url_index = 0

    def extract_proxy_from_web(self, url: str):
        response = requests.get(url)
        if "api.proxyscrape.com" in url:
            self.filter_data_m2(response.text)
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        self.filter_data_m1(soup=soup)


    def filter_data_m1(self, soup: BeautifulSoup):
        # Find the table rows with proxy data
        table = soup.find('table', class_='table table-striped table-bordered')
        if table == None:
            print("No data found in table...")
            return
        
        for row in table.tbody.find_all('tr'):
            columns = row.find_all('td')
            
            if columns[6].text.strip() == 'yes':  # HTTPS proxies only
                proxy = f"{columns[0].text.strip()}:{columns[1].text.strip()}"
                if proxy not in self.proxy_list:
                    self.proxy_list.append(proxy)


    def filter_data_m2(self, html: str):
        for ip_str in html.split("\n"):
            if "http" in ip_str:
                self.proxy_list.append((ip_str[ip_str.find('//') + 2 : ]  ).strip())


    def test_proxies(self, proxy):
        if proxy in self.invalid_proxy:
            return None, None

        try:
            response = requests.get(self.test_url, proxies={"https": proxy}, timeout=1)
            print(f"res-> {response.status_code} for {proxy}")
            if response.status_code == 200:
                print("Ip ==> ", response.json()['ip'])
                speed = self.measure_proxy_speed(proxy=proxy)
                if speed == None:
                    self.invalid_proxy.append(proxy)

                return proxy, speed

        except:
            print(f"Invalid proxy -> {proxy}")
            self.invalid_proxy.append(proxy)
            return None, None


    def get_my_proxy(self, trial = False):
        if len(self.proxy_list) == 0:
            log("Running again to get proxy from website...")
            self.run()

        while self.proxy_list:
            
            proxy = self.proxy_list.pop(0)
            proxy, speed = self.test_proxies(proxy = proxy)

            if not proxy:
                continue

            log(f"Found proxy : {proxy} with speed : {speed}")
            return proxy


        if not trial:
            return self.get_my_proxy(trial=True)
        
        return None


    def run(self, trial_num = 0):
        url = self.urls[self.at_url_index]
        self.extract_proxy_from_web(url = url)

        self.at_url_index = self.at_url_index + 1 if (self.at_url_index + 1) < len(self.urls) else 0
        print(f"Total Proxy Found : {len(self.proxy_list)}")

        if len(self.proxy_list) == 0:
            if trial_num > 2:
                self.proxy_list = self.used_proxies.copy()
                self.used_proxies.clear()
                return
            
            self.run(trial_num = trial_num + 1)



    def measure_proxy_speed(self, proxy):
        test_url = "http://mahadevadity8080.pythonanywhere.com/static/static/img/video2.mp4"  #
        
        # Measure download speed
        try:
            start_time = time.time()
            response = requests.get(test_url, proxies={"https": proxy}, stream=True, timeout=3)
            total_size = 0
            for chunk in response.iter_content(1024):  # Measure in chunks
                total_size += len(chunk)

                if total_size > 1024 * 5:  # stop after ~5MB
                    break

            elapsed_time = time.time() - start_time
            download_speed = total_size / elapsed_time  # Mbps

            return int(download_speed)
        
        except Exception as e:
            return None
            

if __name__ == "__main__":
    prox = Proxy()

    p, s = prox.test_proxies("14.251.13.0:8080")
    log(f"Found proxy : {p} with speed : {s}")

    # for i in range(100):
    #     ip = prox.get_my_proxy()
    #     log(f"{i}) MyProxy ==> {ip}")