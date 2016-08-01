from google.appengine.ext import ndb
from users_model import User


class Comments(ndb.Model):

    """Comment's Info"""

    author = ndb.StructuredProperty(User)
    blog_id = ndb.IntegerProperty(required = True)
    content = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
