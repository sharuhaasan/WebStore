from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view,signup,admin_home,user_home,upload_screenshot,profile_view,points_view,task_completed

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('admin/', admin_home, name='admin_home'),
    path('user/', user_home, name='user'),
    path('screenshot/', upload_screenshot, name='screenshot'),
    path('profile/', profile_view, name='profile'),
    path('points/', points_view, name='points'),
    path('task/', task_completed, name='task'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
