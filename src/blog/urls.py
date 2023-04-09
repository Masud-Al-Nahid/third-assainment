from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<slug:slug>', views.category_view, name='category'),
    path('<slug:slug>', views.single_view, name='single'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)