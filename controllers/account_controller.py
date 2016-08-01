from main import Controller
from models.blog_model import Blog
from models.users_model import *


class Login(Controller):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)
        if user:
            self.login(user)
            self.redirect('/')
        else:
            error = "Username or password is incorrect"
            self.render('login.html', username = username, error = error)


class Logout(Controller):

    def get(self):
        self.logout()
        self.redirect('/')


class Signup(Controller):

    """Signup Page"""

    def get(self):
        self.render('signup.html')

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username, email = self.email)

        username_exist = User.by_name(self.username)

        if not valid_username(self.username):
            params['error_username'] = "Username is not valid"
            have_error = True
        elif username_exist:
            params['error_username'] = 'That user already exists.'
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "Password is not valid"
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "Email is not valid"
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            user = User.register(self.username, self.password, self.email)
            user.put()
            self.login(user)
            self.redirect('/')
