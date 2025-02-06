from django.urls import path
from . import views
urlpatterns=[
    path('',views.shp_login),
    path('shp_logout',views.shp_logout),


    # ---------------shop--------------------


    path('shp_home',views.shp_home),
    path('add_prod',views.add_prod),
    path('edit_prod/<pid>',views.edit_prod),
    path('delete_prod/<pid>',views.delete_prod),
    path('bookings',views.bookings),


    # --------------user---------------------

      path('view_cart/', views.view_cart, name='view_cart'),
    path('register',views.register),
    path('user_home',views.user_home, name='user_home'),
    path('view_pro/<pid>',views.view_pro),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('view_cart/delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('delete_cart/<id>',views.delete_cart),
    path('user_buy/<cid>',views.user_buy,name='user_buy'),
    path('user_buy1/<pid>',views.user_buy1,name='user_buy1'),
    path('view_cart/user_buy/<int:cid>/',views.user_buy, name='user_buy'),

    
    path('user_booking',views.user_booking),
    path('remove_booking/<int:booking_id>/', views.remove_booking, name='remove_booking'),
    path('user_booking/', views.user_booking, name='user_booking'),
    # The URL pattern for removing a booking
    path('remove_booking/<int:booking_id>/', views.remove_booking, name='remove_booking'),
    path('order/', views.order_create, name='order_create'),
    path('order/success/', views.order_success, name='order_success'),
]



