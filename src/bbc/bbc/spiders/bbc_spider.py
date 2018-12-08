# -*- coding: utf-8 -*-
import logging
import scrapy
from ..items import BbcItem

logger = logging.getLogger('logger')

class BbcSpiderSpider(scrapy.Spider):
    name = 'bbc-spider'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com/news']

    def _merge_content_parts(self, data_list):
        pure_contents = []
        for data in data_list:
            pure_contents.append(data.xpath('string(.)').extract_first())

        return ''.join(pure_contents)

    def _strip(self, element):
        if element is not None:
            return element.strip()
        return element

    def parse(self, response):

        hot_article_block = response.xpath('//div[@class="gel-wrap"]//ol[contains(@class, "gel-layout__item")]')
        articles = hot_article_block.xpath('.//li[contains(@class, "gel-layout__item")]')

        for article in articles:
            detail_relative_path = self._strip(article.xpath('.//a[contains(@class, "nw-o-link")]/@href').extract_first())
            detail_absolute_path = response.urljoin(detail_relative_path)

            yield scrapy.Request(detail_absolute_path, callback=self.detail_page)
    def detail_page(self, response):
        story_body = response.xpath('//div[@class="story-body"]')
        title = self._strip(story_body.xpath('.//h1[@class="story-body__h1"]/text()').extract_first())
        posted_datetimes = self._strip(story_body.xpath('.//div[@class="date date--v2"]/text()').extract_first())

        story_body_contents = story_body.xpath('.//div[@class="story-body__inner"]//p')
        content = self._merge_content_parts(story_body_contents)

        tags = response.xpath('//div[@id="topic-tags"]//ul[@class="tags-list"]/li/a/text()').extract()

        product = BbcItem()

        product['url'] = response.url
        product['title'] = title
        product['content'] = content
        product['posted_datetimes'] = posted_datetimes
        product['tags'] = tags

        yield product
