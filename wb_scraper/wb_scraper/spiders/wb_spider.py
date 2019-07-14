import scrapy

class WildBerriesSpider(scrapy.Spider):
    name = "wb_spider"
    start_urls = ['https://www.wildberries.ru/catalog/obuv/zhenskaya/sabo-i-myuli/myuli']

    def parse(self, response):
        SET_SELECTOR = '//div[@class="dtList i-dtList"]'

        for item in response.xpath(SET_SELECTOR):
            yield {
                   'stock' : 
                   {
                        'count' : self.check_price_for_null(item.xpath('.//span/span/span/a/span/span/span/span/text()').extract_first()),
                        'in_stock' : bool(item.xpath('.//span/span/span/a/span/span/span/span/text()').extract_first()) 
                   },

                   'price' : item.xpath('.//span/span/span/a/div[@class="dtlist-inner-brand"]/div[@class="j-cataloger-price"]/span/span[@class="lower-price"]/text()').extract_first(),
                   'brand' : item.xpath('.//span/span/span/a/div[@class="dtlist-inner-brand"]/div[@class="dtlist-inner-brand-name"]/strong/text()').extract_first(),
                   'section' : response.xpath('//div[@class="breadcrumbs"]/div/a/span/text()').getall()
                   }

    def check_price_for_null(self, extracted_item):
        if bool(extracted_item):
            return int(extracted_item)
        return 0
