
from django.contrib import admin
from.models import Candidate, Vote

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_votes']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'phone', 'mpesa_receipt', 'created_at']
    list_filter = ['candidate', 'created_at']
