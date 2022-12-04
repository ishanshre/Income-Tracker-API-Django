from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView
app_name = 'accounts'


urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path("email-verify", views.EmailVerify.as_view(), name="email_verify"),
]

