from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_url>/', views.tag, name='tag'),
    path('question/<int:pk>/', views.question, name='question'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('ask/', views.ask, name='ask'),
]
