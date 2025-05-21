# Qfnu CAS Token 获取工具

这是一个用于获取曲阜师范大学统一认证系统(CAS)的Token工具，采用模块化设计和面向对象编程实现。

## 功能特点

- 验证码自动识别
- 密码加密处理
- Session会话管理
- 模块化设计，易于扩展和维护

## 安装依赖

```bash
pip install -r requirements.txt
```

## 文件结构

- `get_ids_token.py`: 主认证客户端类
- `utils/passwd_encrypt.py`: 密码加密模块
- `utils/captcha_ocr.py`: 验证码识别模块
- `example.py`: 使用示例

## 使用方法

1. 在项目根目录创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. 修改`example.py`中的账号和密码

```python
username = "your_account"  # 替换为你的账号
password = "your_password"  # 替换为你的密码
```

3. 运行示例

```bash
python example.py
```

## 代码示例

```python
from get_ids_token import QfnuAuthClient

# 创建客户端实例
client = QfnuAuthClient()

# 获取认证Token
redirect_url = client.get_token(
    username="your_account",
    password="your_password",
    redir_uri="http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2Fzhjw.qfnu.edu.cn%2Fsso.jsp"
)

if redirect_url:
    print(f"认证成功！重定向URL：{redirect_url}")
    
    # 获取认证Cookie
    cookies = client.get_auth_cookie()
    print(f"认证Cookie：{cookies}")
```

## 注意事项

- 本工具仅用于学习和研究目的
- 请勿用于非法用途或违反学校规定的行为