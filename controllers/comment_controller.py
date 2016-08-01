import time

from main import Controller
from models.comments_model import Comments
from models.users_model import *


class DeleteComment(Controller):

    """Delete Comment"""

    def get(self, comment_id):
        pass

    def post(self, comment_id):
        key = int(comment_id)
        c = Comments.get_by_id(key)
        blog_id = int(c.blog_id)

        if self.user.name == c.author.name:
            c.key.delete()
            time.sleep(0.1)

        self.redirect('/%s' % blog_id)


class EditComment(Controller):

    """Edit Comment"""

    def get(self, comment_id):
        key = int(comment_id)
        c = Comments.get_by_id(key)

        if self.user:
            self.render('edit-comment.html', content = c.content,
                                             blog_id = c.blog_id)
        else:
            self.redirect('/%s' % c.blog_id)

    def post(self, comment_id):
        key = int(comment_id)
        c = Comments.get_by_id(key)
        content = self.request.get('content')

        if content:
            if self.user.name == c.author.name:
                c.content = content # update the comment's content
                c.put()
                time.sleep(0.1)

        self.redirect('/%s' % c.blog_id)


class NewComment(Controller):

    """New Comment"""

    def get(self, blog_id):
        pass

    def post(self, blog_id):
        blog_id = int(blog_id)
        content = self.request.get('content')

        # new comment have content,
        # the current user, and the blog_id
        if self.user and content:
            c = Comments(content = content,
                         author = self.user,
                         blog_id = blog_id)
            c.put()
            time.sleep(0.1)

        self.redirect('/%s' % blog_id)
