from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Teacher
    path('teacher/notifications/', views.NotificationListCreateView.as_view(), name='notification-list'),
    path('teacher/notifications/<int:pk>/', views.NotificationRetrieveUpdateDestroyView.as_view(), name='notification-detail'),
    path("teacher/", views.TeacherList.as_view()),
    path("teacher/<str:pk>/", views.TeacherDetail.as_view()),
    path("teacher-login", views.teacher_login),
    #Admin
    path('admin/notifications/', views.AdminNotificationListCreateView.as_view()),
    path('admin/notifications/<int:pk>/', views.AdminNotificationRetrieveUpdateDestroyView.as_view()),
    path("admin/", views.AdminList.as_view()),
    path("admin/<str:pk>/", views.AdminDetail.as_view()),
    path("admin-login", views.admin_login),
    # Student
    path("student/", views.StudentList.as_view()),
    path("student/<str:pk>/", views.StudentDetail.as_view()),
    path("student-login", views.student_login),
    # parents
    path("parent/", views.ParentsList.as_view()),
    path("parent/<str:pk>/", views.ParentDetail.as_view()),
    path("parent_login", views.parent_login),
    #Class
    path("class/", views.ClassList.as_view()),
    path("class/<str:pk>/", views.ClassDetail.as_view()),
    #CalendarClass
    # path("Manaclass/", views.ManaclassList.as_view()),
    # path("Manaclass/<int:pk>/", views.ManaclassDetail.as_view()),
    #Schedule
    path("schedule/", views.ScheduleList.as_view()),
    path("schedule/<int:pk>/", views.ScheduleRetrieveView.as_view()),
    path("Schedule/", views.create_schedule),
    # Category
    path("category/", views.CategoryList.as_view()),
    #course
    # path("course/", views.CourseList.as_view()),
    # #course Detail view
    # path("course/<int:pk>/", views.CourseDetailView.as_view()),
    #Chapter
    path("chapter/<int:pk>", views.ChapterDetailView.as_view()),
    #Specific Course Chapter
    path("course-chapters/<int:course_id>", views.CourseChapterList.as_view()),
    # Teacher course
    path("teacher-course/<int:teacher_id>", views.TeacherCourseList.as_view()),
    #course Detail
    path("teacher-course-detail/<int:pk>", views.TeacherCourseDetail.as_view()),
    #Attendance
    path("class-information/", views.classInformation.as_view()),
    path("class-information/<str:pk>/", views.classInformationDetail.as_view()),
    path("attendancerecord/", views.AttendacneRecord.as_view()),
    path("attendancerecord/<int:pk>/", views.AttendacneRecordDetail.as_view()),
    path("lesson-content/", views.Lesson.as_view()),
    path("lesson-content/<int:pk>/", views.LessonDetail.as_view()),
    path("class-session/", views.ClassSession.as_view()),
    path("class-session/<int:pk>/", views.ClassSessionDetail.as_view()),
    path("test/", views.TestandQuiz.as_view()),
    path("test/<int:pk>/", views.TestandQuizDetail.as_view()),
    path("score/", views.Score.as_view()),
    path("score/<int:pk>/", views.ScoreDetail.as_view()),
    path("cost/", views.cost.as_view()),
    path("file/", views.FileDetail.as_view()),
    path("file/<int:pk>/", views.FileListDetail.as_view()),
   

]   