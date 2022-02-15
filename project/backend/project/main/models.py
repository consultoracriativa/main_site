from django.db import models
from datetime import datetime


class ContentCategory(models.Model):
    category = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True)  # Category items / menu items should be unique
    text_show = models.CharField(max_length=100, blank=False, null=False)
    show_on_menu = models.BooleanField(blank=False, default=True)
    order = models.IntegerField(blank=True, default=0)
    template = models.CharField(
        max_length=50,
        blank=True,
        help_text="If present, use this template instead the standard one")
    user_is_logged = models.BooleanField(
        blank=False,
        default=False,
        help_text="Only display this entry if the user is logged in.")
    active = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return "{} - {} - {}".format(self.text_show, self.active, self.order)


class ContentContent(models.Model):
    category = models.ForeignKey(ContentCategory, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=300, null=True, blank=True)
    card_body = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    teaser_image = models.ImageField(upload_to='images/', blank=True, null=True)
    content_image = models.ImageField(upload_to='images/', blank=True, null=True)
    order = models.IntegerField(blank=True, default=0)
    show_on_homepage = models.BooleanField(blank=False, default=False)
    read_more = models.BooleanField(blank=False, default=False)
    alternate_target_url = models.CharField(
        max_length=50,
        blank=True,
        help_text="If present, detail button will direct to destination, instead of content detail.")
    alternate_read_more_label = models.CharField(
        max_length=50,
        blank=True,
        help_text="If present, will display on 'read more' button.")
    publish_date = models.DateField(blank=False, null=False, default=datetime.now)
    template = models.CharField(
        max_length=50,
        blank=True,
        help_text="If present, use this template instead the standard one")
    user_is_logged = models.BooleanField(
        blank=False,
        default=False,
        help_text="Only display this entry if the user is logged in.")
    active = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return "{} - {}".format(self.title, self.category)
