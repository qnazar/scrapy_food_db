from random import randint
from urllib.parse import urlencode

import requests
from rotating_proxies.middlewares import RotatingProxyMiddleware, logger
from scrapy.exceptions import CloseSpider


class UserAgentsMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.api_key = settings.get('USER_AGENT_API_KEY')
        self.endpoint = settings.get('FAKE_USER_AGENT_ENDPOINT',
                                     'http://headers.scrapeops.io/v1/user-agents?')
        self.fake_user_agents_active = settings.get('FAKE_USER_AGENT_ENABLED', False)
        self.num_results = settings.get('USER_AGENT_NUM_RESULTS', 10)
        self.headers_list = []
        self._get_user_agents_list()
        self._fake_user_agents_enabled()

    def _get_user_agents_list(self):
        payload = {'api_key': self.api_key}
        if self.num_results is not None:
            payload['num_results'] = self.num_results
        response = requests.get(self.endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])

    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]

    def _fake_user_agents_enabled(self):
        if self.api_key is None or self.api_key == '' or self.fake_user_agents_active == False:
            self.fake_user_agents_active = False
        self.fake_user_agents_active = True

    def process_request(self, request, spider):
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent


class MyRotatingProxyMiddleware(RotatingProxyMiddleware):
    def process_request(self, request, spider):
        if 'proxy' in request.meta and not request.meta.get('_rotating_proxy'):
            return
        proxy = self.proxies.get_random()
        if not proxy:
            if self.stop_if_no_proxies:
                raise CloseSpider("no_proxies")
            else:
                logger.warn("No proxies available; marking all proxies "
                            "as unchecked")
                self.proxies.reset()
                proxy = self.proxies.get_random()
                # if proxy is None:
                #     logger.error("No proxies available even after a reset.")
                #     raise CloseSpider("no_proxies_after_reset")
                if proxy in None:
                    request.meta['proxy'] = None
                    return

        request.meta['proxy'] = proxy
        request.meta['download_slot'] = self.get_proxy_slot(proxy)
        request.meta['_rotating_proxy'] = True
