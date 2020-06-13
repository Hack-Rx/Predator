from django.db import models
from django.contrib.auth.models import User
from nutritionix import Nutritionix



from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from django.db.models.signals import post_save
from django.dispatch import receiver


authenticator = IAMAuthenticator('QeULZ3tNyXhuGlh4eQWn0DTJgcQET86_fym6s3Yn_A8z')
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=authenticator
)

visual_recognition.set_service_url(
    'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/e83c2dab-5735-4074-8358-f792e6c3dc47'
    )
nix = Nutritionix(app_id="a43c505b", api_key="ce2e2ad8e38bbf9dbb2043575c591179")
# Create your models here.

WORKOUT_TYPES = [('1' , 'Light'), ('2', 'Heavy')]
GENDER = [('1', 'Male'), ('2', 'Female'), ('3', 'Other')]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, blank=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    BMI = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    workout = models.CharField(max_length=1, choices=WORKOUT_TYPES)
    total_calories = models.IntegerField(default=0)
    total_steps = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.weight is not None and self.height is not None:

            self.BMI = self.weight/(self.height*self.height)/10000
        super().save(*args, **kwargs)

    def add_steps(self, steps):
        self.total_steps += steps

    def add_calories(self, calories):
        self.total_calories += calories
    
    def deduct_calories(self, calories_burnrd):
        self.total_calories -= calories_burnrd
    
    def __str__(self):
        return self.name

class Food(models.Model):
    uploader = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='foods')
    food_image = models.ImageField(null=True, upload_to='foodNet/%Y/%m/%D/')
    food_name = models.CharField(max_length=30, blank=True)
    calories = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        img_file = str(self.food_image)
        classifier_ids = ['Food']
        classes_result = dict()

        with open(img_file, 'rb') as images_file:
            classes_result = visual_recognition.classify(images_file=images_file).get_result()
            
        if 'images' in classes_result:
            print('working')       
            print(classes_result['images'][0]['classifiers'][0]['classes'][0]['class'])
            self.food_name = classes_result['images'][0]['classifiers'][0]['classes'][0]['class']
        
            a = nix.search(self.food_name, results="0:1").json()
            b = a['hits']
            _id = b[0]
            self.calories = nix.item(id=_id['_id']).json()['nf_calories']
            print(self.calories)
            self.uploader.add_calories(self.calories)
            super().save(*args, **kwargs)

        else:
            print('something is wrong') 

    def __str__(self):
        return self.food_name



class Walk(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='walks')
    steps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    calories_burned = models.IntegerField()

    def save(self):
        calories_burned = ((self.user.weight*0.25)/2000)*self.steps
        self.user.add_steps(self.steps)
        self.user.deduct_calories(calories_burned)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.steps) + ' : ' + str(date)

@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)