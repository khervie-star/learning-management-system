from django.urls import path, re_path
from instructor import views

app_name = 'instructor'

urlpatterns = [
    #  course endpoint

    # get all course endpoint
    path('course-list/', views.CourseView.as_view(),),
    # post endpoint
    path('create-course/', views.CourseView.as_view()),
    #  get single course endpoint, patch, delete endpoint
    re_path(r'(?P<slug>[-_a-zA-Z]+)/$', views.CourseView.as_view()),

    # lesson endpoints

    # get all course endpoint
    path('lessons/<slug:lesson_slug>/', views.LessonView.as_view(),),
    # post endpoint
    path('create-lesson/', views.LessonView.as_view()),
    #  get single course endpoint, patch, delete endpoint
    re_path(r'lesson/(?P<slug>[-_a-zA-Z]+)/$', views.LessonView.as_view()),

]
