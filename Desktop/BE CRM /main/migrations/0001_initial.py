# Generated by Django 5.0 on 2024-01-06 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Admin",
            fields=[
                (
                    "usercode",
                    models.CharField(
                        max_length=100, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("full_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("mobile", models.CharField(max_length=100)),
                ("avatar", models.ImageField(null=True, upload_to="ava_admin/")),
                ("role", models.CharField(choices=[("admin", "Admin")], max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "6. Admin",
            },
        ),
        migrations.CreateModel(
            name="AdminNotification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("usercode", models.CharField(max_length=100, null=True)),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("teacher", "Teacher"),
                            ("student", "Student"),
                            ("parent", "Parent"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Chapter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("video", models.FileField(null=True, upload_to="chapter_videos/")),
                ("remarks", models.TextField(null=True)),
            ],
            options={
                "verbose_name_plural": "4. Chapters",
            },
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "class_code",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("class_name", models.CharField(max_length=100)),
                ("course", models.CharField(max_length=100)),
                ("cost", models.FloatField()),
            ],
            options={
                "verbose_name_plural": "7. Class",
            },
        ),
        migrations.CreateModel(
            name="ClassSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("room", models.CharField(blank=True, max_length=100)),
            ],
            options={
                "verbose_name_plural": "Class Sessions",
            },
        ),
        migrations.CreateModel(
            name="CourseCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name_plural": "2. Course Categories",
            },
        ),
        migrations.CreateModel(
            name="TestandQuiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quiz_name", models.CharField(max_length=100)),
                ("score", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Test & Quiz Results",
            },
        ),
        migrations.CreateModel(
            name="classInformation",
            fields=[
                (
                    "class_info",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="main.class",
                    ),
                ),
                ("Payment", models.JSONField(blank=True, null=True)),
            ],
            options={
                "verbose_name_plural": "class information",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("AttendanceRecord", models.JSONField(blank=True, null=True)),
                (
                    "class_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.classsession",
                    ),
                ),
                (
                    "class_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.classinformation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("class_code", models.ManyToManyField(blank=True, to="main.class")),
                (
                    "recipients_classes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="notification_recipients_classes",
                        to="main.class",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="class",
            name="notifications",
            field=models.ManyToManyField(blank=True, to="main.notification"),
        ),
        migrations.CreateModel(
            name="Parent",
            fields=[
                (
                    "usercode",
                    models.CharField(
                        max_length=100, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("full_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("mobile", models.CharField(max_length=100)),
                ("avatar", models.ImageField(null=True, upload_to="ava_parent/")),
                (
                    "role",
                    models.CharField(choices=[("parent", "Parent")], max_length=20),
                ),
                (
                    "AdminNotifications",
                    models.ManyToManyField(
                        blank=True,
                        related_name="adminnotification_parents",
                        to="main.adminnotification",
                    ),
                ),
                (
                    "notifications",
                    models.ManyToManyField(
                        blank=True,
                        related_name="parent_notifications",
                        to="main.notification",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "9. Parents",
            },
        ),
        migrations.AddField(
            model_name="notification",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.parent",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="recipients_parents",
            field=models.ManyToManyField(
                blank=True,
                related_name="notification_recipients_parents",
                to="main.parent",
            ),
        ),
        migrations.CreateModel(
            name="ProFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True, default="", null=True, upload_to="File/"
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="File",
                        to="main.lesson",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("num_sessions_per_course", models.IntegerField()),
                ("num_sessions_per_week", models.IntegerField()),
                ("start_day", models.DateField()),
                ("class_sessions", models.JSONField(blank=True, null=True)),
                (
                    "class_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.class"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "8. Schedule",
            },
        ),
        migrations.AddField(
            model_name="classsession",
            name="schedule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="class_sessions_set",
                to="main.schedule",
            ),
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "usercode",
                    models.CharField(
                        max_length=100, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("full_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("mobile", models.CharField(max_length=100)),
                ("avatar", models.ImageField(null=True, upload_to="ava_student/")),
                (
                    "role",
                    models.CharField(choices=[("student", "Student")], max_length=20),
                ),
                (
                    "AdminNotifications",
                    models.ManyToManyField(
                        blank=True,
                        related_name="adminnotification_students",
                        to="main.adminnotification",
                    ),
                ),
                (
                    "notifications",
                    models.ManyToManyField(
                        blank=True,
                        related_name="notification_students",
                        to="main.notification",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "5. Student",
            },
        ),
        migrations.AddField(
            model_name="parent",
            name="student",
            field=models.ManyToManyField(blank=True, to="main.student"),
        ),
        migrations.AddField(
            model_name="notification",
            name="recipients_students",
            field=models.ManyToManyField(
                blank=True,
                related_name="notification_recipients_students",
                to="main.student",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="usercode",
            field=models.ManyToManyField(
                blank=True, related_name="notification_students", to="main.student"
            ),
        ),
        migrations.CreateModel(
            name="AttendanceRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_present",
                    models.CharField(
                        choices=[("present", "Present"), ("absent", "Absent")],
                        max_length=20,
                    ),
                ),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.classsession",
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Attendance_set",
                        to="main.lesson",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.student"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "usercode",
                    models.CharField(
                        max_length=100, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("full_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("mobile", models.CharField(max_length=100)),
                ("avatar", models.ImageField(null=True, upload_to="ava_teacher/")),
                (
                    "role",
                    models.CharField(choices=[("teacher", "Teacher")], max_length=20),
                ),
                (
                    "notifications",
                    models.ManyToManyField(
                        blank=True,
                        related_name="AdminNotifications_teacher",
                        to="main.adminnotification",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "1. Teachers",
            },
        ),
        migrations.AddField(
            model_name="schedule",
            name="teacher_code",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.teacher"
            ),
        ),
        migrations.CreateModel(
            name="score",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.FloatField()),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.student"
                    ),
                ),
                (
                    "test_and_quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scores",
                        to="main.testandquiz",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="testandquiz",
            name="class_info",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.classinformation",
            ),
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Payment", models.BooleanField()),
                ("date", models.DateField(blank=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.student"
                    ),
                ),
                (
                    "classInformation",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment",
                        to="main.classinformation",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="classinformation",
            name="Teachers",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.teacher"
            ),
        ),
        migrations.AddField(
            model_name="classinformation",
            name="students",
            field=models.ManyToManyField(
                blank=True, related_name="present_students", to="main.student"
            ),
        ),
    ]
