from __future__ import unicode_literals

from django.contrib import admin

from .models import Attribute, Choice, Unit


admin.site.register(Attribute)
admin.site.register(Choice)
admin.site.register(Unit)
