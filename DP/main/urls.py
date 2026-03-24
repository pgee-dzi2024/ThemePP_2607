from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),

    # AUTH
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)