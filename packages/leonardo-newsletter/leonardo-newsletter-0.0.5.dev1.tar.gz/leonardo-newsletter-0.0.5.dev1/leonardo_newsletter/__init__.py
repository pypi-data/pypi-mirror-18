
from django.apps import AppConfig

default_app_config = 'leonardo_newsletter.Config'


LEONARDO_APPS = [
    'leonardo_newsletter',
    'emencia.django.newsletter',
    'tagging'
]

LEONARDO_OPTGROUP = 'Newsletter'

LEONARDO_WIDGETS = [
    'leonardo_newsletter.models.SubscriptionFormWidget'
]

LEONARDO_PLUGINS = [
    ('leonardo_newsletter.apps.newsletter', 'Newsletter Mailing Lists'),
]

LEONARDO_REQUIREMENTS = [
    "http://github.com/michaelkuty/emencia-django-newsletter"
    "/archive/master.zip#emencia_django_newsletter==0.4.5"
]


class Config(AppConfig):
    name = 'leonardo_newsletter'
    verbose_name = "leonardo-newsletter"
