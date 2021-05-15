from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        return redirect('/blog')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email_address'], request.POST['password']):
        messages.error(request, "Invalid Email or Password")
        return redirect('/')
    user = User.objects.get(email_address=request.POST['email_address'])
    request.session['user_id'] = user.id
    return redirect('/blog')

def blog_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'books': Book.objects.all().exclude(users_who_like=user),
        'users_books': Book.objects.filter(users_who_like=user),
        'owner_of_book': Book.objects.filter(uploaded_by=user)
        }
    return render(request, 'books.html', context)

def create_book(request):
    if request.method == "GET":
        return redirect('/')
    errors = Book.objects.book_validator(request.POST)
    if errors:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/blog')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = user,
        )
    user = User.objects.get(id = request.session['user_id'])
    book=book
    book.users_who_like.add(user)
    return redirect('/blog')

def display(request, id):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'users': User.objects.all(),
        'user': user,
        'this_book': Book.objects.get(id=id)
    }
    return render(request, 'display.html', context)

def favorite(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_books.add(book)
    user.save()
    return redirect('/blog')

def unfavorite(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    book.users_who_like.remove(user)
    book.save()
    return redirect('/blog')

def edit(request, id):
    context={
        'book': Book.objects.get(id=id)
    }
    return render(request,"update.html",context)

def update(request, id):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/edit/{id}")
        book_to_update = Book.objects.get(id=id)
        book_to_update.title = request.POST['title']
        book_to_update.desc = request.POST['desc']
        book_to_update.save()
        print(book_to_update.title)
        return redirect('/blog')

def destroy(request, id):
    to_delete = Book.objects.get(id=id)
    to_delete.delete()
    return redirect('/blog')

def logout(request):
    request.session.clear()
    return redirect('/')
datetime.datetime.today() - datetime.timedelta(days=13*365+1)