from django import template
import re

from django.conf.urls import url
from django.urls import reverse


class _Menu:
    parents = []
    childs = []
    models_icon = {}

    def clear(self):
        self.parents = []
        self.childs = []

    def add(self, label, link='', icon='', id='', parent=''):

        if id == '':
            id = label

        if parent != '':
            child = {
                id: {
                    'label': label,
                    'link': link,
                    'icon': icon,
                    'childs': []
                }
            }

            self.childs.append(child)

            for idx, parent_item in enumerate(self.parents):

                if parent in parent_item:
                    self.parents[idx][parent]['childs'].append(child)
                else:
                    for idx, child_item in enumerate(self.childs):
                        if parent in child_item:
                            self.childs[idx][parent]['childs'].append(child)

        else:
            self.parents.append({
                id: {
                    'label': label,
                    'link': link,
                    'icon': icon,
                    'childs': []
                }
            })

    def render(self, context, menus={}):
        r = ''

        if len(menus) <= 0:
            # sorted(self.parents)
            menus = self.parents

            r = '<li><a href="' + reverse('admin:index') + '"><i class="fa fa-dashboard"></i> <span>Home</span></a></li>'

        for group in menus:
            key = [key for key in group][0]
            icon = '<i class="fa fa-circle"></i>'

            if group[key]['icon'] != '':
                if re.match(r'\<([a-z]*)\b[^\>]*\>(.*?)\<\/\1\>', group[key]['icon']):
                    icon = group[key]['icon']
                else:
                    icon = '<i class="%s"></i>' % (group[key]['icon'])

            if len(group[key]['childs']) > 0:
                r += '<li class="treeview"><a href="#">%s <span>%s</span><span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span></a><ul class="treeview-menu">\n' % (
                    icon, group[key]['label'])

                r += self.render(context, group[key]['childs'])

                r += '</ul></li>\n'

            else:
                r += '<li><a href="%s">%s <span>%s</span></a></li>\n' % (
                    group[key]['link'], icon, group[key]['label'])

        return r

    def admin_apps(self, context, r):

        for app in context['available_apps']:
            r += '<li class="treeview"><a href="#"><i class="fa fa-circle"></i> <span>%s</span><span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span></a><ul class="treeview-menu">\n' % (
                app['name'])

            for model in app['models']:
                if 'add_url' in model:
                    url = model['add_url']

                if 'change_url' in model:
                    url = model['change_url']

                # if 'delete_url' in model:
                #     url = model['delete_url']

                if 'admin_url' in model:
                    url = model['admin_url']

                icon = '<i class="fa fa-circle-o"></i>'
                if model['name'] in self.models_icon:
                    if self.models_icon[model['name']] != '':
                        if re.match(r'\<([a-z]*)\b[^\>]*\>(.*?)\<\/\1\>', self.models_icon[model['name']]):
                            icon = self.models_icon[model['name']]
                        else:
                            icon = '<i class="%s"></i>' % (self.models_icon[model['name']])

                r += '<li><a href="%s">%s %s</a></li>' % (url, icon, model['name'])

            r += '</ul></li>\n'

        return r

    def set_model_icon(self, model_name, icon):
        self.models_icon[model_name.title()] = icon

    def get_model_icon(self, context):

        icon = '<i class="fa fa-circle-o"></i>'
        if context['model']['name'] in self.models_icon:
            if self.models_icon[context['model']['name']] != '':
                if re.match(r'\<([a-z]*)\b[^\>]*\>(.*?)\<\/\1\>', self.models_icon[context['model']['name']]):
                    icon = self.models_icon[context['model']['name']]
                else:
                    icon = '<i class="%s"></i>' % (self.models_icon[context['model']['name']])

        return icon

register = template.Library()

Menu = _Menu()


@register.simple_tag(takes_context=True)
def menu(context):
    # user = context['request'].user

    return Menu.admin_apps(context, Menu.render(context))

@register.simple_tag(takes_context=True)
def icon(context):
    return Menu.get_model_icon(context)

