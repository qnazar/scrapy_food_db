# FoodDB scraping with Scrapy
This is a Scrapy project for scraping data about nutritional value of products from
https://www.tablycjakalorijnosti.com.ua/.

## USAGE
This command will start scrapping process and saving all results into DB.
```commandline
srapy crawl products
```

## INSTALLATION
1. **Clone** the repository
2. Create and activate **virtual environment**
3. Install **dependencies** 
```pip -r ```
4. Create PostgreSQL DB.
5. Start the spider.

## DETAILS
This spider implements a few approaches to avoid blocking and also to be more polite.

###  Authotrottle extension

### Rotating User-Agents
I am using ScrapeOps free API to get the list of user agents. Then script is choosing one random user-agent for every request.


### Rotating Proxy
This spider uses list of proxies provided by another one of my projects. You can check ! LINK ! 

Generally, you just need to pass him a path to ```.txt``` file with proxies. ```utils.load_proxy_list``` will take care of it. 

Go to ```settings.py``` and uncomment rotating_proxies.middlewares:
```commandline
DOANLOADER_MIDDLEWARE = {
    ...
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    ...
}
```