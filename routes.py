import webapp2

from controllers.account_controller import *
from controllers.comment_controller import *
from controllers.blog_controller import *
from controllers.index_controller import Index
from controllers.like_controller import *

app = webapp2.WSGIApplication([
    ('/', Index),

    ('/login', Login),
    ('/logout', Logout),
    ('/signup', Signup),

    ('/(\d+)', Permalink),
    ('/newpost', NewPost),
    ('/delete/(\d+)', DeletePost),
    ('/edit/(\d+)', EditPost),

    ('/delete-comment/(\d+)', DeleteComment),
    ('/edit-comment/(\d+)', EditComment),
    ('/new-comment/(\d+)', NewComment),

    ('/like/(\d+)', Like),
    ('/unlike/(\d+)', Unlike)
], debug=True)
