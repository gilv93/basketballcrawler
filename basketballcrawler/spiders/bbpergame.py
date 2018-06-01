# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Stats(scrapy.Item):
    name = scrapy.Field()
    team = scrapy.Field()
    season = scrapy.Field()
    PPG = scrapy.Field()
    RPG = scrapy.Field()
    APG = scrapy.Field()

class BbpergameSpider(CrawlSpider):
    name = 'bbpergame'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://www.basketball-reference.com/players/']

    rules = [
        Rule(LinkExtractor(allow=(r'/players/[a-z]/$')), follow=True),

        Rule(LinkExtractor(allow=(), restrict_xpaths=('//th/strong/a')), callback="parse_item", follow=True),
    ]

    

    def parse_item(self, response):
        stats = Stats()

        
        name = response.css('h1[itemprop="name"]::text').extract_first()

        
        team = response.css('div[itemtype="https://schema.org/Person"] > p').xpath('./a[re:test(@href, "/teams/")]/text()').extract_first()

        
        season = response.xpath('//tr[re:test(@id, "per_game\.\d")]/th/a/text()').extract()

        
        pts_per_g = response.xpath('//tr[re:test(@id, "per_game\.\d")]/td[@data-stat="pts_per_g"]/text()').extract()

        
        trb_per_g = response.xpath('//tr[re:test(@id, "per_game\.\d")]/td[@data-stat="trb_per_g"]/text()').extract()
    
        
        ast_per_g = response.xpath('//tr[re:test(@id, "per_game\.\d")]/td[@data-stat="ast_per_g"]/text()').extract()


        stats['name'] = name
        stats['team'] = team
        stats['season'] = season
        stats['PPG'] = pts_per_g
        stats['RPG'] = trb_per_g
        stats['APG'] = ast_per_g

        yield stats
        #for item in zip(name, team, season, pts_per_g, trb_per_g, ast_per_g):
        #    scraped_info = {
        #        'name' : item[0],
        #        'team' : item[1],
        #        'season' : item[2],
        #        'PPG' : item[3],
        #        'RPG' : item[4],
        #        'APG' : item[5],
        #    }

        #    yield scraped_info
