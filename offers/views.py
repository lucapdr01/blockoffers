import json
import requests
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, OfferForm
from .models import AuctionProduct


def home(request):

    return render(request, "offers/home.html", {})


def feed(request):
    # Get all product objects
    products = AuctionProduct.objects.all()

    # array that will store all best offers stored on Redis
    bestOffers = []

    for num, prod in enumerate(products):
        # populate the array with all best offers
        bestOffers.insert(num, getBestOffer(num+1)[1])

        if bestOffers[num] == 0.0:
            bestOffers.insert(num, prod.basePrice)
        # check if the auction is expired in that case generate json file and make it no more appear in the feed
        if prod.isExpired():
            print("Expired")
            if prod.jsonResult == '':
                # print("entered")
                generateJson(prod, num)
    # print(bestOffers)

    return render(request, 'offers/feed.html', {'products': products, 'bestOffers': bestOffers, })


# function to see all won objects
def wonAuctions(request):
    # Get all product objects
    products = AuctionProduct.objects.filter(whoWon=request.user.username)

    return render(request, 'offers/wins.html', {'products': products, })


# function to access an auction details and submit offers
def productDetail(request, pk):
    product = get_object_or_404(AuctionProduct, pk=pk)
    print("Expired: " + str(product.isExpired()))
    bestOffer = getBestOffer(pk)[1]
    if bestOffer == 0.0:
        bestOffer = product.basePrice

    if request.method == "POST":

        form = OfferForm(request.POST)

        if form.is_valid():

            user = request.user.username
            newOffer = form.cleaned_data.get('offer')
            print(newOffer)

            if float(newOffer) >= float(product.basePrice):
                # code that interacts with the api via post in order to insert the offer on a redis database
                jsonData = {user: newOffer}
                post_data = json.dumps(jsonData)
                headers = {'Content-type': 'application/json'}
                r = requests.post('http://127.0.0.1:8000/feed/product/' + str(pk) + '/api/', data=post_data,
                                  headers=headers, verify=False)
                data = r
                # print(data)

            return redirect("/")

        """
                    Get request

                    r = requests.get('http://127.0.0.1:8000/feed/product/'+str(pk)+'/api/')
                    data = r.json()
                    print(data)
        """
    else:
        # initialise blank form and ip info
        form = OfferForm()
    # render the page
    return render(request, 'offers/productDetail.html', {'product': product, 'bestOffer': bestOffer, 'form': form})


# function that returns the best offer for a product processing data obtained trough a GET request to the api
def getBestOffer(pk):
    # GET request
    r = requests.get('http://127.0.0.1:8000/feed/product/' + str(pk) + '/api/')
    data = r.json()

    maxOffer = 0.0
    maxUser = ''
    for key in data:
        if key == 'items':
            for k in data[key]:
                if float(maxOffer) < float(data[key][k]):
                    maxOffer = data[key][k]
                    maxUser = k
                # print(str(k) + '->' + str(data[key][k]))
    # print('Best offer ' + maxUser + '->' + str(maxOffer))
    return [str(maxUser), maxOffer]


# generate the json recap of with all details of an expired auction
def generateJson(prod, num):
    pk = num + 1
    response = []

    prod.whoWon = str(getBestOffer(pk)[0])
    prod.bestPrice = getBestOffer(pk)[1]
    prod.save()

    response.append(
        {
            'description': prod.description,
            'seller': prod.seller,
            'location': prod.location,
            'basePrice': prod.basePrice,
            'bestPrice': getBestOffer(pk)[1],
            'date': prod.date,
            'whoWon': getBestOffer(pk)[0],
        }
    )
    print(response)
    prod.jsonResult = str(response)
    prod.save()

    # associate json with an Ethereum transaction
    prod.writeOnChain()


# registration form
def register(request):
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        # initialise blank form and ip info
        form = RegisterForm()
    # render the page
    return render(request, "offers/register.html", {"form": form, })


# handle logout
def logoutReq(request):
    logout(request)
    return redirect("/")


# handle login
def loginReq(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('/')
            else:
                return render(request, "offers/login.html", {"form": form})
        else:
            return render(request, "offers/login.html", {"form": form})

    form = AuthenticationForm()
    return render(request, "offers/login.html", {"form": form})
