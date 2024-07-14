
from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    #path('', views.my_view, name='home'),
    path('fetch-data/', views.fetch_data_from_supabase, name='fetch_data_from_supabase'),
    path('', views.mainView, name='mainView'),
    path('recordPage/<str:pk>/',views.recordPage, name="recordPage"),
     #path('search',views.search, name="search"),
    # path('api', views.ChartData.as_view()), 
]
