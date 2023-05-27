from django import forms
from phone_field import PhoneFormField,PhoneWidget
from .models import FeedBack, MenuItem, Order, Customer

class CreateMenuItemForm(forms.ModelForm):
    name=forms.CharField(
        label='Food',
        widget=forms.TextInput(attrs={
        'placeholder':'Eg. Grilled Chicken',
        'class':'menuform'
        })
    )

    foodpic=forms.ImageField(required=False,
        label='Picture of Food',
        widget=forms.ClearableFileInput(attrs={
        'class':'menuform'
        })
    )

    price=forms.DecimalField(
        label='Price',
        widget=forms.TextInput(attrs={
        'class':'menuform'
        })
    )

    ingredients=forms.CharField(label='Ingredients used',
        widget=forms.Textarea(attrs={
        'placeholder':'Eg. Wheat, Eggs, Flour',
        'rows':'2',
        'cols':'6',
        'class':'menuform'

        })
    )

    available=forms.BooleanField(
        label='Availability',required=False,
        widget=forms.CheckboxInput(attrs={
        'class':'menuform'
        })
    )

    nv=forms.ChoiceField(choices=[('1','Veg'),('2','NonVeg'),('3','Both')], 
        label='Veg or Non Veg',
        widget=forms.Select(attrs={
        'class':'menuform'
        })
    )

    class Meta:
        model=MenuItem
        fields=['name','foodpic','nv','available','ingredients','price']

class FeedbackForm(forms.ModelForm):
    name=forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
        'placeholder':'Jonathan',
        'class':'form-control'
        })
    )

    email=forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
        'placeholder':'someone@gmail.com',
        'class':'form-control'
        })
    )

    feedback=forms.CharField(
        label='Feedback',
        widget=forms.Textarea(attrs={
        'placeholder':'Your Suggestions...',
        'class':'form-control',
        'rows':'4',
        'cols':'20'
        })
    )
    
    def clean_email(self):
        return self.cleaned_data['email'] or None

    class Meta:
        model=FeedBack
        fields=['name','email','feedback']

class OrderForm(forms.ModelForm):
    name=forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
        'placeholder':'Jonathan',
        'class':'form-control'
        })
    )

    email=forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
        'placeholder':'someone@gmail.com',
        'class':'form-control'
        })
    )
    phone=PhoneFormField(
        label="Phone No",
        widget=PhoneWidget(attrs={
        'class':'restroform'
        })
    )

    street=forms.CharField(
        label='Street',
        widget=forms.TextInput(attrs={
        'placeholder':'16 Maple Drive',
        'class':'form-control',
        })
    )
    area=forms.CharField(
        label='Area',
        widget=forms.TextInput(attrs={
        'placeholder':'King\'s Cross',
        'class':'form-control',
        })
    )
    city=forms.CharField(
        label='City',
        widget=forms.TextInput(attrs={
        'placeholder':'London',
        'class':'form-control',
        })
    )
    state=forms.CharField(
        label='State',
        widget=forms.TextInput(attrs={
        'placeholder':'Greater London',
        'class':'form-control',
        })
    )
    pincode=forms.IntegerField(
        label='Pincode',
        widget=forms.TextInput(attrs={
        'placeholder':'600100',
        'class':'form-control',
        })
    )

    class Meta:
        model=Order
        fields=['name','phone','email','street','area','city','state','pincode']

class UserProfileForm(forms.ModelForm):
    name=forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
        'placeholder':'Jonathan',
        'class':'form-control'
        })
    )
    picture=forms.ImageField(required=False,
        label='Picture of Food',
        widget=forms.ClearableFileInput(attrs={
        'class':'menuform'
        })
    )

    email=forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
        'placeholder':'someone@gmail.com',
        'class':'form-control'
        })
    )
    phone=PhoneFormField(
        label="Phone No",
        widget=PhoneWidget(attrs={
        'class':'restroform'
        })
    )

    street=forms.CharField(
        label='Street',
        widget=forms.TextInput(attrs={
        'placeholder':'16 Maple Drive',
        'class':'form-control',
        })
    )
    area=forms.CharField(
        label='Area',
        widget=forms.TextInput(attrs={
        'placeholder':'King\'s Cross',
        'class':'form-control',
        })
    )
    city=forms.CharField(
        label='City',
        widget=forms.TextInput(attrs={
        'placeholder':'London',
        'class':'form-control',
        })
    )
    state=forms.CharField(
        label='State',
        widget=forms.TextInput(attrs={
        'placeholder':'Greater London',
        'class':'form-control',
        })
    )
    pincode=forms.IntegerField(
        label='Pincode',
        widget=forms.TextInput(attrs={
        'placeholder':'600100',
        'class':'form-control',
        })
    )

    allergy=forms.CharField(
        label='Allergies',
        widget=forms.TextInput(attrs={
        'placeholder':'Eg. Dairy',
        
        'rows':'3',
        'cols':'6',
        'class':'form-control',
        })
    )

    class Meta:
        model=Customer
        fields=['name','picture','phone','email','street','area','city','state','pincode','allergy']