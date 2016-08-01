import webapp2

from controllers.account_controller import *
from controllers.blog_controller import *
from controllers.index_controller import Index
from controllers.comment_controller import *

app = webapp2.WSGIApplication([
    ('/', Index),

    ('/login', Login),
    ('/logout', Logout),
    ('/newpost', NewPost),
    ('/signup', Signup),

    ('/(\d+)', Permalink),
    ('/delete/(\d+)', DeletePost),
    ('/edit/(\d+)', EditPost),

    ('/delete-comment/(\d+)', DeleteComment),
    ('/edit-comment/(\d+)', EditComment),
    ('/new-comment/(\d+)', NewComment)
], debug = True)
