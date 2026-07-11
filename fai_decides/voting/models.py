
from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200, default="Leader, people’s confidence")
    image = models.ImageField(upload_to='candidates/')

    def total_votes(self):
        return self.vote_set.count()

    def __str__(self):
        return self.name

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    amount = models.IntegerField(default=85)
    mpesa_receipt = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.name} - {self.phone}"
