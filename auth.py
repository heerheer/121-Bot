import os
import pickle
import subprocess

import requests
from bs4 import BeautifulSoup

import utils


class Authenticator:
    def __init__(self, service: str, debug=False):
        # 用于储存登入后的一些数据
        self.service = service
        self.login_data = {}
        self.session = requests.Session()
        self.cookie_file = ".cookies_"+self.service.replace('http://',"").replace('/', '_')+".pkl"  # 根据service生成唯一的cookie文件名
        self.headers = {
            "Host": "ids2.just.edu.cn",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        }
        self.ignore_cookies = ['Location']  # 要忽略的 cookie 名列表
        self.load_cookies()  # 初始化时尝试加载cookie

    def save_cookies(self):
        """保存cookies到文件"""
        filtered_cookies = {name: value for name, value in self.session.cookies.items() if
                            name not in self.ignore_cookies}
        with open(self.cookie_file, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def load_cookies(self):
        """从文件加载cookies"""
        """从文件加载cookies，忽略指定的 cookie 名"""
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file, 'rb') as f:
                cookies = pickle.load(f)
                for name, value in cookies.items():
                    if name not in self.ignore_cookies:
                        self.session.cookies.set(name, value)


    def jsessionid(self):
        '''
        获取JSESSIONID,如果有JSESSIONID返回，否则返回None
        '''
        d = self.session.cookies
        return d["JSESSIONID"] if 'JSESSIONID' in d else None

    def encrypt_with_node(self, password):
        """
        使用 Node.js 脚本加密数据
        :param public_key_hex: 公钥的十六进制字符串
        :param data_to_encrypt: 要加密的数据
        :return: 加密后的数据
        """
        try:
            # 调用 Node.js 脚本
            result = subprocess.run(
                ["node", "./js/encrypt.js", password],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running Node.js script: {e}")
            return None

    def login(self, account: str, password: str):
        """
        接受账户和密码进行登录
        :param account: 账户
        :param password: 密码
        :param: service: 登录的服务
        """
        with self.session as session:

            self.headers['HOST'] = utils.get_host_from_url(self.service)
            # 直接访问service并得到跳转地址
            res = session.get(
                self.service,
                headers=self.headers,
                allow_redirects=False,
            )
            # 该服务登入地址
            target = res.headers["Location"]

            # debug
            print(res.status_code, '->', target)
            print(res.headers)
            print(session.cookies.get_dict())

            # 在跳转时要重置HOST和Origin防止404
            self.headers['HOST'] = utils.get_host_from_url(target)
            self.headers["Origin"] = utils.get_origin(target)

            res = session.get(
                target,
                headers=self.headers,
                allow_redirects=False,
            )

            # debug
            print(res.status_code, '->', target)
            print(res.headers)
            print(session.cookies.get_dict())

            # find execution
            soup = BeautifulSoup(res.text, "html.parser")
            execution_input = soup.find("input", {"name": "execution"})
            if execution_input:
                execution_value = execution_input.get("value")
            else:
                print("未找到名为execution的input元素")
            # login data construct
            data = {
                "username": account,
                "password": self.encrypt_with_node(password),
                "_eventId": "submit",
                "submit": "登+录",
                "encrypted": "true",
                "loginType": "1",
                "execution": execution_value,
            }

            # login
            res = session.post(target, headers=self.headers, data=data, allow_redirects=False)

            if res.status_code == 302:
                print("Login Success")
                self.save_cookies()
                target = res.headers["Location"]
                # debug
                print(res.status_code, '->', target)
                print(session.cookies.get_dict())

                self.headers["Origin"] = utils.get_origin(target)
                self.headers['HOST'] = utils.get_host_from_url(target)

                # last
                res = session.get(
                    target,
                    headers=self.headers,
                    allow_redirects=False)

                # debug
                print(res.status_code)
                print(session.cookies.get_dict())
                # 如果有跳转则输出跳转地址
                if res.status_code == 302:
                    target = res.headers["Location"]
                    print('->', target)



            else:
                print("登录失败")
                return -1

        return 0

    def expire(self):
        """
        强制清除Cookies信息过期
        """
        self.session.cookies.clear()
        # 删除cookie文件
        if os.path.exists(self.cookie_file):
            os.remove(self.cookie_file)

    def check(self):
        """
        检查登录是否失效
        :return: 如果登录有效返回True，否则返回False
        """
        res = self.session.get(
            self.service,
            headers=self.headers,
            allow_redirects=False,
        )
        if res.status_code == 302:
            return False
        else:
            return True
