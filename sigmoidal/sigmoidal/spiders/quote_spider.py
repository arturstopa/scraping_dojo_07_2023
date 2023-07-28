import scrapy
from dotenv import load_dotenv
import js2xml
import lxml.etree
import parsel
import xmltodict

import os
from typing import List, Dict

load_dotenv()


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [os.getenv("INPUT_URL")]
    proxy = os.getenv("PROXY")
    output_file = os.getenv("OUTPUT_FILE")

    def parse(self, response):
        js = response.css("script::text").get()
        xml = lxml.etree.tostring(js2xml.parse(js), encoding="unicode")

        selector = parsel.Selector(text=xml)
        for quote in selector.xpath("//var[@name='data']/array/object").getall():
            data: List[Dict] = (
                xmltodict.parse(quote).get("object", dict()).get("property", list())
            )
            result = dict()
            for property in data:
                if property.get("@name", "") == "text":
                    result["text"] = property.get("string", "")
                if property.get("@name", "") == "author":
                    author_properties: List[Dict] = property.get("object", dict()).get(
                        "property", list()
                    )
                    name = [
                        dictionary.get("string", "")
                        for dictionary in author_properties
                        if dictionary.get(
                            "@name",
                        )
                        == "name"
                    ][0]
                    result["by"] = name
                if property.get("@name") == "tags":
                    try:
                        tags = property.get("array", dict()).get("string", list())
                    except AttributeError:
                        tags = list()
                    result["tags"] = tags if isinstance(tags, list) else [tags]

            yield result

        next_page = response.css("li.next a::attr('href')").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
