目标：爬取angel.co上公司及其职位数据

分析：
    可以不登录就可以进行浏览

公司信息列表：
    https://angel.co/companies
    该页面数据来源：
        GET https://angel.co/companies/startups?ids%5B%5D=54351&ids%5B%5D=6343&ids%5B%5D=127902&ids%5B%5D=28390&ids%5B%5D=210266&ids%5B%5D=383006&ids%5B%5D=33752&ids%5B%5D=359662&ids%5B%5D=251699&ids%5B%5D=458987&ids%5B%5D=19155&ids%5B%5D=238591&ids%5B%5D=806019&ids%5B%5D=107420&ids%5B%5D=167892&ids%5B%5D=452820&ids%5B%5D=77847&ids%5B%5D=633737&ids%5B%5D=268951&ids%5B%5D=3876019&total=4559960&page=1&sort=signal&new=false&hexdigest=e60ed3a6d5177d2814761084d4a2134829a0d762
        最后一个参数hexdigest会有过期时间
            在时间内可以得到正确的数据
            过期后就会404
        数据格式JSON，内容：
            返回数据    example\companies.json
            内容        example\companies.html
        该URL中ids参数来源：
            POST    https://angel.co/company_filters/search_data
            data    sort=signal&page=1
            返回内容：
                example\companies_ids.json
                规律：
                    每页会返回20个公司的id
                    有总数
                    没有停止标记（循环中应该判断page*20 <= total）
            限制：
                csrf-token、referer、origin、dnt
                其中csrf-token在访问https://angel.co/companies是在<meta>中被设置
                其余header都可以为固定值

得到公司列表后根据公司信息请求其详情页面+/jobs  example(https://angel.co/leap-motion/jobs)
在此页面中：
    我需要的数据的格式如下
        <ul class="job-listings">
            <li>
                <div>工作分类</div>
                <div>工作列表</div>
                    <div>工作</div>
                        <div>??</div>
                            <div>??</div>
                                <a href=工作链接>工作名称</a>
                                <div>
                                    "
                                    工作地点
                                    ·
                                    工作性质
                                    "
                                    <span>??</span>
                                    <span>
                                    "
                                    ·
                                    薪资情况
                                    "
                                    </span>
                                </div>
            </li>
            <li>
            ···
            ···
            </li>
            ···
        </ul>


由以上所得信息
数据库可以构建如下：
    表companies:
        <id>    int         primary key [公司id]
        <name>  varchar 255             [公司名称]
        <link>  varchar 255             [公司详情连接]
    表jobs:
        <id>            int 自增    primary key  [工作唯一标识]
        <name>          varchar 255             [工作名称]
        <working_place> varchar 255             [工作地点]
        <class>         varchar 255             [工作类型]
        <type>          varchar 255             [工作性质]
        <salary>        varchar 255             [薪资待遇]
        <link>          varchar 255             [工作详情链接]

新增信息：
    公司摘要
    公司位置
    TAG
    公司规模
    