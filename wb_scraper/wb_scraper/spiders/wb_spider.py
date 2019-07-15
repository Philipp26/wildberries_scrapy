import scrapy
import re
import time 

class WildBerriesSpider(scrapy.Spider):
    name = "wb_spider"
    start_urls = ['https://www.wildberries.ru/catalog/obuv/zhenskaya/sabo-i-myuli/myuli']

    def parse(self, response):
        SET_SELECTOR = '//div[@class="dtList i-dtList"]'

        for item in response.xpath(SET_SELECTOR):
            yield {
                   'id' : item.css('a div ::attr(id)').extract_first(),

                   'url': item.css('a ::attr(href)').extract_first(),

                   'timetamp' : int(time.time()),

                   'stock' : 
                   {
                        'count' : self.check_count_for_null(item.xpath('.//span/span/span/a/span/span/span/span/text()').extract_first()),
                        'in_stock' : bool(item.xpath('.//span/span/span/a/span/span/span/span/text()').extract_first()) 
                   },

                   'price_data' :
                   {
                   'original' : self.parse_value(item.xpath('.//span/span/span/a/div[@class="dtlist-inner-brand"]/div[@class="j-cataloger-price"]/span/span[@class="price-old-block"]/del/text()').extract_first()),
                   'current' : self.parse_value(item.xpath('.//span/span/span/a/div[@class="dtlist-inner-brand"]/div[@class="j-cataloger-price"]/span/ins/text()').extract_first()),
                   'sale_tag' : self.check_discount(item.xpath('.//span/span/span/a/div[@class="dt    list-inner-brand"]/div[@class="j-cataloger-price"]/span/span[@class="price-old-block"]/span/text()').extract_first())
                   },

                   'brand' : item.xpath('.//span/span/span/a/div[@class="dtlist-inner-brand"]/div[@class="dtlist-inner-brand-name"]/strong/text()').extract_first(),
                   'section' : response.xpath('//div[@class="breadcrumbs"]/div/a/span/text()').getall()
                   }

        NEXT_PAGE_SELECTOR = '.next ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                    response.urljoin(next_page),
                    callback = self.parse
                    )

    def check_count_for_null(self, extracted_item):
        if bool(extracted_item):
            return int(extracted_item)
        return 0

    def parse_value(self, extracted_item):
        if bool(extracted_item):
            return float(re.sub('[^0-9]', '', extracted_item))

    def check_discount(self, discount):
        return discount
        if bool(discount):
            return 'Discount is {}%'.format(int(parse_value(extracted_item)))
        return 0





