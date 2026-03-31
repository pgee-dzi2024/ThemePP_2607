from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import index, about, user_login, register, user_logout, history

urlpatterns = [
path("", index, name="index"),
path("about/", about, name="about"),

# AUTH
path("login/", user_login, name="login"),
path("register/", register, name="register"),
path("logout/", user_logout, name="logout"),
path("history/", history, name="history"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)