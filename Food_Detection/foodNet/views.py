from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CalorieForm

import json
from ibm_watson import VisualRecognitionV3, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

authenticator = IAMAuthenticator('QeULZ3tNyXhuGlh4eQWn0DTJgcQET86_fym6s3Yn_A8z')
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=authenticator
)

visual_recognition.set_service_url(
    'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/e83c2dab-5735-4074-8358-f792e6c3dc47'
    )


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
                print('success')
                return redirect('Calorie')
            else:
                print('failed')
    else:
        form = LoginForm()

    return render(request, 'foodNet/login.html', {'form':form})

@login_required
def calorieview(request):
    classes_result = dict()
    if request.method == 'POST':
        form = CalorieForm(request.POST)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            print(img_file)
            classifier_ids = ["food"]
            
            try:
                classes_result = visual_recognition.classify(
                    images_file=img_file, classifier_ids=classifier_ids).get_result()
                print(json.dumps(classes_result))
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        print(classes_result.keys())       
        for classifiers in classes_result["images"]:
            print(classifier["classes"][0]["class"])

    else:
        form = CalorieForm()

    return render(request, 'foodNet/calorie_measurer.html', {'form':form})

    
