from django.contrib import admin    
from django.urls import path
from canteen_app import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('student/menu/', views.student_menu, name='student_menu'),
    path('student/checkout/', views.checkout_view, name='checkout'),
    path('student/order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('student/order-tracking/<int:order_id>/', views.order_tracking, name='order_tracking'),
    path('student/orders/', views.student_orders_history, name='student_orders'),

    path('seller/orders/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/orders/<int:order_id>/', views.seller_order_detail, name='seller_order_detail'),
    path('seller/menu/', views.seller_menu_management, name='seller_menu_management'),
    
    path('api/orders/create/', views.create_order, name='api_create_order'),
    path('api/orders/<int:order_id>/status/<str:new_status>/', views.update_order_status, name='api_update_order_status'),
]

# This block of code is what tells Django to serve media files during development.
# The URL will match your MEDIA_URL setting, and the files will be served from MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)