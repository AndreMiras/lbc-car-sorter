from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from lbcscraper.spiders.leboncoin_spider import LeboncoinPropertySpider

def run_crawler():
    print "run_crawler1"
    domain = "leboncoin.fr"
    start_urls = "http://www.leboncoin.fr/vetements/offres/languedoc_roussillon/herault/"
    spider = LeboncoinPropertySpider(domain=domain, start_urls=start_urls)
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    # reactor.run() # the script will block here
    print "run_crawler2"

if __name__ == '__main__':
    """
    run_crawler()
    log.start()
    reactor.run() # the script will block here
    """
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'leboncoin_property',
        '-a', 'start_urls=http://www.leboncoin.fr/vetements/offres/languedoc_roussillon/herault/',
        '-o', '/tmp/data.json'])
