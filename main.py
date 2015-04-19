import sys
sys.path.append(".")
import os
import secret

from fb_crawler import fbcrawler

if __name__ == "__main__":

    crawler = fbcrawler.FBCrawler("inker610566@yahoo.com.tw", secret.getPass())
    crawler.CrawlGroup("https://www.facebook.com/groups/261103277242087", u"org")
