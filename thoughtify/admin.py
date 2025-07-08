from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Thought, EmotionTag, UserProfile, DraftThought

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'get_anonymous_code', 'date_joined', 'last_login', 'is_staff')
    
    def get_anonymous_code(self, obj):
        try:
            return obj.userprofile.anonymous_code
        except UserProfile.DoesNotExist:
            return '-'
    get_anonymous_code.short_description = 'Anonymous Code'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ('get_author', 'content_preview', 'emotion_tag', 'sentiment', 'is_daily_thought', 'is_public', 'created_at')
    list_filter = ('emotion_tag', 'sentiment', 'is_daily_thought', 'is_public', 'created_at')
    search_fields = ('content', 'author__username', 'author__userprofile__anonymous_code')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def get_author(self, obj):
        try:
            return f"{obj.author.userprofile.anonymous_code} ({obj.author.username})"
        except (AttributeError, UserProfile.DoesNotExist):
            return obj.author.username if obj.author else 'Anonymous'
    get_author.short_description = 'Author'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new thought
            if not obj.author:
                obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(EmotionTag)
class EmotionTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)

@admin.register(DraftThought)
class DraftThoughtAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'emotion_tag', 'session_key', 'created_at')
    list_filter = ('emotion_tag', 'created_at')
    search_fields = ('content', 'session_key')
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
