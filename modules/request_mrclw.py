
import time
from socket import timeout
import requests
import urllib
from requests.exceptions import ConnectionError, HTTPError

class RequestMrclw:
    def __init__(self):
        self.protocol = 'https'
        self.timeout = 8
        self.header = {}

    def send_request(self, _target: str, _value_header: str):

        if _target:
            target_url = None
            target_url = self.protocol + '://'+_target
            try:

                start = time.time()

                obj_urllib = urllib.request.Request(target_url)
                obj_urllib.add_header("Content-type", "application/x-www-form-urlencoded")
                obj_urllib.add_header("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')
                obj_request = urllib.request.urlopen(obj_urllib,timeout=self.timeout)
                obj_request_result = str(obj_request.read().decode('utf-8'))

                time_final = (f'in {time.time() - start:.2f}s')

                if obj_request_result:
                    return obj_request.url, obj_request_result, obj_request.status, time_final
                return target_url, 'Empry', obj_request.status, time_final

            except urllib.error.HTTPError as ehttp:
                return target_url, 'HTTP Error!', ehttp.code, str()
            except timeout:
                return target_url, 'Time!', 'Socket Timed Out', str()
            except urllib.error.URLError as eurl:
                return target_url, 'URL Error!', eurl.reason, str()