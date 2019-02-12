from django.db import models

# Create your models here.

class Company(models.Model):
    c_id = models.IntegerField(verbose_name="公司id", primary_key=True, null=False)
    name = models.CharField(null=False, max_length=255)
    content = models.TextField(verbose_name="公司介绍", name="context", null=True, blank=True)
    addressCountry = models.CharField(max_length=255, null=True, blank=True)
    addressLocality = models.CharField(max_length=255, null=True, blank=True)
    addressRegion = models.CharField(max_length=255, null=True, blank=True)
    numberOfEmployees = models.CharField(max_length=32, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    font_page = models.CharField(max_length=255, null=True, blank=True)
    page = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.c_id)

class User(models.Model):
    u_id = models.IntegerField(verbose_name="用户ID", primary_key=True, null=False)
    name = models.CharField(null=False, max_length=64)
    title = models.CharField(null=True, max_length=64, blank=True)
    bio = models.CharField(null=True, max_length=255, blank=True)
    workfor = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.u_id)
    
class Job(models.Model):
    name = models.CharField(max_length=255, null=False)
    typeof = models.CharField(max_length=16, name="type")
    working_place = models.CharField(max_length=255, null=True, blank=True)
    classof = models.CharField(max_length=255, name="class", null=True, blank=True)
    salary = models.CharField(max_length=128, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    workfor = models.ForeignKey("Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name