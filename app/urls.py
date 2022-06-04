from django.urls import path

from askme.settings import DEBUG
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('vote/', views.vote, name='vote'),
    path('comment_vote/', views.comment_vote, name='comment_vote'),
    path('correct/', views.correct, name='correct'),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
