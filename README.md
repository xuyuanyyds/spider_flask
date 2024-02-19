<h1>spider_flask</h1>
<h2>简介：</h2>
<p>基于Python+Flask轻量级框架的豆瓣爬虫数据分析实战项目</p>
<p>用Flask构建一个豆瓣电影top250排行榜及其详细信息</p>
<p><code>通过抓取抓取豆瓣top250的电影并分析，让其简单明了地查看到电影top250排行榜及其详细信息，方便根据其信息选择电影。</code></p>
<h2>为什么使用Flask？</h2>
<p>Flask:Flask扩展丰富，不臃肿，可自由选择组合各种插件，性能优越，相比其他的web框架十分的轻量级，设计哲学很优雅，易于学习，小型的项目快速的开发，大型的项目也没压力。非常的灵活。</p>
<h2>本项目采用的技术栈</h2>
<pre><code>BeautifulSoup4、flask、pymysql
或者使用xpath也可以，这里大部分用的是bs4
数据库使用的是MYSQL
</code></pre>
<ul>
<li>轻量级web应用框架</li>

</ul>
<ul>
<li>将不同的功能模块化</li>
<li>优化项目的结构</li>
<li>增强可读性，易于维护</li>

</ul>
<hr />
<h2>反爬策略设置</h2>
<p>这里本项目应对反爬虫策略主要包括以下几种：</p>
<ol>
<li><strong>User-Agent设置</strong>：对请求头中的User-Agent值进行检查，使用random随机拼接UA头反爬。</li>
<li><strong>IP地址限制</strong>：监控IP地址的访问频率，如果某个IP地址在短时间内发送了过多请求，则限制或封锁该IP地址。所以采用ip代理池随机选取ip地址进行访问。</li>
<li><strong>HTTP Referer检测</strong>：检查请求的Referer字段，如果请求没有正确的来源页面信息，可能是通过爬虫工具直接访问的。</li>
<li><strong>行为分析</strong>：分析正常用户与爬虫在访问网站时的行为模式差异，如请求频率、页面浏览顺序等，识别出爬虫的行为，所以进行时间间隔，行为请求的差异来反爬。</li>
<li><strong>Cookies和Session验证</strong>：服务器通过设置Cookies和Session状态来验证用户，爬虫请求中如果没有正确的Cookies信息可能会被拒绝。</li>

1. 

```python
def get_random_ua():
    user_agents = [
        // 这个列表将包含常见的User-Agent字符串，用于模拟不同浏览器的请求
    ]
    return random.choice(user_agents)  # 从列表中随机选择一个User-Agent返回

def get_random_ip():
    proxy_list = [
        // 这个列表将包含代理服务器的地址，格式一般为'IP:PORT'
    ]
    proxies = { 'https': random.choice(proxy_list) }  # 为https请求随机选择一个代理服务器
    return proxies  # 返回代理服务器的设置

def generate_random_cookie():
    // 这个函数负责生成随机的Cookie，用于模拟真实用户的会话
    cookie_parts = [f'{key}={value}' for key, value in cookie_template.items()]
    cookie = '; '.join(cookie_parts)  # 生成符合HTTP规范的Cookie字符串
    return cookie  # 返回生成的Cookie字符串
```

## 

![222](https://github.com/xuyuanyyds/spider_flask/assets/95127717/0ff54152-616e-4a8e-81e8-513bcf99f57a)



<h2>flask站点界面截图</h2>

在app.py里面右键运行，并访问该站点
![image](https://github.com/xuyuanyyds/spider_flask/assets/95127717/c3dc6c49-b3f9-4d0d-8378-3ed5a23cf7d6)

![image](https://github.com/xuyuanyyds/spider_flask/assets/95127717/f6ed2fe2-5fe6-43b4-a63a-41e7cdc19af1)

<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<h2>数据库主要结构</h2>
<p>&nbsp;</p>


![image](https://github.com/xuyuanyyds/spider_flask/assets/95127717/eac43eb7-cb93-4200-931c-1416b10d4546)
![image](https://github.com/xuyuanyyds/spider_flask/assets/95127717/7e01e398-3768-4e57-a89d-2dcabae127f7)


