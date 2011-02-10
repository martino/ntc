from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.http import Response
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from user import *
from user_rating import *
from review import * 
from datetime import datetime

class NewstrustSpider(BaseSpider):
    name = "newstrust.net"
    baseurl = "http://newstrust.net"
    allowed_domains = ["newstrust.net"]
    start_urls = [
        'http://newstrust.net/members'
    ]

    def __init__(self):
        #setup sqlalchemy
        sqlite_db = create_engine('sqlite:///newstrust.db')
        metadata = Base.metadata
        metadata.create_all(sqlite_db)
        Session = sessionmaker(bind=sqlite_db)
        self.session = Session()

    def analyze_story(self, response):
        hxs = HtmlXPathSelector(response)
        userid = response.request.meta['userid']
        urlstory = response.request.meta['urlstory']
        fact = hxs.select('//div[@class="ratingLabel"][text()="Facts\n\t"]/..//div[@class="numeric_rating"]/text()').extract()
        if len(fact):
            fact = fact[0]
        else:
            fact = -1
        fairness =  hxs.select('//div[@class="ratingLabel"][text()="Fairness\n\t"]/..//div[@class="numeric_rating"]/text()').extract()
        if len(fairness):
            fairness = fairness[0]
        else:
            fairness = -1
        sourcing = hxs.select('//div[@class="ratingLabel"][text()="Sourcing\n\t"]/..//div[@class="numeric_rating"]/text()').extract()
        if len(sourcing):
            sourcing = sourcing[0]
        else:
            sourcing = -1
        overall = hxs.select('//div[@class="ratingLabel"][text()="Overall"]/../..//div[@class="numeric_rating"]/text()').extract()[0]
        if len(overall):
            overall = overall[0]
        else:
            overall = -1
        quality = hxs.select('//div[@class="ratingLabel"][text()="Quality\n\t"]/..//div[@class="numeric_rating"]/text()').extract()
        if len(quality):
            quality = quality[0]
        else:
            quality = -1
        re = Review(overall, quality, fact, fairness, sourcing)
        re.user_id = userid
        re.url = urlstory
        self.session.add(re)
        self.session.commit()
        
    def crawl_member(self, response):
        hxs = HtmlXPathSelector(response)   
        userid = response.request.meta['userid']
        ur = UserRating()
        #Analyze user details
        ratingA = hxs.select('//div[@class="wrapper"]//div[@class="rating"]/img/@title').extract()
        ratingA = [r.split()[0] for r in ratingA]
        if len(ratingA):
            ur.memberlevel = ratingA[0]
            ur.activity = ratingA[1]
            ur.experience = ratingA[2]
            ur.ratings = ratingA[3]
            ur.transparency = ratingA[4]
            ur.validation= ratingA[5]
        ratingB = hxs.select('//div[@class="wrapper"]//div[@class="rating"]/text()').extract()
        ratingB = [r.strip() for r in ratingB]
        if len(ratingB):
            ur.reviews = ratingB[7]         
            ur.answers = ratingB[8]
            ur.comments = ratingB[9]
            ur.ratingsrec = ratingB[10]
            ur.numbersrater = ratingB[11]
            ur.ratingsgiven = ratingB[12]
            ur.date = datetime.now()
            ur.user_id = userid
            self.session.add(ur)
            self.session.commit()
        #Get all review
        tmpstory = hxs.select('//div[@class="review_detail"]/a/@href').extract()
        stories = [s for s in tmpstory if s.startswith('/stories/')]
        for story in stories:
            storyUrl = self.baseurl+story
            req =  Request(url=storyUrl, callback=self.analyze_story)
            req.meta['userid'] = userid
            req.meta['urlstory'] = storyUrl
            yield req

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        tmpmem = hxs.select('//div/br/../a/@href').extract()
        members = [s for s in tmpmem if s.startswith('/members/')]
        for member in members:
            memberUrl = self.baseurl+member
            try:           
                user = self.session.query(User).filter_by(url=memberUrl).one() 
            except:
                user = User(memberUrl)
                self.session.add(user)
                self.session.commit()
            req = Request(url=memberUrl, callback=self.crawl_member)
            req.meta['userid'] = user.id 
            yield req
