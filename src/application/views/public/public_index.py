# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, request, url_for, render_template

from models import PageModel, HtmlModel
from forms import PageForm

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from decorators import login_required


class PublicIndex(View):

    def dispatch_request(self):
        assigned = PageModel.query(PageModel.assigned == 1, PageModel.url_name == 'home')
        if assigned.count():
            content = assigned.get().page_content
            nav = HtmlModel.query(HtmlModel.name == 'nav').order(-HtmlModel.timestamp).get().content
            return render_template('public/index.html', content = content, nav=nav)
        else:
            return render_template('404.html')


class PublicUrl(View):

    def dispatch_request(self, url_name):
        assigned = PageModel.query(PageModel.assigned == 1, PageModel.url_name == url_name)
        if assigned.count():
            content = assigned.get().page_content
            # nav = PageModel.query(PageModel.assigned == 1).order(PageModel.order)
            nav = HtmlModel.query(HtmlModel.name == 'nav').order(-HtmlModel.timestamp).get().content
            return render_template('public/index.html', content=content, nav=nav)
        else:
            return render_template('404.html')

