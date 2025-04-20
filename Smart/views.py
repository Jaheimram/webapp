from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import TodoItem
from .models import Post
from .models import FAQ 
from .models import CaseStudyZip
from .forms import TodoItemForm
from django.conf import settings
from .utils.case_study_loader import get_case_studies
from .models import TeamMember

import os


# Create your views here.
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def todos(request):
    # Get todos for logged-in user only, ordered by creation date
    todos = TodoItem.objects.filter(user=request.user).order_by('-created_at')
    
    # Handle form submission
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todos')
    else:
        form = TodoItemForm()
    
    return render(request, "todos.html", {
        'todos': todos,
        'form': form,
        'active_tab': 'todos'  # For highlighting active tab
    })

@login_required
def toggle_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todos')

@login_required
def delete_todo(request, pk):
    get_object_or_404(TodoItem, pk=pk, user=request.user).delete()
    return redirect('todos')

def create(request):
    return render(request, "create.html")

def post_list(request):
    posts = Post.objects.all()  # Retrieve all posts
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Retrieve a single post by its primary key
    return render(request, 'blog/post_detail.html', {'post': post})

def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    return render(request, 'faq/faq_list.html', {'faqs': faqs})


def case_study_list(request):
    # Get all uploaded ZIP files
    zip_files = CaseStudyZip.objects.all()
    
    # Get all extracted PDFs
    pdf_files = []
    case_studies_dir = os.path.join(settings.MEDIA_ROOT, 'case_studies')
    
    if os.path.exists(case_studies_dir):
        for case_id in os.listdir(case_studies_dir):
            case_dir = os.path.join(case_studies_dir, case_id)
            if os.path.isdir(case_dir):
                for filename in os.listdir(case_dir):
                    if filename.lower().endswith('.pdf'):
                        pdf_files.append({
                            'name': filename,
                            'url': os.path.join(settings.MEDIA_URL, 'case_studies', case_id, filename),
                            'zip_id': case_id
                        })
    
    return render(request, 'case_studies/list.html', {
        'zip_files': zip_files,
        'pdf_files': pdf_files
    })

def case_study_detail(request, case_id, filename):
    # Verify the file exists
    file_path = os.path.join(settings.MEDIA_ROOT, 'case_studies', case_id, filename)
    if not os.path.exists(file_path):
        return render(request, '404.html', status=404)
    
def contact(request):
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    
    # Preserve your existing contact page context
    context = {
        'team_members': team_members,
        # Add any other existing context variables you had
        'page_title': 'Contact Us',
        # ... your other existing context ...
    }
    return render(request, 'contact.html', context)
    
    return render(request, 'case_studies/detail.html', {
        'pdf_url': os.path.join(settings.MEDIA_URL, 'case_studies', case_id, filename),
        'filename': filename
    })