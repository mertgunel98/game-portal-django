from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Platform, Game, Review, Wishlist

# Customize admin header titles
admin.site.site_header = "GamePortal Administration"
admin.site.site_title = "GamePortal Admin"
admin.site.index_title = "Oyun Portalı Yönetim Merkezi"


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('get_cover_preview', 'title', 'release_date', 'get_rating_badge', 'developer', 'is_featured')
    list_editable = ('is_featured',)
    list_filter = ('is_featured', 'genres', 'platforms', 'release_date')
    search_fields = ('title', 'developer', 'publisher', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-release_date', '-created_at')
    
    filter_horizontal = ('genres', 'platforms') # Easier ManyToMany UI
    
    # Custom CSS injection for premium dark theme styling
    class Media:
        css = {
            'all': ('games/css/custom_admin.css',)
        }

    def get_cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" class="admin-cover-preview" />', obj.cover_image)
        return format_html('<span style="color: #666;">Resim Yok</span>')
    get_cover_preview.short_description = 'Kapak'

    def get_rating_badge(self, obj):
        if obj.rating_metacritic:
            rating = obj.rating_metacritic
            if rating >= 90:
                css_class = 'rating-high'
            elif rating >= 80:
                css_class = 'rating-mid'
            else:
                css_class = 'rating-low'
            return format_html('<span class="admin-rating-badge {}">{}</span>', css_class, rating)
        return format_html('<span style="color: #999;">-</span>')
    get_rating_badge.short_description = 'Metacritic'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'get_user_display', 'get_rating_stars', 'get_text_excerpt', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('text', 'game__title', 'user__username')
    ordering = ('-created_at',)

    class Media:
        css = {
            'all': ('games/css/custom_admin.css',)
        }

    def get_user_display(self, obj):
        return obj.user.username if obj.user else format_html('<span style="color: #d946ef; font-weight: bold;">Anonim</span>')
    get_user_display.short_description = 'Kullanıcı'

    def get_rating_stars(self, obj):
        stars_filled = "★" * obj.rating
        stars_empty = "☆" * (10 - obj.rating)
        return format_html(
            '<span style="color: #fbbf24; font-size: 13px; font-weight: bold; letter-spacing: 1px;" title="{}/10">{}<span style="color: #4b5563;">{}</span></span>',
            obj.rating, stars_filled, stars_empty
        )
    get_rating_stars.short_description = 'Puan'

    def get_text_excerpt(self, obj):
        if len(obj.text) > 60:
            return obj.text[:60] + "..."
        return obj.text
    get_text_excerpt.short_description = 'Yorum Detayı'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_games_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    class Media:
        css = {
            'all': ('games/css/custom_admin.css',)
        }

    def get_games_count(self, obj):
        return obj.games.count()
    get_games_count.short_description = 'Toplam Oyun'


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_games_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    class Media:
        css = {
            'all': ('games/css/custom_admin.css',)
        }

    def get_games_count(self, obj):
        return obj.games.count()
    get_games_count.short_description = 'Toplam Oyun'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_games_count')
    search_fields = ('user__username',)

    class Media:
        css = {
            'all': ('games/css/custom_admin.css',)
        }

    def get_games_count(self, obj):
        return obj.games.count()
    get_games_count.short_description = 'İstek Listesindeki Oyunlar'
