from django.views import View
from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from Client.models import Order, MenuItem, Category
from Client.models import Profile as Prof
from Client.forms import CreateMenuItemForm
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from Restaurant.models import Restaurant,Rating,RestaurantReview
from Restaurant.forms import RestaurantForm
from .models import Agent,AgentRating,AgentReview
from .forms import AgentForm

    
class CreateAgent(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        form=AgentForm()
        context={
            'form':form
        }
        return render(request,"DeliveryPartner/create_agent.html",context)
    
    def post(self, request, *args, **kwargs):
        form=AgentForm(request.POST, request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            f.user=request.user
            f.rate=None
            f.save()
            p=Prof.objects.filter(user=request.user).update(role='3')
            a=Agent.objects.get(user=request.user)
            return redirect("agent-profile",a.pk)

        
        context={
            'form':form
        }
        return render(request,"DeliveryPartner/create_agent.html",context)
    
class AgentProfile(View):
    def get(self,request,pk,*args,**kwargs):
        a=Agent.objects.get(pk=pk)
        ar=AgentReview.objects.filter(rest=pk)

        context={
            'a':a,
            'ar':ar
        }
        return render(request,"DeliveryPartner/agent_profile.html",context)
    
class AgentProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Agent
    fields=['name','aadhar','pic','phone','email','vehile_license','emergency_contact','address','previous_workplace']
    context_object_name="ag"
    template_name = 'DeliveryPartner/edit_agent_profile.html'

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('agent-profile', kwargs={'pk': pk})
    
    def get_object(self):
        ag=Agent.objects.get(user=self.request.user)
        return ag

    def test_func(self):
        ag = self.get_object()
        return self.request.user == ag.user
    
class AgentProfileDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model= Agent
    template_name = 'DeliveryPartner/delete_agent_profile.html'
    context_object_name="ag"
    success_url=reverse_lazy('home')
    
    def get_success_url(self):
        p=Prof.objects.filter(user=self.request.user).update(role='1')
        return reverse_lazy('home')

    def get_object(self):
        ag=Agent.objects.get(user=self.request.user)
        return ag

    def test_func(self):
        ag = self.get_object()
        return self.request.user == ag.user
    

class AgentsList(View):
    def get(self,request, *args, **kwargs):
        ag=Agent.objects.all()
        context={
            'ag':ag
        }
        return render(request,"DeliveryPartner/list_agents.html",context)
    def post(self,request, *args, **kwargs):
        ag=Agent.objects.all()
        context={
            'ag':ag
        }
        return render(request,"DeliveryPartner/list_agents.html",context)