import sys
sys.path.append(".")
import os
import secret
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


class FBCrawler:
    def __init__(self, email, password):

        # init
        #self.browser = webdriver.Firefox()#port=5566, service_log_path="./syslog")
        self.browser = webdriver.Chrome()
        self._login(email, password)
        

    def _login(self, username, password):
        self.browser.get("https://www.facebook.com/")
        input_box = self.browser.find_element_by_name("email")
        input_box.send_keys(username)
        input_box = self.browser.find_element_by_name("pass")
        input_box.send_keys(password)
        loginButton = self.browser.find_element_by_id("loginbutton")
        loginButton.click()

    def CrawlGroup(self, url, GroupName):
        self.browser.get(url)

        posts = self.browser.find_elements_by_class_name("userContentWrapper")
        # scroll to target date
        while True:
            posts = self.browser.find_elements_by_class_name("userContentWrapper")

            # find last 3 post in 2014 then stop
            for i in range(3):
                time = self._getPostTime(posts[-i]).find("2014")
                if time == -1: break
            else:
                break

            ActionChains(self.browser).send_keys("j").send_keys("j").send_keys("j").send_keys("j").send_keys("j").perform()
            sleep(1)
        
        # mkdir for save result
        try:
            os.mkdir(GroupName)
        except OSError: pass
        os.chdir(GroupName)

        # report
        rf = open("log", "w")

        idx = 0
        # all results in posts
        for post in posts:

            # expand all reply in post
            while True:
                icons = post.find_elements_by_class_name("UFIPagerIcon");
                if not icons: break
                assert len(icons) == 1
                    
                # check if visible
                try:
                    if not icons[0].is_displayed():
                        assert idx == 0
                        break
                except StaleElementReferenceException:
                    # report
                    rf.writelines(["post %d selenium.common.exceptions.StaleElementReferenceException"%(idx,)])
                    break
                    


                icons[0].click()
                sleep(1)

            f = open("%09d.html" %(idx,), "w")
            f.write(post.get_attribute("outerHTML").encode("utf-8"))
            f.close()
            idx += 1

            rf.close()

        os.chdir("..")


    def _getPostTime(self, div):
        '''
            @param div userContentWrapper
        '''
        time = div.find_element_by_tag_name("abbr").text
        return time


if __name__ == "__main__":

    crawler = FBCrawler("inker610566@yahoo.com.tw", secret.getPass())
    crawler.CrawlGroup("https://www.facebook.com/groups/261103277242087", u"org")
