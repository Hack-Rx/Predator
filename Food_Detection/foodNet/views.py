from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, FoodForm, CreateProfileForm, UpdateProfileForm, WalkForm



# Create your views here.

def indexview(request):
    return render(request, 'foodNet/index.html')

def loginview(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
                )
            if user is not None:
                return redirect('create_profile')
           
            else:
                print('Failed')
    else:
        form = LoginForm()

    return render(request, 'foodNet/login.html', {'form':form})

    
@login_required
def create_profile_view(request):
    if request.method == "POST" and request.user.profile is None:
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect('show_profile')
    else:
        form = CreateProfileForm()

    return render(request, 'foodNet/create_profile.html', {'form':form})

@login_required
def show_profile_view(request):
    profile = request.user.profile
    print(profile)
    return render(request, 'foodNet/show_profile.html', {'profile': profile})

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        form = UpdateProfileForm(request.POST, profile)
        if form.is_valid():
            form.save()
            return redirect('show_profile')
    else:
        form = UpdateProfieForm()

    return render(request, 'foodNet/create_profile.html', {'form':form})

@login_required
def add_food_view(request):
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            new_food = form.save(commit=False)
            new_food.uploader = request.user.profile
            new_food.save()
            return redirect('food_list')

    else:
        form = FoodForm()
    
    return render(request, 'foodNet/add_food.html',{'form':form})

@login_required
def food_list_view(request):
    
    foods = request.user.profile.foods.all()

    return render(request,'foodNet/show_food.html', {'foods':foods})

@login_required
def create_walk_view(request):
    if request.method == "POST":
        form = WalkForm(request.POST)
        if form.is_valid():
            new_walk = form.save(commit=False)
            new_walk.user = request.user.profile
            new_walk.save()
            return redirect('walk_list')

    else:
        form = WalkForm()

    return render(request, 'foodNet/create_walk.html', {'form':form})

@login_required
def walk_list_view(request):

    walks = request.user.profile.foods

    return render(request, 'foodNet/walk_list_html', {'walks':walks})

    

