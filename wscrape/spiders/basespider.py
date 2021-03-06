#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.http import Request
# from scrapy_redis.spiders import RedisSpider
from wscrape.bloom_scrapy_redis import CloseableRedisSpider
from .utils import get_config, PRIORITY_TOP


class BaseSpider(CloseableRedisSpider):
    
    # config placeholder
    config = {}
    config_name = ''

    # white list for bloom filter
    whitelist = set()

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):

        def init_config():
            if self.config:
                return
            self.config = get_config(self.config_name)

        obj = super().from_crawler(crawler, *args, **kwargs)
        init_config()
        return obj

    def make_base_request(self, url):
        return Request(url, priority=PRIORITY_TOP+1)
    
    def errback(self, failure):
        self.logger.error(repr(failure))
    
    def parse(self, response):
        stats = self.crawler.stats
        
    def _update_stats(self, site, category, type_):
        self.crawler.stats.inc_value('%(site)s_%(category)s_%(type_)s' % {'site': site, 'category': category, 'type_': type_})