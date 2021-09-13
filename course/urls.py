from django.urls import path, re_path
from course import views

app_name = 'course'

urlpatterns = [
    #  course endpoint

    # get all course endpoint
    path('course-list/', views.CourseView.as_view(),),
    # post endpoint
    path('create/course/', views.CourseView.as_view()),
    #  get single course endpoint, patch, delete endpoint
    re_path(r'course/(?P<slug>[-_a-zA-Z]+)/$', views.CourseView.as_view()),

    # lesson endpoints

    # get a  single lesson instance
    path('lesson/<slug:lesson_slug>/', views.LessonView.as_view()),

    # post endpoint
    path('create/lesson/', views.LessonView.as_view()),
    # get all lessons associated to a course
    re_path(r'lessons/(?P<related_course_slug>[-_a-zA-Z]+)/$', views.LessonView.as_view()),


    # content endpoints
    path('create/content/text/', views.create_text_content, ),
    # [get, delete, update]
    path('content/text/<int:id>/', views.get_edit_delete_text_content, ),

    # course enrollments
    path('enroll', views.course_enrollment),

]
