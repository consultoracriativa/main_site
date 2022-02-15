from datetime import datetime
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from . import models


def get_basics(user_is_logged) -> tuple:
    """
    Menu entries are filtered by user is logged or not.
    :param bool user_is_logged:
    :return: objects of menu, header and footer contex
    :rtype: tuple
    """
    menu = models.ContentCategory.objects.filter(active=True,
                                                 show_on_menu=True).values('category', 'text_show').order_by('order')
    if not user_is_logged:
        menu = menu.filter(user_is_logged=False)

    header = models.ContentContent.objects.filter(category__category='header', active=True).first()
    footer = models.ContentContent.objects.filter(category__category='footer', active=True).first()

    return menu, header, footer


class Home(View):
    template_name = 'main/home.html'
    context = {
        'page_title': 'Home Page',
        'data': {
            'name': "Home Page",
        }
    }

    def get(self, request):
        user_is_logged = request.user.is_authenticated
        menu, header, footer = get_basics(user_is_logged)

        self.context['user_is_logged'] = user_is_logged
        self.context['menu'] = menu
        self.context['header'] = header
        self.context['footer'] = footer

        carousel = models.ContentContent.objects.filter(category__category='carousel',
                                                        active=True,
                                                        publish_date__lte=datetime.now().date()).order_by('?')  # Random order

        content = models.ContentContent.objects.filter(show_on_homepage=True,
                                                       active=True,
                                                       publish_date__lte=datetime.now().date()).order_by('order')

        if not user_is_logged:
            carousel = carousel.filter(user_is_logged=False)
            content = content.filter(user_is_logged=False, category__user_is_logged=False)

        self.context['content'] = content
        self.context['carousel'] = carousel

        return render(request, self.template_name, self.context)


class Category(View):
    template_name = 'main/category.html'

    def get(self, request, category):
        does_not_exist = False
        content = None
        category_desc = menu_item = None

        try:
            category_obj = models.ContentCategory.objects.get(category=category)
        except models.ContentCategory.DoesNotExist:
            does_not_exist = '[ Content not available ]'

        user_is_logged = request.user.is_authenticated
        menu, header, footer = get_basics(user_is_logged)

        if not does_not_exist:
            content = models.ContentContent.objects.filter(
                category__category=category,
                active=True, publish_date__lte=datetime.now().date()
            ).order_by('order', Lower('title'))

            if not user_is_logged:
                content = content.filter(user_is_logged=False)

            category_desc = [x for x in menu if x['category'] == category][0]['text_show']

            if category_obj.template:
                self.template_name = f"main/category/{category_obj.template}.html"

        context = {
            'page_title': category,
            'category_desc': category_desc,
            'user_is_logged': user_is_logged,
            'menu': menu,
            'header': header,
            'footer': footer,
            'does_not_exist': does_not_exist,
            'content': content,
        }
        return render(request, self.template_name, context)


class Content(View):
    template_name = 'main/content.html'

    def get(self, request, category, content_id):

        def _content_not_available():
            return None, "[Content not available ]"

        user_is_logged = request.user.is_authenticated
        content = None
        does_not_exist = False
        category_desc = menu_item = None

        try:
            content = models.ContentContent.objects.get(pk=content_id, active=True, publish_date__lte=datetime.now())
        except models.ContentContent.DoesNotExist:
            content, does_not_exist = _content_not_available()
        else:
            if not user_is_logged:
                if (content.user_is_logged or content.category.user_is_logged)is True:
                    content, does_not_exist = _content_not_available()

        menu, header, footer = get_basics(user_is_logged)

        if content:
            menu_item = content.category.category
            category_desc = content.category.text_show

            if content.template:
                self.template_name = f"main/content/{content.template}.html"

        context = {
            'page_title': category_desc,
            'menu': menu,
            'user_is_logged': user_is_logged,
            'header': header,
            'footer': footer,
            'menu_item': menu_item,
            'category_desc': category_desc,
            'does_not_exist': does_not_exist,
            'content': content,
        }
        return render(request, self.template_name, context)


class ContactForm(View):

    """ Handles the submission of ContactForm """

    def get(self, request):
        """ If contact_form called directly, return home page"""
        return HttpResponseRedirect('/')

    def post(self, request, **kwargs):
        print("request.POST")
        print(request.POST)
        return HttpResponseRedirect('/')
