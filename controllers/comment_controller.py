import time

from main import Controller
from models.comments_model import Comments
from models.users_model import *


class DeleteComment(Controller):

    def get(self, comment_id):
        key = int(comment_id)
        c = Comments.get_by_id(key)
        blog_id = int(c.blog_id)

        if self.user.name == c.author.name:
            c.key.delete()
            time.sleep(0.1)

        self.redirect('/%s' % blog_id)


class EditComment(Controller):

    def get(self):
        self.render('edit-comment.html')


class NewComment(Controller):

    def get(self, blog_id):
        pass

    def post(self, blog_id):
        blog_id = int(blog_id)
        content = self.request.get('content')

        if self.user and content:
            c = Comments(content = content,
                         author = self.user,
                         blog_id = blog_id)
            c.put()
            time.sleep(0.1)

        self.redirect('/%s' % blog_id)
