from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class developers(models.Model):
    dev_name = models.ForeignKey(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    experience = models.IntegerField()
    def __str__(self):
        return self.dev_name.username




class testers(models.Model):
    tester_name = models.ForeignKey(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    experience = models.IntegerField()
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.tester_name.username


class Defects_details(models.Model):
    defect_id = models.CharField(max_length=100)
    defect_name = models.CharField(max_length=100)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_defects')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_defects')
    description = models.TextField()
    defect_status = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.defect_name

class defect_screen_shorts(models.Model):
    defect = models.ForeignKey(Defects_details,on_delete=models.CASCADE)
    defect_img = models.ImageField(upload_to='defects/',blank=True,null=True)