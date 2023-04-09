from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.utils.crypto import get_random_string

# Create your models here.

class Blog(models.Model):
    blog_name = models.CharField(max_length=200)
    blog_descriptions = models.TextField()
    author_image = models.ImageField(upload_to='uploads/', null=True,blank=True)
    logo = models.ImageField(upload_to='uploads', null=True,blank=True)
    facebook_url = models.CharField(max_length=150, null=True,blank=True)
    twitter_url = models.CharField(max_length=150, null=True,blank=True)
    youtube_url = models.CharField(max_length=150, null=True,blank=True)
    pintarest_url = models.CharField(max_length=150, null=True,blank=True)
    instagram_url = models.CharField(max_length=150, null=True,blank=True)
    google_url = models.CharField(max_length=150, null=True,blank=True)

    def __str__(self):
        return self.blog_name
    
class author(models.Model):
    author_name = models.CharField(max_length=200)
    author_descriptions = models.TextField()
    


    def __str__(self):
        return self.author_name
    
class category(models.Model):
    category_name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
            while category.objects.filter(slug=self.slug).exists():
                self.slug = f'{slugify(self.category)}-{get_random_string(2)}'
        super().save(*args, **kwargs)
    
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    post_title = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    post_category = models.ForeignKey(category, on_delete=models.PROTECT)
    post_image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    post_author = models.ForeignKey(author, on_delete=models.CASCADE)
    post_content = RichTextUploadingField()
    tags = TaggableManager(blank=True)
    post_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    post_date = models.DateField(auto_now_add=True)
    mod_post = models.DateField(auto_now=True)
    featured_post = models.BooleanField(default=False)
    views = models.IntegerField(default=0, blank=True, null=True)
    meta_title = models.CharField(max_length=160, blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.post_title
    
    class Meta:
        ordering = ['post_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.post_title)
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f'{slugify(self.post_title)}-{get_random_string(2)}'
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'