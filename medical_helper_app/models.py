from django.db import models
from django.contrib.auth.models import User



class Drug(models.Model):
    name = models.CharField( max_length=255, unique=True)

    def __str__(self):
        return self.name



class Dosage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    starting_dose = models.DecimalField(max_digits=5, decimal_places=2)
    min_dose = models.DecimalField(max_digits=5, decimal_places=2)
    max_dose = models.DecimalField(max_digits=5, decimal_places=2)
    elderly_dose = models.DecimalField(max_digits=5, decimal_places=2)
    other_adjustments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.drug.name} - Dosage"

class SideEffect(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    effect_description = models.TextField()
    probability = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.drug.name} - Side Effect"

class Theme(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    content = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return f"{self.drug.name} - Note"
