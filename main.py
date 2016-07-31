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
import time
import webapp2

from blog import *
from users import *

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):

    """ Defines functions for rendering pages & setting cookies """

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key.id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


class BlogHandler(Handler):

    def get(self):
        blogs = ndb.gql("SELECT * FROM Blog ORDER BY created DESC")
        self.render('blog.html', blogs = blogs)


class IndexHandler(Handler):

    """Redirect to BlogHandler"""

    def get(self):
        self.redirect('/blog')


class LoginHander(Handler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)
        if user:
            self.login(user)
            self.redirect('/')
        else:
            error = "Username or password is incorrect"
            self.render('login.html', username = username, error = error)


class LogoutHandler(Handler):

    def get(self):
        self.logout()
        self.redirect('/')


class NewPostHandler(Handler):

    def get(self):
        if self.user:
            self.render('newpost.html')
        else:
            self.redirect('/login')


    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            b = Blog(subject = subject, content = content)
            b.put() # insert into database
            time.sleep(0.1) #sleep is used because of replication lag time
            self.redirect('/blog/%d' % b.key.id()) #redirect to some permalink
        else:
            self.render('newpost.html', subject = subject, content = content)



class PermalinkHandler(Handler):

    def get(self, blog_id):
        key = Blog.get_by_id(int(blog_id))
        self.render("blogpost.html", blogs = [key])


class DeletePostHandler(PermalinkHandler):

    def get(self, blog_id):
        key = int(blog_id) # get id and turns into integer
        item = Blog.get_by_id(key) # use id to fine the blog post item
        item.key.delete() # delete the found item
        time.sleep(0.1) # sleep is used because of replication lag time
        self.redirect('/blog') # redirect to home


class SignupHandler(Handler):

    """Signup Page"""

    def get(self):
        self.render('signup.html')

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username, email = self.email)

        username_exist = User.by_name(self.username)

        if not valid_username(self.username):
            params['error_username'] = "Username is not valid"
            have_error = True
        elif username_exist:
            params['error_username'] = 'That user already exists.'
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "Password is not valid"
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "Email is not valid"
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            user = User.register(self.username, self.password, self.email)
            user.put()
            self.login(user)
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', IndexHandler),

    ('/login', LoginHander),
    ('/logout', LogoutHandler),
    ('/newpost', NewPostHandler),
    ('/signup', SignupHandler),

    ('/blog', BlogHandler),
    ('/blog/(\d+)', PermalinkHandler),
    ('/blog/delete/(\d+)', DeletePostHandler)
], debug=True)
