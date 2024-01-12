import scrapy
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider
#import re
from unidecode import unidecode

class MyCrawler(scrapy.Spider):
    name = "cnn-spider"
    start_urls = ["https://edition.cnn.com","https://edition.cnn.com/world/middle-east","https://edition.cnn.com/style/architecture","https://edition.cnn.com/business/tech"]

    def parse(self, response):
        for related_content in response.xpath('//div[contains(@class, "card container__item")]'):
            link = urljoin("https://edition.cnn.com",related_content.css('a::attr(href)').get())
            yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link}, dont_filter=False)

    def parse_link(self,response):
        
        link = response.meta.get('link')
        title = ' '.join([unidecode(text.strip()) for text in response.css('div.headline__wrapper ::text').extract() if text.strip()])
        article = ' '.join([unidecode(text.strip()) for text in response.css('div.article__content ::text').extract() if text.strip()])
        # article = re.sub(r"(?i)CNN", "", article)

        if not article.strip():
            self.log(f"Skipped {link} - Empty article")
            return
        

        yield {
            'link': link,
            'article': article,
            'title': title
        }


        for related_link in response.css('a.related-content__link ::attr(href)'):
            link = urljoin("https://edition.cnn.com",related_link.get())
            yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link}, dont_filter=False)



    