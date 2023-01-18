import os
from dotenv import load_dotenv
from .utils import load_proxy_list

load_dotenv()

BOT_NAME = 'food_scraping'

SPIDER_MODULES = ['food_scraping.spiders']
NEWSPIDER_MODULE = 'food_scraping.spiders'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 16

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'uk,uk-UA;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,en;q=0.5',
    'User-Agent': os.getenv('MY_USER_AGENT'),
}

DOWNLOADER_MIDDLEWARES = {
    'food_scraping.middlewares.UserAgentsMiddleware': 400,
    # 'food_scraping.middlewares.MyRotatingProxyMiddleware': 600,
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

ITEM_PIPELINES = {
    'food_scraping.pipelines.SaveToPostgresPipeline': 300,
}

DOWNLOAD_DELAY = 1

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = True

USER_AGENT_API_KEY = os.getenv('USER_AGENT_API_KEY')
USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
FAKE_USER_AGENT_ENABLED = True
USER_AGENT_NUM_RESULTS = 10

ROTATING_PROXY_LIST = load_proxy_list(r'C:\Users\user\Documents\GitHub\FoodScrapingDB\food_scraping\data\proxy.txt')
ROTATING_PROXY_PAGE_RETRY_TIMES = 3

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_USER = os.environ.get('PG_USER')
PG_PSSWRD = os.environ.get('PG_PASSWORD')
PG_DATABASE = os.environ.get('PG_DATABASE')

# TELNETCONSOLE_ENABLED = False

# COOKIES_ENABLED = False

# SPIDER_MIDDLEWARES = {
#    'food_scraping.middlewares.FoodScrapingSpiderMiddleware': 543,
# }

# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
