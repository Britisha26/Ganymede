from django import forms
from .models import Restaurant
from phone_field import PhoneFormField,PhoneWidget

class RestaurantForm(forms.ModelForm):
    name=forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
        'placeholder':'Eg. PalmShore',
        'class':'restroform'
        })
    )

    lic=forms.IntegerField(
        label='Restaurant License No',
        widget=forms.TextInput(attrs={
        'class':'restroform'   
        })
    )

    pic=forms.ImageField(
        label="Restaurant Picture",
        widget=forms.ClearableFileInput(attrs={
        'class':'restroform'
        })
    )

    phone=PhoneFormField(
        label="Phone No",
        widget=PhoneWidget(attrs={
        'class':'restroform'
        })
    )

    email=forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
        'class':'restroform'
        })
    )

    cuisine=forms.CharField(
        label="Cuisine",
        widget=forms.TextInput(attrs={
        'placeholder':'Eg. Italian',
        'class':'restroform'
        })
    )
    
    address=forms.CharField(label="Address",
        widget=forms.Textarea(attrs={
        'placeholder':'Eg 26 Maple Drive',
        'rows':'3',
        'cols':'6',
        'class':'restroform'
        })
    )
    
    nv=forms.ChoiceField(choices=[('1','Veg'),('2','NonVeg'),('3','Both')],
    label="Veg or Non Veg",
    widget=forms.Select(attrs={
        'class':'restroform'
        })
    )

    def clean_phone(self):
        return self.cleaned_data['phone'] or None
    
    def clean_email(self):
        return self.cleaned_data['email'] or None
    
    class Meta:
        model=Restaurant
        fields=['name','lic','pic','phone','email','cuisine','address','nv']