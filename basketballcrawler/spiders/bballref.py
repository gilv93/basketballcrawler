# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BballrefSpider(CrawlSpider):
    name = 'bballref'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://www.basketball-reference.com/players/']

    rules = [
        Rule(LinkExtractor(allow=(r'/players/[a-z]/$')), follow=True),

        Rule(LinkExtractor(allow=(), restrict_xpaths=('//th/strong/a')), callback="parse_item", follow=True),
    ]


    def parse_item(self, response):

        name = response.css('h1[itemprop="name"]::text').extract()

        #ugly but must be done to properly import into JSON data file, think 'Golden State' versus ['Golden State']
        team =  []
        team.append(response.css('div[itemtype="https://schema.org/Person"] > p').xpath('./a[re:test(@href, "/teams/")]/text()').extract_first())
        
        points = response.css('h4.poptip[data-tip="Points"]').xpath('./following-sibling::p[1]/text()').extract()
        

        rebounds = response.css('h4.poptip[data-tip="Total Rebounds"]').xpath('./following-sibling::p[1]/text()').extract()
        

        assists = response.css('h4.poptip[data-tip="Assists"]').xpath('./following-sibling::p[1]/text()').extract()

        
        
        #creating content row wise
        for item in zip(name, team, points, rebounds, assists):
            scraped_info = {
                'name' : item[0],
                'team' : item[1],
                'points' : item[2],
                'rebounds' : item[3],
                'assists' : item[4],
            }

            yield scraped_info

    
        


