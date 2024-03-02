from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import TeacherSerializer,CategorySerializer,ChapterSerializer,AdminSerializer,ClassSerializer,ScheduleSerializer,StudentSerializer,ParentSerializer,NotificationSerializer,AdminNotificationSerializer,classInformationSerializer,AttendanceRecordSerializer,LessonSerializer,ClassSessionSerializer,TestandQuizSerializer,ScoreSerializer,costSerializer,ProFileSerializer
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from . import models
import json
from django.utils import timezone
# Create your views here.
class TeacherList(generics.ListCreateAPIView):
        # authentication_classes = [TokenAuthentication]
        queryset=models.Teacher.objects.all()
        serializer_class = TeacherSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['full_name', 'email','usercode']
        # permission_classes=[permissions.IsAuthenticated]
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Teacher.objects.all()
        serializer_class = TeacherSerializer
        # permission_classes=[permissions.IsAuthenticated]
@csrf_exempt
def teacher_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    print(f'Email: {email}, Password: {password}')

    try:
        teacherData = models.Teacher.objects.get(email=email, password=password)
    except models.Teacher.DoesNotExist:
        teacherData = None
    if teacherData:
        return JsonResponse({'bool': True, 'teacher_usercode': teacherData.usercode})
    else:
        return JsonResponse({'bool': False})
class CategoryList(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.CourseCategory.objects.all()
        serializer_class = CategorySerializer
        # permission_classes=[permissions.IsAuthenticated]

#Course
# class CourseList(generics.ListCreateAPIView):
#         # authentication_classes = [SessionAuthentication, BasicAuthentication]
#         queryset=models.Course.objects.all()
#         serializer_class = CourseSerializer
#         # permission_classes=[permissions.IsAuthenticated]
#         def get_queryset(self):
#                 qs=super().get_queryset()
#                 if 'result' in self.request.GET:
#                         limit=int(self.request.GET['result'])
#                         qs=models.Course.objects.all().order_by('-id')[:limit]
#                 return qs
# class CourseDetailView(generics.RetrieveAPIView):
#         # authentication_classes = [SessionAuthentication, BasicAuthentication]
#         queryset=models.Course.objects.all()
#         serializer_class = CourseSerializer
#         # permission_classes=[permissions.IsAuthenticated]
# Specific Teacher Course
class TeacherCourseList(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        # permission_classes=[permissions.IsAuthenticated]
        def get_queryset(self):
                teacher_id=self.kwargs['teacher_id']
                teacher=models.Teacher.objects.get(pk=teacher_id)
                return models.Course.objects.filter(teacher=teacher)
# # Specific Teacher Course
class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        pass
        # permission_classes=[permissions.IsAuthenticated]
#Chapter List
class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Chapter.objects.all()
        serializer_class = ChapterSerializer
        # permission_classes=[permissions.IsAuthenticated]

class CourseChapterList(generics.ListAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        serializer_class = ChapterSerializer
        # permission_classes=[permissions.IsAuthenticated]
        def get_queryset(self):
                course_id=self.kwargs['course_id']
                course=models.Course.objects.get(pk=course_id)
                return models.Chapter.objects.filter(course=course)

#Admin

class AdminList(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Admin.objects.all()
        serializer_class = AdminSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['full_name', 'email','usercode']
        # permission_classes=[permissions.IsAuthenticated]

class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Admin.objects.all()
        serializer_class = AdminSerializer
        # permission_classes=[permissions.IsAuthenticated]

@csrf_exempt
def admin_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    print(f'Email: {email}, Password: {password}')

    try:
        adminData = models.Admin.objects.get(email=email, password=password)
    except models.Admin.DoesNotExist:
        adminData = None
    if adminData:
        return JsonResponse({'bool': True, 'admin_usercode': adminData.usercode})
    else:
        return JsonResponse({'bool': False})
#Parents
class ParentsList(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Parent.objects.all()
        serializer_class = ParentSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['full_name', 'email','usercode']
        # permission_classes=[permissions.IsAuthenticated]

class ParentDetail(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Parent.objects.all()
        serializer_class = ParentSerializer
        # permission_classes=[permissions.IsAuthenticated]

@csrf_exempt
def parent_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    print(f'Email: {email}, Password: {password}')

    try:
        parentData = models.Parent.objects.get(email=email, password=password)
    except models.Parent.DoesNotExist:
        parentData = None
    if parentData:
        return JsonResponse({'bool': True, 'parent_usercode': parentData.usercode})
    else:
        return JsonResponse({'bool': False})
class ClassList(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Class.objects.all()
        serializer_class = ClassSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['class_code', 'class_name','course']
        # permission_classes=[permissions.IsAuthenticated]
class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Class.objects.all()
        serializer_class = ClassSerializer
        # permission_classes=[permissions.IsAuthenticated]
class ScheduleList(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        serializer_class = ScheduleSerializer
        queryset=models.Schedule.objects.all()
@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        # Nhận dữ liệu từ request
        data = json.loads(request.body)

        # In tất cả dữ liệu nhận được từ request
        for key, value in data.items():
            print(f"{key}: {value}")

        # Tạo Schedule mới
        schedule = models.Schedule.objects.create(**data)
        print(JsonResponse(schedule.serialize()))

        return JsonResponse(schedule.serialize(), status=201)
    else:
        return JsonResponse({}, status=405)
class ScheduleRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Schedule.objects.all()
    serializer_class = ScheduleSerializer
class StudentList(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Student.objects.all()
        serializer_class = StudentSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['full_name', 'email','usercode']
        # permission_classes=[permissions.IsAuthenticated]
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.Student.objects.all()
        serializer_class = StudentSerializer
@csrf_exempt
def student_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    print(f'Email: {email}, Password: {password}')

    try:
        studentData = models.Student.objects.get(email=email, password=password)
    except models.Student.DoesNotExist:
        studentData = None
    if studentData:
        return JsonResponse({'bool': True, 'student_usercode': studentData.usercode})
    else:
        return JsonResponse({'bool': False})

#CalendarClass

# class ManaclassList(generics.ListCreateAPIView):
#         # authentication_classes = [SessionAuthentication, BasicAuthentication]
#         queryset=models.Manaclass.objects.all()
#         serializer_class = ManaclassSerializer
#         # permission_classes=[permissions.IsAuthenticated]

# class ManaclassDetail(generics.RetrieveUpdateDestroyAPIView):
#         # authentication_classes = [SessionAuthentication, BasicAuthentication]
#         queryset=models.Manaclass.objects.all()
#         serializer_class = ManaclassSerializer
#         # permission_classes=[permissions.IsAuthenticated]
    

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'message']

class NotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = NotificationSerializer

class AdminNotificationListCreateView(generics.ListCreateAPIView):
    queryset = models.AdminNotification.objects.all()
    serializer_class = AdminNotificationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id','title', 'content']

class AdminNotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AdminNotification.objects.all()
    serializer_class = AdminNotificationSerializer

class classInformation(generics.ListCreateAPIView):
    queryset = models.classInformation.objects.all()
    serializer_class = classInformationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['Teachers', 'class_info','students']

class classInformationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.classInformation.objects.all()
    serializer_class = classInformationSerializer
class AttendacneRecord(generics.ListCreateAPIView):
    queryset = models.AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer

class AttendacneRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
class Lesson(generics.ListCreateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer
@csrf_exempt
def create_lesson(request):
    if request.method == 'POST':
        # Nhận dữ liệu từ request
        data = json.loads(request.body)

        # In tất cả dữ liệu nhận được từ request
        for key, value in data.items():
            print(f"{key}: {value}")

        # Tạo lesson mới
        serializer = LessonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({}, status=405)
class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer
class ClassSession(generics.ListCreateAPIView):
    queryset = models.ClassSession.objects.all()
    serializer_class = ClassSessionSerializer

class ClassSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
class TestandQuiz(generics.ListCreateAPIView):
    queryset = models.TestandQuiz.objects.all()
    serializer_class = TestandQuizSerializer

class TestandQuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestandQuiz.objects.all()
    serializer_class = TestandQuizSerializer
class Score(generics.ListCreateAPIView):
    queryset = models.score.objects.all()
    serializer_class = ScoreSerializer

class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.score.objects.all()
    serializer_class = ScoreSerializer
class cost(generics.ListCreateAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = costSerializer

class FileDetail(generics.ListCreateAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.ProFile.objects.all()
        serializer_class = ProFileSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['lesson__id']
class FileListDetail(generics.RetrieveUpdateDestroyAPIView):
        # authentication_classes = [SessionAuthentication, BasicAuthentication]
        queryset=models.ProFile.objects.all()
        serializer_class = ProFileSerializer