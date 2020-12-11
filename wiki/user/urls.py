from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/reg
    url(r"^reg$", views.reg_view, name="reg"),
    # http://127.0.0.1:8000/login
    url(r"^login$", views.login_view, name="login"),
    # http://127.0.0.1:8000/logout
    url(r"^logout$", views.logout_view, name="logout"),
]