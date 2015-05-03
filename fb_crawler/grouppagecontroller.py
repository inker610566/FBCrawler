from fbcontroller import FBController
from time import sleep
from selenium.common.exceptions import ElementNotVisibleException

class GroupPageController(FBController):
    def __init__(self, browser):
        print "OK"
        super(GroupPageController, self).__init__(browser)
        self.rewind()

    def rewind(self):
        self.post_index = -1
        self._updatePosts()

    def getNextPost(self):
        self.post_index += 1
        while self.post_index >= len(self.posts):
            self.ScrollDown(5)
            sleep(2)
            self._updatePosts()

        post = self.posts[self.post_index]
        self._expandSeeMore(post)
        self._expandReply(post)
        self._expandViewMore(post)
        return post

    def getLastThreePost(self):
        return tuple(self.posts[-1:-4:-1])

    def _updatePosts(self):
        self.posts = self.browser.find_elements_by_class_name("userContentWrapper")

    def _expandSeeMore(self, post):
        while True:
            link = post.find_elements_by_class_name("see_more_link")
            try:
                if link: link[0].click()
                break
            except ElementNotVisibleException:
                print "_expandSeeMore ElementNotVisibleException exception"
                print self.getPostTime(post)
            sleep(5)


        
    def _expandReply(self, post):
        while True:
            icons = post.find_elements_by_class_name("UFIPagerLink");
            if not icons: break
            assert len(icons) == 1
                
            # check if visible
            if not icons[0].is_displayed(): break

            icons[0].click()
            sleep(1)

    def _expandViewMore(self, post):
        while True:
            buttons = post.find_elements_by_class_name("fss");
            if not buttons: break
            for button in buttons:
                button.click()

        

