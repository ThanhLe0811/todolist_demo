from django.db import models
from django.core import serializers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from datetime import timedelta
from django.db.models import signals
import re
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import get_default_password_validators
# Create your models here.
#Teacher Model
class Teacher(models.Model):
    usercode = models.CharField(primary_key=True,max_length=100, unique=True) #default='GV00001'
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    avatar=models.ImageField(upload_to='ava_teacher/',null=True)
    role = models.CharField(max_length=20,choices=[('teacher','Teacher')])
    notifications = models.ManyToManyField('AdminNotification', blank=True,related_name='AdminNotifications_teacher')
    def get_role(self):
        return 'teacher'
    class Meta:
        verbose_name_plural = "1. Teachers"

    def __str__(self):
        return f"{self.full_name} - {self.usercode}"

    def save(self, *args, **kwargs):
        validate_password(self.password)
        if not self.usercode:
            last_usercode = Teacher.objects.all().order_by('-usercode').first().usercode
            if last_usercode:
                last_usercode_int = int(last_usercode[2:])  # Chuyển đổi từ mã hiện tại thành số nguyên
                new_usercode_int = last_usercode_int + 1  # Tạo số nguyên mới bằng cách tăng giá trị lên 1
                new_usercode = 'GV' + str(new_usercode_int).zfill(5)  # Chuyển số nguyên thành chuỗi và thêm "GV"
            else:
                new_usercode = 'GV00001'  # Cố định mã người dùng ban đầu nếu không có bản ghi nào trong bảng

            self.usercode = new_usercode

        super().save(*args, **kwargs)
#Course model
class CourseCategory(models.Model):
    title=models.CharField(max_length=150)
    description=models.TextField()
    class Meta:
        verbose_name_plural="2. Course Categories"

    def __str__(self):
        return self.title
#Chapter Model
class Chapter(models.Model):
    title=models.CharField(max_length=150)
    description=models.TextField()
    video=models.FileField(upload_to='chapter_videos/',null=True)
    remarks=models.TextField(null=True)
    class Meta:
        verbose_name_plural="4. Chapters"
#Student Model
class Student(models.Model):
    usercode = models.CharField(primary_key=True,max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    full_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    avatar=models.ImageField(upload_to='ava_student/',null=True)
    role = models.CharField(max_length=20,choices=[('student','Student')])
    notifications = models.ManyToManyField('Notification', blank=True,related_name='notification_students')
    AdminNotifications = models.ManyToManyField('AdminNotification', blank=True,related_name='adminnotification_students')
    def get_role(self):
        return 'student'
    class Meta:
        verbose_name_plural="5. Student"
 #default='GV00001'
    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        validate_password(self.password)
        if not self.usercode:  
            last_usercode = Student.objects.all().order_by('-usercode').first().usercode
            print(last_usercode)
            if last_usercode:
                last_usercode_int = int(last_usercode[2:])  # Chuyển đổi từ mã hiện tại thành số nguyên
                new_usercode_int = last_usercode_int + 1  # Tạo số nguyên mới bằng cách tăng giá trị lên 1
                new_usercode = 'ST' + str(new_usercode_int).zfill(5)  # Chuyển số nguyên thành chuỗi và thêm "GV"
            else:
                new_usercode = 'ST00001'  # Cố định mã người dùng ban đầu nếu không có bản ghi nào trong bảng

            self.usercode = new_usercode
        super().save(*args, **kwargs)
class Admin(models.Model):
    usercode = models.CharField(primary_key=True,max_length=100,unique=True)
    full_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    avatar=models.ImageField(upload_to='ava_admin/',null=True)
    role = models.CharField(max_length=20,choices=[('admin','Admin')])
    created_at = models.DateTimeField(auto_now_add=True)
    def get_role(self):
        return 'admin'
    def save(self, *args, **kwargs):
        validate_password(self.password)
        if not self.usercode:
            last_usercode = Admin.objects.all().order_by('-usercode').first().usercode
            if last_usercode:
                last_usercode_int = int(last_usercode[2:])  # Chuyển đổi từ mã hiện tại thành số nguyên
                new_usercode_int = last_usercode_int + 1  # Tạo số nguyên mới bằng cách tăng giá trị lên 1
                new_usercode = 'AD' + str(new_usercode_int).zfill(5)  # Chuyển số nguyên thành chuỗi và thêm "GV"
            else:
                new_usercode = 'AD00001'  # Cố định mã người dùng ban đầu nếu không có bản ghi nào trong bảng

            self.usercode = new_usercode
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural="6. Admin"
    def __str__(self):
        return self.full_name
def validate_password(value):
    # Validate that the password contains at least one uppercase letter
    if not any(char.isupper() for char in value):
        raise ValidationError("The password must contain at least one uppercase letter.")

    # Validate that the password contains at least one special character
    special_characters = r"[~!@#$%^&*()_+{}[\]:;<>,.?/\|\\]"
    if not re.search(special_characters, value):
        raise ValidationError("The password must contain at least one special character.")

    # Use Django's default password validators for additional checks
    validators = get_default_password_validators()
    errors = []
    for validator in validators:
        try:
            validator.validate(value)
        except ValidationError as e:
            errors.extend(e.error_list)

    if errors:
        raise ValidationError(errors)
class Class(models.Model):
    class_code=models.CharField(max_length=100,primary_key=True)
    class_name=models.CharField(max_length=100)
    course=models.CharField(max_length=100)
    cost=models.FloatField()
    notifications = models.ManyToManyField('Notification', blank=True)
    class Meta:
        verbose_name_plural="7. Class"
    def __str__(self):
        return f"{self.class_code}" 
    
class Schedule(models.Model):
    teacher_code=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    class_code= models.ForeignKey(Class,on_delete=models.CASCADE)
    num_sessions_per_course = models.IntegerField()
    num_sessions_per_week = models.IntegerField()
    start_day = models.DateField()
    class_sessions = models.JSONField(blank=True,null=True)
    def __str__(self):
        return f"{self.class_code} "
    class Meta:
        verbose_name_plural = "8. Schedule"
class Parent(models.Model):
    usercode = models.CharField(primary_key=True,max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    avatar=models.ImageField(upload_to='ava_parent/',null=True) #default='PH00001'
    role = models.CharField(max_length=20, choices=[('parent', 'Parent')])
    notifications = models.ManyToManyField('Notification', blank=True,related_name='parent_notifications')
    AdminNotifications = models.ManyToManyField('AdminNotification', blank=True,related_name='adminnotification_parents')
    student = models.ManyToManyField(Student,blank=True)

    # Mô hình Parent liên kết với mô hình Student để biết là phụ huynh của học sinh nào
    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name_plural = "9. Parents"

    def save(self, *args, **kwargs):
        validate_password(self.password)
        if not self.usercode:
            last_usercode = Parent.objects.all().order_by('-usercode').first().usercode
            if last_usercode:
                last_usercode_int = int(last_usercode[2:])  # Chuyển đổi từ mã hiện tại thành số nguyên
                new_usercode_int = last_usercode_int + 1  # Tạo số nguyên mới bằng cách tăng giá trị lên 1
                new_usercode = 'PH' + str(new_usercode_int).zfill(5)  # Chuyển số nguyên thành chuỗi và thêm "GV"
            else:
                new_usercode = 'PH00001'  # Cố định mã người dùng ban đầu nếu không có bản ghi nào trong bảng

            self.usercode = new_usercode
        super().save(*args, **kwargs)
class ClassSession(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='class_sessions_set')
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.day} - {self.start_time} to {self.end_time}, Room: {self.room}"

    class Meta:
        verbose_name_plural = "Class Sessions"

class Notification(models.Model):
    class_code=models.ManyToManyField(Class, blank=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    usercode = models.ManyToManyField(Student,blank=True,related_name='notification_students')
    # usercode = models.ManyToManyField(Parent,blank=True, related_name='notification_parents')
    recipients_classes = models.ManyToManyField('Class', related_name='notification_recipients_classes', blank=True)
    recipients_parents = models.ManyToManyField('Parent', related_name='notification_recipients_parents', blank=True)
    recipients_students = models.ManyToManyField('Student', related_name='notification_recipients_students', blank=True)
    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']

class AdminNotification(models.Model):
    usercode = models.CharField(max_length=100,null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.usercode}"
    role = models.CharField(max_length=20, choices=[('teacher', 'Teacher'), ('student', 'Student'), ('parent', 'Parent')])

    def save(self, *args, **kwargs):
        if not self.role and self.usercode:
            self.role = self.get_role_from_usercode(self.usercode)
        super().save(*args, **kwargs)
        if self.role:
            users = Teacher.objects.filter(role=self.role)
            for user in users:
                user.notifications.add(self)

    def get_role_from_usercode(self, usercode):
        if usercode.startswith('GV'):
            return 'teacher'
        elif usercode.startswith('ST'):
            return 'student'
        elif usercode.startswith('PH'):
            return 'parent'
        else:
            return 'unknown'
class classInformation(models.Model):
    Teachers = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_info = models.OneToOneField(Class, primary_key=True, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='present_students',blank=True)
    Payment = models.JSONField(blank=True,null=True)
    def __str__(self):
        return str(self.class_info)
    class Meta:
        verbose_name_plural = "class information"
class Lesson(models.Model):
    class_info = models.ForeignKey(classInformation, on_delete=models.CASCADE)
    content = models.TextField()
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    AttendanceRecord = models.JSONField(blank=True,null=True)
    @property
    def session_day(self):
        return self.class_session.day
    def __str__(self):
        return str(self.class_info)
class AttendanceRecord(models.Model):
    date = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent')])
    lesson =  models.ForeignKey(Lesson, on_delete=models.CASCADE, editable=False,related_name='Attendance_set')
    @property
    def session_day(self):
        return self.date.day
class TestandQuiz(models.Model):
    class_info = models.ForeignKey(classInformation, on_delete=models.CASCADE,blank=True)
    quiz_name = models.CharField(max_length=100)
    score = models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.quiz_name
        
    class Meta:
         verbose_name_plural = "Test & Quiz Results"
class ProFile(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name = "File")
    file = models.FileField(upload_to="File/", default="", null=True, blank=True)
    
class score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    test_and_quiz = models.ForeignKey(TestandQuiz, on_delete=models.CASCADE,related_name='scores')
class Payment(models.Model):
    Payment=models.BooleanField()
    classInformation= models.ForeignKey(classInformation,on_delete=models.CASCADE,editable=False,related_name='payment')
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date = models.DateField(blank=True)