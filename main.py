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
import hashlib
import hmac
import jinja2
import re
import time
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def hash_str(s):
    SECRET = 'imsosecret'
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


# Regex for username, password, and email
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


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


class SignupHandler(Handler):

    def get(self):
        self.render('signup.html')

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username, email = email)

        if not valid_username(username):
            params['error_username'] = "Username is not valid"
            have_error = True

        if not valid_password(password):
            params['error_password'] = "Password is not valid"
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "Email is not valid"
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.redirect('/success?username=' + username)


class SuccessHandler(Handler):

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('success.html', username = username)
        #else:
            #self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', IndexHandler), # redirect to BlogHandler
    ('/newpost', NewPostHandler),
    ('/signup', SignupHandler),
    ('/success', SuccessHandler),
    ('/blog', BlogHandler),
    ('/blog/newpost', NewPostHandler), # redirect to '/'
    ('/blog/signup', SignupHandler), # redirect to '/signup'
    ('/blog/(\d+)', PermalinkHandler)
], debug=True)
