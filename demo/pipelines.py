# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import codecs
import json
import csv


class DemoPipeline:
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline():
    def __init__(self):
        # self.file = codecs.open('demoJSON', 'w', encoding='utf-8')
        self.csv = open('222.csv', 'w')
        self.writer = csv.writer(self.csv)

    def process_item(self, item, spider):
        # self.file.write(item['title'])
        # self.file.write(item['content'])
        self.writer.writerow([item['title'], item['content']])
        # liens = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # self.file.write(liens)
        return item

    def spider_close(self, spider):
        # self.file.close()
        self.csv.close()
