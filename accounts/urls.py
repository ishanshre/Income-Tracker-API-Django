from django.urls import path
from accounts import views
app_name = 'accounts'


urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
]


