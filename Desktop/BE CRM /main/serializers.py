from . import models
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    class_code = serializers.PrimaryKeyRelatedField(queryset=models.Class.objects.all(), many=True)
    class Meta:
        model = models.Notification
        fields = ['id','title', 'message', 'created_at', 'usercode','class_code','class_code']
    def create(self, validated_data):
        class_codes_data = validated_data.pop('class_code')
        usercode_data = validated_data.pop('usercode', None) 
        notification = models.Notification.objects.create(**validated_data)
        if class_codes_data:
            notification.class_code.set(class_codes_data)

        if usercode_data:
            notification.usercode.set(usercode_data)

        # Xử lý dữ liệu khi tạo đối tượng Notification
        return notification
        # Xử lý dữ liệu khi tạo đối tượng Notification
class TeacherSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    usercode = serializers.CharField(read_only=True)
    notifications = serializers.SerializerMethodField()
    def get_notifications(self, obj):
        notifications = models.AdminNotification.objects.filter(usercode=obj.usercode)
        notification_data = [{'title': notification.title,
                              'content': notification.content,
                              'created_at': notification.created_at.strftime("%Y-%m-%d %H:%M:%S") } for notification in notifications]
        return notification_data
    class Meta:
        model = models.Teacher
        fields = ['full_name','email','password', 'mobile','avatar','role','usercode','notifications','created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id','title','description']

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Course
#         fields = ['id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs', 'course_chapters']
#         depth = 1

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['id','course', 'title','description','video','remarks']

#Admin
class AdminSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    usercode = serializers.CharField(read_only=True)
    class Meta:
        model = models.Admin
        fields = ['full_name', 'email', 'password', 'mobile','role','usercode','avatar','created_at']

#Class
class ClassSerializer(serializers.ModelSerializer):
    notifications = serializers.SerializerMethodField()
    class Meta:
        model = models.Class
        fields = [ 'class_code', 'class_name', 'course','notifications','cost']
        depth = 1
    def get_notifications(self, obj):
        notifications = models.Notification.objects.filter(class_code=obj)
        notification_data = [{'title': notification.title,
                              'message': notification.message,
                              'created_at': notification.created_at.strftime("%Y-%m-%d %H:%M:%S") } for notification in notifications]
        return notification_data
class ClassSessionSerializer(serializers.ModelSerializer):
    schedule = serializers.PrimaryKeyRelatedField(queryset=models.Schedule.objects.all(), required=False) 
    class Meta:
        model = models.ClassSession
        fields = ['id','schedule','room', 'end_time', 'start_time','day']
def validate(self, data):
  data['schedule'] = None  
  return data

# class ManaclassSerializer(serializers.ModelSerializer):
#     class_code = serializers.StringRelatedField(source='schedule.class_code')
#     room = serializers.StringRelatedField(source='schedule.room')

#     class Meta:
#         model = models.Manaclass
#         fields = ['id', 'schedule','day', 'start_time', 'end_time', 'room', 'class_code']



class ScheduleSerializer(serializers.ModelSerializer):
    # teacher = serializers.PrimaryKeyRelatedField(queryset=models.Teacher.objects.all())
    class_sessions_set = ClassSessionSerializer(many=True)
    teacher_name = TeacherSerializer(read_only=True)
    class Meta:
        model = models.Schedule
        fields = ['id', 'teacher_code','teacher_name', 'class_code', 'num_sessions_per_course', 'num_sessions_per_week', 'start_day', 'class_sessions_set']

    def create(self, validated_data):
        class_sessions_data = validated_data.pop('class_sessions_set')  # Change this line
        schedule = models.Schedule.objects.create(**validated_data)

        # Tạo các thể hiện của ClassSession cho mỗi phần tử trong class_sessions_data
        for class_session_data in class_sessions_data:
            # Associate the ClassSession with the Schedule
            class_session = models.ClassSession.objects.create(schedule=schedule, **class_session_data)

        # Retrieve the ClassSession objects associated with the Schedule
        class_sessions_queryset = models.ClassSession.objects.filter(schedule=schedule)
         # Update the reverse relationship using set()
        schedule.class_sessions_set.set(class_sessions_queryset)
        return schedule
    def update(self, instance, validated_data):
        # Xoá tất cả ClassSession cũ
        instance.class_sessions_set.all().delete()

        # Tạo ClassSession mới từ dữ liệu cập nhật
        class_sessions_data = validated_data.pop('class_sessions_set')
        for class_session_data in class_sessions_data:
            models.ClassSession.objects.create(schedule=instance, **class_session_data)

        return super().update(instance, validated_data)

class AdminNotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.AdminNotification
        fields = '__all__'

#Parent
class StudentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    usercode = serializers.CharField(read_only=True)
    notifications = serializers.SerializerMethodField()
    AdminNotifications = serializers.SerializerMethodField()  # Corrected the case here

    def get_notifications(self, obj):
        notifications = models.Notification.objects.filter(usercode=obj)
        notification_data = [{'title': notification.title,
                              'message': notification.message,
                              'created_at': notification.created_at.strftime("%Y-%m-%d %H:%M:%S")} for notification in notifications]
        return notification_data

    def get_AdminNotifications(self, obj):
        AdminNotifications = models.AdminNotification.objects.filter(usercode=obj.usercode)
        AdminNotifications_data = [{
            'title': notification.title,
            'content': notification.content,
            'created_at': notification.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for notification in AdminNotifications]

        return AdminNotifications_data

    class Meta:
        model = models.Student
        fields = ['full_name', 'email', 'password', 'avatar', 'role', 'mobile', 'usercode',
                  'notifications', 'AdminNotifications','created_at'] 
class ParentSerializer(serializers.ModelSerializer):
    usercode = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = models.Parent
        fields = ['full_name', 'email', 'password','mobile','avatar','role','usercode','student','created_at']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    session_day = serializers.CharField(source='date.day', read_only=True)
    class Meta:
        model = models.AttendanceRecord
        fields = '__all__'
class ProFileSerializer(serializers.ModelSerializer):
    # files = serializers.ListField(
    # #     child=serializers.FileField(), required=False, write_only=True, default=[]
    # # )

    class Meta:
        model = models.ProFile
        fields = ('id', 'lesson', 'file')

    def create(self, validated_data):
        files_data = validated_data.pop("files", [])
        profile = models.ProFile.objects.create(**validated_data)

        for file_data in files_data:
            models.ProFile.objects.create(lesson=profile.lesson, file=file_data)

        return profile

    def update(self, instance, validated_data):
        # Create or update files
        files_data = validated_data.pop('files', [])
        instance.files.all().delete()

        for file_data in files_data:
            models.ProFile.objects.create(lesson=instance.lesson, file=file_data)

        return super().update(instance, validated_data)

class LessonSerializer(serializers.ModelSerializer):
    Attendance_set = AttendanceRecordSerializer(many=True,required=False,allow_null=True)
    session_day = serializers.CharField(source='class_session.day', read_only=True)
    File = ProFileSerializer(many=True,read_only=True)
    # files = serializers.ListField(
    #     child=serializers.FileField(), required=False, write_only=True,default=[]
    # )
    class Meta:
        model = models.Lesson
        fields = ('id', 'class_info', 'content', 'class_session', 'Attendance_set','session_day','File')
    def create(self, validated_data):
        attendance_set_data = validated_data.pop('Attendance_set',[])
        lesson = models.Lesson.objects.create(**validated_data)
        # Create a list to hold the AttendanceRecord instances
        attendance_records = []

        for attendance_data in attendance_set_data:
            # Associate the AttendanceRecord data with the Lesson
            attendance_data['lesson'] = lesson
            attendance_record = models.AttendanceRecord.objects.create(**attendance_data)
            attendance_records.append(attendance_record)

        # Use the set method to add the attendance records to the lesson
        lesson.Attendance_set.set(attendance_records)
        return lesson

    def update(self, instance, validated_data):
        attendance_records_data = validated_data.pop('Attendance_set', [])
        # Clear old AttendanceRecords
        instance.Attendance_set.all().delete()
        # Create or update files
        for attendance_data in attendance_records_data:
            attendance_data['lesson'] = instance
            attendance_record = models.AttendanceRecord.objects.create(**attendance_data)
            instance.Attendance_set.add(attendance_record)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Extract AttendanceRecord data from the ManyToMany field
        attendance_data = instance.Attendance_set.all()
        if attendance_data:
            # Assuming AttendanceRecord is a list of dictionaries
            representation['Attendance_set'] = AttendanceRecordSerializer(attendance_data, many=True).data
        else:
            representation['Attendance_set'] = []
        representation['content'] = representation['content'].replace('\r\n', ' ')
        return representation
class costSerializer(serializers.ModelSerializer):
    classInformation = serializers.PrimaryKeyRelatedField(queryset=models.classInformation.objects.all())

    class Meta:
        model = models.Payment
        fields = '__all__'
class classInformationSerializer(serializers.ModelSerializer):
    payment = costSerializer(many=True, required=False)

    class Meta:
        model = models.classInformation
        fields = ('Teachers', 'class_info', 'students', 'payment')

    def create(self, validated_data):
        students_data = validated_data.pop('students', [])
        payment_data = validated_data.pop('payment', [])

        class_information = models.classInformation.objects.create(**validated_data)

        # Create Payment instances associated with the classInformation using PaymentSerializer
        payment_set = []
        for payment_data_item in payment_data:
            payment_data_item['classInformation'] = class_information
            payment_instance = models.Payment.objects.create(**payment_data_item)
            payment_set.append(payment_instance)

        class_information.payment.set(payment_set)
        class_information.students.set(students_data)

        return class_information
    def update(self, instance, validated_data):
        payment_records_data = validated_data.pop('payment', [])
        instance.payment.all().delete()
        instance.class_info = validated_data.get('class_info', instance.class_info)
        for payments_data in payment_records_data:
            payments_data['classInformation'] = instance
            payment_record = models.Payment.objects.create(**payments_data)
            instance.payment.add(payment_record)
        instance.save()
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Extract AttendanceRecord data from the ManyToMany field
        payments_data = instance.payment.all()
        return representation
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.score
        fields = ['id', 'student', 'score','test_and_quiz']
class TestandQuizSerializer(serializers.ModelSerializer): 
    scores = ScoreSerializer(many=True, required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = models.TestandQuiz
        fields = ('id', 'class_info', 'quiz_name', 'scores','created_at')

    def create(self, validated_data):
        score_set_data = validated_data.pop('scores', [])
        test = models.TestandQuiz.objects.create(**validated_data)

        # Create a list to hold the score instances
        score_records = []

        for score_data in score_set_data:
            # Associate the score data with the TestandQuiz instance
            score_data['test_and_quiz'] = test
            score_record = models.score.objects.create(**score_data)
            score_records.append(score_record)

        # Use the set method to add the score records to the TestandQuiz
        test.scores.set(score_records)

        return test
    def update(self, instance, validated_data):
        score_set_data = validated_data.pop('scores', [])
        # Clear old AttendanceRecords
        instance.scores.all().delete()

        # Create new AttendanceRecord instances from the updated data
        for score_data in score_set_data:
            score_data['test_and_quiz'] = instance
            score_set_record = models.score.objects.create(**score_data)
            instance.scores.add(score_set_record)


        return super().update(instance, validated_data)
