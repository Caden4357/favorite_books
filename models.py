from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
import bcrypt 
import re 

#checking if email is proper email format 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        #checking for proper email format 
        if not EMAIL_REGEX.match(postData['email_address']):
            errors['email_address'] = "invalid email address"

        #checking for duplicate email address
        email_check = User.objects.filter(email_address = postData['email_address'])
        if email_check:
            errors['duplicate'] = "Email already registered to an account"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if postData['pw_confirm'] != postData['pw_confirm']:
            errors['password'] = "Passwords do not match"
        return errors

    def register(self, postData):
        #encrypting password with salt 
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email_address = postData['email_address'],
            password = pw,
        )
    
    def authenticate(self, email_address, password):
        users = User.objects.filter(email_address=email_address)
        if users:
            user=users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False

                
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors["title"] = "Title Cannot Be Left Blank"

        if len(postData['desc']) < 5:
            errors["desc"] = "Description must be at least 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=1000)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=CASCADE)
    users_who_like = models.ManyToManyField(User, related_name='liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()