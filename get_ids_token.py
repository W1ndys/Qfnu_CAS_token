from bs4 import BeautifulSoup, Tag
import requests
import time
from utils.passwd_encrypt import PasswordEncryptor
from utils.captcha_ocr import CaptchaOCR


class QfnuAuthClient:
    """曲阜师范大学统一认证客户端"""

    def __init__(self):
        """初始化客户端"""
        self.session = requests.session()
        self.ocr = CaptchaOCR()
        self.encryptor = PasswordEncryptor()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.5938.63 Safari/537.36"
        }

    def get_salt_and_execution(self, redir_uri):
        """获取密码加密盐值和execution参数

        Args:
            redir_uri (str): 重定向URI

        Returns:
            tuple: (salt_data, execution_data) 或在失败时 (None, None)
        """
        headers = self.headers.copy()
        headers["Referer"] = "http://libyy.qfnu.edu.cn/"

        try:
            response_data = self.session.get(url=redir_uri, headers=headers).text
            soup = BeautifulSoup(response_data, "html.parser")

            # 修复BeautifulSoup的使用方法，添加正确的类型检查
            execution_element = soup.find(id="execution")
            salt_element = soup.find(id="pwdEncryptSalt")

            if execution_element and isinstance(execution_element, Tag):
                execution_data = execution_element.get("value")
                if salt_element and isinstance(salt_element, Tag):
                    salt_data = salt_element.get("value")
                    return salt_data, execution_data

            print("[!]-----未能找到加密盐或execution参数")
            return None, None
        except Exception as e:
            print(f"[!]-----获取加密盐和execution失败: {str(e)}")
            return None, None

    def check_need_captcha(self, username):
        """检查是否需要验证码

        Args:
            username (str): 用户名

        Returns:
            bool: 是否需要验证码
        """
        uri = "http://ids.qfnu.edu.cn/authserver/checkNeedCaptcha.htl"
        data = {"username": username, "_": int(round(time.time() * 1000))}

        try:
            res = self.session.get(url=uri, params=data, headers=self.headers)
            return "true" in res.text
        except Exception as e:
            print(f"[!]-----检查是否需要验证码失败: {str(e)}")
            return True  # 出错时默认返回需要验证码

    def get_captcha(self):
        """获取验证码图像

        Returns:
            bytes: 验证码图片的字节数据，失败时返回None
        """
        uri = f"http://ids.qfnu.edu.cn/authserver/getCaptcha.htl?{int(round(time.time() * 1000))}"

        try:
            res = self.session.get(url=uri, headers=self.headers)
            return res.content
        except Exception as e:
            print(f"[!]-----获取验证码失败: {str(e)}")
            return None

    def get_token(self, username, password, redir_uri):
        """获取认证token

        Args:
            username (str): 用户名
            password (str): 密码
            redir_uri (str): 重定向URI

        Returns:
            str: 带有ticket的链接，失败时返回None
        """
        # 获取盐值和execution
        salt, execution_data = self.get_salt_and_execution(redir_uri)
        if not salt or not execution_data:
            return None

        # 验证码处理
        cap_res = ""
        print("[+]-----正在检查是否需要验证码")
        if self.check_need_captcha(username):
            print("[+]-----需要验证码，正在尝试获取验证码")
            try:
                cap_pic = self.get_captcha()
                if cap_pic:
                    cap_res = self.ocr.recognize(cap_pic)
                    if isinstance(cap_res, str):
                        cap_res = cap_res.lower()
                        print(f"[+]-----验证码识别结果: {cap_res}")
            except Exception as e:
                print(f"[!]-----获取或识别验证码失败: {str(e)}")
        else:
            print("[+]-----无需验证码，尝试获取Token")

        # 加密密码
        enc_passwd = self.encryptor.encrypt_password(password, salt)

        # 准备提交数据
        headers = self.headers.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = {
            "username": username,
            "password": enc_passwd,
            "captcha": cap_res,
            "_eventId": "submit",
            "cllt": "userNameLogin",
            "dllt": "generalLogin",
            "lt": "",
            "execution": execution_data,
        }

        # 提交认证请求
        try:
            res = self.session.post(
                url=redir_uri, headers=headers, data=data, allow_redirects=False
            )

            if "Location" in res.headers:
                return res.headers["Location"]
            else:
                print("[!]-----认证失败，未获得重定向链接")
                return None
        except Exception as e:
            print(f"[!]-----认证过程发生错误: {str(e)}")
            return None

    def get_auth_cookie(self):
        """获取会话中的认证Cookie

        Returns:
            dict: Cookie字典
        """
        return self.session.cookies.get_dict()


if __name__ == "__main__":
    client = QfnuAuthClient()
    redirect_url = client.get_token(
        "your_account",
        "your_password",
        "http://ids.qfnu.edu.cn/authserver/login?service=http://zhjw.qfnu.edu.cn/jsxsd/framework/xsMain.jsp",
    )

    if redirect_url:
        print(f"[+]-----认证成功，重定向链接: {redirect_url}")
        print(f"[+]-----Cookie: {client.get_auth_cookie()}")
    else:
        print("[!]-----认证失败")
