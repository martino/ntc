from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.http import Response

class NewstrustSpider(BaseSpider):
    name = "newstrust.net"
    baseurl = "http://newstrust.net"
    allowed_domains = ["newstrust.net"]
    start_urls = [
        'http://newstrust.net/members'
    ]

    def analyze_story(self, response):
        print("Analyze %s"%response.url)
        hxs = HtmlXPathSelector(response)
        hxs.select('//div[@class="content clearfix"]//div[@class="ratingLabel"]/text() | //div[@class="content clearfix"]//div[@class="numeric_rating"]/text()').extract()


    def crawl_member(self, response):
        print("Visited %s"%response.url)
        hxs = HtmlXPathSelector(response)   
        #Analyze user details
        rating_labels = hxs.select('//div[@class="wrapper"]//div[@class="ratingLabel"]/text()').extract()
        ratinga = hxs.select('//div[@class="wrapper"]//div[@class="rating"]/img/@title').extract()
        ratingb = hxs.select('//div[@class="wrapper"]//div[@class="rating"]/text()').extract()
        [r.strip() for r in ratingb]
        #Get all review
        tmpstory = hxs.select('//div[@class="review_detail"]/a/@href').extract()
        stories = [s for s in tmpstory if s.startswith('/stories/')]
        for story in stories:
            yield Request(url=self.baseurl+story, callback=self.analyze_story)

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        tmpmem = hxs.select('//div/br/../a/@href').extract()
        members = [s for s in tmpmem if s.startswith('/members/')]
        #save user details in table user
        for member in members:
            yield Request(url=self.baseurl+member, callback=self.crawl_member)

