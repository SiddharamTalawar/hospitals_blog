from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError




choice_list = [('Mental health','Mental health'),('heart disease','heart disease'),('covid 19','covid 19'),('immunization','immunization')]


class post(models.Model):
    title=models.CharField(max_length=250)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    summary=models.TextField()
    content=models.TextField()
    category=models.CharField(choices=choice_list, max_length=250,default="Mental health")
    post_image=models.ImageField(null=True, blank=True, upload_to="images/post_images/")
    date_created=models.DateTimeField(auto_now_add=True)
    draft=models.BooleanField(default=False)


    def __str__(self):
        return self.title +' by '+  str(self.author)

    def get_absolute_url(self):
        return reverse('home')



class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
	Frist_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	confirm_password = models.CharField(max_length=250)
	Address = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	pincode = models.CharField(max_length=100)
	Doctor = models.BooleanField(default=False)


    
	def __str__(self):
		return str(self.user)

	def get_absolute_url(self):
		return reverse('home')

	
		        
        
    
    









