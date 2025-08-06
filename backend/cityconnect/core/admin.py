from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Report, Task, Redemption, News


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'eco_coins', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')
    list_filter = ('status',)
    search_fields = ('title',)
    fields = ('title', 'description', 'category', 'status', 'admin_feedback', 'user', 'image')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task_type', 'is_verified')
    fields = ('user', 'task_type', 'proof_image', 'is_verified', 'admin_feedback')


@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_name', 'coins_spent', 'status', 'requested_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'item_name')
    readonly_fields = ('requested_at',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'created_by__username')
    readonly_fields = ('created_at',)
