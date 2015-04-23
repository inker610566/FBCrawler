import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import os
from time import sleep
from time import strftime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from fbcontroller import FBController

class FBCrawler:
    def __init__(self, email, password):

        # init
        self.browser = webdriver.Firefox()#port=5566, service_log_path="./syslog")
        self.browser.set_page_load_timeout(10)

        #self.browser = webdriver.Chrome()
        self.fbControl = FBController(self.browser)
        try:
            self.fbControl.Login(email, password)
        except TimeoutException:
            self._log("Login timeout")

    def CrawlGroup(self, url, GroupName):
        self.fbControl.GoToPage(url)

        self._log("Scroll to target date")
        posts = self.browser.find_elements_by_class_name("userContentWrapper")
        while True:
            posts = self.browser.find_elements_by_class_name("userContentWrapper")

            # find last 3 post in 2014 then stop
            for i in range(3):
                time = self._getPostTime(posts[-i-1])
                self._log(time)
                if time.find("2014") == -1: break
            else:
                break

            self._log("ScrollDown")
            try:
                self.fbControl.ScrollDown(5)
            except TimeoutException:
                self._log("Timeout")
            sleep(1)
        
        self._log("mkdir for save result")
        try:
            os.mkdir(GroupName)
        except OSError:
            pass
        os.chdir(GroupName)

        idx = 0
        # all results in posts
        for post in posts:

            self._log("saving post %d" % (idx,))
            # expand all reply in post
            while True:
                icons = post.find_elements_by_class_name("UFIPagerLink");
                if not icons: break
                assert len(icons) == 1
                    
                # check if visible
                try:
                    if not icons[0].is_displayed():
                        assert idx == 0
                        break
                except StaleElementReferenceException:
                    break

                icons[0].click()
                sleep(1)

            # expand all "view more" in reply
            while True:
                buttons = post.find_elements_by_class_name("fss");
                if not buttons: break
                for button in buttons:
                    button.click()

            f = open("%09d.html" %(idx,), "w")
            f.write(post.get_attribute("outerHTML").encode("utf-8"))
            f.close()
            idx += 1

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
