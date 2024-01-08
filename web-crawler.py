import scrapy
from urllib.parse import urljoin

x = 0

class MyCrawler(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://edition.cnn.com"]
    def parse(self, response):
        for related_content in response.xpath('//div[contains(@class, "card container__item")]'):
            link = urljoin("https://edition.cnn.com",related_content.css('a::attr(href)').get())
            yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})
            if x_add() == 2:
                print('Done!')
                break
    
    
    def parse_link(self,response):
        link = response.meta.get('link')
        title = response.css('div.headline__wrapper ::text').extract()
        article = response.css('div.article__content ::text').extract()
        yield {
            'link': link,
            'title': title,
            'article': article
        }

def x_add():
    global x
    x = x + 1
    return x