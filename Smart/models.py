from django.db import models
from django.contrib.auth.models import User
import zipfile
import os
from django.conf import settings

# Create your models here.

class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {'Done' if self.completed else 'Pending'}"

class Post(models.Model):
    title = models.CharField(max_length=200)  # Title of the post
    content = models.TextField()  # Content of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Author of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the post was last updated

    def __str__(self):
        return self.title  # String representation of the post
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Determines display order")

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question
    
class CaseStudyZip(models.Model):
    title = models.CharField(max_length=200)
    zip_file = models.FileField(upload_to='case_studies/zips/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def extract_zip(self):
        # Path where ZIP will be extracted
        extract_path = os.path.join(settings.MEDIA_ROOT, 'case_studies', str(self.id))
        os.makedirs(extract_path, exist_ok=True)
        
        # Extract the ZIP
        with zipfile.ZipFile(self.zip_file.path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        return extract_path
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.extract_zip()

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='team_photos/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.name