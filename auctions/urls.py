from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("categories", views.category, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create_listing, name="createlisting"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("displayCategory", views.displayCategory, name="displayCategory")
]
