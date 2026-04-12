from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    index,
    user_login,
    register,
    user_logout,
    history,
    about,
    download_csv,
    clear_analysis_session,
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("logout/", user_logout, name="logout"),
    path("history/", history, name="history"),
    path("download-csv/", download_csv, name="download_csv"),
    path("clear-analysis/", clear_analysis_session, name="clear_analysis_session"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)