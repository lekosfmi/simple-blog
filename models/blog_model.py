from google.appengine.ext import ndb
from users_model import User

def blog_key(name = 'default'):

    """Assign a key to Blog"""

    return ndb.Key('blogs', name)


class Blog(ndb.Model):

    """Blog's Info"""

    author = ndb.StructuredProperty(User)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    like = ndb.IntegerProperty(default = 0)
    subject = ndb.StringProperty(required = True)
