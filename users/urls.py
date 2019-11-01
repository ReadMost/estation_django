from django.urls import path
from . import views

app_name = 'user_api'
urlpatterns = [
    path('passenger/signin/', views.signin),
    path('passenger/signup/', views.passenger_signup),
    path('employee/signup/', views.employee_signup),
    # path('employee/signin/', views.passenger_signup),


    # path('user/avatar/', views.ImageUploadView.as_view() )
];