import scrapy


class MyCrawler(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://nbcnews.com"]

    def parse(self, response):
        for related_content in response.css('div.related-content-tease'):
            link = related_content.css('a::attr(href)').extract_first()
            text = related_content.css('.related-content-tease__headline::text').extract_first()
            yield {
                'link': link,
                'text': text,
            }
