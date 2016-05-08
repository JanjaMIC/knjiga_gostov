#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Guestbook


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class PosljivguestbookHandler(BaseHandler):
    def post(self):
        uporabnikovo_ime = self.request.get("ime")
        uporabnikov_priimek = self.request.get("priimek")
        uporabnikov_email = self.request.get("email")
        uporabnikovo_sporocilo = self.request.get("sporocilo")
        ustvarjeno = self.request.get("ustvarjeno")

        guestbook = Guestbook(ime=uporabnikovo_ime, priimek=uporabnikov_priimek, email=uporabnikov_email, sporocilo=uporabnikovo_sporocilo, ustvarjeno=ustvarjeno)
        guestbook.put()

        return self.render_template("guestbook_poslano.html")


class PrikaziGuestbooklaHandler(BaseHandler):
    def get(self):
        vsi_vnosi = Guestbook.query().order(Guestbook.ustvarjeno).fetch()

        view_vars = {
            "vsi_vnosi": vsi_vnosi
        }

        return self.render_template("prikazi_vnose.html", view_vars)


class PosamezenVnos(BaseHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))

        view_vars = {
            "guestbook": guestbook
        }

        return self.render_template("posamezen_vnos.html", view_vars)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/guestbook_poslano', PosljivguestbookHandler),
    webapp2.Route('/prikazi_vnose', PrikaziGuestbookHandler),
    webapp2.Route('/guestbook/<guestbook_id:\d+>', PosamezenVnos),
], debug=True)
