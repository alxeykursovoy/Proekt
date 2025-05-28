from django.contrib import admin
from .models import Category, Tag, Product, Feedback

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Feedback)