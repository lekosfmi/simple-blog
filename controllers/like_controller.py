import time

from models.blog_model import Blog
from main import Controller
from models.likes_model import Likes
from google.appengine.ext import ndb


class Like(Controller):

    def get(self, blog_id):
        pass

    def post(self, blog_id):
        key = int(blog_id)
        post = Blog.get_by_id(key)

        if post and self.user:
            post.like += 1
            like = Likes(blog_id = key, author = self.user)
            like.put()
            post.put()
            time.sleep(0.2)
            self.redirect('/%s' % key)
        else:
            self.redirect('/login')


class Unlike(Controller):

    def get(self, blog_id):
        pass

    def post(self, blog_id):
        key = int(blog_id)
        post = Blog.get_by_id(key)

        if post and self.user:
            post.like -= 1
            like = Likes(blog_id = key, author = self.user)
            like.put()
            post.put()
            time.sleep(0.2)
            self.redirect('/%s' % key)
        else:
            self.redirect('/login')
