import requests, random


class get_headers:
    header = {
        "user-agent"            : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }


    langs = ["en;", "fr;", "af;", "ja;", "ko;", "ru;"]


    ip_addr_en = ["61.252", "63.212", "64.13", "64.24", "64.17", "65.141",
                "128.238", "129.73", "146.188", "216.19", "216.76", "216.59", "62.28",
                "62.50", "62.125", "62.31"]


    ip_addr_fr = ["57.24", "57.93", "57.62", "57.79", "57.86", "57.44", "57.127",
                "57.99", "57.161", "57.186", "57.192", "57.203", "57.246", "62.23", "80.8",
                "129.182", "139.100", "156.18", "171.18"]


    ip_addr_af = ["62.184", "62.185", "62.186", "62.200", "192.117", "195.213"]


    ip_addr_ja = ["43.229", "43.238", "43.224", "61.24", "61.115", "61.117",
                "61.125", "131.113", "133.8", "157.6", "202.16", "202.18", "202.25", "202.33"
                "203.180", "202.48", "210.248"]


    ip_addr_ko = ["61.35", "61.75", "165.186", "203.239", "203.240", "203.241",
                "203.244", "211.104", "211.119", "211.176", "211.193", "211.202", "218.49",
                "219.144"]


    ip_addr_ru = ["144.206", "145.249", "159.93", "194.58", "194.190", "62.76", "62.118",
                "80.95", "81.19", "159.93"]
    

    user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            ]

    def get_headers(self):
        self.header["user-agent"] = self.user_agents[random.randint(0, len(self.user_agents) - 1)]
        lanum = random.randint(0, 5)
        self.header["accept-language"] = self.langs[lanum]
        ip = self.switch(lanum)
        self.header["x-forwarded-for"] = ip
        self.header["Proxy-Client-IP"] = ip
        self.header['WL-Proxy-Client-IP'] = ip
        self.header['HTTP_CLIENT_IP'] = ip
        self.header['HTTP_X_FORWARDED_FOR'] = ip
        return self.header

    def switch(self, lanum):
        return{
            0 : "%s.%d.%d"%(self.ip_addr_en[random.randint(0,len(self.ip_addr_en)-1)], random.randint(0, 255), random.randint(0, 255)),
            1 : "%s.%d.%d"%(self.ip_addr_fr[random.randint(0, len(self.ip_addr_fr)-1)], random.randint(0, 255), random.randint(0, 255)),
            2 : "%s.%d.%d"%(self.ip_addr_af[random.randint(0, len(self.ip_addr_af)-1)], random.randint(0, 255), random.randint(0, 255)),
            3 : "%s.%d.%d"%(self.ip_addr_ja[random.randint(0, len(self.ip_addr_ja)-1)], random.randint(0, 255), random.randint(0, 255)),
            4 : "%s.%d.%d"%(self.ip_addr_ko[random.randint(0, len(self.ip_addr_ko)-1)], random.randint(0, 255), random.randint(0, 255)),
            5 : "%s.%d.%d"%(self.ip_addr_ru[random.randint(0, len(self.ip_addr_ru)-1)], random.randint(0, 255), random.randint(0, 255))
        }.get(lanum, "255.255.255.255")