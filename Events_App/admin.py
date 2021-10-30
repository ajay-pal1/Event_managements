from django.contrib import admin
from .models import Event,EventJoined

# Register your models here.
    
class EventAdmin(admin.ModelAdmin):
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
      obj.creator = request.user
      obj.creator_id = request.user.id
      obj.last_modified_by = request.user
      obj.save()
      super().save_model(request, obj, form, change)   

admin.site.register(Event, EventAdmin)
admin.site.register(EventJoined)


