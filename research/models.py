from django.db import models


class ResearchInformation(models.Model):
    class Meta:
        db_table = 'research_information'

    name = models.CharField(max_length=100, blank=True)
    number = models.CharField(max_length=10, unique=True)
    period = models.CharField(max_length=10, blank=True)
    range = models.CharField(max_length=20, blank=True)
    code = models.CharField(max_length=20, blank=True)
    institute = models.CharField(max_length=20, blank=True)
    stage = models.CharField(max_length=20, blank=True)
    target_number = models.IntegerField(blank=True)
    office = models.CharField(max_length=20, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
