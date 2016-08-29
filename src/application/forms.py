"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from models import ExampleModel
from models import PageModel


class ClassicExampleForm(wtf.Form):
    example_name = wtf.TextField('Name', validators=[validators.Required()])
    example_description = wtf.TextAreaField('Description', validators=[validators.Required()])

# App Engine ndb model form example
ExampleForm = model_form(ExampleModel, wtf.Form, field_args={
    'example_name': dict(validators=[validators.Required()]),
    'example_description': dict(validators=[validators.Required()]),
})


# class ClassicPageForm(wtf.Form):
#     page_name = wtf.TextField('PageName', validators=[validators.Required()])
#     page_content = wtf.TextAreaField('PageContent', validators=[validators.Required()])
#     added_by = wtf.TextField('Author', validators=[validators.Required()])
#     order = wtf.TextField('order', validators=[validators.Required()])
#     assigned = wtf.TextField('assigned', validators=[validators.Required()])

PageForm = model_form(PageModel, wtf.Form, field_args={
    'page_name': dict(validators=[validators.Required()]),
    'url_name': dict(validators=[validators.Required()]),
    'page_content': dict(validators=[validators.Required()])
})
