
import datetime
import scrapy
from enum import Enum     
import re


PageType = Enum('PageType', 'links article datatable')

class CNNSpider(scrapy.Spider):
    name = "cnn_spider"
    allowed_domains = ['cnn.com']
    start_urls = [
                    'https://www.cnn.com/business'
                    # 'https://www.cnn.com/2021/02/09/investing/robinhood-lawsuit-suicide/index.html'
    ]

    def parse(self, response):

        page_type = get_page_type(response)

        # for h3 in response.xpath('//h3/text()').getall():
        #     yield {"title": h3}

        # for body_text in response.xpath('//*[(@id = "body-text")]').getall():
        #     yield {"body": body_text}

        links = response.xpath('//a')        
        for index, link in enumerate(links):    

            try:

                href_text_1 = xstr(link.xpath('text()').get()).rstrip()
                href_text_2 = xstr(" ".join(link.xpath('span/text()').getall())).rstrip()
                href_text = ('{0} {1}').format(href_text_1, href_text_2).rstrip().lstrip()
                href_xpath = link.xpath('@href').get()


                # TODO
                # Test for page type [links, article, data table]    
                # Rules for link follow
                    #	PATH:
                    # 0	Source -> Follow links
                    # 1	If content stop
                    #     If (depth < max_depth) continue
                    #     If links goto 0

                if href_text:
                    yield_object = {
                            "origin" :  self.name
                            ,"datetime" : datetime.datetime.now() 
                            # ,"raw_link" : link
                            , "current_page" : response.url
                            , "href_index" : index
                            , "href_xpath" : href_xpath
                            , "href_text" : href_text
                            , "depth" : 1
                            , "page_type" : page_type 
                            , "url" : "https://www.cnn.com/2021/02/09/investing/robinhood-lawsuit-suicide/index.html"                       
                            
                    }
                    # print(yield_object)
                    yield yield_object

            except Exception as e:
                print(e)
            

def xstr(s):
    if s is None:
        return ''
    return str(s)


def get_page_type(response):

    number_of_links = len(response.xpath('//a')) 
    text_size = 0

    # text = response.xpath("//div/descendant-or-self::*[not(ancestor::*/a or script)]/text()").getall()
    #text = response.xpath("//div/descendant-or-self::*[not(ancestor::*/a or script)]").getall()
    # text = response.xpath("//div/descendant-or-self::*[not(ancestor::*/a) and not(script)]").getall()
    # text = response.xpath("//div/descendant-or-self::*").getall()
    cleaned_text = filter(clean_list, response.xpath("//*[not(self::script or self::style or self::a)]/text()").getall())
    text = list(cleaned_text)
    number_of_pure_text_elements = len(text)
    total_avg = sum( map(len, text) ) / len(text)
	

    print(len(text))

    #PageType.article
    # contains an article tag
    # has large continuous text blocks

    #PageType.links
    # has a lot of links to the source domain?
    #   weird threshold here because most news articles have a lot of links below the article. 
    return PageType.links.value

def clean_list(item):
    if re.findall("\w", item):
        return True
    return False

