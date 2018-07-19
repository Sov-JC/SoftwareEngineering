from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, reverse

from .forms import *
from database.models import USER, ADDRESS, USER_HOME_ADDRESS, CART, RESERVED_CREDIT_CARD, CREDIT_CARD
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User as AuthUser # <-------

from myCart import utility

def home (request):
    #return render(request, "home.html", {})
    return render(request, "homepage/index.html", {}) #temp

def RegistrationView (request):
    
    if request.method =="POST":
        request.session
        #test
        print("WAS POST")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            First_Name = request.POST.get('First_Name')
            Last_Name = request.POST.get('Last_Name')
            Username = request.POST.get('Username')
            Email = request.POST.get('Email', ' ')
            #Address = request.POST.get('Address', ' ') 
            HomeAddress = request.POST.get('Address', ' ')
            City = request.POST.get('City', ' ')
            Zip_Code = request.POST.get('Zip_Code', ' ')
            psw = request.POST.get('psw')
            #user_obj = USER(Email = Email, Username = Username,Fname= First_Name, Lname= Last_Name, Password= psw ) #won't work with new model, USER attributes changed
            
            #Store Address
            print("creating Address...")
            HomeAddr = USER_HOME_ADDRESS()
            Addr = ADDRESS()
            Addr.Zip_Post = Zip_Code
            Addr.Address_1 = "" #fill this in later when user can fill this in a seperate form
            Addr.Address_2 = "" #fill this in later when user can fill this in a seperate form
            Addr.Country = "" #fill this in later when user can fill this in a seperate form
            Addr.State = "" #fill this in later when user can fill this in a seperate form
            Addr.City_Town = City
            Addr.Name = "" #fill this in later when user can fill this in a seperate form
            
            print("saving address...")
            Addr.save()
            HomeAddr.Address_ID = Addr
            HomeAddr.save()

            #Store AuthUser
            print("creating AuthUser")
            AuthUser_ID = AuthUser()
            AuthUser_ID.first_name = First_Name
            AuthUser_ID.last_name = Last_Name
            AuthUser_ID.email = Email
            AuthUser_ID.set_password(psw)
            AuthUser_ID.username = Username
            print("saving AuthUser...")
            AuthUser_ID.save() #if error occurs later on, username will still be saved in db! fix later
            
            print("creating USER...")
            #Store USER
            user_obj = USER()
            user_obj.AuthUser_ID = AuthUser_ID
            user_obj.Home_address_ID
            user_obj.Preferred_credit_card_ID = None

            cart = CART(Cart_ID = utility.generate_Cart_ID()) #for now!
            cart.save() #for now!
            user_obj.Cart_ID = cart #for now!

            user_obj.Nick_name = ''
            print("Saving user_obj....")
            user_obj.save()
            
            print("Sucess!:)")
            


            
            #return HttpResponse(reversed ('home::register'))
            return HttpResponseRedirect(reverse('homepage:index'))#send to home page for now, i'm not sure what above statement does
        else:
            #test
            print("Form was invalid!!!")
            print(form.errors)
    else:
        #test
        print("NOT POST")
        form = RegistrationForm()

    #return render (request, 'register.html', {'form': form,})
    return render (request, 'prof/register.html', {'form': form,})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["Username"]
            password = form.cleaned_data["Password"]

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('homepage:index')) 
                else:
                    HttpResponse("Uh oh, your account is currently not active! Send us an email so we can resolve the problem!")
            else:
                raise Http404("Invalid password, please try again<br><a href='/'> Go back to homepage <a/>")
        else:
            #form data was invalid. force user to reload page so he can try again
            return render(request, "prof/login.html")
    else:
        return render(request, "prof/login.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage:index"))

@login_required
def profileInfo(request):    
    authUser = request.user
    user = authUser.user #taking advantage of one-to-one relationship. user is a USER object.

    #get all the reserved credit cards that point to the user
    reserved_credit_cards = user.reserved_credit_card_set.all() #let me know if you don't understand this line

    credit_cards = [] #will store all the credit cards that belong to the user.

    for rcc in reserved_credit_cards:
        print(str(rcc))
        credit_cards.append(rcc.C_card_number)

    print("----------------------------")
        
    for credit_card in credit_cards:
        print(str(credit_card) + " belongs to " + str(user.AuthUser_ID.username)) 

    print(type(user))

    #user is passed to get things like first name, lastname, username, etc.
    #credit cards is passed so we can view what credit cards he has added to his billing information
    context = {"userinfo":user, "credit_cards":credit_cards}    
    return render(request, "prof/profileInfo.html", context=context)

@login_required
def add_preferred_card(request):
    return None

@login_required
def add_reserved_card(request):
    
    if request.method == "POST":
        form = AddReservedCardForm(request.POST)
        
        if form.is_valid():
            print("form is valid!")
            C_card_number = form.cleaned_data["C_card_number"]
            CVV = form.cleaned_data["CVV"]
            Exp_month = form.cleaned_data["Exp_month"]
            Exp_year = form.cleaned_data["Exp_year"]
            Fname = form.cleaned_data["Fname"]
            Lname = form.cleaned_data["Lname"]
            Mname = form.cleaned_data["Mname"]

            credit_card = CREDIT_CARD(C_card_number=C_card_number)
            print("credit_card number is: " + str(credit_card))
            credit_card.CVV = CVV
            credit_card.Exp_month = Exp_month
            credit_card.Exp_year = Exp_year
            credit_card.Fname = Fname
            credit_card.Lname = Lname
            credit_card.Mname = Mname
            credit_card.save()
            
            authUser = request.user #AuthUser object
            print("authUser is: " + str(authUser))
            user = authUser.user #USER object
            print("user is: " + str(user))

            rcc = RESERVED_CREDIT_CARD()
            rcc.C_card_number = credit_card
            rcc.ProfileID = user
            rcc.save()

            return HttpResponseRedirect(reverse("prof:profileInfo"))
        else:
            print("Form is invalid")
            return render(request, "prof/add_reserved_card.html", context = {"form" : form})

    else:
        #Was not post, therefore show user a form to input reserved card info that the person wants to add to his account
        print("call was not POST")
        return render(request, "prof/add_reserved_card.html")
        
    return HttpResponse("Read CMD")
