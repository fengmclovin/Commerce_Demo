from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bidding


def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    # isListingInWatchlist = request.user in listingData.watchlist.all()
    isListingInWatchlist = listingData.watchlist.filter(
        id=request.user.id).exists()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })


def close_auction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username

    isListingInWatchlist = listingData.watchlist.filter(
        id=request.user.id).exists()
    allComments = Comment.objects.filter(listing=listingData)

    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Auction Closed"
    })


def remove_watchlist(request, id):
    listtingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listtingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def add_watchlist(request, id):
    listtingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listtingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# args=(id, ) is creating a tuple with a single element,
# which is the id. The trailing comma distinguishes it as a tuple.
# If you omit the comma, it will be treated as a regular expression with parentheses, not a tuple.

# The main difference between a tuple and a list is that a tuple is immutable,
# meaning its elements cannot be changed after the tuple is created.


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories
    })


def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(
            isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def watchlist(request):
    currentUser = request.user
    listings = currentUser.listing_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def add_bid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)

    isListingInWatchlist = listingData.watchlist.filter(
        id=request.user.id).exists()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username

    if float(newBid) > listingData.price.bid:
        updatedBid = Bidding(user=request.user, bid=newBid)
        updatedBid.save()
        listingData.price = updatedBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bidding Accepted",
            "update": True,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner
        })

    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bidding Denied",
            "update": False,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner
        })


def add_comment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def category(request):
    return render(request, "auctions/categories.html")


def create_listing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageURL = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        currentUser = request.user

        categoryData = Category.objects.get(categoryName=category)

        bid = Bidding(bid=float(price), user=currentUser)
        bid.save()

        newListing = Listing(
            title=title,
            description=description,
            imageURL=imageURL,
            price=bid,
            category=categoryData,
            owner=currentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
