import time

from main import Controller
from models.blog_model import Blog
from models.comments_model import Comments
from google.appengine.ext import ndb


class NewPost(Controller):

    def get(self):
        if self.user:
            self.render('newpost.html')
        else:
            self.redirect('/login')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if self.user and subject and content:
            b = Blog(subject = subject, content = content, author = self.user)
            b.put() # insert into database
            time.sleep(0.1) #sleep is used because of replication lag time
            self.redirect('/%d' % b.key.id()) #redirect to some permalink
        else:
            self.render('newpost.html', subject = subject, content = content)


class Permalink(Controller):

    def get(self, blog_id):
        blog_key = Blog.get_by_id(int(blog_id))
        comment_key = Comments.gql("WHERE blog_id = %s "
                                   "ORDER BY created DESC" % int(blog_id))

        self.render("blogpost.html", blogs = [blog_key], comments = comment_key)


class DeletePost(Permalink):

    def get(self, blog_id):
        pass

    def post(self, blog_id):
        key = int(blog_id) # get id and turns into integer
        post = Blog.get_by_id(key) # use id to fine the blog post item

        if self.user.name == post.author.name:
            post.key.delete() # delete the found item
            time.sleep(0.1) # sleep is used because of replication lag time

        self.redirect('/') # redirect to home


class EditPost(Permalink):

    def get(self, blog_id):
        key = Blog.get_by_id(int(blog_id))

        if self.user:
            self.render("editpost.html", blogs = [key])
        else:
            self.redirect("/login")

    def post(self, blog_id):
        key = int(blog_id) # get id and turns into integer
        post = Blog.get_by_id(key) # use id to fine the blog post item
        subject = self.request.get('subject')
        content = self.request.get('content')

        if self.user.name == post.author.name:
            if subject and content:
                post.subject = subject
                post.content = content
                post.put()
                time.sleep(0.1)
                self.redirect('/%s' % key)
            else:
                msg = "Something went wrong. Please try again."
                self.render("editpost.html", blogs = [key], error_message = msg)
        else:
            self.redirect('/login')
