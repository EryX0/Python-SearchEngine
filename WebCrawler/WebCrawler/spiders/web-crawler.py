import scrapy
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider
import re
from unidecode import unidecode

class MyCrawler(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://edition.cnn.com","https://edition.cnn.com/world/middle-east","https://edition.cnn.com/style/architecture","https://edition.cnn.com/business/tech"]
    count = 0
    limit = 50  # Set your limit here

    def parse(self, response):
        for related_content in response.xpath('//div[contains(@class, "card container__item")]'):
            link = urljoin("https://edition.cnn.com",related_content.css('a::attr(href)').get())
            yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link}, dont_filter=False)

    def parse_link(self,response):
        
        link = response.meta.get('link')
        title = (''.join([text.strip() for text in response.css('div.headline__wrapper ::text').extract() if text.strip()])).encode('ascii', 'ignore').decode('ascii')
        article = (''.join([text.strip() for text in response.css('div.article__content ::text').extract() if text.strip()])).encode('ascii', 'ignore').decode('ascii')
        
        if not article.strip():
            self.log(f"Skipped {link} - Empty article")
            self.count -= 1
            return
        
        if self.count < self.limit:
            self.count += 1
            print(self.count)
        else:
            raise CloseSpider('Limit reached')
            print(self.count , "finsih -----------------")

        yield {
            'link': link,
            'title': title,
            'article': article
        }


        for related_link in response.css('a.related-content__link ::attr(href)'):
            link = urljoin("https://edition.cnn.com",related_link.get())
            yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link}, dont_filter=False)


    