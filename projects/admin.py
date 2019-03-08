from django.contrib import admin

from .models import Project, PromotedProject, PromotionSettings, Task, TaskFile, Delivery, ProjectCategory, Team, TaskFileTeam


class TaskInline(admin.TabularInline):
    model = Task
    verbose_name_plural = 'Tasks'

class ProjectAdmin(admin.ModelAdmin):
    inlines = (TaskInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return super(ProjectAdmin, self).get_inline_instances(request, obj)
        return list()

class PromotedProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'start', 'end')
    fieldsets = [
        (None,                      {'fields': ['id']}),
        ("Project details",         {'fields': ['project']}),
    ]

class PromotionSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pool_size', 'display_amount', 'duration_in_days','promotion_fee')

admin.site.register(Project, ProjectAdmin)
admin.site.register(PromotionSettings, PromotionSettingsAdmin)
admin.site.register(PromotedProject, PromotedProjectAdmin)
admin.site.register(Task)
admin.site.register(TaskFile)
admin.site.register(Delivery)
admin.site.register(ProjectCategory)
admin.site.register(Team)
admin.site.register(TaskFileTeam)
