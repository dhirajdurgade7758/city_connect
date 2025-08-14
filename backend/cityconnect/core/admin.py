from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task, News, IssuePost, Like, Comment, SavedPost, UserBadge
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'area')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Eco System'), {'fields': ('eco_coins',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'role', 'area', 'eco_coins'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'eco_coins', 'area', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'area')
    ordering = ('username',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'task_type', 'is_verified', 'initial_eco_coins', 'verified_eco_coins', 'total_eco_coins_awarded', 'submitted_at')
    list_filter = ('is_verified', 'task_type')
    search_fields = ('user__username', 'title', 'description', 'task_type')
    fields = ('user', 'title', 'description', 'task_type', 'proof_image', 'is_verified', 'admin_feedback', 'initial_eco_coins', 'verified_eco_coins', 'total_eco_coins_awarded')
    readonly_fields = ('submitted_at', 'initial_eco_coins', 'verified_eco_coins', 'total_eco_coins_awarded')

    actions = ['verify_selected_tasks']

    def verify_selected_tasks(self, request, queryset):
        for task in queryset:
            if not task.is_verified:
                task.award_additional_eco_coins()
        self.message_user(request, "Selected tasks have been verified and EcoCoins awarded.")
    verify_selected_tasks.short_description = "Verify selected tasks and award additional EcoCoins"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'created_by__username')
    readonly_fields = ('created_at',)


# Admin for IssuePost model
@admin.register(IssuePost)
class IssuePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'area', 'department', 'status', 'likes_count', 'comments_count', 'created_at') # Added 'department'
    list_filter = ('status', 'area', 'department', 'created_at') # Added 'department'
    search_fields = ('title', 'description', 'location_details', 'user__username')
    readonly_fields = ('likes_count', 'comments_count', 'created_at', 'updated_at')
    actions = ['mark_in_progress', 'mark_resolved']
    fieldsets = ( # Reorganized fieldsets for better clarity
        (None, {
            'fields': ('user', 'title', 'description', 'image')
        }),
        ('Location & Department', {
            'fields': ('area', 'location_details', 'department') # Grouped location and department
        }),
        ('Status & Counts', {
            'fields': ('status', 'likes_count', 'comments_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, "Selected issue posts marked as 'In Progress'.")
    mark_in_progress.short_description = "Mark selected as In Progress"

    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved')
        self.message_user(request, "Selected issue posts marked as 'Resolved'.")
    mark_resolved.short_description = "Mark selected as Resolved"



@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('timestamp',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'post__title', 'text')
    readonly_fields = ('timestamp', 'updated_at')

@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('saved_at',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_name', 'badge_type', 'unlocked_at')
    list_filter = ('badge_type',)
    search_fields = ('user__username', 'badge_name')
    readonly_fields = ('unlocked_at',)
