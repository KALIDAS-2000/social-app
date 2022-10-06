from django.contrib import admin
from ekart.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(Reviews)

