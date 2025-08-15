from django.contrib import admin
from defects.models import Defects_details,developers,testers,defect_screen_shorts


# Register your models here.
admin.site.register(Defects_details)
admin.site.register(developers)
admin.site.register(testers)
admin.site.register(defect_screen_shorts)