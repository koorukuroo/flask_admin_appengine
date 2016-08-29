# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request

from models import PageModel
from models import HtmlModel
from forms import PageForm

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from decorators import login_required

import json

# from jinja2 import Undefined


class MenuOrder(View):

    # def dispatch_request(self):
    #     return redirect(url_for('list_examples'))
    def dispatch_request(self):
        nonassigned = PageModel.query(PageModel.assigned==0).order(PageModel.order, -PageModel.timestamp)
        assigned = PageModel.query(PageModel.assigned==1).order(PageModel.order)
        html = ''
        """
            {% for page in assigned %}
                {% set page_id = page.key.id() %}
                {% if page.depth == 0 %}
                <li id="list_2_{{ page_id }}">
                    <div>{{ page.page_name }}</div>

                {% elif page.depth == 1 %}
                <ol>
                    <li id="list_2_{{ page_id }}">
                        <div>{{ page.page_name }}</div>

                {% elif page.depth == 2 %}
                <ol>
                    <li id="list_2_{{ page_id }}">
                        <div>{{ page.page_name }}</div>
                {% endif %}
            {% endfor %}
        """
        for idx, page in enumerate(assigned):
            if idx == 0:
                html = """<li id='list_2_"""+str(page.key.id())+"""'><div>"""+page.page_name+"""</div><cand1></li><cand0>"""
                before_depth = 0
                continue
            if page.depth == 0:
                cand0 = ''
                if before_depth == 0:
                    html = html.replace('<cand1>', '')
                elif before_depth == 1:
                    html = html.replace('<cand2>', '')
                    html = html.replace('<cand1>', '</ol>')
                elif before_depth == 2:
                    html = html.replace('<cand2>', '</ol>')
                    html = html.replace('<cand1>', '</ol>')
                cand0 += """<li id='list_2_"""+str(page.key.id())+"""'><div>"""+page.page_name+"""</div><cand1></li><cand0>"""
                html = html.replace('<cand0>', cand0)
            elif page.depth == 1:
                cand1 = ''
                if before_depth == 0:
                    cand1 += '<ol>'
                elif before_depth == 1:
                    html = html.replace('<cand2>', '')
                elif before_depth == 2:
                    html = html.replace('<cand2>', '</ol>')
                cand1 += """<li id='list_2_"""+str(page.key.id())+"""'><div>"""+page.page_name+"""</div><cand2></li><cand1>"""
                html = html.replace('<cand1>', cand1)
            elif page.depth == 2:
                cand2 = ''
                if before_depth == 1:
                    cand2 += '<ol>'
                cand2 += """<li id='list_2_"""+str(page.key.id())+"""'><div>"""+page.page_name+"""</div></li><cand2>"""
                html = html.replace('<cand2>', cand2)

            before_depth = page.depth

        # return html
        return render_template('menu_order.html', nonassigned=nonassigned, assigned=html)

class MenuOrderData(View):
    # def dispatch_request(self):
    #     return redirect(url_for('list_examples'))
    # @login_required
    # 무단으로 주소에 POST 날릴 때를 고려.
    def dispatch_request(self):
        data = request.values.get('data') # POST Value
        kind = request.values.get('kind')
        if kind == 'output1':
            kind = 0
        elif kind == 'output2':
            kind = 1

        # print '=================================='
        # print data



        """
        list_1[5629499534213120]=root&list_1[5066549580791808]=root&list_1[6192449487634432]=root&list_1[4785074604081152]=6192449487634432
        """
        # data = json.loads(data) # Type Converting
        # print '=================================='
        # print data
        """ Data Parsing """
        data = data.replace('list_1[', '').replace('list_2[', '').replace(']', '')
        if data == '':
            return '200'
        result = dict()
        for idx, d in enumerate(data.split('&')):
            key, value = d.split('=')
            if value == 'root':
                depth = 0
            else:
                depth = result[value] + 1
            result[key] = depth
            # print '====================='
            # print key
            page = PageModel.get_by_id(int(key))
            page.assigned = kind
            page.order = idx
            page.depth = depth
            page.put()
            # print idx, key, value, depth


        # jQuery.nestable CODE
        # result = []
        # idx = 0
        # for datum in data:
        #     if 'iid' in datum:
        #         continue
        #
        #     # Find children : depth 1
        #     if 'children' in datum:
        #         for d in datum['children']:
        #             # print '=================================='
        #             # print d
        #             # print d['id']
        #             # Find second children : depth 2
        #             if 'children' in d:
        #                 for dd in d['children']:
        #                     depth = 2
        #                     page = PageModel.get_by_id(dd['id'])
        #                     page.assigned = kind
        #                     page.order = idx
        #                     page.depth = depth
        #                     page.put()
        #                     idx += 1
        #
        #             depth = 1
        #             page = PageModel.get_by_id(d['id'])
        #             page.assigned = kind
        #             page.order = idx
        #             page.depth = depth
        #             page.put()
        #             idx += 1
        #
        #     # print 'id:::::', str(datum['id'])
        #     depth = 0
        #     page = PageModel.get_by_id(datum['id'])
        #     page.assigned = kind
        #     page.order = idx
        #     page.depth = depth
        #     page.put()
        #     idx += 1
        #     page_name = page.page_name
        #     result.append((page_name, datum['id']))

        """ Make Nav HTML """
        nav = PageModel.query(PageModel.assigned == 1).order(PageModel.order)
        for idx, page in enumerate(nav):
            if idx == 0:
                html = """<li class="dropdown active"><a href="javascript:void(0);" class="dropdown-toggle" data-hover="dropdown" data-toggle="dropdown">"""+page.page_name+"""</a><cand1></li><cand0>"""
                before_depth = 0
                continue
            if page.depth == 0:
                cand0 = ''
                if before_depth == 0:
                    html = html.replace('<cand1>', '')
                elif before_depth == 1:
                    html = html.replace('<cand2>', '')
                    html = html.replace('<cand1>', '</ol>')
                elif before_depth == 2:
                    html = html.replace('<cand2>', '</ol>')
                    html = html.replace('<cand1>', '</ol>')
                cand0 += """<li><a href='"""+page.url_name+"""'>"""+page.page_name+"""</a><cand1></li><cand0>"""
                html = html.replace('<cand0>', cand0)
            elif page.depth == 1:
                cand1 = ''
                if before_depth == 0:
                    cand1 += '<ul class="dropdown-menu">'
                elif before_depth == 1:
                    html = html.replace('<cand2>', '')
                elif before_depth == 2:
                    html = html.replace('<cand2>', '</ol>')
                cand1 += """<li><a href='"""+page.url_name+"""'>"""+page.page_name+"""</a><cand2></li><cand1>"""
                html = html.replace('<cand1>', cand1)
            elif page.depth == 2:
                cand2 = ''
                if before_depth == 1:
                    cand2 += '<ol>'
                cand2 += """<li id='list_2_"""+str(page.key.id())+"""'><div>"""+page.page_name+"""</div></li><cand2>"""
                html = html.replace('<cand2>', cand2)
            before_depth = page.depth
        html = html.replace('<cand0>', '').replace('<cand1>', '')
        # HTML Write
        html = HtmlModel(
            name='nav',
            content=html,
            added_by=users.get_current_user()
        )
        html.put()
        # print 'writing..............'
        # with open("./menutest.txt", "wb") as fo:
        #     fo.write("This is Test Data")
        # text_file = open("./menutest.html", "w")
        # text_file.write(html)
        # text_file.close()

        return '200'

        # print str(request.values.get('data'))
        # return render_template('menu_order.html', nonassigned=nonassigned, assigned=assigned)

#
# class PageCreate(View):
#
#     def dispatch_request(self):
#         page = PageModel.query()
#         form = PageForm()
#         if form.validate_on_submit():
#             page = PageModel(
#                 page_name=form.page_name.data,
#                 page_content=form.page_content.data,
#                 added_by=users.get_current_user()
#             )
#             try:
#                 page.put()
#                 page_id = page.key.id()
#                 flash(u'Page %s successfully saved.' % page_id, 'success')
#                 return redirect(url_for('page_list'))
#             except CapabilityDisabledError:
#                 flash(u'App Engine Datastore is currently in read-only mode.', 'info')
#                 return redirect(url_for('page_list'))
#         return render_template('page_create.html', page=page, form=form)
#
#
# class PageEdit(View):
#
#     @login_required
#     def dispatch_request(self, page_id):
#         page = PageModel.get_by_id(page_id)
#         if page == None:
#             return render_template('error.html')
#
#         form = PageForm(obj=page)
#         if request.method == "POST":
#             if form.validate_on_submit():
#                 page.page_name = form.data.get('page_name')
#                 page.page_content = form.data.get('page_content')
#                 page.put()
#                 flash(u'Page %s successfully saved.' % page_id, 'success')
#                 return redirect(url_for('page_list'))
#         return render_template('page_edit.html', page=page, form=form)
#
#
# class PageDelete(View):
#
#     @login_required
#     def dispatch_request(self, page_id):
#         page = PageModel.get_by_id(page_id)
#         if request.method == "POST":
#             try:
#                 page.key.delete()
#                 flash(u'Page %s successfully deleted.' % page_id, 'success')
#                 return redirect(url_for('page_list'))
#             except CapabilityDisabledError:
#                 flash(u'App Engine Datastore is currently in read-only mode.', 'info')
#                 return redirect(url_for('page_list'))
#
