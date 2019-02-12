import requests

server = 'http://23.83.243.75:8000/'
#员工表写入
def employee_dump(employees):
    """
{
    "u_id": null,
    "name": "",
    "title": "",
    "bio": "",
    "workfor": null
}
    """
    workfor = employees['id']
    for employee in employees['employees']:
        data = {
            "u_id": employee['id'],
            "name": employee['name'],
            "title": employee['title'],
            "bio": employee['bio'],
            "workfor": workfor
        }
        r = requests.post(server+"user/", data=data)
        if r.status_code > 299:
            print(data)
            print(r.text)

#公司表写入
def company_dump(detail):
    """
{
    "c_id": null,
    "name": "",
    "context": "",
    "addressCountry": "",
    "addressLocality": "",
    "addressRegion": "",
    "numberOfEmployees": "",
    "tags": "",
    "font_page": "",
    "page": ""
}
    """
    addressCountry = ""
    addressLocality = ""
    addressRegion = ""
    if len(detail['address'])>0:
        count = 0
        for address in detail['address']:
            addressCountry += "[%d]%s;"%(count, address['addressCountry'])
            addressLocality += "[%d]%s;"%(count, address['addressLocality'])
            addressRegion += "[%d]%s;"%(count, address['addressRegion'])
            count += 1
    else:
        addressCountry += "[0];"
        addressLocality += "[0]%s;"%(detail['location'])
        addressRegion += "[0];"
    data = {
        "c_id": detail['id'],
        "name": detail['name'],
        "context": detail['content'],
        "addressCountry": addressCountry,
        "addressLocality": addressLocality,
        "addressRegion": addressRegion,
        "numberOfEmployees": detail['numberOfEmployees'],
        "tags": ';'.join(detail['tags']),
        "font_page": detail['font_page'],
        "page": detail['page']
    }
    r = requests.post(server+"company/", data=data)
    if r.status_code > 299:
        print(data)
        print(r.text)
    employee_dump(detail)


#工作表写入
def job_dump(jobs):
    """
{
    "name": "",
    "type": "",
    "working_place": "",
    "class": "",
    "salary": "",
    "link": "",
    "workfor": null
}
    """
    workfor = jobs['id']
    for key in jobs['jobs']:
        for job in jobs['jobs'][key]:
            data = {
                "name"          : job['name'],
                "type"          : job['type'],
                "working_place" : job['working_place'],
                "class"         : key,
                "salary"        : str(job['salary']),
                "link"          : job['link'],
                "workfor"       : workfor
            }
            r = requests.post(server+"job/", data=data)
            if r.status_code > 299:
                print(data)
                print(r.text)

#写入分类
def dump(result):
    if result['type']:
        company_dump(result['result'])
    else:
        job_dump(result['result'])