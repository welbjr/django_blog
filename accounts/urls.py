from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import SignUpView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(next_page='home'), name='logout')
]
