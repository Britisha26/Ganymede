from django.urls import path
from .views import Home, About, Contact, Menu,RestaurantView,MenuDetail,OrderConfirmation, UserProfile, UserProfileEditView, OrderDetail #AddOrder,RemoveOrder,

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('about/',About.as_view(),name='about'),
    path('contact/',Contact.as_view(),name='contact'),
    path('profile/<int:pk>',UserProfile.as_view(),name='profile'),
    path('profile/edit/<int:pk>',UserProfileEditView.as_view(),name='profile-edit'),
    path('restaurant/<int:pk>/menu',Menu.as_view(),name='menu'),
    path('restaurant/<int:r_pk>/menu-info/<int:pk>',MenuDetail.as_view(),name='menu-detail'),
    path('list/restaurants/',RestaurantView.as_view(),name='list-res'),
    path('order/confirmation/<int:pk>',OrderConfirmation.as_view(),name='order-confirmation'),
    path('order/details/<int:pk>',OrderDetail.as_view(),name='order-detail'),
   # path('order/res/<int:r_pk>/add-menuitem/<int:pk>',AddOrder.as_view(),name='add-item'),
    #path('order/res/<int:r_pk>/add-menuitem/<int:pk>',RemoveOrder.as_view(),name='remove-item'),
]