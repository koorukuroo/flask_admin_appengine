"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class ExampleModel(ndb.Model):
    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

class PageModel(ndb.Model):
    """Page Model"""
    page_name = ndb.StringProperty(required=True)
    url_name = ndb.StringProperty(required=True)
    page_content = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    order = ndb.IntegerProperty(default=0)
    assigned = ndb.IntegerProperty(default=0)
    depth = ndb.IntegerProperty(default=0)

class PageOrderModel(ndb.Model):
    """Page Order Model"""
    page_name = ndb.StringProperty(required=True)
    page_id = ndb.StringProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    order = ndb.IntegerProperty()
    assigned = ndb.IntegerProperty()

class HtmlModel(ndb.Model):
    """Page Order Model"""
    name = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
