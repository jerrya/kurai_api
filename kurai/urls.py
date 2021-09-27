from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('contracts/', include('contracts.urls')),
    path('orders/', include('orders.urls')),
]
