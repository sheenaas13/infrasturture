from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    image = models.ImageField(upload_to='project_images/')
    challenge_text = models.TextField(verbose_name="The Challenge")
    solution_text = models.TextField(verbose_name="The Solution")
    impact_text = models.TextField(verbose_name="The Impact")
    
    def __str__(self):
        return self.name
    
class Query(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    sector = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class JobApplication(models.Model):
    POSITION_CHOICES = [
        ('uiux', 'UI/UX Designer'),
        ('developer', 'Web Developer'),
        ('marketing', 'Marketing Executive'),
        ('designer', 'Graphic Designer'),
        ('civil_engineer', 'Civil Engineer'),
        ('site_manager', 'Site Manager'),
        ('project_manager', 'Project Manager'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    experience = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.position}"
    
class Vacancy(models.Model):
    position_name = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience_required = models.CharField(max_length=50)

    def __str__(self):
        return self.position_name
    
class News(models.Model):
    CATEGORY_CHOICES = [
        ('popular', 'Popular'),
        ('recent', 'Recent'),
        ('business', 'Business'),
        ('trending', 'Trending'),
        ('top', 'Top'),
        ('searched', 'Most Searched'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    CATEGORY_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Recent', 'Recent'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
    
from django.db import models

class AlertRegistration(models.Model):

    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('hindi', 'Hindi'),
    ]
    TIMING_CHOICES = [
        ('immediate', 'Immediately as they happen'),
        ('daily', 'Daily Summary'),
        ('limited', 'Only during certain hours'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    channels = models.CharField(max_length=100)  
    alert_types = models.CharField(max_length=255)  
    timing = models.CharField(max_length=20, choices=TIMING_CHOICES)
    specific_hours = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    

class AlertMade(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    location = models.CharField(max_length=255)
    alert_type = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"

class EstimateCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class EstimateImageGallery(models.Model):
    category = models.ForeignKey(EstimateCategory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='estimate_gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.caption or 'Image'}"
    
class CostRates(models.Model):
    development_type = models.CharField(max_length=50, choices=[
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed-Use'),
    ])
    base_rate = models.PositiveIntegerField()  # per sq ft
    green_feature_cost = models.PositiveIntegerField(default=50000)
    design_percentage = models.FloatField(default=10.0)
    permit_cost = models.PositiveIntegerField(default=50000)

    def __str__(self):
        return f"{self.development_type.capitalize()} Rates"
    
class Blog(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    meta_description = models.CharField(max_length=255)  
    short_description = models.TextField(blank=True, null=True) 
    extra_description = models.TextField(blank=True, null=True) 

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class UserFeedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"

class UserIssueReport(models.Model):
    ISSUE_TYPES = [
        ('road', 'Road Damage'),
        ('water', 'Water Leakage'),
        ('power', 'Power Outage'),
        ('garbage', 'Garbage Issue'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPES)
    location = models.CharField(max_length=500, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue_type.title()} issue by {self.name}"


