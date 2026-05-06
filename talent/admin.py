from django.contrib import admin

from talent.models import TalentMedia, TalentPortfolio

# Register your models here.
admin.site.register(TalentPortfolio)
admin.site.register(TalentMedia)