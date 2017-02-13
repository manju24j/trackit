from django import forms
from django.contrib.auth.models import User
from expans.models import Item,Supplier,Transaction,Mylist,Oraganization

#user form enter normally

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# # user profile form
# class UserProfileForm(forms.ModelForm):
#     contactno=forms.CharField(help_text="enter your contactno", required=True)
#     picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

#     class Meta:
#         model = UserProfile
#         fields = ('contactno', 'picture')

# organization form
class OraganizationForm(forms.ModelForm):
    name=forms.CharField(help_text="enter your company name",required=True)
    address=forms.CharField(help_text="enter your address",required=True)
    contactno=forms.CharField(help_text="enter your contactno",required=True)
    picture=forms.ImageField(help_text="Select image/log of ur Oraganization",required=False)

    class Meta:
        model=Oraganization
        fields=('name','address','contactno','picture')

# forms for add item
class ItemForm(forms.ModelForm):

    name = forms.CharField(help_text="Please enter name.", required=True)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = Item
        fields = ('name', 'picture')

#  Supplier adding forms
class SupplierForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    address = forms.CharField(max_length=128)
    contactno=forms.IntegerField()
    picture=forms.ImageField(help_text="suplier-pic",required=False)
  
    class Meta:
        model = Supplier
        fields = ('name','address','contactno','picture')

# forms for daily adding 
class TransactionForm(forms.Form):
    qnty = forms.IntegerField(help_text="quantity")
 
# forms for measured ment and settign price for item
class MylistForm(forms.Form):
    measured=forms.CharField(help_text="qnty measured in")
    price=forms.IntegerField(help_text="price per quantity")
