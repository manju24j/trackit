from django.shortcuts import render ,redirect
from django.shortcuts import (render_to_response)
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime ,date ,timedelta
from django.db import IntegrityError
from django.contrib import messages
from expans.models import Item ,Supplier,Transaction,Mylist,Oraganization ,Payment
from expans.forms import ItemForm,MylistForm

from django.core import serializers

from django.http import Http404

# def home(request):
#    context = RequestContext(request,
#                            {'user': request.user})

#    return render_to_response('expans/base.html',
#                              context_instance=context)
def index(request):
    context = RequestContext(request)
    context_dict={}

    return render_to_response('expans/index.html', context_dict, context)

def register(request):
    # Request the context.
    context = RequestContext(request)
    context_dict = {}
    # Boolean telling us whether registration was successful or not.
    # Initially False; presume it was a failure until proven otherwise!
    registered = False

    # If HTTP POST, we wish to process form data and create an account.
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        phoneno=request.POST['phoneno']
        category=request.POST['category']

        try:
            people=request.POST['people']
            ophone=Oraganization.objects.get(phoneno=phoneno)
            messages.warning(request, "user containing this no already in use")
            return HttpResponseRedirect('/expans/register/')
        except:
            try:
                if category=='c':
                    user = User(username=username,password=password)
                    user.set_password(user.password)
                    user.save()

                    org=Oraganization(phoneno=phoneno,people=people)
                    org.user = user
                    org.save()
                    registered = True

            except IntegrityError as e:
                messages.warning(request, "this company name already in use")
                return HttpResponseRedirect('/expans/register/')
                # return render_to_response('expans/register.html',context_dict,context)

        try:
            sphone=Supplier.objects.get(phoneno=phoneno)
            messages.warning(request, "user containing this no already in use")
            return HttpResponseRedirect('/expans/register/')
        except:
            try:
                if category=='s':
                    user = User(username=username,password=password)
                    user.set_password(user.password)
                    user.save()
                    sup=Supplier(phoneno=phoneno)
                    sup.user=user
                    sup.save()
                    registered = True
            except IntegrityError as e:
                messages.warning(request,"supplier with this name already in use")
                return HttpResponseRedirect('/expans/register/')
                # return render_to_response('expans/register.html',context_dict,context)


    # Not a HTTP POST, so we render the two ModelForms to allow a user to input their data.

    context_dict['registered'] = registered

    # Render and return!
    return render_to_response('expans/register.html',context_dict,context)

def user_login(request):
    # Obtain our request's context.
    context = RequestContext(request)
    context_dict = {}

    # If HTTP POST, pull out form data and process it.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Attempt to log the user in with the supplied credentials.
        # A User object is returned if correct - None if not.
        user = authenticate(username=username, password=password)

        # A valid user logged in?
        if user is not None:
            # Check if the account is active (can be used).
            # If so, log the user in and redirect them to the homepage.
            if user.is_active:
                login(request, user)
                context = RequestContext(request,
                           {'user': request.user})
                try:
                    u=Oraganization.objects.get(user=request.user)
                    return HttpResponseRedirect('/expans/company/')
                except:
                    return HttpResponseRedirect('/expans/supplier/')                
                    # The account is inactive; tell by adding variable to the template context.
            # else:
            #     context_dict['disabled_account'] = True
            #     # Invalid login details supplied!
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('expans/login.html', context_dict, context)

    # Not a HTTP POST - most likely a HTTP GET. In this case, we render the login form for the user.
    else:
        return render_to_response('expans/login.html', context_dict, context)

# Only allow logged in users to logout - add the @login_required decorator!
@login_required
def user_logout(request):
    # As we can assume the user is logged in, we can just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/expans/')


def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def get_org_list(user):
    orglist = []
    orglist = Oraganization.objects.filter(user=user)
        
    return orglist


def get_mylist_list(org):
    mylist = []
    mylist = Mylist.objects.filter(org=org)
    
    return mylist

    
#  COMPANIES ACTIVITY STARTS=================================
@login_required
def company(request):
    org=Oraganization.objects.get(user=request.user)
    mylist = Mylist.objects.filter(org=org)
    # mylist=get_mylist_list(org.id)
    if mylist:
        return company_home(request)
    else:
        return select_supplier(request)

    return company(request)

@login_required
def company_home(request):
    context = RequestContext(request)
    item_list=get_item_list()
    supplier_list=get_supplier_list()
    form = MylistForm()

    context_dict = {'item_list': item_list,
                    'supplier_list':supplier_list,
                    'form':form,
                    }
    org_u=Oraganization.objects.get(user=request.user)
    mylist=Mylist.objects.filter(org=org_u.id)
    context_dict['mylist']=mylist
    return render_to_response('expans/company/company_home.html',context_dict,context)    

@login_required
def company_mylist(request):
    context = RequestContext(request)
    item_list=get_item_list()
    supplier_list=get_supplier_list()
    context_dict = {
                    'item_list': item_list,
                    'supplier_list':supplier_list,
                    }
   
    org=Oraganization.objects.get(user=request.user)
    mylist=Mylist.objects.filter(org=org)
    context_dict['mylist']=mylist
    return render_to_response('expans/company/company_mylist.html',context_dict,context)

# adding no of qnty to the entry
@login_required
def company_add_entry(request,mylistid):
    context = RequestContext(request)
    context_dict={}
    
    if request.method == 'POST':
        my=Mylist.objects.get(id=mylistid)
        qnty=int(request.POST['qnty'])
        price=my.price
        total=qnty*float(price)

        trasaction_obj =Transaction(mylist=my,qnty=qnty,total=total)
        trasaction_obj.save()
        
        count=0
        trans=Transaction.objects.filter(mylist_id=mylistid)
        for t in trans:
            count=count+t.qnty

        payment2=Payment.objects.filter(mylist=mylistid)
        payment=payment2.latest('date')
        
        payment_list=Payment.objects.filter(mylist=mylistid)
        total=0
        for adv in payment_list:
            total=total+adv.advance
        balance=total

        total1=count*float(price)
        due=payment.balance-total1

        pay_obj = Payment(mylist=my,balance=balance,due=due,qnty=count,total=total1)
        pay_obj.save()
        

        qntty = str(qnty)
        company=str(my.org.user)
        measured=str(my.measured)
        item=str(my.item)
        messages.success(request, "You Added "+qntty+" "+measured+" of "+item+" ")
        return HttpResponseRedirect('/expans/company/')
        # return render_to_response('expans/company/company_home.html',context_dict,context)

    return render_to_response('expans/company/company_transaction.html',context_dict,context)


# Selecting new Item from the company side
@login_required
def  select_Item(request):
    context = RequestContext(request)
    item_list=get_item_list()
    supplier_list=get_supplier_list()  
    context_dict = {'item_list':item_list,}

    return render_to_response('expans/company/select_Item.html',context_dict,context)

def select_supplier(request):
    context = RequestContext(request)
    item_list=get_item_list()
    supplier_list=get_supplier_list()
    context_dict={ 'item_list':item_list,
                    'supplier_list':supplier_list,
                    }
                 
    return render_to_response('expans/company/select_supplier.html',context_dict,context)

def comp_add_supplier(request):
    context = RequestContext(request)
    context_dict={}
    if request.method == 'POST':
        username=request.POST['username']
        phoneno=request.POST['phoneno']
        itemid=request.POST['itemid']
        user=request.user
        print user
        org=Oraganization.objects.get(user=request.user)
        print org.id
        print phoneno
        try:
            item_present=Mylist.objects.get(org=org,item=itemid)
            print org.id
            print itemid
            print item_present.org.id
            messages.warning('already you have selected this Item, select other Item')
            return HttpResponseRedirect('/expans/comp_add_supplier/')
                # context_dict['this supplier is already in use select from list']=True
                # return render_to_response('expans/company/select_Item.html',context,context_dict)
            # return render_to_response('expans/company/comp_add_supplier.html',context,context_dict)
        except:
            try:
                sphone=Supplier.objects.get(phoneno=phoneno)
                messages.danger('this supplier is already registered select from list')
                return HttpResponseRedirect('/expans/comp_add_supplier/')
                # context_dict['this supplier is already in use select from list']=True
                # return render_to_response('expans/company/select_Item.html',context,context_dict)
            except:
                try:
                    password=12345
                    user = User(username=username,password=password)
                    user.set_password(user.password)
                    user.save()
                    sup=Supplier(phoneno=phoneno)
                    sup.user=user
                    sup.save()

                    org=Oraganization.objects.get(user=request.user)
                    measured=request.POST['measured']
                    price=request.POST['price']
                    itemid=request.POST['itemid']
                    item=Item.objects.get(id=itemid)
                    mylist=Mylist(item=item,measured=measured,price=price,org=org,sup=sup)
                    mylist.save()
                    messages.success(request," supplier  and item is added to your list")
                    return company_home(request)
                except IntegrityError as e:
                    messages.warning(request,"supplier with this name already in use")
                    return HttpResponseRedirect('/expans/comp_add_supplier/')
               
    return render_to_response("expans/company/select_supplier.html",context,context_dict)

def comp_select_supplier(request):
    if request.method == 'POST':
        itemid=request.POST['itemid']
        sphoneno=request.POST['phoneno']   
        org=Oraganization.objects.get(user=request.user)
        try:
            item_present=Mylist.objects.get(org=org,item=itemid)
            context_dict['Item is already selected']=True
            return render_to_response('expans/company/comp_add_supplier.html',context,context_dict)
        except:
            org=Oraganization.objects.get(user=request.user)
            sup=Supplier.objects.get(phoneno=sphoneno)
            measured=request.POST['measured']
            price=request.POST['price']
            item=Item.objects.get(id=itemid)
            mylist=Mylist(item=item,measured=measured,price=price,org=org,sup=sup)
            mylist.save()
            messages.success(request," supplier  and item is added to your list")
            return company_home(request)
               
    return render_to_response('expans/company/comp_add_supplier.html',context,context_dict)

#adding new item by the admin
@login_required
def add_item(request):
    # Request the context.
    context = RequestContext(request)
    item_list = get_item_list()
    context_dict={}
    form = ItemForm()
    context_dict={
            "form" : form,
            }
    # If HTTP POST, we wish to process form data and create an account.
    if request.method == 'POST':
        # Grab raw form data - making use of both FormModels.
        item_form = ItemForm(data=request.POST)

        # Two valid forms?
        if item_form.is_valid():
            # We'll be setting values for the instance ourselves, so commit=False prevents Django from saving the instance automatically.
            item = item_form.save(commit=False)
            
            # Profile picture supplied? If so, we put it in the new UserProfile.
            if 'picture' in request.FILES:
                item.picture = request.FILES['picture']

            # Now we save the model instance!
            item.save()
            
            # Return and render the response, ensuring the count is passed to the template engine.r
            return render_to_response('expans/add_item.html' ,context_dict, context)    
        # Invalid form(s) - just print errors to the terminal.
        else:
            print item_form.errors
            
    # Not a HTTP POST, so we render the two ModelForms to allow a user to input their data.
        
        # Return and render the response, ensuring the count is passed to the template engine.r
    return render_to_response('expans/add_item.html' ,context_dict, context)

# select query for item
def get_item_list():
    item_list = []
    item_list = Item.objects.filter()
        
    return item_list

#select query for supplier
def get_supplier_list():
    supplier_list = []
    supplier_list = Supplier.objects.filter()
        
    return supplier_list

# list of which company selected which items and suppliers

# transaction detils of entry added by the company
@login_required
def company_transaction(request):
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    transaction_list= Transaction.objects.all()
    print transaction_list
    item_list=get_item_list()
    supplier_list=get_supplier_list()
    day=date.today()
    now= datetime.now()
    month=now.month
    yesterday=(day-timedelta(days=1))
    week=(day-timedelta(days=7))
    transaction_list=Transaction.objects.filter(date__contains=day)
    transaction_list2=Transaction.objects.filter(date__contains=yesterday)
    transaction_list3=Transaction.objects.filter(date__range=[week,day])
    transaction_list4=Transaction.objects.filter(date__year="2017",date__month=month)
    context_dict = {'item_list': item_list,
                    'supplier_list':supplier_list,
                    'transaction_list':transaction_list,
                    'transaction_list2':transaction_list2,
                    'transaction_list3':transaction_list3,
                    'transaction_list4':transaction_list4,
                    'day':day,
                    'week':week,
                    'yesterday':yesterday,
                    'month':month,
                    }
    org=Oraganization.objects.get(user=request.user)
    mylist=get_mylist_list(org=org)
    context_dict['mylist']=mylist
    print mylist
    print transaction_list
    return render_to_response('expans/company/company_transaction.html',context_dict,context)

# making payment redirection
@login_required
def payment(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('expans/payment.html',context_dict,context)



# SUPPLIERS ACTIVITY===========================================
@login_required
def supplier(request):
    context = RequestContext(request)
    item_list=get_item_list()
    supplier_list=get_supplier_list()

    context_dict = {
                    'item_list': item_list,
                    'supplier_list':supplier_list,}
    sup=Supplier.objects.get(user=request.user)
    mylist=Mylist.objects.filter(sup=sup)
    context_dict['mylist']=mylist

    sup=Supplier.objects.get(user=request.user)
    mylist=Mylist.objects.filter(sup=sup.id)   
    if mylist:
        return supplier_home(request)
    else:
        return select_company(request)

    return supplier(request)

@login_required
def supplier_home(request):
    context = RequestContext(request)
    day=date.today()
    item_list=get_item_list()
    supplier_list=get_supplier_list()

    context_dict = {
                    'item_list': item_list,
                    'supplier_list':supplier_list,}
    sup=Supplier.objects.get(user=request.user)
    mylist=Mylist.objects.filter(sup=sup)
    context_dict['mylist']=mylist

    # sup=Supplier.objects.get(user=request.user)

    # myorg=Mylist.objects.filter(sup=sup).values('org').distinct()
    # print myorg

    # for o in myorg:
    #     print o['org']
    #     m=o['org']
    #     myorgsup=Mylist.objects.get(id=m)
    #     print myorgsup.measured

    # mylist=Mylist.objects.filter(sup=sup)

    # orglist=Oraganization.objects.all()
    # context_dict = {'day':day,
    #                 'myorg':myorg,
    #                 'mylist':mylist,
    #                  'orglist':orglist,
    #                 }
    return render_to_response('expans/supplier/supplier_home.html',context_dict,context)    


@login_required
def  select_company(request):
    context = RequestContext(request)
    item_list=get_item_list()
    supplier_list=get_supplier_list()
    context_dict = {'item_list':item_list,}

    return render_to_response('expans/supplier/select_company.html',context_dict,context)

@login_required
def supplier_add_entry(request,mylistid):
    context = RequestContext(request)
    context_dict={}
    
    if request.method == 'POST':
        my=Mylist.objects.get(id=mylistid)
        qnty=int(request.POST['qnty'])
        price=my.price
        total=qnty*float(price)

        trasaction_obj =Transaction(mylist=my,qnty=qnty,total=total)
        trasaction_obj.save()
        
        count=0
        trans=Transaction.objects.filter(mylist_id=mylistid)
        for t in trans:
            count=count+t.qnty

        payment2=Payment.objects.filter(mylist=mylistid)
        payment=payment2.latest('date')
        
        payment_list=Payment.objects.filter(mylist=mylistid)
        total=0
        for adv in payment_list:
            total=total+adv.advance
        balance=total

        total1=count*float(price)
        due=payment.balance-total1

        pay_obj = Payment(mylist=my,balance=balance,due=due,qnty=count,total=total1)
        pay_obj.save()
        

        qntty = str(qnty)
        company=str(my.org.user)
        measured=str(my.measured)
        messages.success(request, "You Added "+qntty+" "+measured+" To "+company+" company")
        return HttpResponseRedirect('/expans/supplier/') 
        # return render_to_response('expans/details.html',context_dict,context)

    return render_to_response('/expans/supplier/supplier_home.html',context_dict,context)

@login_required
def supplier_entry(request,myorgid):
    context = RequestContext(request)
    sup=Supplier.objects.get(user=request.user)    
    mylist=Mylist.objects.filter(sup=sup,org=myorgid)
    context_dict={'mylist':mylist,}
    return render_to_response('expans/supplier/supplier_entry.html',context_dict,context)


def sup_add_company(request):
    context=RequestContext(request)
    context_dict={}
    if request.method == 'POST':
        username=request.POST['username']
        phoneno=request.POST['phoneno']
        itemid=request.POST['itemid']
        try:
            org=Oraganization.objects.get(phoneno=phoneno)
            messages.warning(request," company is already registered")
            return HttpResponseRedirect('/expans/select_company/')
        except:
            try:
                password=12345
                user = User(username=username,password=password)
                user.set_password(user.password)
                user.save()
            
                org=Oraganization(phoneno=phoneno)
                org.user=user
                org.save()

                sup=Supplier.objects.get(user=request.user)
                measured=request.POST['measured']
                price=request.POST['price']
                item=Item.objects.get(id=itemid)
                payoption=request.POST['paydate']
                advance=request.POST['advance']
                mylist=Mylist(item=item,measured=measured,price=price,org=org,sup=sup,payoption=payoption)
                mylist.save()
                pay=Payment(advance=advance,balance=advance)
                pay.mylist=mylist
                pay.save()

                messages.success(request," company and item is added to your list")
                return supplier_home(request)
            
            except IntegrityError as e:
                messages.warning(request,"company with this name already in use")
                return HttpResponseRedirect('/expans/select_company/')

               
    return render_to_response('expans/supplier/select_company.html',context,context_dict)

def sup_select_company(request):
    if request.method == 'POST':
        itemid=request.POST['itemid']
        orgid=request.POST['orgid']
        org=Oraganization.objects.get(phoneno=orgid)
        try:
            item_present=Mylist.objects.get(org=org,item=itemid)
            context_dict['Item is already selected for this company']=True
            return render_to_response('expans/supplier/select_company.html',context,context_dict)
        except:
            sup=Supplier.objects.get(user=request.user)
            measured=request.POST['measured']
            price=request.POST['price']
            item=Item.objects.get(id=itemid)
            advance=request.POST('advance')
            payoption=request.POST['paydate']
            mylist=Mylist(item=item,measured=measured,price=price,org=org,sup=sup,payoption=payment2)
            mylist.save()
            
            pay=Payment(advance=advance,balance=advance)
            pay.mylist=mylist
            pay.save()

            messages.success(request," company  and item is added to your list")
            return supplier_home(request)
               
    return render_to_response('expans/supplier/select_company.html',context,context_dict)

@login_required
def supplier_mylist(request):
    context = RequestContext(request)
    item_list=get_item_list()
    supplier_list=get_supplier_list()

    context_dict = {
                    'item_list': item_list,
                    'supplier_list':supplier_list,}
    sup=Supplier.objects.get(user=request.user)
    mylist=Mylist.objects.filter(sup=sup)
    context_dict['mylist']=mylist
   
    return render_to_response('expans/supplier/supplier_mylist.html',context_dict,context)

@login_required
def supplier_transaction(request):
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    transaction_list= Transaction.objects.all()
    item_list=get_item_list()
    supplier_list=get_supplier_list()
    day=date.today()
    now= datetime.now()
    month=now.month
    yesterday=(day-timedelta(days=1))
    week=(day-timedelta(days=7))
    transaction_list=Transaction.objects.filter(date__contains=day)
    transaction_list2=Transaction.objects.filter(date__contains=yesterday)
    transaction_list3=Transaction.objects.filter(date__range=[week,day])
    transaction_list4=Transaction.objects.filter(date__year="2017",date__month=month)

    context_dict = {'item_list': item_list,
                    'supplier_list':supplier_list,
                    'transaction_list':transaction_list,
                    'transaction_list2':transaction_list2,
                    'transaction_list3':transaction_list3,
                    'transaction_list4':transaction_list4,
                    'day':day,
                    'week':week,
                    'yesterday':yesterday,
                    'month':month,
                    }

    sup=Supplier.objects.get(user=request.user)
    mylist=Mylist.objects.filter(sup=sup)
    context_dict['mylist']=mylist
    
    # for k in mylist:
    #     print k.id
    #     trans=Transaction.objects.filter(mylist=k.id)
        # print trans.id
    
    print mylist
    print transaction_list
    return render_to_response('expans/supplier/supplier_transaction.html',context_dict,context)

@login_required
def supplier_add_advance(request,mylistid):
    context = RequestContext(request)
    context_dict={}
    
    if request.method == 'POST':
        my=Mylist.objects.get(id=mylistid)
        advance=int(request.POST['advance'])
        # try:
            # payment_list=Payment.objects.filter(mylist=mylistid)
            # print payment_list
            # for adv in payment_list:
            #     print adv.advance
        #     print 0
        #     print balance

        #     pay_obj =Payment(mylist=my,advance=advance,balance=balance)
        #     pay_obj.save()
        #     advance = str(advance)
        #     company = str(my.org.user)
        #     mylist_id= str(my.id)
        #     messages.success(request, "You Added advance of Rs "+advance+" To "+company+" company")
        #     return HttpResponseRedirect('/expans/suppliermyitemdetails/'+mylist_id+'/')
        # except:
        #     print 2222
        payment_list=Payment.objects.filter(mylist=mylistid)

        total=0
        for adv in payment_list:
            total=total+adv.advance
        balance=total+advance

        trans=Transaction.objects.filter(mylist_id=mylistid)
        count=0
        for t in trans:
            count=count+t.qnty
        total=count*float(my.price)
        due=balance-total

        pay_obj =Payment(mylist=my,advance=advance,balance=balance,due=due,qnty=count,total=total)
        pay_obj.save()
        advance = str(advance)
        company = str(my.org.user)
        mylist_id= str(my.id)
        messages.success(request, "You Added advance of Rs "+advance+" To "+company+" company")
        return HttpResponseRedirect('/expans/suppliermyitemdetails/'+mylist_id+'/')



def get_item_details(request):
    if request.is_ajax():
        item = request.GET.get('data')
        items_json = serializers.serialize('json', Item.objects.filter(name__icontains = item))
        # items_json = 'tea'
        # print items_json
        return HttpResponse(items_json, content_type = 'json')
        # return HttpResponse(items_json)

def get_sup_details(request):
    if request.is_ajax():
        sup = request.GET.get('data')
        suplier_json = serializers.serialize('json', Supplier.objects.filter(phoneno__icontains = sup))

        return HttpResponse(suplier_json, content_type = 'json')

def get_org_details(request):
    if request.is_ajax():
        org = request.GET.get('data')
        company_json = serializers.serialize('json', Oraganization.objects.filter(phoneno__icontains = org))

        return HttpResponse(company_json, content_type = 'json')


def handler_404(request):
    response=render_to_response('404.html',{},context_instance=RequestContext(request))
    response.status_code=404
    return response

def custom_error_view(request):
    return render_to_response('500.html',RequestContext(request))

def custom_permission_denied_view():
    return render_to_response('403.html',RequestContext(request))

def custom_bad_request_view():
    return render_to_response('400.html',RequestContext(request),status_code=404)


@login_required
def suppliermyitemdetails(request,mylistid):
    try:
        context = RequestContext(request)
        mylist1=Mylist.objects.get(id=mylistid)
        
        context_dict = {
                    'mylist1':mylist1, 
                         }
        payment2=Payment.objects.filter(mylist=mylistid)
        payment=payment2.latest('date')
        context_dict['payment']=payment
        return render_to_response('expans/supplier/myitemdetails.html',context_dict,context)
    except:
        context = RequestContext(request)
        count=0
        trans=Transaction.objects.filter(mylist_id=mylistid)
        for i in trans :
            count=count+i.qnty

        mylist1=Mylist.objects.get(id=mylistid)
        total= mylist1.price*count 
        
        context_dict = {   'total':total,
                        }
        balance=-total
        advance=0
        context_dict['balance']=balance
        context_dict['advance']=advance
        context_dict['mylist1']=mylist1

        return render_to_response('expans/supplier/myitemdetails.html',context_dict,context)

@login_required
def companymyitemdetails(request,mylistid):
    try:
        context = RequestContext(request)
        mylist1=Mylist.objects.get(id=mylistid)
        
        context_dict = {
                    'mylist1':mylist1, 
                         }
        payment2=Payment.objects.filter(mylist=mylistid)
        payment=payment2.latest('date')
        context_dict['payment']=payment
        return render_to_response('expans/company/myitemdetails.html',context_dict,context)
    except:
        context = RequestContext(request)
        count=0
        trans=Transaction.objects.filter(mylist_id=mylistid)
        for i in trans :
            count=count+i.qnty

        mylist1=Mylist.objects.get(id=mylistid)
        total= mylist1.price*count 
        
        context_dict = {   'total':total,
                        }
        balance=-total
        advance=0
        context_dict['balance']=balance
        context_dict['advance']=advance
        context_dict['mylist1']=mylist1

        return render_to_response('expans/company/myitemdetails.html',context_dict,context)
    # return render_to_response('expans/company/myitemdetails.html',context_dict,context)

@login_required
def company_add_advance(request,mylistid):
    context = RequestContext(request)
    context_dict={}
    
    if request.method == 'POST':
        my=Mylist.objects.get(id=mylistid)
        advance=int(request.POST['advance'])
        payment_list=Payment.objects.filter(mylist=mylistid)

        total=0
        for adv in payment_list:
            total=total+adv.advance
        balance=total+advance

        trans=Transaction.objects.filter(mylist_id=mylistid)
        count=0
        for t in trans:
            count=count+t.qnty
        total=count*float(my.price)
        due=balance-total

        pay_obj =Payment(mylist=my,advance=advance,balance=balance,due=due,qnty=count,total=total)
        pay_obj.save()
        advance = str(advance)
        supplier = str(my.sup.user)
        mylist_id= str(my.id)
        messages.success(request, "You given advance of Rs "+advance+" To supplier "+supplier+" ")
        return HttpResponseRedirect('/expans/companymyitemdetails/'+mylist_id+'/')

@login_required
def dashboard(request):
    context = RequestContext(request)
    transaction_list=Transaction.objects.all()
    dashlist=[]
    for t in transaction_list:
        print t.id
        print t.qnty
        print t.mylist_id
        dashlist.extend(list(Mylist.objects.filter(id=t.mylist_id)))

    context_dict={ 'transaction_list':transaction_list,
                    'dishlist':dashlist }
    return render_to_response('expans/dashboard.html',context_dict,context)
