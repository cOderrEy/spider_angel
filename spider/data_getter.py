import requests, time, random
from headers import get_headers
import data_selector

headers_getter = get_headers()
proxy_pool = [
    "23.83.243.75:8989",
    "172.93.33.29:8989",
    "138.128.199.17:8989"
]

#随机代理池选取代理
def random_proxy():
    index = random.randint(0, len(proxy_pool) - 1)
    return {
        "http"  : proxy_pool[index],
        "https" : proxy_pool[index]
    }

#延时
def delay():
    delay_time = random.randint(7,25)
    #print(delay_time)
    time.sleep(delay_time)

#反爬机制的预浏览得到请求头
def pre_requests():
    delay()
    session = requests.session()
    session.headers.update(headers_getter.get_headers())
    r = session.get("https://angel.co/companies", proxies = random_proxy())
    csrf_token = data_selector.csrf_token(r.text)
    session.headers.update({"referer": "https://angel.co/companies", "csrf-token": csrf_token[0], "x-requested-with": "XMLHttpRequest", "origin": "https://angel.co", "dnt": "1"})
    delay()
    return session

#获取公司总数
def companies_total():
    r = requests.get("https://angel.co/company_filters/search_data", proxies = random_proxy())
    result = r.json()
    return result['total']

#获取公司列表
def companies_list(page):
    """
    输入页数
    返回该页20个公司信息
    {
      公司名称: 
      {
          "page": 详情页面,
          "id"  : 公司id
      }
    }
    """
    session = pre_requests()
    r = session.post("https://angel.co/company_filters/search_data", data={"sort": "signal", "page": page}, proxies = random_proxy())
    search_data = r.json()
    url = "https://angel.co/companies/startups?"
    for c_id in search_data['ids']:
        url += "ids%%5B%%5D=%d&"%c_id
    url += "&total=%d&page=%d&sort=%s&new=%s&hexdigest=%s"%(search_data['total'], search_data['page'], search_data['sort'], search_data['new'], search_data['hexdigest'])
    #url = "https://angel.co/companies/startups?ids%5B%5D=54351&ids%5B%5D=6343&ids%5B%5D=127902&ids%5B%5D=28390&ids%5B%5D=210266&ids%5B%5D=383006&ids%5B%5D=33752&ids%5B%5D=359662&ids%5B%5D=251699&ids%5B%5D=458987&ids%5B%5D=19155&ids%5B%5D=238591&ids%5B%5D=806019&ids%5B%5D=107420&ids%5B%5D=167892&ids%5B%5D=452820&ids%5B%5D=77847&ids%5B%5D=633737&ids%5B%5D=268951&ids%5B%5D=3876019&total=4560720&page=1&sort=signal&new=false&hexdigest="+hexdigest
    r = session.get(url, proxies = random_proxy())
    #print(url)
    # with open("response.html", 'w') as f:
    #     f.write(r.text)
    companies_data = r.json()
    session.close()
    return data_selector.companies_info(companies_data)

#获取公司详情页面
def company_detail(url):
    session = pre_requests()
    r = session.get(url, proxies = random_proxy())
    session.close()
    return r.text

#获取公司招聘职位
def company_jobs(url):
    """
    输入得到的page URL
    返回该公司职位页面
    """
    url += "/jobs"
    session = pre_requests()
    try:
        r = session.get(url, proxies = random_proxy())
        session.close()
        with open("jobs_response.html", 'w', encoding='utf-8') as f:
            f.write(r.text)
    except:
        print(url)
        return{
            "result"    : False,
            "context"   : session.headers.get("user-agent")
        }
    return {
        "result"    : True,
        "context"   : r.text
    }

#获取公司团队
def employees(url):
    """
    将页面中 View all xx Employees 的URL 提供过来
    返回该URL 的json数据
    """
    url = "https://angel.co"+url
    session = pre_requests()
    r = session.get(url, proxies = random_proxy())
    session.close()
    return r.json()

#获取个人信息
def user(id):
    url = "https://angel.co/follows/tooltip?type=User&id=%s"%id
    session = pre_requests()
    r = session.get(url, proxies = random_proxy())
    session.close()
    return r.text