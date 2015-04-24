import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import os
from time import sleep
from time import strftime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from grouppagecontroller import GroupPageController

class FBCrawler:
    def __init__(self, email, password):

        # init
        self.browser = webdriver.Firefox()#port=5566, service_log_path="./syslog")
        #self.browser.set_page_load_timeout(10)

        #self.browser = webdriver.Chrome()
        self.fbControl = GroupPageController(self.browser)
        try:
            self.fbControl.Login(email, password)
        except TimeoutException:
            self._log("Login timeout")

    def _savePost(self, post, saveName):
        f = open(saveName, "w")
        f.write(post.get_attribute("outerHTML").encode("utf-8"))
        f.close()


    def CrawlGroup(self, url, GroupName):
        self.fbControl.GoToPage(url)

        self._log("mkdir for save result")
        try:
            os.mkdir(GroupName)
        except OSError:
            pass
        os.chdir(GroupName)

        idx = -1
        while True:
            post = self.fbControl.getNextPost()
            idx += 1

            # save post
            self._log("saving post %d" % (idx,))
            self._savePost(post, "%09d.html" %(idx,))

            # find last 3 post in 2014 then stop
            for post in self.fbControl.getLastThreePost():
                time = self._getPostTime(post)
                self._log(time)
                if time.find("2014") == -1: break
            else:
                break

        os.chdir("..")


    def _getPostTime(self, div):
        '''
            @param div userContentWrapper
        '''
        time = div.find_element_by_tag_name("abbr").text
        return time

    def _log(self, msg):
        print strftime("[%H:%M:%S]") + msg


if __name__ == "__main__":

    crawler = FBCrawler("inker610566@yahoo.com.tw", secret.getPass())
    crawler.CrawlGroup("https://www.facebook.com/groups/261103277242087", u"org")
