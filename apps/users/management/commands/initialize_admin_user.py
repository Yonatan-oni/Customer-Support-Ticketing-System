from django.core.management.base import BaseCommand
from apps.users.models import User

class Command(BaseCommand):

    help = 'Initialize Admin User'

    def handle(self, *args, **kwargs):
        admin = User.objects.filter(email="leulsegedyonatan@gmail.com").first()
        if admin is None:
            user = User(
            name="Yonatan",
            email="leulsegedyonatan@gmail.com",
            role="Admin"
            )
            user.set_password("123456") 
            user.save()
            self.stdout.write(self.style.SUCCESS('Admin Account Created'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin Account Already Exists'))