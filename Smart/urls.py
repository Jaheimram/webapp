from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from .views import faq_list, case_study_list, case_study_detail
from .views import todos, toggle_todo, delete_todo 

urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('todos/', todos, name='todos'),
    path('todos/<int:pk>/toggle/', toggle_todo, name='toggle_todo'),
    path('todos/<int:pk>/delete/', delete_todo, name='delete_todo'),
    path("create/", views.create, name="create"),  # Create page
    path('posts/', views.post_list, name='post_list'),  # List of all posts
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),  # Detail view for a single postt
    path('faq/', faq_list, name='faq'),
    path('case-studies/', case_study_list, name='case_study_list'),
    path('case-studies/<str:case_id>/<str:filename>/', case_study_detail, name='case_study_detail'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 