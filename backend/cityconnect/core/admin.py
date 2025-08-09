from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Report, Task, Redemption, News
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


from .models import IssuePost, Like, Comment,SavedPost

admin.site.register(IssuePost)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(SavedPost)
