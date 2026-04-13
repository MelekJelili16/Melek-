from django.db import models

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('TRAVAIL', 'Travail'),
        ('LOISIRS', 'Loisirs'),
        ('COURSES', 'Courses'),
        ('AUTRE', 'Autre'),
    ]
    
    PRIORITY_CHOICES = [
        ('1', 'Normale'),
        ('2', 'Urgente '),
    ]

    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='AUTRE')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='1')
    # Nouveau champ pour la date d'échéance
    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title