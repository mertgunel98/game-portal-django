import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from .models import Genre, Platform, Game, Review, Wishlist

def home(request):
    """Render the landing page with featured, trending, and latest games."""
    featured_games = Game.objects.filter(is_featured=True)
    trending_games = Game.objects.order_by('-rating_metacritic')[:8]
    latest_games = Game.objects.order_by('-release_date')[:8]
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    
    # Selected hero game for home header backdrop
    hero = featured_games.first() if featured_games.exists() else Game.objects.first()

    context = {
        'hero': hero,
        'featured_games': featured_games,
        'trending_games': trending_games,
        'latest_games': latest_games,
        'genres': genres,
        'platforms': platforms,
    }
    return render(request, 'games/home.html', context)

def game_detail(request, slug):
    """Display detailed specifications, embedded trailers, and reviews for a single game."""
    game = get_object_or_404(Game, slug=slug)
    reviews = game.reviews.all().select_related('user')
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        in_wishlist = wishlist.games.filter(id=game.id).exists()
    
    # Recommendations based on sharing similar genres
    recommendations = Game.objects.filter(genres__in=game.genres.all()).exclude(id=game.id).distinct()[:4]
    
    context = {
        'game': game,
        'reviews': reviews,
        'genres': genres,
        'platforms': platforms,
        'in_wishlist': in_wishlist,
        'recommendations': recommendations,
    }
    return render(request, 'games/detail.html', context)

def browse(request):
    """Handle catalog browsing with dynamic filtering, sorting, and pagination."""
    game_list = Game.objects.all()
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    
    # Filters
    query = request.GET.get('q')
    genre_slug = request.GET.get('genre')
    platform_slug = request.GET.get('platform')
    min_rating = request.GET.get('rating')
    sort_by = request.GET.get('sort')

    if query:
        game_list = game_list.filter(
            Q(title__icontains=query) | 
            Q(developer__icontains=query) | 
            Q(publisher__icontains=query) |
            Q(description__icontains=query)
        )
        
    if genre_slug:
        game_list = game_list.filter(genres__slug=genre_slug)
        
    if platform_slug:
        game_list = game_list.filter(platforms__slug=platform_slug)
        
    if min_rating:
        try:
            game_list = game_list.filter(rating_metacritic__gte=int(min_rating))
        except ValueError:
            pass
            
    # Sorting
    if sort_by == 'rating':
        game_list = game_list.order_by('-rating_metacritic')
    elif sort_by == 'title':
        game_list = game_list.order_by('title')
    else:  # default 'latest'
        game_list = game_list.order_by('-release_date')

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(game_list, 6)  # 6 games per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'game_list': page_obj,
        'page_obj': page_obj,
        'genres': genres,
        'platforms': platforms,
        'selected_genre': genre_slug,
        'selected_platform': platform_slug,
        'selected_rating': min_rating,
        'selected_sort': sort_by,
        'search_query': query,
    }
    return render(request, 'games/browse.html', context)

@login_required
def watchlist_view(request):
    """Display the logged-in user's saved wishlist games and personal reviews."""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    game_list = wishlist.games.all()
    my_reviews = Review.objects.filter(user=request.user).select_related('game')
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    
    context = {
        'game_list': game_list,
        'my_reviews': my_reviews,
        'genres': genres,
        'platforms': platforms,
    }
    return render(request, 'games/watchlist.html', context)

@login_required
def toggle_watchlist(request, game_id):
    """AJAX-compatible view to add/remove a game to/from the user's wishlist."""
    from django.http import JsonResponse
    game = get_object_or_404(Game, id=game_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    in_wishlist = False
    
    if wishlist.games.filter(id=game.id).exists():
        wishlist.games.remove(game)
        message = f"{game.title} istek listenizden kaldırıldı."
        if not is_ajax:
            messages.success(request, message)
    else:
        wishlist.games.add(game)
        in_wishlist = True
        message = f"{game.title} istek listenize eklendi."
        if not is_ajax:
            messages.success(request, message)
            
    if is_ajax:
        return JsonResponse({
            'success': True,
            'in_wishlist': in_wishlist,
            'message': message
        })
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def add_review(request, game_id):
    """Create or update a game review, supporting anonymous submissions."""
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        
        try:
            rating = int(rating)
            if 1 <= rating <= 10 and text:
                # Check if it should be anonymous
                is_anonymous = not request.user.is_authenticated or request.POST.get('is_anonymous') == 'on'
                
                if is_anonymous:
                    Review.objects.create(
                        game=game,
                        user=None,
                        text=text,
                        rating=rating
                    )
                    messages.success(request, "Değerlendirmeniz anonim olarak başarıyla kaydedildi.")
                else:
                    # Update review if already reviewed, or create new
                    Review.objects.update_or_create(
                        game=game,
                        user=request.user,
                        defaults={'text': text, 'rating': rating}
                    )
                    messages.success(request, "Değerlendirmeniz başarıyla kaydedildi.")
            else:
                messages.error(request, "Lütfen geçerli bir puan (1-10) ve yorum girin.")
        except (ValueError, TypeError):
            messages.error(request, "Değerlendirme sırasında bir hata oluştu.")
            
    return redirect('game_detail', slug=game.slug)

def auth_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wishlist.objects.create(user=user)  # Create empty wishlist
            login(request, user)
            messages.success(request, f"Kayıt başarılı! Hoş geldiniz, {user.username}.")
            return redirect('home')
    else:
        form = UserCreationForm()
        
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    return render(request, 'games/signup.html', {'form': form, 'genres': genres, 'platforms': platforms})

def auth_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Create wishlist if it was somehow missing
            Wishlist.objects.get_or_create(user=user)
            messages.success(request, f"Giriş yapıldı. Tekrar hoş geldiniz, {user.username}!")
            return redirect(request.GET.get('next', 'home'))
    else:
        form = AuthenticationForm()
        
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    return render(request, 'games/login.html', {'form': form, 'genres': genres, 'platforms': platforms})

def auth_logout(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yapıldı.")
    return redirect('home')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Bu sayfaya erişim yetkiniz bulunmamaktadır.")
        return redirect('home')
        
    all_games = Game.objects.all().prefetch_related('genres', 'platforms')
    all_reviews = Review.objects.all().select_related('game', 'user')
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    
    context = {
        'all_games': all_games,
        'all_reviews': all_reviews,
        'genres': genres,
        'platforms': platforms,
    }
    return render(request, 'games/admin_dashboard.html', context)

@login_required
def add_game(request):
    if not request.user.is_staff:
        messages.error(request, "Bu işlemi gerçekleştirme yetkiniz bulunmamaktadır.")
        return redirect('home')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_date_str = request.POST.get('release_date')
        rating_metacritic = request.POST.get('rating_metacritic')
        cover_image = request.POST.get('cover_image')
        backdrop_image = request.POST.get('backdrop_image')
        developer = request.POST.get('developer')
        publisher = request.POST.get('publisher')
        video_url = request.POST.get('video_url')
        store_url = request.POST.get('store_url')
        is_featured = request.POST.get('is_featured') == 'on'
        
        genres_ids = request.POST.getlist('genres')
        platforms_ids = request.POST.getlist('platforms')
        
        release_date = None
        if release_date_str:
            try:
                release_date = datetime.datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        try:
            rating = int(rating_metacritic) if rating_metacritic else 0
        except ValueError:
            rating = 0
            
        if title and description:
            # Check slug unique
            slug = slugify(title)
            original_slug = slug
            counter = 1
            while Game.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
                
            game = Game.objects.create(
                title=title,
                slug=slug,
                description=description,
                release_date=release_date,
                rating_metacritic=rating,
                cover_image=cover_image,
                backdrop_image=backdrop_image,
                developer=developer,
                publisher=publisher,
                video_url=video_url,
                store_url=store_url,
                is_featured=is_featured
            )
            
            # Add relationships
            game.genres.set(genres_ids)
            game.platforms.set(platforms_ids)
            
            messages.success(request, f"{game.title} oyunu başarıyla eklendi.")
        else:
            messages.error(request, "Lütfen en azından Oyun Başlığı ve Açıklamasını doldurun.")
            
    return redirect('admin_dashboard')

@login_required
def delete_game(request, game_id):
    if not request.user.is_staff:
        messages.error(request, "Bu işlemi gerçekleştirme yetkiniz bulunmamaktadır.")
        return redirect('home')
        
    game = get_object_or_404(Game, id=game_id)
    title = game.title
    game.delete()
    messages.success(request, f"{title} oyunu veritabanından silindi.")
    return redirect('admin_dashboard')

@login_required
def toggle_featured(request, game_id):
    if not request.user.is_staff:
        messages.error(request, "Bu işlemi gerçekleştirme yetkiniz bulunmamaktadır.")
        return redirect('home')
        
    game = get_object_or_404(Game, id=game_id)
    game.is_featured = not game.is_featured
    game.save()
    
    if game.is_featured:
        messages.success(request, f"{game.title} oyunu vitrin listesine eklendi.")
    else:
        messages.success(request, f"{game.title} oyunu vitrin listesinden kaldırıldı.")
        
    return redirect('admin_dashboard')

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    # Check if user is staff OR the owner of the review
    if not request.user.is_staff and review.user != request.user:
        messages.error(request, "Bu işlemi gerçekleştirme yetkiniz bulunmamaktadır.")
        return redirect('home')
        
    game_slug = review.game.slug
    review.delete()
    messages.success(request, "Yorum başarıyla silindi.")
    
    # Redirect back to where it was deleted from
    referer = request.META.get('HTTP_REFERER', '')
    if 'admin-dashboard' in referer:
        return redirect('admin_dashboard')
    if 'watchlist' in referer:
        return redirect('wishlist')
    return redirect('game_detail', slug=game_slug)

from django.http import JsonResponse

def api_game_list(request):
    games = Game.objects.all().prefetch_related('genres', 'platforms')
    data = []
    for game in games:
        data.append({
            'id': game.id,
            'title': game.title,
            'slug': game.slug,
            'description': game.description,
            'release_date': game.release_date.strftime('%Y-%m-%d') if game.release_date else None,
            'rating_metacritic': game.rating_metacritic,
            'cover_image': game.cover_image,
            'backdrop_image': game.backdrop_image,
            'developer': game.developer,
            'publisher': game.publisher,
            'video_url': game.video_url,
            'store_url': game.store_url,
            'is_featured': game.is_featured,
            'genres': [genre.name for genre in game.genres.all()],
            'platforms': [platform.name for platform in game.platforms.all()]
        })
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def api_game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    data = {
        'id': game.id,
        'title': game.title,
        'slug': game.slug,
        'description': game.description,
        'release_date': game.release_date.strftime('%Y-%m-%d') if game.release_date else None,
        'rating_metacritic': game.rating_metacritic,
        'cover_image': game.cover_image,
        'backdrop_image': game.backdrop_image,
        'developer': game.developer,
        'publisher': game.publisher,
        'video_url': game.video_url,
        'store_url': game.store_url,
        'is_featured': game.is_featured,
        'genres': [genre.name for genre in game.genres.all()],
        'platforms': [platform.name for platform in game.platforms.all()],
        'user_rating_average': game.get_user_rating_average(),
        'reviews': [
            {
                'id': review.id,
                'user': review.user.username if review.user else 'Anonim',
                'text': review.text,
                'rating': review.rating,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for review in game.reviews.all().select_related('user')
        ]
    }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
