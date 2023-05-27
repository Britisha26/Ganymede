from django.urls import path    
from .views import AgentProfile, AgentProfileDeleteView,AgentsList, AgentProfileEditView, CreateAgent

urlpatterns=[
    path('profile/<int:pk>/',AgentProfile.as_view(),name='agent-profile'),
    path('profile/edit/<int:pk>/',AgentProfileEditView.as_view(),name='agent-profile-edit'),
    path('profile/delete/<int:pk>/',AgentProfileDeleteView.as_view(),name='agent-profile-delete'),
    path('create/',CreateAgent.as_view(),name='create-agent'),
    path('list/agents/',AgentsList.as_view(),name='list-agent'),


]