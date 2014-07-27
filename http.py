from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.web.util import redirectTo
from twisted.web.util import Redirect

class LoginPage(Resource):
    def render_GET(self,request):
        return self.login()
    def render_POST(self,request):
        username=request.args['admin'][0]
        password=request.args['pwd'][0]

        return self.authentication(username,password,request)
    def login(self):
        with open("html/login.html") as login:
            html=login.read()
        return html
    def authentication(self,username,password,request):
        username=username
        password=password
        if username != 'admin':
            return redirectTo('admin',request)
        return redirectTo ('home',request)


class HomePage(Resource):
    def render_GET(self,request):
        self.setHeader("Content-Type","text/html; charset=GB2312")
        return self.home()
    def home(self):
        with open("html/home.html") as home:
            html=home.read()
        return html

root=Resource()
root.putChild("admin",LoginPage())
root.putChild("home",HomePage())
HttpFactory=Site(root)