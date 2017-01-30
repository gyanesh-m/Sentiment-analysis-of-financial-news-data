import scrapy
from scrapy.spiders import CrawlSpider,Rule
class GoogleResults(scrapy.Spider):
	name='gresults'
	pages=0
	#allowed_domains=['www.google.com']
	start_urls=["https://www.google.co.in/search?q=site%3Areuters.com+apple&num=100&biw=1111&bih=495&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2014%2Ccd_max%3A1%2F1%2F2017&tbm=nws"]
	def parse(self,response):
		yield{
		'page-'+str(self.pages/100):response.xpath("*//h3/a/@href").extract()
		}
		self.pages+=len(response.xpath("*//h3/a/@href").extract())
		yield self.logger.info(str(self.pages)+" urls collected")
		try:
			nextp=response.xpath("//div[@id='foot']").xpath('.//td[@class=\'b\']').xpath('.//a/@href').extract()[1]
		except:
			nextp=response.xpath("//div[@id='foot']").xpath('.//td[@class=\'b\']').xpath('.//a/@href').extract()[0]
		if nextp is not None:
			next_p=response.urljoin(nextp)
			yield scrapy.Request(next_p,callback=self.parse)
		else:
			yield self.logger.info("next page unavailable|LIMIT REACHED")
		
