from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.category, name="categories"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("create", views.create_listing, name="createlisting"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("remove/<int:id>", views.remove_watchlist, name="removewatchlist"),
    path("add/<int:id>", views.add_watchlist, name="addwatchlist"),
    path("addComment/<int:id>", views.add_comment, name="addComment"),
    path("addBid/<int:id>", views.add_bid, name="addBid"),
    path("closeAuction/<int:id>", views.close_auction, name="closeAuction")
]
