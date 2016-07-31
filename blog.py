from users import User
from google.appengine.ext import ndb

def blog_key(name = 'default'):

    """Assigns a key to Blog"""

    return ndb.Key('blogs', name)


class Blog(ndb.Model):

    """Blog's Model info"""

    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)


class Comment(ndb.Model):

    """Comment's Model Info"""

    post_id = ndb.IntegerProperty(required = True)
    author = ndb.StructuredProperty(User)
    content = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)


class Like(ndb.Model):

    """Like's Model Info"""

    post_id = ndb.IntegerProperty(required = True)
    author = ndb.StructuredProperty(User)
