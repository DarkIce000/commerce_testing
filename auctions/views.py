from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, list_item, comment, watchlist
from django.contrib.auth.decorators import login_required


#form for the create page  

class formCreate(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control my-2 form-control-sm", "name":"title"}))
    Description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"class":"form-control my-2", "name":"description"}))
    url = forms.CharField(label="URL of Image (optional)", widget=forms.TextInput(attrs={"class":"form-control my-2 form-control-sm", "name":"url", "type":"url"}))
    category = forms.CharField(label="Category", widget=forms.TextInput(attrs={ "class" : "form-control form-control-sm my-2", "name":"category"}) ) 
    initialBid = forms.CharField(label="Initial", widget=forms.TextInput(attrs={ "class" : "form-control form-control-sm my-2", "name":"initialBid", "type":"number"}) ) 


class formComment(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "type":"text"}))
    msg = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))

class formWatchlist(forms.Form):
    addToWatchlist = forms.BooleanField()

# forms endhere 
# view functions 

#index page for listing all the items 
def index(request):  
    listItem = list_item.objects.all()
    
    return render(request, "auctions/index.html", {
        "listItem": listItem 
    }) 


# create a list on the site 
@login_required(login_url="/login")
def createListing(request):
    #getting the submitted data after the user is submitted 
    if request.method == "POST":
        listing = formCreate(request.POST)

        if listing.is_valid():
            title = listing.cleaned_data["title"]
            url = listing.cleaned_data["url"]
            description = listing.cleaned_data["Description"]
            initialBid = listing.cleaned_data["initialBid"]

            listItem = list_item(product_title = title, description=description, seller=request.user, imageUrl=url, initialBid=initialBid)  
            listItem.save()
        else:
            return render(request, "auctions/createListing.html",{
                "form": formCreate(initial={"title":title, "description": description, "url":url, "initialBid":initialBid})
            })

    return render(request, "auctions/createListing.html", {
        "form": formCreate
    })

def product(request, product_id):
    product = list_item.objects.get(id=product_id)  


    return render(request, "auctions/productPage.html",{
        "product_info": product,
        "add_watchlist": formWatchlist(),
        "formComment":formComment()
    })

def commentMade(request, product_id):
    commentobj = formComment(request.POST) 
    if request.method == "POST": 
        if commentobj.is_valid():            
            comment_title = commentobj.cleaned_data['title']
            comment_msg = commentobj.cleaned_data["msg"]
            comment_save = comment(title=comment_title, msg=comment_msg)
            comment_save.save()
            return HttpResponseRedirect(reverse("product_page", args=(product_id,)))

        return HttpResponseRedirect(reverse("product_page", args=(product_id,)), {"message" :
                                                                                     "comment is invalid"})
     
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def watchList(request, product_id ):
    #adding a item to the watchlist
    if request.method == "POST":
        print(request.POST['addToWatchlist'])
        return HttpResponse(f"Added to the watchlist ") 
    else:
        return HttpResponse(f"Something error at watchlist ")


























def login_view(request):

    next = ""
    if request.GET: 
        next = request.GET['next']

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            if next is not "":
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html", {
            "next" : next
        })


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