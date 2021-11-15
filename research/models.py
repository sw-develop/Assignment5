from django.db   import models

class ResearchInformation(models.Model): 

    class Meta: 
        db_table = 'research_informations'

    name          = models.CharField(max_length=100)
    number        = models.CharField(max_length=10, unique=True)
    period        = models.CharField(max_length=10, blank=True)
    range         = models.CharField(max_length=20)
    code          = models.CharField(max_length=20)
    institute     = models.CharField(max_length=20)
    stage         = models.CharField(max_length=20)
    target_number = models.IntegerField()
    office        = models.CharField(max_length=20)
    created_at    = models.DateField(auto_now_add=True)
    updated_at    = models.DateField(auto_now=True)