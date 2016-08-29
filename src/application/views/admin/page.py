# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request

from models import PageModel
from forms import PageForm

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from decorators import login_required

# from jinja2 import Undefined


class PageList(View):

    # def dispatch_request(self):
    #     return redirect(url_for('list_examples'))
    def dispatch_request(self):
        pages = PageModel.query().order(-PageModel.timestamp)
        return render_template('page_list.html', pages=pages)


class PageCreate(View):

    def dispatch_request(self):
        page = PageModel.query()
        form = PageForm()
        # print 2222222222222222222222222222222222222222222222222222222222222222222222
        # print(form.errors)
        if form.validate_on_submit():
            page = PageModel(
                page_name=form.page_name.data,
                url_name=form.url_name.data,
                page_content=form.page_content.data,
                added_by=users.get_current_user()
            )
            # print 11111111111111111111111111111111111111111111111111111111111111111111111111111
            # print page.page_name
            try:
                page.put()
                page_id = page.key.id()
                flash(u'Page %s successfully saved.' % page_id, 'success')
                return redirect(url_for('page_list'))
            except CapabilityDisabledError:
                flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                return redirect(url_for('page_list'))
        return render_template('page_create.html', page=page, form=form)


class PageEdit(View):

    @login_required
    def dispatch_request(self, page_id):
        page = PageModel.get_by_id(page_id)
        if page == None:
            return render_template('error.html')

        form = PageForm(obj=page)
        if request.method == "POST":
            if form.validate_on_submit():
                page.page_name = form.data.get('page_name')
                page.url_name = form.data.get('url_name')
                page.page_content = form.data.get('page_content')
                page.put()
                flash(u'Page %s successfully saved.' % page_id, 'success')
                return redirect(url_for('page_list'))
        return render_template('page_edit.html', page=page, form=form)


class PageDelete(View):

    @login_required
    def dispatch_request(self, page_id):
        page = PageModel.get_by_id(page_id)
        if request.method == "POST":
            try:
                page.key.delete()
                flash(u'Page %s successfully deleted.' % page_id, 'success')
                return redirect(url_for('page_list'))
            except CapabilityDisabledError:
                flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                return redirect(url_for('page_list'))

