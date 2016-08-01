from google.appengine.ext import ndb
from users_model import User


class Likes(ndb.Model):

    """Like's Model Info"""

    post_id = ndb.IntegerProperty(required = True)
    author = ndb.StructuredProperty(User)
