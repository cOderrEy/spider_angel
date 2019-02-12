import data_getter, data_selector, math, json, dump
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def companies_list():
    pool = ThreadPoolExecutor(max_workers=5)
    all_task = []
    total = data_getter.companies_total()
    for page in range(1, math.ceil(total/20)):
        all_task.append(pool.submit(every_page, page))
        #break
    for task in as_completed(all_task):
        print(task.result())

def every_page(page):
    companies = data_getter.companies_list(page)
    pool = ThreadPoolExecutor(max_workers=5)
    all_task = []
    for company in companies:
        all_task.append(pool.submit(company_detail, company))
        #all_task.append(pool.submit(company_jobs, company))
    for task in as_completed(all_task):
        dump.dump(task.result())
    return "page %d is finished"%page

def company_detail(comapny):
    context = data_getter.company_detail(comapny['page'])
    detail = data_selector.company_detail(context)
    detail['name'] = comapny['name']
    detail['page'] = comapny['page']
    detail['id'] = comapny['id']
    result = {
        "type": True,
        "result": detail
    }
    return result

def company_jobs(comapny):
    context = data_getter.company_jobs(comapny['page'])
    if context['result']:
        jobs = {}
        jobs["jobs"] = data_selector.jobs_list(context['context'])
    else:
        jobs = {"UA": context['context']}
    jobs['name'] = comapny['name']
    jobs['page'] = comapny['page']
    jobs['id'] = comapny['id']
    print(jobs)
    result = {
        "type": False,
        "result": jobs
    }
    return result

if __name__ == "__main__":
    companies_list()