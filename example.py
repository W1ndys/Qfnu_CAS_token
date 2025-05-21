#!/usr/bin/env python
# -*- coding: utf-8 -*-

from get_ids_token import QfnuAuthClient


def main():
    """示例：如何使用认证客户端获取Token"""
    # 创建客户端实例
    client = QfnuAuthClient()

    # 设置账号密码和认证目标URL
    username = "2022416246"
    password = "qfnuWS0814@"
    target_url = "http://ids.qfnu.edu.cn/authserver/login?service=http://zhjw.qfnu.edu.cn/jsxsd/framework/xsMain.jsp"

    print("正在尝试获取认证Token...")

    # 获取认证Token
    redirect_url = client.get_token(
        username=username, password=password, redir_uri=target_url
    )

    # 处理认证结果
    if redirect_url:
        print(f"认证成功！重定向URL：{redirect_url}")

        # 获取认证Cookie
        cookies = client.get_auth_cookie()
        print(f"认证Cookie：{cookies}")

        # 访问重定向URL
        response = client.session.get(redirect_url)
        print(response.text)

    else:
        print("认证失败，请检查账号密码是否正确或网络连接")


if __name__ == "__main__":
    main()
