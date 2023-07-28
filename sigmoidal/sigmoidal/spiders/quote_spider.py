import scrapy
from dotenv import load_dotenv

import os

load_dotenv()


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [os.getenv("INPUT_URL")]
    start_urls = ["https://quotes.toscrape.com/tag/humor/"]
    proxy = os.getenv("PROXY")
    output_file = os.getenv("OUTPUT_FILE")

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
                "tags": quote.xpath("div/a/text()").getall(),
            }

        next_page = response.css("li.next a::attr('href')").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
