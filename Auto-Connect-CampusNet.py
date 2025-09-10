import json
import os
from urllib.parse import urlparse

import requests

# 从配置文件加载敏感信息与站点参数
def load_config():
    """加载配置文件 config.json（或 CAMPUSNET_CONFIG 环境变量指定的路径）。"""
    config_path = os.getenv("CAMPUSNET_CONFIG")
    if not config_path:
        # 默认读取与脚本同目录的 config.json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "config.json")

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"未找到配置文件: {config_path}。请复制 config.example.json 为 config.json 并填写你的信息。"
        )

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    return cfg


def build_runtime_from_config(cfg: dict):
    """根据配置组装运行所需的 URL、Headers 与 Cookies。"""
    # 登录地址（可在 config.json 覆盖），默认使用示例校园网地址
    login_url = cfg.get(
        "login_url",
        "http://10.71.29.181/eportal/InterFace.do?method=login",
    )
    host = urlparse(login_url).hostname or "10.71.29.181"

    # 默认非敏感 Cookie 取值，可被 config["cookies"] 覆盖
    default_cookies = {
        "EPORTAL_COOKIE_DOMAIN": "false",
        "EPORTAL_COOKIE_SAVEPASSWORD": "true",
        "EPORTAL_COOKIE_OPERATORPWD": "",
        "EPORTAL_COOKIE_NEWV": "true",
        # 下面这些通常与用户/学校相关，建议在 config.json 中提供
        # "EPORTAL_COOKIE_USERNAME": "",
        # "EPORTAL_COOKIE_PASSWORD": "",
        # "EPORTAL_COOKIE_SERVER": "",
        # "EPORTAL_COOKIE_SERVER_NAME": "",
        # "EPORTAL_USER_GROUP": "",
        # "JSESSIONID": "",
    }
    user_cookies = cfg.get("cookies", {})
    cookies = {**default_cookies, **user_cookies}

    # Headers：允许在 config.json 的 headers.User-Agent 覆盖 UA
    user_agent = (
        cfg.get("headers", {}).get(
            "User-Agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        )
    )
    headers = {
        "Host": host,
        "User-Agent": user_agent,
    }
    # 如果配置里有 JSESSIONID，按原逻辑附加同名 Header（部分门户需要）
    jsessionid = cookies.get("JSESSIONID")
    if jsessionid:
        headers["JSESSIONID"] = jsessionid

    # 用于 POST 的 service 与 user_group 参数
    service = cfg.get("service", cookies.get("EPORTAL_COOKIE_SERVER", ""))
    user_group = cfg.get("user_group", cookies.get("EPORTAL_USER_GROUP", ""))

    return login_url, headers, cookies, service, user_group


# 检查是否已登录校园网
def check_network_status():
    try:
        # 访问任意网页（如百度）以检测是否会被重定向
        response = requests.get("http://www.baidu.com")
        response_text = response.text

        # 检查是否包含重定向到校园网登录页的 `<script>` 标签
        if "top.self.location.href='http://10.71.29.181" in response_text:
            print("未连接校园网，需要登录")
            return False
        else:
            print("已连接校园网，无需登录")
            return True

    except requests.RequestException as e:
        print(f"网络请求失败：{e}")
        return False


# 获取 query_string
def get_query_string(session):
    response = session.get("http://10.71.29.181/")
    query_string = response.text
    st = query_string.find("index.jsp?") + 10
    end = query_string.find("'</script>")
    query_string = query_string[st:end]
    print("获取到 query_string:", query_string)
    return query_string


def login():
    # 加载配置并构建运行参数
    cfg = load_config()
    login_url, headers, cookies, service, _user_group = build_runtime_from_config(cfg)

    session = requests.Session()
    query_string = get_query_string(session)
    post_data = {
        "userId": cookies.get("EPORTAL_COOKIE_USERNAME", ""),
        "password": cookies.get("EPORTAL_COOKIE_PASSWORD", ""),
        "service": service,
        "queryString": query_string,
        "operatorPwd": "",
        "operatorUserId": "",
        "validcode": "",
        "passwordEncrypt": "true",
    }

    response = session.post(login_url, headers=headers, data=post_data, cookies=cookies)
    try:
        data = response.json()
    except ValueError:
        print("登录失败：返回内容不是 JSON，可能门户接口或参数有变动。")
        print("响应状态码:", response.status_code)
        print("响应文本片段:", response.text[:200])
        return

    if data.get("result") == "success":
        print("登录成功！")
    else:
        print("登录失败，原因:", data.get("message"))


# 运行检测和登录
if not check_network_status():
    login()
else:
    print("跳过登录")
