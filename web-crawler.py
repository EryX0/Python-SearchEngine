import scrapy


class MyCrawler(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://edition.cnn.com"]

    def parse(self, response):
        for related_content in response.xpath('//div[contains(@class, "card container__item")]'):
            yield {
            #    'full': related_content.css('*').get()
                'span': related_content.css('span::text').get(),
                'a': "https://edition.cnn.com" + related_content.css('a::attr(href)').get()
            }
        
