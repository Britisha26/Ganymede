from django.urls import path
from .views import CreateMenuItem,RestaurantProfile,CreateRestaurant,ResProfileEditView
from .views import EditMenuItem,DeleteMenuItem,ResProfileDeleteView

urlpatterns=[
    path('profile/<int:pk>/',RestaurantProfile.as_view(),name='res-profile'),
    path('profile/edit/<int:pk>/',ResProfileEditView.as_view(),name='res-profile-edit'),
    path('profile/delete/<int:pk>/',ResProfileDeleteView.as_view(),name='res-profile-delete'),
    path('create/',CreateRestaurant.as_view(),name='create-res'),
    
    path('<int:pk>/create-menuitem/',CreateMenuItem.as_view(),name='create-menu'),
    path('<int:r_pk>/edit-menuitem/<int:pk>',EditMenuItem.as_view(),name='menuitem-edit'),
    path('<int:r_pk>/delete-menuitem/<int:pk>',DeleteMenuItem.as_view(),name='menuitem-delete'),
]