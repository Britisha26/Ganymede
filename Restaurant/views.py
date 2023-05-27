from django.views import View
from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from Client.models import Order, MenuItem, Category
from Client.models import Profile as Prof
from Client.forms import CreateMenuItemForm
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Restaurant,Rating,RestaurantReview
from .forms import RestaurantForm

class CreateMenuItem(UserPassesTestMixin,LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        form=CreateMenuItemForm()
        res=Restaurant.objects.get(pk=pk)
        context={
            'form':form,
            'res':res
        }
        return render(request,'Restaurant/create_menu.html',context)
    def post(self,request,pk,*args,**kwargs):
        is_submitted=False
        if request.method == 'POST':
            form=CreateMenuItemForm(request.POST,request.FILES)
            r=Restaurant.objects.get(pk=pk)
            if form.is_valid():
                f=form.save(commit=False)
                f.res=r
                f.save()
                is_submitted=True
                form=CreateMenuItemForm()
        context={
            'form':form,
            'res':r,
            'is_submitted':is_submitted
        }
        return render(request,'Restaurant/create_menu.html',context)
    
    def test_func(self):
        pk=self.kwargs['pk']
        p=Prof.objects.get(user=self.request.user).role
        if p=='2':
            res=Restaurant.objects.get(pk=pk)
            return res.user==self.request.user
        else:
            return False
        
class EditMenuItem(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model=MenuItem
    fields=['name','foodpic','nv','available','ingredients','price']
    #context_object_name="menu"
    template_name='Restaurant/edit_menu.html'

    def get_success_url(self):
        pk=self.kwargs['r_pk']
        return reverse_lazy('menu', kwargs={'pk': pk})

    def test_func(self):
        menu=self.get_object()
        return self.request.user == menu.res.user
    
class DeleteMenuItem(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model= MenuItem
    #context_object_name="menu"
    template_name='Restaurant/delete_menu.html'
    
    def get_success_url(self):
        pk=self.kwargs['r_pk']
        return reverse_lazy('menu', kwargs={'pk': pk})

    def test_func(self):
        menu=self.get_object()
        return self.request.user == menu.res.user
    
class RestaurantProfile(View):
    def get(self,request,pk,*args,**kwargs):
        r=Restaurant.objects.get(pk=pk)
        rr=RestaurantReview.objects.filter(rest=pk)

        context={
            'r':r,
            'rr':rr
        }
        return render(request,"Restaurant/restro_profile.html",context)
    
class ResProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Restaurant
    fields = ['name','pic','lic', 'phone','email', 'cuisine', 'address', 'nv']
    context_object_name="res"
    template_name = 'Restaurant/edit_restro_profile.html'

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('res-profile', kwargs={'pk': pk})
    
    def get_object(self):
        res=Restaurant.objects.get(user=self.request.user)
        return res

    def test_func(self):
        res = self.get_object()
        return self.request.user == res.user
    
class ResProfileDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model= Restaurant
    template_name = 'Restaurant/delete_restro_profile.html'
    context_object_name="res"
    success_url=reverse_lazy('home')
    
    def get_success_url(self):
        p=Prof.objects.filter(user=self.request.user).update(role='1')
        return reverse_lazy('home')

    def get_object(self):
        res=Restaurant.objects.get(user=self.request.user)
        return res

    def test_func(self):
        res = self.get_object()
        return self.request.user == res.user
   
class CreateRestaurant(LoginRequiredMixin,View):
    def get(self,request):
        form=RestaurantForm()
        context={
            'form':form
        }
        return render(request,"Restaurant/create_restro.html",context)
    
    def post(self, request):
        form=RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            f.user=request.user
            f.rate=None
            f.save()
            p=Prof.objects.filter(user=request.user).update(role='2')
            r=Restaurant.objects.get(user=request.user)
            return redirect("res-profile",r.pk)

        
        context={
            'form':form
        }
        return render(request,"Restaurant/create_restro.html",context)
        
