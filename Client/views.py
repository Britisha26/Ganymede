from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.models import User,AnonymousUser
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from .models import Order,FeedBack,MenuItem, Customer
from .models import Profile as Prof
from Restaurant.models import Restaurant, RestaurantReview
from DeliveryPartner.models import Agent
from .forms import FeedbackForm, OrderForm
from django.core.exceptions import ObjectDoesNotExist
#from .models import

class Home(View):
    def get(self, request, *args, **kwargs):
        r=0
        c=0

        if request.user.is_anonymous:
            a=True
        else:
            a=False
            c=request.user.profile.role
            if c=='1':
                try:
                    r=Customer.objects.get(user=request.user)
                except Customer.DoesNotExist:
                    r=Customer.objects.create(user=request.user)
                    

            if c=='2':
                r=Restaurant.objects.get(user=request.user).pk
            if c=='3':
                r=Agent.objects.get(user=request.user).pk


        context={
            'a':a,
            'c':c,
            'r':r,
            
            }

        return render(request,'Client/home.html',context)

class About(View):
    def get(self, request, *args, **kwargs): 
        return render(request,'Client/about.html')
    
class UserProfile(LoginRequiredMixin,View):
    def get(self, request,pk, *args, **kwargs): 
        profile=Prof.objects.get(pk=pk)
        try:
            c=Customer.objects.get(user=profile.user)
        except Customer.DoesNotExist:
            c=Customer.objects.create(user=profile.user)
        rr=RestaurantReview.objects.filter(user=profile.user).order_by('-posted_on')
        context={
            'profile':profile,
            'c':c,
            'rr':rr,
        } 
        return render(request,'Client/profile.html',context)
    

class UserProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Customer
    fields=['name','picture','phone','email','street','area','city','state','pincode','allergy']
    template_name = 'Client/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        customer = self.get_object()
        return self.request.user == customer.user

    
class Contact(View):
    def get(self,request, *args, **kwargs):
        form=FeedbackForm()
        is_submitted=False
        context={
            'is_submitted':is_submitted,
            'form':form
        }
        return render(request,'Client/contact.html',context)
    def post(self,request, *args, **kwargs):
        form=FeedbackForm(request.POST)
        is_submitted=False
        if form.is_valid():
            f=form.save(commit=False)
            if request.user.is_authenticated:
                f.user=request.user
            else:
                f.user=None
            f.save()
            is_submitted=True
        form=FeedbackForm()
        context={
            'form':form,
            'is_submitted':is_submitted
        }  
        return render(request,'Client/contact.html',context)



class Menu(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        restro=Restaurant.objects.get(pk=pk)
        menu_items=MenuItem.objects.filter(res=restro).all()
        form=OrderForm()
        e=0
        context={
            'menu':menu_items,
            'res':restro,
            'form':form,
            'e':e
        }

        return render(request,'Client/menu.html',context)
    
    
    def post(self,request,pk, *args, **kwargs):
        e=0
        restro=Restaurant.objects.get(pk=pk)
        menu_items=MenuItem.objects.filter(res=restro).all()
        if request.method=="POST":
            form=OrderForm(request.POST)
            
            order_items={
                'items':[]
            }
            items=request.POST.getlist('items[]')
            for item in items:
                menu_item = MenuItem.objects.get(pk__contains=int(item))
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.name,
                    'price': menu_item.price
                }
                order_items['items'].append(item_data)
            if order_items['items'] == []:
                form = OrderForm()
                e=0
                context={
                    'menu':menu_items,
                    'res':restro,
                    'form':form,
                    'e':e
                }

                return render(request,'Client/menu.html',context)

            price = 0
            item_ids = []

            for item in order_items['items']:
                price += item['price']
                item_ids.append(item['id'])
            
            if form.is_valid():
                f=form.save(commit=False)
                f.user=request.user
                f.res=restro
                print(price)
                f.price=price
                f.save()
                f.items.add(*item_ids)


                # After everything is done, send confirmation email to the user
                body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                        f'Your total: {price}\n'
                        'Thank you again for your order!')

                send_mail(
                    'Thank You For Ordering from PlatePal!',
                    body,
                    'example@example.com',
                    [f.email],
                    fail_silently=False
                )

                context = {
                    'items': order_items['items'],
                    'price': price
                }
                
                return redirect('order-confirmation', pk=f.pk)
            else:
                e=form.errors
                context={
                    'menu':menu_items,
                    'res':restro,
                    'form':form,
                    'e':e
                }

                return render(request,'Client/menu.html',context)
        else:
            form = OrderForm()
            e=0
            context={
                'menu':menu_items,
                'res':restro,
                'form':form,
                'e':e
            }

            return render(request,'Client/menu.html',context)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'Client/order_confirmation.html', context)
    def post(self, request, pk, *args, **kwargs):
        o= Order.objects.filter(pk=pk).update(is_paid=True)
        order=Order.objects.get(pk=pk)
        has_paid=True
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
            'has_paid':has_paid
        }
        if request.method=="POST":
            return redirect('order-detail',order.pk)
        return render(request, 'Client/order_confirmation.html', context)
    
class OrderDetail(View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'Client/order_details.html', context)

        
class MenuDetail(View):
    def get(self,request,r_pk,pk, *args, **kwargs):
        r=Restaurant.objects.get(pk=r_pk)
        m=MenuItem.objects.get(pk=pk)
        context={
            'menu':m,
            'res':r
        }

        return render(request,'Client/menu_detail.html',context)

class RestaurantView(View):
    def get(self,request, *args, **kwargs):
        res=Restaurant.objects.all()
        context={
            'res':res
        }
        return render(request,"Client/restaurants.html",context)
    def post(self,request, *args, **kwargs):
        res=Restaurant.objects.filter()
        context={
            'res':res
        }
        return render(request,"Client/restaurants.html",context)