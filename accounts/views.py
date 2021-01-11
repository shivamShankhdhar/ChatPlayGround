
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
# FORMS 
from accounts.forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
# IMPORTED FOR CREATING LOGIN, LOGOUT AND AUTHENTICATING TO THE USER 
from django.contrib.auth import login, authenticate, logout, views
# imported for BASE_URL
from django.conf import settings 
# ACCOUNTS MODELS
from accounts.models import Account

#required for image cropping and saving

from django.core.files.storage import FileSystemStorage, default_storage
# from django.core.files.storage import FileSystemStorage
import os
import cv2
import json
import base64
# import requests
from django.core import files

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


# views 

def register_view(request, *args, **kwargs):
    template_name = 'accounts/register.html'
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
        
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # after registerration user will automatic login 
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("home")

        else:
            context['registration_form'] = form

    return render(request, template_name, context )


def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request, *args, **kwargs):
    template_name = 'accounts/login.html'
    context = {}

    if request.user.is_authenticated:
        return redirect('home')
    
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['login_form'] = form

    return render(request, template_name, context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.Get.get("next"):
            redirect = str(request.GET.get('next'))


def account_view(request, *args, **kwargs):
    """
        -Logic here is kidn of tricky
        is_self (boolean)    
            -1: NO_REQUEST_SENT
            0:THEM_SENT_TO_YOU
            1:YOU_SENT_TO_THEM
    """
    context = {}
    template_name = 'accounts/account.html'
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk = user_id)
    except Account.DoesNotExist:
        return HttpResponse("that user doesn't exist.")
    
    # if account exists 
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # state tamplate  variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context["is_self"] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request, template_name, context)



# search functionality
def account_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
            user = request.user
            accounts = [] # [(account1, True), (account2, False), ...]
            for account in search_results:
                accounts.append((account, False)) # you have no friends yet
            context['accounts'] = accounts
        
    return render(request, "accounts/search_result.html", context)

# views commentd 
"""
context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
			user = request.user
			accounts = [] # [(account1, True), (account2, False), ...]
			for account in search_results:
				accounts.append((account, False)) # you have no friends yet
			context['accounts'] = accounts
				
	return render(request, "accounts/search_results.html", context)
"""
# end views

def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
            return redirect("login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            #delete old profile image so the name preserved
            account.profile_image.delete()
            form.save()
            new_username = form.cleaned_data['username']
            return redirect("accounts:view", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                initial={
                    "id": account.pk,
                    "email": account.email, 
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                    "id": account.pk,
                    "email": account.email, 
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "accounts/edit_account.html", context)


def save_temp_profile_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists( f"{settings.TEMP}/{user.pk}" ):
            os.mkdir( f"{settings.TEMP}/{user.pk}" )
        url = os.path.join(f"{settings.TEMP}/{user.pk}", TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location = url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "=" + ({4 - ( len(imageString) % 4) % 4 })
            return save_temp_profile_image_from_base64String(imageString, user)
    return None

# croping image with cv2 
def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get("image")
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = cv2.imread(url)

            #  4 parameters of croped image 
            cropX = int(float(str(request.POST.get("cropX"))))  # crpopX == bottom left x coordinate
            cropY= int(float(str(request.POST.get("cropY"))))  # crpopY == bottom left y coordinate
            cropwidth = int(float(str(request.POST.get("cropwidth")))) # width
            cropheight = int(float(str(request.POST.get("cropheight")))) # height

            # checking for negative
            if cropX < 0 :
                cropX = 0
            if cropY < 0:
                cropY = 0
            crop_img = img[cropY:cropY + cropheight, cropX:cropX + cropwidth] # this open cv2 stuf
            cv2.imwrite(url, crop_img)

            user.profile_image.delete()
            user.profile_image.save("profile_image.png", files.File(open(url, "rb")))
            user.save()

            payload["result"] = "Success"
            payload["cropped_profile_image"] = user.profile_image.url
            # removing temp image 
            os.remove(url)


        except Exception as e:
            payload["result"] = "error"
            payload["exception"]  = str(e)
    return HttpResponse(json.dumps(payload), content_type = "application/json")