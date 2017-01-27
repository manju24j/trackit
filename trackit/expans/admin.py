from django.contrib import admin
from expans.models import Transaction,Mylist,Item,Supplier

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Mylist)
admin.site.register(Transaction)
