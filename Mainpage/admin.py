from django.contrib import admin
from Mainpage.models import *

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date']



admin.site.register(Query)
admin.site.register(JobApplication)
admin.site.register(Vacancy)
admin.site.register(News)
admin.site.register(Event)
admin.site.register(AlertRegistration)
admin.site.register(AlertMade)
admin.site.register(EstimateImageGallery)
admin.site.register(EstimateCategory)
admin.site.register(CostRates)
admin.site.register(UserFeedback)
admin.site.register(UserIssueReport)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'meta_description', 'created_at')
    search_fields = ('name', 'meta_description')