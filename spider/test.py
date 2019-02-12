from lxml import etree
import json
import data_getter

def company_info(context):
    result = {}
    selector = etree.HTML(context)
    #公司简介
    content1 = selector.xpath("//div[@class='new_product section']/div[1]/div[3]/div[1]/div[1]/text()")
    content2 = selector.xpath("//div[@class='new_product section']/div[1]/div[3]/div[1]/div[1]/span[2]/text()")
    result['content'] = content1[0] + content2[0]

    #公司位置、标签
    tags = selector.xpath("//a[@class='tag']/text()")
    result['location'] = tags.pop(0)
    result['tags'] = tags

    #雇员信息
    urls = selector.xpath("//a[@class='view_all']/@href")
    for url in urls:
        if("/startup_roles?role=employee&startup_id") in url:
            result['employees'] = employees_info(data_getter.employees(url))

    #公司联系方式、公司规模（员工数量）、详细位置、公司主页
    text = selector.xpath("//script[@type='application/ld+json']/text()")
    info = json.loads(text[0])
    result['contact'] = info['sameAs']
    result['numberOfEmployees'] = info['numberOfEmployees']
    result['address'] = []
    for address in info['address']:
        result['address'].append({
        "addressCountry": address['addressCountry'],
        "addressLocality": address['addressLocality'],
        "addressRegion": address['addressRegion']
    })
    result['font_page'] = info['url']
    return result

def employees_info(employees):
    result = []
    for employee in employees["startup_roles/startup_profile"]:
        selector = etree.HTML(employee["html"])
        name = selector.xpath("//a[@class='profile-link']/text()")
        title = selector.xpath("//div[@class='role_title']/text()")
        bio = selector.xpath("//div[@class='bio']/p/text()")
        result.append({
            "name"  : name[0],
            "title" : title,
            "bio"   : bio
        })
    return result

if __name__ == "__main__":
    #test company_info
    context = ""
    with open("example/company_detail.html") as f:
        context = f.read()
    with open("example/company_detail.json", 'w', encoding='utf-8') as f:
        json.dump(company_info(context), f)
    #test employees_info
    # employees = {}
    # with open("example/employees.json") as f:
    #     employees = json.load(f)
    # print(employees_info(employees))