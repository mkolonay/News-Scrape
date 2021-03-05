from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from .modules import cnn_spider
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from . import settings as import_settings
import os
import sys
from sys import path

def run_spider():
    try:    

        dir_path = os.path.dirname(os.path.realpath(__file__))
        sys.path.insert(0, dir_path)

        settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        settings.setmodule(import_settings, priority='project')


        # runner = CrawlerRunner(get_project_settings())
        runner = CrawlerRunner(settings)

        d = runner.crawl(cnn_spider.CNNSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=0) # the script will block here until all crawling jobs are finished
        return True
    except Exception as e:
        print(e)
        return False




