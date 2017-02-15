from django.conf.urls import patterns, url
from expans import views , api_views
from django.conf import settings
from django.conf.urls.static import static


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
	url(r'^companymyitemdetails/(?P<mylistid>\d+)/$',views.companymyitemdetails,name='companymyitemdetails'),
    url(r'^company_add_advance/(?P<mylistid>\d+)/$',views.company_add_advance,name='company_add_advance'),
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
	url(r'^suppliermyitemdetails/(?P<mylistid>\d+)/$',views.suppliermyitemdetails,name='suppliermyitemdetails'),

#	url(r'^add_oraganization/$',views.add_oraganization,name='add_oraganization'),
    url(r'^supplier_add_advance/(?P<mylistid>\d+)/$',views.supplier_add_advance,name='supplier_add_advance'),
#================================================================================
    url(r'^dashboard/$',views.dashboard,name='dashboard'),


	
#=================== API VIEWS URL=========================================>

	# user list
    url(r'^api/user/$', api_views.UserList.as_view()),
	url(r'^api/create_user/$', api_views.UserCreate.as_view()),

    url(r'^api/item/$', api_views.ItemList.as_view()),
    url(r'^api/item/(?P<pk>[0-9]+)/$', api_views.ItemDetail.as_view()),
    # url(r'^api/item/(?P<pk>[0-9]+)/$', api_views.ChoiceDetail.as_view()),
  
  # complete mylist
  	url(r'^api/mylist/$', api_views.MylistList.as_view()),
    
    # mylist for supplier
    url(r'^api/supmylist/(?P<pk>[0-9]+)/$', api_views.SupMyList.as_view()),

    url(r'^api/suporgmylist/(?P<pk1>[0-9]+)/(?P<pk2>[0-9]+)/$', api_views.SupOrgMyList.as_view()),
    
    # mylist for organization
    url(r'^api/orgmylist/(?P<pk>[0-9]+)/$', api_views.OrgMyList.as_view()),
   
    url(r'^api/mylist/(?P<pk>[0-9]+)/$', api_views.MylistDetail.as_view()),

    # for transaction
    url(r'^api/trans/$', api_views.TransactionList.as_view()),
    url(r'^api/transtoday/(?P<pk>[0-9]+)/$', api_views.Transtoday.as_view()),
    url(r'^api/transweek/(?P<pk>[0-9]+)/$', api_views.Transweek.as_view()),
    url(r'^api/transmonth/(?P<pk>[0-9]+)/$', api_views.Transmonth.as_view()),
    


    # transaction for supplier
    url(r'^api/mytrans/(?P<pk>[0-9]+)/$', api_views.MyTransactionList.as_view()),
   
    # url(r'^api/trans/(?P<pk>[0-9]+)/$', api_views.TransactionDetail.as_view()),

    url(r'^api/payment/(?P<pk>[0-9]+)/$', api_views.payment.as_view()),
    url(r'^api/mypayment/(?P<pk>[0-9]+)/$', api_views.Mypayment.as_view()),

	)