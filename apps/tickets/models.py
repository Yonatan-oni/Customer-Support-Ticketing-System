from django.db import models

class Priorities(models.TextChoices):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Status(models.TextChoices):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resloved"

# Create your models here.
class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    ticketTitle = models.CharField(max_length=255)
    ticketDescription = models.TextField()
    priority = models.CharField(max_length=10, choices=Priorities)
    status = models.CharField(max_length=20, choices=Status, default="Open") 
    senderName = models.CharField(max_length=30)
    senderEmail = models.EmailField()
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
