from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, FoodForm, UpdateProfileForm, WalkForm



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
                return redirect('update_profile')
           
            else:
                print('Failed')
    else:
        form = LoginForm()

    return render(request, 'foodNet/login.html', {'form':form})

    

@login_required
def show_profile_view(request):
    profile = request.user.profile
    print(profile)
    return render(request, 'foodNet/show_profile.html', {'profile': profile})

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        form = UpdateProfileForm(request.POST)
        if form.is_valid():

            profile.name = form.cleaned_data.get('name')
            profile.height = form.cleaned_data.get('height')
            profile.weight = form.cleaned_data.get('weight')
            profile.gender = form.cleaned_data.get('gender')
            profile.workout = form.cleaned_data.get('workout')
            profile.save()
        
            return redirect('show_profile')
    else:
        form = UpdateProfileForm()

    return render(request, 'foodNet/update_profile.html', {'form':form})

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

    return render(request, 'foodNet/add_walk.html', {'form':form})

@login_required
def walk_list_view(request):

    walks = request.user.profile.walks.all()

    return render(request, 'foodNet/show_walk.html', {'walks':walks})

    

# import tensorflow as tf
# import numpy as np

# def excersice(workout):

#     if workout=='less':
#         w=[1,0,0]
#     elif workout=='med':
#         w=[0,1,0]
#     elif workout=='high':
#         w=[0,0,1]
#     return w   

# def sex(gender):
    
#     if gender=='m':
#         g=[1,0]
#     elif gender=='f':
#         g=[0,1]
#     return g
        
# def cal(calorie):
    
#     if calorie<=2000:
#         c=[1,0,0]
#     elif calorie<=2500:
#         c=[0,1,0]
#     elif calorie>2500:
#         c=[0,0,1]
#     return c

# def preprocessing(workout,bmi,gender,calorie):
#     w=np.array(excersice(workout),dtype='float32')
#     g=np.array(sex(gender),dtype='float32')
#     w_b=np.append(w,[bmi],axis=0)
#     w_b_g=np.append(w_b,g,axis=0)
#     c=np.array(cal(calorie))
#     return np.array([np.append(w_b_g,c,axis=0)],dtype='float32')

# def output(array):
#     r=np.array(np.reshape(array,(6,)),dtype='int')
#     j=1
#     for i in r:
#         if i==0:
#             j=j+1
#     return j

# model=tf.keras.models.load_model("foodNet/recc_diet.h5")

# def rec_view(request):
#     profile = request.user.profile
#     ans=output(model.predict(preprocessing(profile.workout,profile.age,profile.gender,profile.total_calories)))
#     if ans == '1':
#         return render(request, 'foodNet/diet4.html')
#     elif ans == '2':
#         return render(request, 'foodNet/diet5.html')
#     elif ans == '3':
#         return render(request, 'foodNet/diet6.html')
#     elif ans == '4':
#         return render(request, 'foodNet/diet1.html')
#     elif ans == '5':
#         return render(request, 'foodNet/diet2.html')
#     elif ans == '6':
#         return render(request, 'foodNet/diet3.html')

