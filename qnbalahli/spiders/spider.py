import scrapy

from scrapy.loader import ItemLoader

from ..items import QnbalahliItem
from itemloaders.processors import TakeFirst


class QnbalahliSpider(scrapy.Spider):
	name = 'qnbalahli'
	start_urls = ['https://www.qnb.com/sites/qnb/qnbglobal/page/en/ennews.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="page-subpage-content"]/p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="page-subpage-content"]/text()[normalize-space()]').get()
		try:
			date = date.split(':')[1]
		except:
			date = None

		item = ItemLoader(item=QnbalahliItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
