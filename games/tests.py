from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from games.models import Genre, Platform, Game, Review, Wishlist
import datetime

class GamePortalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.staff_user = User.objects.create_superuser(username='staffuser', email='staff@example.com', password='staffpassword')
        
        self.genre = Genre.objects.create(name='Aksiyon')
        self.platform = Platform.objects.create(name='PC')
        
        self.game = Game.objects.create(
            title='Test Game',
            description='This is a test description.',
            release_date=datetime.date(2026, 1, 1),
            rating_metacritic=90,
            cover_image='https://example.com/cover.jpg',
            backdrop_image='https://example.com/backdrop.jpg',
            developer='Test Developer',
            publisher='Test Publisher',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        self.game.genres.add(self.genre)
        self.game.platforms.add(self.platform)
        
        self.wishlist = Wishlist.objects.create(user=self.user)

    def test_model_creation(self):
        self.assertEqual(self.game.title, 'Test Game')
        self.assertEqual(self.game.slug, 'test-game')
        # Check YouTube video url sanitization to nocookie format
        self.assertEqual(self.game.video_url, 'https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ')
        self.assertEqual(str(self.game), 'Test Game')
        self.assertEqual(self.game.get_genres_display(), 'Aksiyon')
        self.assertEqual(self.game.get_platforms_display(), 'PC')

    def test_homepage_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/home.html')

    def test_game_detail_view(self):
        response = self.client.get(reverse('game_detail', kwargs={'slug': self.game.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/detail.html')
        self.assertContains(response, 'Test Game')

    def test_browse_catalog_view_and_pagination(self):
        # Create more games to test pagination (we set it to 6 per page)
        for i in range(10):
            Game.objects.create(
                title=f'Game {i}',
                description='Desc',
                rating_metacritic=80
            )
        response = self.client.get(reverse('browse'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/browse.html')
        # Page 1 should contain 6 games (including Test Game makes 7 total in DB, so page 1 has 6)
        self.assertEqual(len(response.context['game_list']), 6)

    def test_wishlist_functionality(self):
        # Login
        self.client.login(username='testuser', password='testpassword')
        
        # Toggle add to watchlist
        response = self.client.get(reverse('toggle_watchlist', kwargs={'game_id': self.game.id}))
        self.assertTrue(self.wishlist.games.filter(id=self.game.id).exists())
        
        # Toggle remove from watchlist
        response = self.client.get(reverse('toggle_watchlist', kwargs={'game_id': self.game.id}))
        self.assertFalse(self.wishlist.games.filter(id=self.game.id).exists())

    def test_ajax_wishlist_toggle(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('toggle_watchlist', kwargs={'game_id': self.game.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'success': True,
            'in_wishlist': True,
            'message': 'Test Game istek listenize eklendi.'
        })

    def test_review_creation_and_rating_averages(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('add_review', kwargs={'game_id': self.game.id}),
            {'text': 'Great game!', 'rating': '10'}
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(self.game.get_user_rating_average(), 10.0)

    def test_anonymous_review_creation(self):
        # Without logging in (anonymous guest)
        response = self.client.post(
            reverse('add_review', kwargs={'game_id': self.game.id}),
            {'text': 'Anonymous review!', 'rating': '8'}
        )
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertIsNone(review.user)
        self.assertEqual(self.game.get_user_rating_average(), 8.0)

    def test_logged_in_user_anonymous_review_creation(self):
        # Logged in but choosing anonymous checkbox
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('add_review', kwargs={'game_id': self.game.id}),
            {'text': 'Anonymous user review!', 'rating': '9', 'is_anonymous': 'on'}
        )
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertIsNone(review.user)
        self.assertEqual(self.game.get_user_rating_average(), 9.0)

    def test_admin_dashboard_authorization(self):
        # Non-staff user gets redirected or error
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302) # Redirect to home
        
        # Staff user succeeds
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_rest_api_list(self):
        response = self.client.get(reverse('api_game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        
    def test_rest_api_detail(self):
        response = self.client.get(reverse('api_game_detail', kwargs={'game_id': self.game.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

    def test_toggle_featured(self):
        self.client.login(username='staffuser', password='staffpassword')
        self.assertFalse(self.game.is_featured)
        
        response = self.client.get(reverse('toggle_featured', kwargs={'game_id': self.game.id}))
        self.assertEqual(response.status_code, 302)
        
        self.game.refresh_from_db()
        self.assertTrue(self.game.is_featured)
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('toggle_featured', kwargs={'game_id': self.game.id}))
        self.assertEqual(response.status_code, 302)

    def test_review_self_deletion(self):
        # Create a review owned by testuser
        review = Review.objects.create(game=self.game, user=self.user, text="My comment", rating=8)
        
        # Another user tries to delete it (should fail)
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.get(reverse('delete_review', kwargs={'review_id': review.id}))
        self.assertEqual(response.status_code, 302) # Redirect to home
        self.assertTrue(Review.objects.filter(id=review.id).exists())
        
        # The author of the review tries to delete it (should succeed)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete_review', kwargs={'review_id': review.id}))
        self.assertEqual(response.status_code, 302) # Redirect
        self.assertFalse(Review.objects.filter(id=review.id).exists())

