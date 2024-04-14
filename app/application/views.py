from django.shortcuts import render, redirect
from django.db import connection


# Create your views here.

def home(request):
    username = request.session.get('username')
    return render(request, 'home.html', {'username': username})

def signup(request):
    if request.method == 'POST':
        # Retrieve form data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic form validation
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Insert data into the database
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s)",
                           [firstname, lastname, email, username, password1])

        return redirect('home') 
    else:
        return render(request, 'signup.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE username = %s AND password = %s", [username, password])
            user = cursor.fetchone()

        if user:
            request.session['username'] = username
            return redirect('home')  # Redirect to home page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout(request):
    request.session.clear()
    return redirect('home') 

def profile(request): 
    return render(request, 'profile.html')