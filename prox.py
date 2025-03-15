import requests
from bs4 import BeautifulSoup
from threading import Thread
import time


class Proxy:
    def __init__(self):
        self.urls = [
            # "https://free-proxy-list.net/",
            "https://www.sslproxies.org/",
            # "https://www.us-proxy.org/",
        ]

        self.proxy_list = []
        self.working_proxies = []

        self.test_url = "https://mahadevadity8080.pythonanywhere.com/ipaddr"
        self.child = []
        self.conn_speed = {}

    def run(self):
        self.get_proxies()
        print(f"Total Proxy Found : {len(self.proxy_list)}")
        self.thread_test()
        print(f"WorkingProxies : {self.working_proxies}")
        print(f"Speed : ", self.conn_speed)


    def get_faster_proxy(self, count = 5):
        keys = list(self.conn_speed.keys())
        keys.sort(reverse=True)

        fast_proxy = []
        num = 0
        for speed in keys:
            for proxy in self.conn_speed[speed]:
                fast_proxy.append(proxy)
                num += 1

                if num == count:
                    return fast_proxy
                
        return fast_proxy


    def get_proxies(self):
        for url in self.urls:

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the table rows with proxy data
            table = soup.find('table', class_='table table-striped table-bordered')
            if table == None:
                print("No data found in table...")
                continue

            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                
                if columns[6].text.strip() == 'yes':  # HTTPS proxies only
                    proxy = f"{columns[0].text.strip()}:{columns[1].text.strip()}"
                    if proxy not in self.proxy_list:
                        self.proxy_list.append(proxy)

    

    def test_proxies(self, proxies):
        for proxy in proxies:
            try:
                response = requests.get(self.test_url, proxies={"https": proxy}, timeout=3)
                if response.status_code == 200:
                    self.working_proxies.append(proxy)
                    print("Ip ==> ", response.json()['ip'])
                    speed = self.measure_proxy_speed(proxy=proxy)
                    if speed == 0:
                        continue
            
                    if speed in self.conn_speed:
                        self.conn_speed[speed].append(proxy)
                    else:
                        self.conn_speed[speed] = [proxy]
            except:
                pass

    def thread_test(self):
        print("testing proxy....")
        size = 15
        while len(self.proxy_list) != 0:

            one_list = []
            for i in range(size):
                try:
                    one_list.append(self.proxy_list.pop(0))

                except:
                    print("List is empty...")
                    break
            

            thrd = Thread(target=self.test_proxies, args=(one_list,), daemon=True)
            self.child.append(thrd)
            thrd.start()

            break

            
        print("Joinging thread...")
        for thrd  in self.child:
            thrd.join()

        

    def measure_proxy_speed(self, proxy):
        test_url = "http://mahadevadity8080.pythonanywhere.com/static/static/img/video2.mp4"  # 100MB test file
        
        # Measure download speed
        try:
            start_time = time.time()
            response = requests.get(test_url, proxies={"https": proxy}, stream=True, timeout=10)
            total_size = 0
            for chunk in response.iter_content(1024):  # Measure in chunks
                total_size += len(chunk)
            elapsed_time = time.time() - start_time
            download_speed = total_size / elapsed_time  # Mbps

            return int(download_speed)
        
        except Exception as e:
            print(e)
            return 0
            

if __name__ == "__main__":
    prox = Proxy()
    prox.run()

    best_proxy = prox.get_faster_proxy(count=5)
    print("Best Proxy : ", best_proxy)