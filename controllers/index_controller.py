from google.appengine.ext import ndb
from main import Controller


class Index(Controller):

    """Home Route Showing All Blog Post(s)"""

    def get(self):
        blogs = ndb.gql("SELECT * FROM Blog ORDER BY created DESC")
        self.render('blog.html', blogs = blogs)
