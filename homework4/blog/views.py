from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from datetime import datetime
from django.core.mail import send_mail
from random import randrange

from blog.models import *
from blog.forms import *

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404
# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

bloggers_list = User.objects.all()


def home(request):
    
    if request.user.is_authenticated():
        c_user = request.user
        c_user_follows = Follows.objects.filter(user=c_user); 
        other_bloggers = User.objects.exclude(email=c_user.email)
        tit='Home'
        #otherBloggers = []
        #print c_user.first_name, "follows", len(c_user_follows), "bloggers. They are : "
        #for u in c_user_follows:
            #print u.user_follows.email
        
        items = Item.objects.none()
        for u in c_user_follows:
            if items is None:
                items = Item.objects.filter(user=u.user_follows)
            else:
                items = items | Item.objects.filter(user=u.user_follows)
        items = items.order_by('-added')
        context = {'tit' : tit , 'items' : items, 'other_bloggers': other_bloggers, 'c_user_follows': c_user_follows}
        return render(request, 'blog/index.html', context)
    
    else:
        tit='Home'
        other_bloggers = User.objects.all()
        #for u in other_bloggers:
            #print u.email
        items = Item.objects.all()
        items = items.order_by('-added')
        context = {'items' : items,'other_bloggers' : other_bloggers, 'tit' : tit}
        return render(request, 'blog/index.html', context)
        


@login_required
def add_item(request):
    tit = 'My Posts'
    new_entry = Item(user=request.user , added=datetime.now())
    form = ItemForm(request.POST, request.FILES, instance=new_entry)
    if not form.is_valid():
        items = Item.objects.filter(user=request.user)
        items = items.order_by('-added')
        c_user = request.user
        c_user_follows = Follows.objects.filter(user=c_user); 
        other_bloggers = User.objects.exclude(email=c_user.email)    
        context = {'form':form, 'items' : items, 'other_bloggers':other_bloggers,}
        return render(request, 'blog/manage.html', context)
    #print request.POST.get('text')
    form.save()
    items = Item.objects.filter(user=request.user)
    items = items.order_by('-added')
    c_user = request.user
    c_user_follows = Follows.objects.filter(user=c_user); 
    other_bloggers = User.objects.exclude(email=c_user.email)    
    context = {'tit': tit, 'items' : items, 'other_bloggers':other_bloggers}
    return render(request, 'blog/index.html', context)
    
    
@login_required
def delete_item(request, id):
    errors = []

    # Deletes item if the logged-in user has an item matching the id
    try:
	item_to_delete = Item.objects.get(id=id, user=request.user)
	item_to_delete.delete()
    except ObjectDoesNotExist:
	errors.append('No post to delete')

    items = Item.objects.filter(user=request.user)
    items = items.order_by('-added')

    c_user = request.user
    c_user_follows = Follows.objects.filter(user=c_user); 
    other_bloggers = User.objects.exclude(email=c_user.email)    
    context = {'items' : items, 'errors' : errors, 'other_bloggers' : other_bloggers}
    
    return render(request, 'blog/index.html', context)


def register(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        other_bloggers = User.objects.all();
        context = {'other_bloggers' : other_bloggers }
        return render(request, 'blog/register.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data

    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First Name is required.')

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last Name is required.')

    if not 'username' in request.POST or not request.POST['username'] or not'@' in request.POST['username']:
	   errors.append('Please enter your email address')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
	context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
	   errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
	   errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
	errors.append('Passwords did not match.')


    if len(User.objects.filter(username = request.POST['username'])) > 0:
	errors.append('You have already registered with this email address.')

    if errors:
        return render(request, 'blog/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'],\
                                        email=request.POST['username'],\
                                        first_name=request.POST['firstname'],\
                                        last_name=request.POST['lastname'],
                                        )
    #new_user.is_active=False
    new_user.is_active=False
    new_user.save()
    new_user_follows = Follows(user=new_user,user_follows=new_user)
    new_user_follows.save();
    uname= request.POST['username']
    rNum = randrange(10000)
    new_obj= Validation(rNum=rNum,user=new_user)
    new_obj.save();
    link='http://localhost:8000/blog/confirmation?username='+uname+'&conf='+str(rNum)
    send_mail('Please Activate your account at BLOG', link, 'mayurs@cmu.edu',
    [uname], fail_silently=False)
    other_bloggers = User.objects.all();
    context = {'other_bloggers' : other_bloggers }
    return render(request,'blog/registered.html',context);


def validation(request):
        uname = request.GET['username'];
        user1=User.objects.filter(username = uname)
        valida = Validation.objects.filter(user = user1[0]) 
        if valida[0].rNum == int(request.GET['conf']):
            temp=User.objects.filter(username = valida[0].user)
            temp1=temp[0]
            temp1.is_active=True
            temp1.save()
            return render(request,'blog/confirmed.html',{})

        return render(request, 'blog/failed.html',{})

@login_required
def manage(request):
        c_user = request.user
        other_bloggers = User.objects.exclude(email=c_user.email)
        c_user_follows = Follows.objects.filter(user=c_user); 
        items = Item.objects.filter(user=c_user)
        items = items.order_by('-added') 
        context = {'form': ItemForm(), 'items' : items, 'other_bloggers': other_bloggers, 'c_user_follows': c_user_follows}
        return render(request, 'blog/manage.html', context)
       
def watch(request):
    errors = []
    email = request.GET.get('id')
    try:
        user_to_watch = User.objects.get(email=email)
    except ObjectDoesNotExist:
        errors.append('User does not exist')
    other_bloggers = User.objects.all()
    items = Item.objects.filter(user=user_to_watch)
    items = items.order_by('-added')
    context = {'items' : items, 'errors' : errors, 'other_bloggers' : other_bloggers }
    return render(request, 'blog/index.html', context)

@login_required
def follow(request):
    errors = []
    email = request.GET.get('id')
    c_user=request.user
    message=''
    tit='Home'
    try:
        blogger_status_change = User.objects.get(email=email)
        try:
            c_user_follows = Follows.objects.get(user=c_user, user_follows=blogger_status_change)
            message = 'You have unfollowed '+ blogger_status_change.first_name
            #print "Found ", c_user_follows.user_follows, ". Now unfollowing."
            c_user_follows.delete()
            

        except ObjectDoesNotExist:
            c_user_follows = Follows(user=c_user,user_follows=blogger_status_change)
            message = 'You are now following '+ blogger_status_change.first_name
            #print "Not Found ", c_user_follows.user_follows, ". Now Following."
            c_user_follows.save();
    except ObjectDoesNotExist:
        errors.append('User does not exist')

    c_user_follows = Follows.objects.filter(user=c_user); 
    other_bloggers = User.objects.exclude(email=c_user.email)
    #print c_user.first_name, "follows", len(c_user_follows), "bloggers. They are : "
    #for u in c_user_follows:
        #print u.user_follows.email

    items = Item.objects.none()
    for u in c_user_follows:
        if items is None:
            items = Item.objects.filter(user=u.user_follows)
        else:
            items = items | Item.objects.filter(user=u.user_follows)
    items = items.order_by('-added')
    context = {'tit':tit, 'items' : items, 'other_bloggers': other_bloggers, 'c_user_follows': c_user_follows, 'message' : message}
    return render(request, 'blog/index.html', context)


def get_bloggers(request):
    if request.user.is_authenticated():
        c_user = request.user
        other_bloggers = User.objects.exclude(email=c_user.email)
    else:
        other_bloggers = User.objects.all()
    
    context = {'other_bloggers' : other_bloggers}
    return render(request, 'blog/blogger_list.xml', context, content_type='application/xml');



def get_photo(request, id ):
    entry = get_object_or_404(Item , id=id)
    if not entry.picture:
        raise Http404

    content_type = guess_type(entry.picture.name)
    return HttpResponse(entry.picture, mimetype=content_type)

























