import urllib2
import httplib2
import re
import socks
import Queue
import threading
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.'
    '13) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;'
    'q=0.8',
    'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
    'Accept-Charset': 'windows-1251,utf-8;q=1,*;q=0',
    'Keep-Alive': '300',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

def worker():
    while True:
        ip, port = q.get()
        if not ip:
            break
        try:
            print "start", ip, port
            http = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, ip, int(port)), timeout = 15)
            url = "http://tube.sfu-kras.ru/video/1873?playlist=1866"
            response,body = http.request(url, "GET", headers=headers)

            a = re.findall(r'edit-auto-submit-token" value="(.{32})', body)
            if len(a):
                token = a[0]
                url = "http://tube.sfu-kras.ru/fivestar/vote/node/1873/vote/100?token=" + token
                response,body = http.request(url, "GET", headers=headers)

                if response.status == 200:
                    print ip, port, "vote"
        except:
            print ip, port, "no vote"

        q.task_done()
        time.sleep(3)

q = Queue.Queue()
list_tasks = map(lambda x: q.put(x.split(':')), open("proxies.txt").read().split("\n"))
threads = []
num_worker_threads = 3

for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

q.join()