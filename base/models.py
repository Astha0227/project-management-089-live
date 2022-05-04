from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Developer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)


	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Project(models.Model):
	

	name = models.CharField(max_length=200, null=True)
	no_of_days = models.IntegerField(null=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name




class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Processing', 'Processing'),
			('Done', 'Done'),
			)
	PRIORITY = (
			('High', 'High'),
			('Medium', 'Medium'),
			('Low', 'Low'),
			) 

	developer = models.ForeignKey(Developer, null=True, on_delete= models.SET_NULL)
	project = models.ForeignKey(Project, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	priority = models.CharField(max_length=200, null=True, choices=PRIORITY)
	note = models.CharField(max_length=1000, null=True) 

	def __str__(self):
		return self.project.name




	