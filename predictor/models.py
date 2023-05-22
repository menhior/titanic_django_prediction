from django.db import models


class PredResults(models.Model):

    pclass = models.CharField(max_length=1,)
    isalone = models.CharField(max_length=1,)
    parch = models.CharField(max_length=20)
    sibsp = models.CharField(max_length=20)
    age = models.FloatField()
    sex = models.CharField(max_length=10)
    embarked = models.CharField(max_length=20)
    title = models.CharField(max_length=10)
    classification = models.CharField(max_length=30)

    def __str__(self):
        return self.classification
