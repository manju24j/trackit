from django.conf.urls import patterns, url
from expans import views

urlpatterns = patterns('',

	url(r'^$', views.index, name='index'),
#	url(r'^about/$', views.about, name='about'),
    url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^add_item/$', views.add_item, name='add_item'),

# COMPANY SIDE OPERATIONS===================>

	url(r'^company/$',views.company,name='company'),
    url(r'^select_Item/$', views.select_Item, name='select_Item'),
    url(r'^select_supplier/$',views.select_supplier,name='select_supplier'),

    url(r'^comp_add_supplier/$',views.comp_add_supplier,name='comp_add_supplier'),
    url(r'^comp_select_supplier/$',views.comp_select_supplier,name='comp_select_supplier'),

    url(r'^get_item_details/$', views.get_item_details, name='get_item_details'),
	url(r'^get_sup_details/$', views.get_sup_details, name='get_sup_details'),

	url(r'^company_add_entry/(?P<mylistid>\d+)/$',views.company_add_entry,name='company_add_entry'),

	url(r'^company_mylist/$',views.company_mylist,name='company_mylist'),
	url(r'^company_transaction/$',views.company_transaction,name='company_transaction'),
	url(r'^payment/$',views.payment,name='payment'),

# SUPLIER SIDE OPERATIONS===================>
	url(r'^supplier/$',views.supplier,name='supplier'),

	url(r'^supplier_mylist/$',views.supplier_mylist,name='supplier_mylist'),
	url(r'^supplier_transaction/$',views.supplier_transaction,name='supplier_transaction'),

	url(r'^sup_add_company/$',views.sup_add_company,name='sup_add_company'),
	url(r'^sup_select_company/$',views.sup_select_company,name='sup_select_company'),

	url(r'^get_org_details/$', views.get_org_details, name='get_org_details'),

	url(r'^supplier_add_entry/(?P<mylistid>\d+)/$',views.supplier_add_entry,name='supplier_add_entry'),

	url(r'^supplier_entry/(?P<myorgid>\d+)/$',views.supplier_entry,name='supplier_entry'),

	url(r'^select_company/$',views.select_company,name='select_company'),
#	url(r'^myitemdetails/(?P<mylistid>\d+)/$',views.myitemdetails,name='myitemdetails'),
#	url(r'^add_oraganization/$',views.add_oraganization,name='add_oraganization'),
	


	)

  