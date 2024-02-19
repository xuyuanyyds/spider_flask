import requests
from lxml import etree
from bs4 import BeautifulSoup
import pymysql as pymysql
import re
import random
import time
import hashlib
from requests.exceptions import ProxyError

def getDB():
    #连接数据库
    db = pymysql.connect(user='root',password='root',host='localhost',database='db')
    return db

#反爬策略
def get_random_ua():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
    ]
    return random.choice(user_agents)

def get_random_ip():
    proxy_list = [
        '182.34.36.6:9999',
        '216.137.184.253:80',
        '117.1.117.98:4002',
        '103.155.62.163:8080',
        '188.132.222.166:8080',
        '103.216.50.143:8080',
        '202.83.102.83:8080',
        '182.34.16.3:9999',
        '182.34.35.229:9999',
        '114.231.41.160:9999',
        '113.124.95.186:9999',
        '182.34.103.235:9999',
        '113.121.38.12:9999',
        '123.169.36.174:9999',
        '182.140.244.163:8118',
        '27.192.168.250:9000',
        '218.75.102.198:8000'

    ]
    proxies = { 'https': random.choice(proxy_list) }
    return proxies


def generate_random_cookie():
    timestamp = int(time.time())
    random_number = random.randint(100000, 999999)
    user_unique_id = hashlib.md5(str(random_number).encode('utf-8')).hexdigest()

    cookie_template = {
        'bid': user_unique_id[:10],
        '_pk_id.100001.4cf6': user_unique_id + '.' + str(timestamp),
        '__utmz': '30149280.' + str(timestamp) + '.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'll': '"108288"',
        '_vwo_uuid_v2': user_unique_id.upper()[:24] + '|abcdefghijklmnopqrstuvwxyz012345'[random.randint(0, 31)],
        '__utma': '30149280.' + str(random_number) + '.' + str(timestamp) + '.' + str(timestamp) + '.' + str(
            timestamp) + '.1',
        '__utmb': '30149280.' + str(random.randint(1, 9)) + '.10.' + str(timestamp),
        '__utmc': '30149280',
        'ap_v': '0,6.0',
        '_pk_ses.100001.4cf6': str(random.randint(1, 9)),
        '__utmt': str(random.randint(1, 9))
    }

    cookie_parts = [f'{key}={value}' for key, value in cookie_template.items()]
    cookie = '; '.join(cookie_parts)
    return cookie

# 设置随机请求头 (User-Agent)
def ua():
    headers = {
        'User-Agent': get_random_ua(),
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',  # 添加Accept-Encoding头
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cookie': generate_random_cookie(),
        'Host': 'movie.douban.com',
        'Referer': 'https://www.baidu.com'  # 添加Referer头
    }
    return headers

# 发送请求及异常处理
def request_url(url, headers=None, proxies=None, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            proxies = proxies or get_random_ip()
            response = requests.get(url, headers=headers or ua(), proxies=proxies, timeout=10)
            response.raise_for_status()
            if response.status_code == 200:
                time.sleep(random.uniform(1, 3))  # 浮点数增加反爬虫随机性
                return response
        except (requests.exceptions.HTTPError, ProxyError) as e:
            print(f'Request failed: {e}')
            attempt += 1
        except requests.exceptions.ConnectionError as e:
            print(f'Connection Error: {e}')
            attempt += 1
        except requests.exceptions.Timeout as e:
            print(f'Timeout Error: {e}')
            attempt += 1
        except requests.exceptions.RequestException as e:
            print(f'Request Exception: {e}')
            attempt += 1
        # 每次重试间增加等待时间
        time.sleep(random.uniform(1, 5))
    return None  # 所有重试失败，则返回None

#获取每个电影相应的’链接‘和‘外国名称’
def get_url(url):

    headers = ua()
    print("爬取网站：",url)
    resp = requests.get(url=url,headers=headers)
    html_doc = resp.content.decode("utf-8")
    html = etree.HTML(html_doc)
    title_link = html.xpath("//div[@class='pic']//@href")
    soup = BeautifulSoup(html_doc,'lxml')
    fo_movename = []
    div_list = soup.find_all('div',class_='hd')
    for x in div_list:
        foname = x.a.contents[3].text.strip()
        foname = foname[2:]
        fo_movename.append(foname)

    return title_link,fo_movename

#获取电影详细信息
def get_detail(url1,fo_movename,id):
    headers = ua()
    print("爬取网站：", url1)
    resp = requests.get(url=url1, headers=headers)
    html_doc = resp.content.decode("utf-8")
    html = etree.HTML(html_doc)
    soup = BeautifulSoup(html_doc, 'lxml')

    #排名
    numberrank = soup.find(attrs={'class':'top250-no'}).text.split('.')[1] # 使用'.'分割字符串并取出



    #电影中文名
    name = html.xpath("//span[@property='v:itemreviewed']/text()")
    first_na = name[0]
    first_name = first_na.split(' ')[0]

    #导演
    director = html.xpath("//a[@rel='v:directedBy']/text()")
    first_director = director[0]

    #编剧
    try:
        resp1 = soup.find('div', id='info').find_all('span', 'attrs')
        write1 = resp1[1].text  # 编剧
    except (AttributeError, IndexError):
        write1 = "未知"  # 如果出错了没取到，就将write1设为"未知"
        # 继续往下的代码

    #主演
    try:
        actor = resp1[2].text
    except (AttributeError, IndexError):
        actor = '未知'
    #类型
    film_type = soup.find(attrs={'id':'info'}).text.split('\n')[4].split(':')[1].strip()

    #制片国家/地区:
    area = soup.find(attrs={'id':'info'}).text.split('\n')[5].split(':')[1].strip()

    #语言
    languge = soup.find(attrs={'id':'info'}).text.split('\n')[6].split(':')[1].strip()

    #上映时间
    time = soup.find(attrs={'id':'info'}).text.split('\n')[7].split(':')[1].strip()

    #片长
    length = soup.find(attrs={'id':'info'}).text.split('\n')[8].split(':')[1].strip()


    #电影评分
    score = soup.find('strong','ll rating_num').text


    #评分人数
    num = soup.find('div',class_='rating_sum').text.split('人')[0].strip()

    #电影简介
    sumary = soup.find('div',id='link-report-intra').find('span').text.strip()
    sumary = pymysql.converters.escape_str(sumary)


    sql = 'insert into movies(numberrank,first_name,first_director,write1,actor,film_type,area,languge,time,length,score,num,sumary,fo_movename,link) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'.format(numberrank,first_name,first_director,write1,actor,film_type,area,languge,time,length,score,num,sumary,fo_movename,url1)
    db = getDB()
    try:
        curses = db.cursor()
        curses.execute(sql)
        curses.execute('insert into moviehash(movieid) values ("{}")'.format(id))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

    curses.close()
    db.close()



if __name__ == '__main__':
    print("开始爬取")

    # 获取数据库连接对象
    db = getDB()

    # 调用数据库连接对象的方法，获取用于执行SQL查询的游标对象
    cursor = db.cursor()
    for i in range(0,250,25):
        # 调用一个函数来获取电影的URL，并将结果存储在两个变量中
        title_link, fo_movename = get_url("https://movie.douban.com/top250?start="+str(i)+"&filter=")

        # 使用for循环遍历film_urls列表的索引
        for film_url in range(len(title_link)):

            # 使用正则表达式在每个URL中查找数字ID，并将第一个匹配组存储起来
            id = re.search('\d\d+', title_link[film_url]).group()

            # 准备一个SQL语句，从一个表中选择电影ID，其中movieid与我们找到的ID匹配
            sql = 'select movieid from moviehash where movieid="{}";'.format(id)

            # 使用游标对象执行SQL语句
            cursor.execute(sql)

            # 获取执行SQL语句返回的所有记录，并将它们存储在变量'data'中
            data = cursor.fetchall()

            # 检查'data'是否为空（表示在数据库中未找到电影ID的结果）
            if not data:
                # 如果未找到数据，则调用一个函数，使用URL和ID获取电影信息
                get_detail(title_link[film_url], fo_movename[film_url], id)


