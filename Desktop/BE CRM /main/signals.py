# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Teacher, Student, Parent, AdminNotification
from django.utils import timezone

@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=Parent)
def create_notification(sender, instance, created, **kwargs):
    if created:
        usercode = instance.usercode
        role = None
        if usercode.startswith('GV'):
            role = 'teacher'
        elif usercode.startswith('ST'):
            role = 'student'
        elif usercode.startswith('PH'):
            role = 'parent'