from google.appengine.ext import ndb


class Guestbook(ndb.Model):
    ime = ndb.StringProperty()
    priimek = ndb.StringProperty()
    email = ndb.StringProperty()
    sporocilo = ndb.StringProperty()
    ustvarjeno = ndb.DateTimeProperty(auto_now_add=True)
