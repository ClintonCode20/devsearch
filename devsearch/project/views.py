from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

# Create your views here.
def IndexView(request):
    search_query = ''

# Building Search Bar 
    if request.GET.get('text'):
        search_query = request.GET.get('text')
    tags = Tag.objects.filter(name__icontains = search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains = search_query) | 
    Q(owner__name__icontains = search_query) |
    Q(description__icontains = search_query) |
    Q(tags__in = tags))


# Page Pagination
    page = request.GET.get('page')
    num = 3
    paginator = Paginator(projects, num)

    try:
        projects = paginator.page(page)
    
    except PageNotAnInteger: 
        page = 1
        projects = paginator.page(page)
    
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)


        


    context = {'projects':projects, 'search_query': search_query, "paginator": paginator}
    return render(request, 'project/index.html', context)

def DetailView(request, pk):
    project = Project.objects.get(id = pk)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.getVoteCount
            messages.info(request, 'Your review was added successfully')
            return redirect('detailview', pk = project.id)
    context = {'project': project, 'review_form': review_form}
    return render(request, 'project/project-detail.html', context)

def CreateProject(request):
    profile = request.user.profile
    form = ProjectForm(request.FILES)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'project/create_project.html', context)


def UpdateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form, 'project':project}
    return render(request, 'project/create_project.html', context)


def DeleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    if request.method == 'POST':
        project.delete()
        return redirect('index')
    context = {'object': project}
    return render(request, 'delete.html', context)

