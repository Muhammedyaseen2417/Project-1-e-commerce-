from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns=[
    path('shp_login',views.shp_login , name='shp_login'),
    path('shp_logout',views.shp_logout, name='shp_logout'),


    # ---------------shop--------------------

    
    path('shp_home',views.shp_home,name='shp_home'),
    path('add_prod',views.add_prod,name='add_prod'),
    path('edit_prod/<pid>',views.edit_prod),
    path('delete_prod/<pid>',views.delete_prod),
    path('bookings/',views.bookings),





    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # --------------user---------------------
     
    
   
    path('view_cart/', views.view_cart, name='view_cart'),
    path('register/',views.register,name='register'),
    path('user_home',views.user_home, name='user_home'),
    path('view_pro/<pid>',views.view_pro),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('view_cart/delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('delete_cart/<id>',views.delete_cart),
    path('user_buy/<cid>',views.user_buy,name='user_buy'),
    path('user_buy1/<pid>',views.user_buy1,name='user_buy1'),
    path('view_cart/user_buy/<int:cid>/',views.user_buy, name='user_buy'),
    path('shp_logout/', views.shp_logout, name='shp_logout'),
    


   

    
    path('user_booking',views.user_booking),
    path('remove_booking/<int:booking_id>/', views.remove_booking, name='remove_booking'),
    path('user_booking/', views.user_booking, name='user_booking'),
    # The URL pattern for removing a booking
    path('remove_booking/<int:booking_id>/', views.remove_booking, name='remove_booking'),
    path('order/', views.order_create, name='order_create'),
    path('order_success/', views.order_success, name='order_success'),
    path('', views.homepage, name='homepage'),
    path('clear_all_orders2', views.clear_all_orders2, name='clear_all_orders2'),
    # path('payment_success/', views.payment_success, name='payment_success'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('verifyotp',views.verify_otp_reg, name='verify_otp'),
]




