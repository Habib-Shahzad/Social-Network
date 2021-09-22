
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('posts', views.posts, name='posts'),
    path("addpost", views.addpost, name='addpost'),
    path('addlike/<int:id>', views.addlike, name='addlike'),
    path('likes', views.likes, name='likes'),
    path('profile/<str:name>', views.profile, name='profile'),
    path('follow/<str:name>/<int:boo>', views.follow, name='follow'),
    path('followed/<str:name>', views.followed, name='followed'),
    path('following', views.following, name='following'),
    path('posts/<int:ID>', views.getpost, name='getpost'),
    path('edit/<int:ID>', views.edit, name='edit'),
    path('getpage', views.getpage, name='getpage'),
    path('numpagesP', views.numpagesP, name='numpagesP'),
    path('numpagesF', views.numpagesF, name='numpagesF'),
    path('numpagesU/<str:name>', views.numpagesU, name='numpagesU'),
    path('getfollow/<str:name>', views.getfollow, name='getfollow')
]
