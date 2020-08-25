import requests
from scrapy.selector import Selector
import pymysql

# 连接数据库
conn = pymysql.connect(host='47.94.13.255', user='root', password='quan', db='proxy', charset='utf8')
cursor = conn.cursor()
# str = 'http://www.biquge.info/0_383/'
str = 'https://www.baidu.com'


# 爬取西刺网站上的代理ip

def crawler_ips():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    all_ips = []
    all_ports = []
    for i in range(1, 11):
        url = 'https://ip.jiangxianli.com/?country=%E4%B8%AD%E5%9B%BD&page='.format(i)
        r = requests.get(url, headers=headers)
        selector = Selector(text=r.text)
        all_ips.extend(selector.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/table/tbody//td[1]/text()').extract())
        all_ports.extend(selector.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/table/tbody//td[2]/text()').extract())

    print(all_ips)
    print(all_ports)

    cursor.execute("DELETE FROM proxy_ip")
    conn.commit()

    for i in range(0, len(all_ips)):
        cursor.execute("insert proxy_ip(ip,port) VALUES(%s,%s)", [all_ips[i], all_ports[i]])
        conn.commit()


# print(crawler_ips())

class Get_ip(object):
    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = str
        proxy_url = 'https://{0}:{1}'.format(ip, port)
        try:
            proxy_dict = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except:
            print("该ip：{0}不可用".format(ip))
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("ip:{0}有效".format(ip))
                return True
            else:
                print("该ip：{0}不可用".format(ip))
                self.delete_ip(ip)
                return False

    def delete_ip(self, ip):
        delete_sql = """
        delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def get_random_ip(self):
        random_sql = """
        SELECT ip,port from proxy_ip ORDER BY RAND() LIMIT 1
        """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return 'http://{0}:{1}'.format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    crawler_ips()
    get_ip = Get_ip()
    a = get_ip.get_random_ip()
