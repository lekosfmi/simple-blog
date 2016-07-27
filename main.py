#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import re
import time
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blog(db.Model):

    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class IndexHandler(Handler):

    def get(self):
        self.redirect('/blog')


class BlogHandler(Handler):

    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render('blog.html', blogs = blogs)


class NewPostHandler(Handler):

    def get(self):
        self.render('newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            b = Blog(subject = subject, content = content)

            # insert into database
            b.put()

            #sleep is used because of replication lag time
            time.sleep(0.1)

            #redirect to some permalink
            self.redirect('/blog/%d' % b.key().id())


class PermalinkHandler(Handler):
    
    def get(self, blog_id):
        key = Blog.get_by_id(int(blog_id))
        self.render("blogpost.html", blogs = [key])

    def post(self, blog_id):

        # get id and turns into integer
        key = int(blog_id)

        # use id to fine the blog post item
        item = Blog.get_by_id(key)

        # delete the found item
        item.delete()

        # sleep is used because of replication lag time
        time.sleep(0.1)

        # redirect to home
        self.redirect('/blog')


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/blog', BlogHandler),
    ('/blog/(\d+)', PermalinkHandler),
    ('/newpost', NewPostHandler)
], debug=True)
