from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Genre(models.Model):
    """Model representing game categories/genres (e.g. Action, RPG, Strategy)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Platform(models.Model):
    """Model representing game runtime environments/platforms (e.g. PC, PS5)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Game(models.Model):
    """Model representing game records with rich metadata, covers, and trailer URLs."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    rating_metacritic = models.PositiveIntegerField(default=0, help_text="Metacritic rating (0-100)")
    
    # Image URLs for box art and banner backgrounds
    cover_image = models.URLField(max_length=500, blank=True, help_text="Box art/Poster image URL")
    backdrop_image = models.URLField(max_length=500, blank=True, help_text="Hero backdrop image URL")
    
    genres = models.ManyToManyField(Genre, related_name='games')
    platforms = models.ManyToManyField(Platform, related_name='games')
    developer = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    
    video_url = models.URLField(max_length=500, blank=True, help_text="YouTube embed URL for official trailer")
    store_url = models.URLField(max_length=500, blank=True, help_text="Steam, Epic, Store link")
    
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Convert standard YouTube, Vimeo, or Dailymotion URLs to embed URLs
        if self.video_url:
            import re
            
            # YouTube
            yt_pattern = r'(?:youtu\.be/|v/|u/\w/|embed/|watch\?v=|&v=)([^#&?]+)'
            yt_match = re.search(yt_pattern, self.video_url)
            if yt_match:
                video_id = yt_match.group(1)
                self.video_url = f"https://www.youtube-nocookie.com/embed/{video_id}"
            
            # Vimeo
            elif "vimeo.com" in self.video_url:
                vimeo_pattern = r'vimeo\.com/(?:video/)?([0-9]+)'
                vimeo_match = re.search(vimeo_pattern, self.video_url)
                if vimeo_match:
                    video_id = vimeo_match.group(1)
                    self.video_url = f"https://player.vimeo.com/video/{video_id}"
            
            # Dailymotion
            elif "dailymotion.com" in self.video_url or "dai.ly" in self.video_url:
                dm_pattern = r'(?:dailymotion\.com/video/|dai\.ly/)([a-zA-Z0-9]+)'
                dm_match = re.search(dm_pattern, self.video_url)
                if dm_match:
                    video_id = dm_match.group(1)
                    self.video_url = f"https://www.dailymotion.com/embed/video/{video_id}"
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_genres_display(self):
        return ", ".join([genre.name for genre in self.genres.all()])

    def get_platforms_display(self):
        return ", ".join([platform.name for platform in self.platforms.all()])

    def get_user_rating_average(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    class Meta:
        ordering = ['-release_date', '-created_at']

class Review(models.Model):
    """Model representing user rating and text review comments for games."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reviews', null=True, blank=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=10, help_text="Rating on a scale of 1-10")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        username = self.user.username if self.user else "Anonim"
        return f"{username} on {self.game.title} ({self.rating}/10)"

class Wishlist(models.Model):
    """Model representing a user's bookmarked games list (watchlist)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    games = models.ManyToManyField(Game, blank=True, related_name='wishlist_users')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
