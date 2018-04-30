# -*- coding: utf-8 -*-
import scrapy
from ..items import TuigirlItem

class DownloadtuigirlSpider(scrapy.Spider):
    name = 'downloadtuigirl'
    allowed_domains = ['www.setuw.com']
    start_urls = 'http://www.setuw.com/'

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        headers = {'User-Agent': user_agent}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)
 
    def parse(self, response):
        sel=scrapy.selector.Selector(response)
        categories=sel.xpath('//body/div/div/div[@class="headernav"]/ul[@class="as as1"]/a/text()').extract()  #obtain categories/sex etc.
        categories_urls=sel.xpath('//body/div/div/div[@class="headernav"]/ul[@class="as as1"]/a/@href').extract()  #obtain corresponding urls list
        mainpageUrl="http://www.setuw.com"

        for categories_url in categories_urls:
            item=TuigirlItem()
            try:
                yield scrapy.Request(url=mainpageUrl+categories_url, callback=self.second_parse) #obtain full links of categories for further crawl
            except Exception:
                pass

    def second_parse(self,response):
        goodlists=response.xpath('//body/div[@class="bodydiv"]/div[@class="mntype_contentbg mntype_listall"]/ul/li/a/@href').extract()
        mainpageUrl="http://www.setuw.com"
        for goodlist in goodlists:
            try:
                yield scrapy.Request(url=mainpageUrl+goodlist, callback=self.detail_parse)
            except Exception:
                pass
        if response.xpath('//div[@class="turnpage"]/a[1]/text()').extract()[0]!='2':  #for turn pages
            lastpage=response.xpath('//div[@class="turnpage"]/a[1]/@href').extract()[0]
            yield scrapy.Request(url=mainpageUrl+lastpage, callback=self.second_parse)

    def detail_parse(self, response):
        downloadurlslist=response.xpath('//body/div/div/div/div/div[@class="small"]/ul/li/img/@datas').extract()
        figurenumber=len(downloadurlslist)
        figureno=1
        for downloadurl in downloadurlslist:
            item=TuigirlItem()
            download_link_obtained=str(downloadurl).split("'")[-2]
            try:
                item['category_name']=response.xpath('//p[@class="here"]/a[2]/text()').extract()[0]
                item['detail_name']=response.xpath('//p[@class="here"]/a[3]/text()').extract()[0].split("(")[0]
                item['download_link']=download_link_obtained
                item['imagefilename']=str(figureno)+'.jpg'
            except Exception:
                pass
            figureno=figureno+1
            yield item

            
