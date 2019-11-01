from django.urls import path
from . import views


urlpatterns = [

    path('schedule/find_by_day/', views.find_by_name),
    path('station/all/', views.StationList.as_view()),


    # path('user/avatar/', views.ImageUploadView.as_view() )
];