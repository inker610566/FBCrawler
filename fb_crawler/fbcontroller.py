import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import os
import secret
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException


class FBController(object):
    def __init__(self, browser):
        '''
                @param browser: selenium webdriver instance
        '''
        self.browser = browser


    def Login(self, username, password):
        self.browser.get("https://www.facebook.com/")
        input_box = self.browser.find_element_by_name("email")
        input_box.send_keys(username)
        input_box = self.browser.find_element_by_name("pass")
        input_box.send_keys(password)
        loginButton = self.browser.find_element_by_id("loginbutton")
        loginButton.click()
    
    def GoToPage(self, url):
        self.browser.get(url)
    
    def ScrollDown(self, steps):
        assert steps >= 0
        ac = ActionChains(self.browser)
        for _ in range(steps):
            ac = ac.send_keys("j")
        while True:
            try:
                ac.perform()
                break
            except UnexpectedAlertPresentException:
                sleep(5)

    @staticmethod
    def getPostTime(post):
        '''
            @param div userContentWrapper
        '''
        time = post.find_element_by_tag_name("abbr").text
        return time



