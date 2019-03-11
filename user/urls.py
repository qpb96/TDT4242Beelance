from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.login, {'template_name': 'user/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('<username>', views.view_user_profile, name='view_user_profile'),
    path('edit/<user_id>', views.edit_user_profile, name = 'edit_user_profile'),
    path('<username>/review  ', views.make_review, name='createReview'),

]
