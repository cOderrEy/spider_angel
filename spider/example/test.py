from lxml import etree

html = ""
with open("companies.html") as f:
    html = f.read()
result = []
selector = etree.HTML(html)

companies_page = selector.xpath("//a[@class='startup-link']/@href")
for page in companies_page:
    result.append(page)
result = list(set(result))
print(len(result))