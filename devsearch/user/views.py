from django.shortcuts import render, redirect
from .models import *
from .forms import CreateUser
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm, SkillForm, MessageUserForm
from django.db.models import Q
from django.core.paginator import Paginator,  PageNotAnInteger, EmptyPage

# Create your views here.
def UserProfile(request):
    search_query = ''

# Building Search Bar
    if request.GET.get('text'):
        search_query = request.GET.get('text')
    
    skills = Skill.objects.filter(name__icontains = search_query)
    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) | 
    Q(profession__icontains = search_query) |
    Q(skill__in = skills))

# Page Pagination
    page = request.GET.get('page')
    num = 3
    paginator = Paginator(profiles, num)

    
    try:
        profiles = paginator.page(page)
    
    except PageNotAnInteger: 
        page = 1
        profiles = paginator.page(page)
    
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)


    context = {'profiles': profiles, 'search_query': search_query, "paginator": paginator }
    return render(request, 'user/profiles.html', context)

def ProfileDetail(request, pk):
    profile = Profile.objects.get(id=pk)
    skill_d = profile.skill_set.filter(about__gte = '20')
    skill = profile.skill_set.exclude(about__gte = '20')
    projects = profile.project_set.all()
    context = {'profile': profile, 'skill_d': skill_d, 'skill': skill, 'projects':projects}
    return render(request, 'user/ProfileDetail.html', context)

def SignUp(request):
    page = 'register'
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('signin')
    context = {'form': form, 'page': page}
    return render(request, 'user/signup.html', context)

def SignIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        else:
            messages.error(request, 'Oops invalid credentials')
    return render(request, 'user/signup.html')

def SignOut(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def UserAccount(request):
    user = request.user.profile
    context = {'user': user}
    return render(request, 'user/account.html', context)

@login_required(login_url='signin')
def UpdateProfile(request):
    profile = request.user.profile
    form = UpdateProfileForm(instance = profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance = profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile Updated')
            return redirect('account')
    context = {"form": form}
    return render(request, 'user/update_profile.html', context)

@login_required(login_url='signin')
def CreateSKill(request):
    form = SkillForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit = False)
            skill.owner = profile
            skill.save()
            messages.info(request, 'New skill added')
            return redirect('account')
    context = {'form':form}
    return render(request, 'user/skillform.html', context)

@login_required(login_url='signin')
def UpdateSKill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.info(request, 'Skill Updated')
            return redirect('account')
    context = {'form':form}
    return render(request, 'user/skillform.html', context)

@login_required(login_url='signin')
def DeleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        messages.info(request, 'Skill Deleted')
        return redirect('account')
    context={'object': skill}
    return render(request, 'delete.html', context)

@login_required(login_url='signin')
def SentMessages(request):
    profile = request.user.profile
    requestedMessages = profile.allmessages.all()
    unreadMessagesCount = profile.allmessages.filter(is_read=False).count()
    context = {'requestedMessages': requestedMessages, 'unread': unreadMessagesCount}
    return render(request, 'user/inbox.html', context )
    
@login_required(login_url='signin')
def ReadMessage(request, pk):
    profile = request.user.profile
    receivedMessages = profile.allmessages.get(id=pk)
    if receivedMessages.is_read == False:
        receivedMessages.is_read = True
        receivedMessages.save()
    context = {'msg': receivedMessages}
    return render(request, 'user/message.html', context)

def MessageProfile(request, pk):
    recipient = Profile.objects.get(id = pk)
    form = MessageUserForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageUserForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = recipient
            # message.save()
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was sent successfully!')
            return redirect('profile-detail', pk=recipient.id)
    context = {'recipient': recipient, 'form':form}
    return render(request, 'user/send_message.html', context)

    