from rest_framework import serializers
from django.contrib.auth.models import User
from expans.models import Item ,Supplier,Transaction,Mylist,Oraganization,Payment

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class OrganizationSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	class Meta:
		model = Oraganization
		fields='__all__'

class SupplierSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	class Meta:
		model = Supplier
		fields='__all__'

class MylistSerializer(serializers.ModelSerializer):
	sup=SupplierSerializer()
	org=OrganizationSerializer()
	item=ItemSerializer()

	class Meta:
		model = Mylist
		fields= '__all__'

class TransactionSerializer(serializers.ModelSerializer):
	mylist=MylistSerializer()
	class Meta:
		model = Transaction
		fields= ('id', 'date', 'qnty','total','mylist')

    # def create(self, validated_data):
    # 	my=Mylist.objects.get(id=mylistid)
    # 	price=my.price	
    #     trans = Transaction(mylist=my,qnty = validated_data["qnty"],
    #         total = (qnty*float(price))
    #     )
    #     trans.save()
    #     return Transaction

class PaymentSerializer(serializers.ModelSerializer):
    mylist=MylistSerializer()
    class Meta:
        model = Payment
        fields= ('id','date','balance','qnty','total','due','mylist')
        