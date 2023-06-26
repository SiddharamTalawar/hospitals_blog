from django.urls import path,include
from .views import  registerview

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', registerview.as_view() , name=' register'),
  
]