import requests
from requests.adapters import HTTPAdapter


class Verify_email():
    def verify(self,email):
        url = 'http://vmail.waimaolang.cn/Validation.aspx?email={}&type=mailbox'.format(email)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        }
        valid = 0
        try:
            requests.adapters.DEFAULT_RETRIES = 2  # 增加重连次数
            s = requests.session()
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            s.keep_alive = False  # 关闭多余连接
            html = s.get(url=url,headers=headers,timeout=30).json()
            if html['status'] == True:
                valid = 1
            else:
                valid = 0

        except:
            valid = 0

        finally:
            return valid























