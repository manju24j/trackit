from rest_framework import generics
from .serializers import ItemSerializer, UserSerializer,MylistSerializer,TransactionSerializer,PaymentSerializer
from django.contrib.auth.models import User
from expans.models import Item ,Supplier,Transaction,Mylist,Oraganization ,Payment
from datetime import datetime ,date ,timedelta

class UserList(generics.ListCreateAPIView):
    # Get / Create questions
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    """ Create a User """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


# ====== Items list==============
class ItemList(generics.ListCreateAPIView):
    # Get / Create questions
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# ========= perticular item list ===========
class ItemDetail(generics.RetrieveDestroyAPIView):
    # Get / Delete questions
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


#======== Mylist which supplier is suppling which item for which company=======

class MylistList(generics.ListCreateAPIView):
     # Get / Update a Choice
    queryset = Mylist.objects.all()
    serializer_class = MylistSerializer


# ===== Supplier Mylist +==============================

class SupMyList(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = MylistSerializer
    def get_queryset(self):
    	user_id= self.kwargs['pk']
        sup=Supplier.objects.get(user=user_id)
    	return Mylist.objects.filter(sup=sup).order_by('org')

class SupOrgMyList(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = MylistSerializer
    def get_queryset(self):
    	sup_id= self.kwargs['pk1']
    	org_id=self.kwargs['pk2']
    	return Mylist.objects.filter(sup=sup_id,org=org_id).order_by('org')

# ===== Company Mylist +==============================

class OrgMyList(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = MylistSerializer
    def get_queryset(self):
    	org_id= self.kwargs['pk']
    	return Mylist.objects.filter(org=org_id).order_by('item')

    # queryset = Mylist.objects.all()
    # serializer_class = MylistSerializer  OrgMyList

class MylistDetail(generics.ListCreateAPIView):
     # Get / Update a Choice
    serializer_class = MylistSerializer
    def get_queryset(self):
    	id= self.kwargs['pk']
    	return Mylist.objects.filter(org=id)

# ===== Transaction List ==============================

class TransactionList(generics.ListCreateAPIView):
	#get/Create questions
	queryset=Transaction.objects.all()
	serializer_class = TransactionSerializer

# ======= Transaction filter ======================

class MyTransactionList(generics.ListCreateAPIView):
	#get/Create questions
	serializer_class = TransactionSerializer
	def get_queryset(self):
		# queryset = Transaction.objects.filter(mylist_in=[mylist.id for mylist in Mylist.objects.filter(sup=sup.id)])
		# queryset=Transaction.objects.all()
		sup_id= self.kwargs['pk']
		queryset=[]
		my=Mylist.objects.filter(sup=sup_id)
		for s in my:
			print s.id
			queryset.extend(list(Transaction.objects.filter(mylist=s.id)))
		return queryset

#========== Transaction ==================
class Transactionentry(generics.CreateAPIView):
    """ Create a User """
    serializer_class = Transaction

class Transtoday(generics.ListCreateAPIView):
	#get/Create questions
	serializer_class = TransactionSerializer
	def get_queryset(self):
		# queryset = Transaction.objects.filter(mylist_in=[mylist.id for mylist in Mylist.objects.filter(sup=sup.id)])
		# queryset=Transaction.objects.all()
		user_id= self.kwargs['pk']
		queryset=[]
		day=date.today()
		my=Mylist.objects.filter(sup=sup_id)
		for s in my:
			print s.id
			queryset.extend(list(Transaction.objects.filter(mylist=s.id,date__contains=day)))
		return queryset

class  Transweek(generics.ListCreateAPIView):
    serializer_class=TransactionSerializer
    def get_queryset(self):
        day=date.today()
        t1=(day+timedelta(days=1))
        week=(t1-timedelta(days=7))
        print t1
        print week
        sup_id=self.kwargs['pk']
        queryset=[]
        my=Mylist.objects.filter(sup=sup_id)
        for s in my:
            queryset.extend(list(Transaction.objects.filter(mylist=s.id,date__range=[week,t1])))
        return queryset

# class Transweek(generics.ListCreateAPIView):
#     # Get / Create questions
#     serializer_class = TransactionSerializer
#     def get_queryset(self):
#     	day=date.today()
#     	week=(day-timedelta(days=7))
#     	# return Transaction.objects.filter(date__range=[week,day])
#     	sup_id= self.kwargs['pk']
#     	queryset=[]
#     	my=Mylist.objects.filter(sup=sup_id)
#     	for s in my:
#     		queryset.extend(list(Transaction.objects.filter(mylist=s.id,date__range=[week,day])))
# 		return queryset

class Transmonth(generics.ListCreateAPIView):
	#get/Create questions
	serializer_class = TransactionSerializer
	def get_queryset(self):
		# queryset = Transaction.objects.filter(mylist_in=[mylist.id for mylist in Mylist.objects.filter(sup=sup.id)])
		# queryset=Transaction.objects.all()
		sup_id= self.kwargs['pk']
		now= datetime.now()
		month=now.month
		queryset=[]
		my=Mylist.objects.filter(sup=sup_id)
		for s in my:
			print s.id
			queryset.extend(list(Transaction.objects.filter(mylist=s.id,date__year="2017",date__month=month)))
		return queryset

class payment(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    def get_queryset(self):
        mylist_id=self.kwargs['pk']
        queryset=Payment.objects.filter(mylist=mylist_id).order_by('date').reverse()[:1]

        #queryset=queryset.reverse()[:5]

        return queryset

class Mypayment(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    def get_queryset(self):
        user_id=self.kwargs['pk']
        sup=Supplier.objects.get(user=user_id)

        supmylist=Mylist.objects.filter(sup=sup)
        
        queryset=[]
        for p in supmylist:
            queryset.extend(list(Payment.objects.filter(mylist=p.id).order_by('date').reverse()[:1]))

        #queryset=queryset.reverse()[:5]

        return queryset
                

