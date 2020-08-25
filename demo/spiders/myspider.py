import scrapy
from scrapy.http import Request
from demo.items import DemoItem


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['www.biquge.info']
    start_urls = ['http://www.biquge.info/0_383/']

    def parse(self, response):
        urls = response.xpath('//*[@id="list"]/dl//a/@href').extract()
        # print(urls)
        for url in urls:
            yield Request(url=response.url + url, callback=self.parse_article)

    def parse_article(self, response):
        article_item = DemoItem()
        title_selector = response.xpath('//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()')
        content_selector = response.xpath('// *[ @ id = "content"]/text()')
        content = '\n'.join(content_selector.extract())
        article_item['content'] = content
        article_item['title'] = title_selector.extract_first()
        # print(content)
        yield article_item
        pass
