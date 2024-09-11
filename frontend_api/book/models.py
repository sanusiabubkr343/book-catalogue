from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.email

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    borrowed_until = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    


    class Meta:
        ordering = ('-updated_at',)


    def __str__(self):
        return self.title
    
