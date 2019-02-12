from lxml import etree
import json, data_getter, re

#获取公司名称、详情链接、ID
def companies_info(context):
    """
    输入GET https://angel.co/companies/startups 得到的json数据
    输出该页面中的公司详情地址
    """
    context = context['html']
    result = []

    selector = etree.HTML(context)
    #读取出详情页面地址
    companies_page = selector.xpath("//a[@class='startup-link']")

    for page in companies_page:
        data = {
            "page"  : page.get("href"),
            "id"    : page.get("data-id"),
            "name"  : page.text
        }
        if page.text == None:
            continue
        else:
            result.append(data)
    #print(len(result))
    #print(result)
    return result

#反爬机制的token获取
def csrf_token(context):
    selector = etree.HTML(context)
    return selector.xpath("//meta[@name='csrf-token']/@content")

#获取某公司职位列表
def jobs_list(context):
    """
    输入公司职位页面
    返回一个字典对象
    {
        "工作类别": [
            {"name": "工作名字", "link":"工作详情页面", "type":"工作性质", "working_place":"工作地点", "salary":"薪资待遇"},...
        ],...
    }
    """
    with open("jobs_response.html", 'w', encoding='utf-8') as f:
         f.write(context)
    result = {}
    selector = etree.HTML(context)
    classes = selector.xpath("//ul[@class='job-listings']/li")
    #逐个遍历工作类别
    for li in classes:
        divs = li.getchildren()
        class_name = divs[0].text.strip("\n")
        result[class_name] = []
        jobs = divs[1].getchildren()
        #遍历类别中的每个职位
        for job in jobs:
            #职位名称
            job_name = job.getchildren()[0].getchildren()[0].getchildren()[0].text
            #职位详情链接
            job_link = job.getchildren()[0].getchildren()[0].getchildren()[0].get("href")
            job_detail = job.getchildren()[0].getchildren()[0].getchildren()[1].text.strip('\n')
            job_arr = job_detail.split('\n')
            #工作性质
            job_type = job_arr[2]
            #工作地点
            working_place = job_arr[0]
            #薪资待遇
            try:
                salary = job.getchildren()[0].getchildren()[0].getchildren()[1].getchildren()[1].text.split('\n')[2]
            except:
                with open("bad_select.html", 'w', encoding='utf-8') as f:
                    f.write(context)
                salary = 0
            result[class_name].append({
                "name"          : job_name,
                "link"          : job_link,
                "type"          : job_type,
                "working_place" : working_place,
                "salary"        : salary
            })
    return result

#获取公司详情
def company_detail(context):
    with open("detail_response.html", 'w', encoding='utf-8') as f:
         f.write(context)
    result = {}
    selector = etree.HTML(context)
    #公司简介
    company_name = selector.xpath("//h1/text()")
    result['name'] = company_name[0]
    content = selector.xpath("//div[@class='js-truncated-preamble s-vgBottom_5']/span/text()")
    if content or len(content) == 0:
        content1 = selector.xpath("//div[@class='content']/text()")
        #print(content1)
        content2 = selector.xpath("//div[@class='content']/span/text()")
        #print(content2)
        content = content1 + content2
    string = "".join(content)
    string = string.strip('\n')
    result['content'] = string
    #print(result['content'])

    #公司位置、标签
    tags = selector.xpath("//a[@class='tag']/text()")
    try:
        result['location'] = tags.pop(0)
    except:
        result["location"] = ""
    result['tags'] = tags

    #公司联系方式、公司规模（员工数量）、详细位置、公司主页
    text = selector.xpath("//script[@type='application/ld+json']/text()")
    info = json.loads(text[0])
    result['contact'] = info['sameAs']
    result['numberOfEmployees'] = info['numberOfEmployees']
    result['address'] = []
    for address in info['address']:
        try:
            result['address'].append({
                "addressCountry": address['addressCountry'],
                "addressLocality": address['addressLocality'],
                "addressRegion": address['addressRegion']
            })
        except:
            break
    result['font_page'] = info['url']

    #雇员信息
    urls = selector.xpath("//a[@class='view_all']/@href")
    for url in urls:
        if("/startup_roles?role=employee&startup_id") in url:
            result['employees'] = employees_info(data_getter.employees(url))
    #部分公司没有团队介绍，只能从招聘者取出雇员来作为团队
    try:
        _ = result['employees']
    except:
        """
        通过上面得到的info来获取founder的用户id
        根据用户id去访问
        https://angel.co/follows/tooltip?type=User&id=【id】
        会得到用户数据
        可能会有公司没有团队的介绍，但是每个公司都会有founder的数据
        """
        founders = info['founders']
        result['employees'] = []
        for founder in founders:
            image_url = founder['image']
            #print(image_url)
            search = re.search(r'.*/users/(.*)-medium.*', image_url)
            try:
                context = data_getter.user(search.group(1))
                result['employees'].append(user_info(context))
            except:
                continue
    for key in result:
        if result[key] is None:
            result[key] = ""
    return result

#获取公司雇员信息
def employees_info(employees):
    result = []
    for employee in employees["startup_roles/startup_profile"]:
        selector = etree.HTML(employee["html"])
        name = selector.xpath("//a[@class='profile-link']/text()")
        user_id = selector.xpath("//a[@class='profile-link']/@data-id")
        #部分人员没有链接，只有名字
        try:
            name = name[0]
            user_id = user_id[0]
        except:
            name = selector.xpath("//div[@class='name']/text()")
            try:
                name = name[0]
                name = name.strip("\n")
            except:
                name = ""
        else:
            title = selector.xpath("//div[@class='role_title']/text()")
            #部分人员没有填写职位信息
            try:
                title = title[0]
            except:
                title = ""
            bio = selector.xpath("//div[@class='bio']/p/text()")
            #部分人员没有描述信息
            try:
                bio = bio[0]
            except:
                bio = ""
            result.append({
                "id"    : user_id,
                "name"  : name,
                "title" : title,
                "bio"   : bio.strip('\n')
            })
    return result

#获取用户信息
def user_info(context):
    selector = etree.HTML(context)
    name = selector.xpath("//a[@class='profile-link']/text()")
    user_id = selector.xpath("//a[@class='profile-link']/@data-id")
    name = name[0]
    title = ""
    bio = selector.xpath("//div[@class='body']/text()")
    bio = bio[0]

    return {
        "id"    : user_id[0],
        "name"  : name,
        "title" : title,
        "bio"   : bio
    }

#测试代码
if __name__ == "__main__":
    #test company_detail
    context = ""
    with open("detail_response.html", encoding='utf-8') as f:
        context = f.read()
    print(company_detail(context))

    #test employees_info
    # employees = {}
    # with open("example/employees.json") as f:
    #     employees = json.load(f)
    # print(employees_info(employees))

    #test companies_info
    # context = {}
    # with open("example/companies.html") as f:
    #     context = json.load(f)
    # print(companies_info(context))

    #test jobs_list
    # context = ""
    # with open("example/jobs.html") as f:
    #     context = f.read()
    # print(jobs_list(context))

    pass