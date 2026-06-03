from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth.models import User
from games.models import Genre, Platform, Game, Review, Wishlist
import datetime

class Command(BaseCommand):
    help = 'Seeds the database with high-quality game platform data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Eski veriler temizleniyor...')
        Review.objects.all().delete()
        Game.objects.all().delete()
        Platform.objects.all().delete()
        Genre.objects.all().delete()

        self.stdout.write('Türler ekleniyor...')
        genres_data = [
            'Aksiyon', 'Macera', 'RYG (RPG)', 'Nişancı', 'Spor', 
            'Strateji', 'Bağımsız (Indie)', 'Bulmaca', 'Yarış'
        ]
        genres = {}
        for name in genres_data:
            genre, created = Genre.objects.get_or_create(name=name)
            genres[name] = genre

        self.stdout.write('Platformlar ekleniyor...')
        platforms_data = [
            'PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch'
        ]
        platforms = {}
        for name in platforms_data:
            platform, created = Platform.objects.get_or_create(name=name)
            platforms[name] = platform

        self.stdout.write('Oyunlar ekleniyor...')
        games_list = [
            {
                'title': 'Elden Ring',
                'description': 'Elden Ring, George R. R. Martin tarafından tasarlanan fantastik bir dünyada geçen, FromSoftware imzalı aksiyon-rol yapma oyunudur. Geniş açık dünyası, zorlu düşmanları ve destansı bölüm tasarımları ile oyun dünyasında devrim yaratmıştır. Altın Düzen\'in yok oluşuyla parçalanan topraklarda, Kadim Yüzük\'ün gücünü kuşanmak ve Kadim Lord olmak için tehlikeli bir arayışa çıkın.',
                'release_date': datetime.date(2022, 2, 25),
                'rating_metacritic': 96,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1245620/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1245620/library_hero.jpg',
                'developer': 'FromSoftware',
                'publisher': 'Bandai Namco Entertainment',
                'video_url': 'https://www.youtube.com/watch?v=E3Huy2cdih0',
                'store_url': 'https://store.steampowered.com/app/1245620/ELDEN_RING/',
                'is_featured': True,
                'genres_list': ['Aksiyon', 'Macera', 'RYG (RPG)'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'Red Dead Redemption 2',
                'description': 'Rockstar Games\'ten neslin en çok alkışlanan yapımlarından biri. 1899 yılında, Amerika modernleşmeye başlarken kanun kaçakları Arthur Morgan ve Van der Linde çetesi hayatta kalmak için çalmak, yağmalamak ve savaşmak zorundadır. İçsel çelişkiler çeteyi bölme noktasına getirirken Arthur, kendi idealleri ile kendisini yetiştiren çeteye olan sadakati arasında bir seçim yapmalıdır.',
                'release_date': datetime.date(2018, 10, 26),
                'rating_metacritic': 97,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1174180/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1174180/library_hero.jpg',
                'developer': 'Rockstar Games',
                'publisher': 'Rockstar Games',
                'video_url': 'https://www.youtube.com/watch?v=RQhwEgHri1s',
                'store_url': 'https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/',
                'is_featured': True,
                'genres_list': ['Aksiyon', 'Macera'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'Cyberpunk 2077',
                'description': 'Cyberpunk 2077, güç, ihtişam ve vücut modifikasyonuna saplanıp kalmış bir megakent olan Night City\'de geçen bir aksiyon-macera rol yapma oyunudur. Şöhret ve ölümsüzlüğün anahtarı olan benzersiz bir implantın peşinden giden paralı asker V olarak oynayın. Karakterinizin siber donanımını, yeteneklerini ve oynanış tarzını özelleştirin; kararlarınızın hikayeyi ve şehri şekillendirdiği devasa bir dünyayı keşfedin.',
                'release_date': datetime.date(2020, 12, 10),
                'rating_metacritic': 86,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1091500/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1091500/library_hero.jpg',
                'developer': 'CD Projekt Red',
                'publisher': 'CD Projekt',
                'video_url': 'https://www.youtube.com/watch?v=vjF9GgrY9c0',
                'store_url': 'https://store.steampowered.com/app/1091500/Cyberpunk_2077/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'RYG (RPG)'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'The Witcher 3: Wild Hunt',
                'description': 'The Witcher 3: Wild Hunt, kararların büyük önem taşıdığı, görsel olarak göz alıcı ve hikaye odaklı bir açık dünyada geçen yeni nesil bir rol yapma oyunudur. Canavar avcısı Rivyalı Geralt olarak, dünyayı yerle bir edebileceği kehanet edilen kadim bir silahı, yani Ciri\'yi bulmak üzere amansız bir takibe çıkın.',
                'release_date': datetime.date(2015, 5, 19),
                'rating_metacritic': 93,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/292030/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/292030/library_hero.jpg',
                'developer': 'CD Projekt Red',
                'publisher': 'CD Projekt',
                'video_url': 'https://www.youtube.com/watch?v=c0i88t0Kacs',
                'store_url': 'https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/',
                'is_featured': False,
                'genres_list': ['Macera', 'RYG (RPG)'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch']
            },
            {
                'title': 'The Legend of Zelda: Tears of the Kingdom',
                'description': 'The Legend of Zelda: Breath of the Wild oyununun devamı niteliğindeki bu efsanevi macerada, gökyüzünün ötesine uzanan devasa Hyrule topraklarında kendi yolunuzu çizin. Link\'in yeni kazandığı yaratıcı yeteneklerini kullanarak garip yapılar inşa edin, bulmacaları çözün ve Hyrule krallığını tehdit eden karanlık güçlere karşı savaşın.',
                'release_date': datetime.date(2023, 5, 12),
                'rating_metacritic': 96,
                'cover_image': '/static/games/images/zelda_cover.jpg',
                'backdrop_image': '/static/games/images/zelda_backdrop.jpg',
                'developer': 'Nintendo EPD',
                'publisher': 'Nintendo',
                'video_url': 'https://www.youtube.com/watch?v=2SNF4M_v7wc',
                'store_url': 'https://www.nintendo.com/store/products/the-legend-of-zelda-tears-of-the-kingdom-switch/',
                'is_featured': True,
                'genres_list': ['Aksiyon', 'Macera'],
                'platforms_list': ['Nintendo Switch']
            },
            {
                'title': 'Hades',
                'description': 'Hades, Supergiant Games tarafından geliştirilen, rogue-like elementlerine sahip hızlı tempolu bir aksiyon hack-and-slash oyunudur. Yeraltı Dünyası\'nın asi prensi Zagreus olarak, Olimpos Tanrıları\'nın desteğiyle babanız Hades\'in pençelerinden kaçmaya ve yeryüzüne ulaşmaya çalışın. Her kaçış denemesinde yollar değişecek ve yepyeni hikaye diyalogları açılacaktır.',
                'release_date': datetime.date(2020, 9, 17),
                'rating_metacritic': 93,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1145360/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1145360/library_hero.jpg',
                'developer': 'Supergiant Games',
                'publisher': 'Supergiant Games',
                'video_url': 'https://www.youtube.com/watch?v=91t0ha9x0AE',
                'store_url': 'https://store.steampowered.com/app/1145360/Hades/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'RYG (RPG)', 'Bağımsız (Indie)'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch']
            },
            {
                'title': 'God of War Ragnarök',
                'description': 'Santa Monica Studio\'dan büyük beğeni toplayan God of War (2018)\'un devam oyunu. Fimbulwinter tüm hızıyla yaklaşırken, Kratos ve Atreus dünyayı sona erdireceği kehanet edilen savaşa hazırlanmak için Dokuz Diyar\'ın her birine seyahat etmek zorundadır. İskandinav Tanrıları ve canavarlarla yüzleşirken, aile bağları ve kader arasında bir denge kurmaya çalışacaklar.',
                'release_date': datetime.date(2022, 11, 9),
                'rating_metacritic': 94,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/2322010/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/2322010/library_hero.jpg',
                'developer': 'Santa Monica Studio',
                'publisher': 'Sony Interactive Entertainment',
                'video_url': 'https://www.youtube.com/watch?v=hfJ4Km46A-0',
                'store_url': 'https://store.playstation.com/concept/10001850/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'Macera', 'RYG (RPG)'],
                'platforms_list': ['PC', 'PlayStation 5']
            },
            {
                'title': 'Portal 2',
                'description': 'Portal 2, yenilikçi oyun mekanikleri, kara mizah dolu hikayesi ve unutulmaz karakterleri ile tüm zamanların en iyi bulmaca oyunlarından biridir. Test deneği Chell olarak, Aperture Science tesislerinde yapay zekalı GLaDOS ile yeniden karşı karşıya gelin. Portallar açın, momentum koruyarak uçun ve fizik kurallarına meydan okuyan test odalarını çözün.',
                'release_date': datetime.date(2011, 4, 18),
                'rating_metacritic': 95,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/620/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/620/library_hero.jpg',
                'developer': 'Valve',
                'publisher': 'Valve',
                'video_url': 'https://www.youtube.com/watch?v=tax4e4hBBZc',
                'store_url': 'https://store.steampowered.com/app/620/Portal_2/',
                'is_featured': False,
                'genres_list': ['Nişancı', 'Bulmaca'],
                'platforms_list': ['PC']
            },
            {
                'title': 'Grand Theft Auto V',
                'description': 'Genç bir sokak dolandırıcısı, eski bir banka soyguncusu ve acımasız bir psikopat, kendilerini yeraltı dünyasının, ABD hükümetinin ve eğlence sektörünün en korkutucu unsurlarıyla karşı karşıya bulur. Bu acımasız şehirde hayatta kalabilmek için birbirlerine güvenmekten başka çareleri yoktur; bu yüzden bir dizi tehlikeli soyguna girişirler.',
                'release_date': datetime.date(2013, 9, 17),
                'rating_metacritic': 96,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/271590/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/271590/library_hero.jpg',
                'developer': 'Rockstar North',
                'publisher': 'Rockstar Games',
                'video_url': 'https://www.youtube.com/watch?v=olEGtoYs_8A',
                'store_url': 'https://store.steampowered.com/app/271590/Grand_Target_Auto_V/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'Macera'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'Forza Horizon 5',
                'description': 'Meksika\'nın canlı ve sürekli gelişen açık dünya manzaralarında, dünyanın en iyi yüzlerce arabasıyla sınırsız, eğlenceli sürüş aksiyonuyla dolu nefes kesici maceralara liderlik edin. Horizon Festivali\'nde kendi hikayenizi yaratın, yüzlerce yarış mücadelesine katılın ve değişen mevsim koşullarının tadını çıkarın.',
                'release_date': datetime.date(2021, 11, 9),
                'rating_metacritic': 92,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1551360/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1551360/library_hero.jpg',
                'developer': 'Playground Games',
                'publisher': 'Xbox Game Studios',
                'video_url': 'https://www.youtube.com/watch?v=FYH9n37B7Yw',
                'store_url': 'https://store.steampowered.com/app/1551360/Forza_Horizon_5/',
                'is_featured': False,
                'genres_list': ['Spor', 'Yarış'],
                'platforms_list': ['PC', 'Xbox Series X']
            },
            {
                'title': 'Dark Souls III',
                'description': 'Yaktığın ateşi söndürmeye çalışan Kül Kahramanı olarak Lothric topraklarında zorlu düşmanlara, devasa boss\'lara ve karanlık bir kadere karşı mücadele et. FromSoftware\'in efsanevi aksiyon-RYG serisinin destansı finali.',
                'release_date': datetime.date(2016, 4, 12),
                'rating_metacritic': 89,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/374320/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/374320/library_hero.jpg',
                'developer': 'FromSoftware',
                'publisher': 'Bandai Namco Entertainment',
                'video_url': 'https://www.youtube.com/watch?v=_zDZYrIUgKE',
                'store_url': 'https://store.steampowered.com/app/374320/DARK_SOULS_III/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'RYG (RPG)'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'Sekiro: Shadows Die Twice',
                'description': '1500\'lerin sonlarında, Sengoku dönemi Japonya\'sında geçen ödüllü aksiyon-macera oyununda intikam arayışındaki tek kollu bir shinobi olarak onurunu geri kazan. Amansız savaş mekanikleriyle düşmanlarını alt et.',
                'release_date': datetime.date(2019, 3, 22),
                'rating_metacritic': 88,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/814380/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/814380/library_hero.jpg',
                'developer': 'FromSoftware',
                'publisher': 'Activision',
                'video_url': 'https://www.youtube.com/watch?v=7Po7INInqzE',
                'store_url': 'https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice_GOTY_Edition/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'Macera'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'Baba Is You',
                'description': 'Kuralların nesneler olarak temsil edildiği ve bunları değiştirerek oyunun gidişatını, fiziksel yasalarını baştan yazabildiğiniz devrim niteliğinde bir bulmaca oyunu. Blokları iterek kuralları değiştirin ve hedefe ulaşın.',
                'release_date': datetime.date(2019, 3, 13),
                'rating_metacritic': 87,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/736260/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/736260/library_hero.jpg',
                'developer': 'Hempuli',
                'publisher': 'Hempuli',
                'video_url': 'https://www.youtube.com/watch?v=U7MJljsoUSo',
                'store_url': 'https://store.steampowered.com/app/736260/Baba_Is_You/',
                'is_featured': False,
                'genres_list': ['Bulmaca', 'Bağımsız (Indie)'],
                'platforms_list': ['PC', 'Nintendo Switch']
            },
            {
                'title': 'Sid Meier\'s Civilization VI',
                'description': 'Taş devrinden bilgi çağına kadar zamana meydan okuyacak bir imparatorluk kurup yönetin. Tarihin en büyük liderleriyle rekabet edin veya ittifaklar kurarak dünyayı fethedin.',
                'release_date': datetime.date(2016, 10, 21),
                'rating_metacritic': 88,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/289070/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/289070/library_hero.jpg',
                'developer': 'Firaxis Games',
                'publisher': '2K',
                'video_url': 'https://www.youtube.com/watch?v=jvgAi-sQO0U',
                'store_url': 'https://store.steampowered.com/app/289070/Sid_Meiers_Civilization_VI/',
                'is_featured': False,
                'genres_list': ['Strateji'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch']
            },
            {
                'title': 'Hearts of Iron IV',
                'description': 'İkinci Dünya Savaşı\'nın kaderini belirleyin. Hearts of Iron IV, tarihin en büyük askeri çatışmasında herhangi bir ulusun liderliğini üstlenmenizi sağlar. Cephe hatlarını yönetin askeri tümenleri eğitin, endüstriyel üretim hatlarını koordine edin ve müttefiklerinizle birlikte zafere ulaşmak için en gelişmiş savaş stratejilerini devreye sokun.',
                'release_date': datetime.date(2016, 6, 6),
                'rating_metacritic': 83,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/394360/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/394360/library_hero.jpg',
                'developer': 'Paradox Development Studio',
                'publisher': 'Paradox Interactive',
                'video_url': 'https://www.youtube.com/watch?v=F-uGP2DkZKE',
                'store_url': 'https://store.steampowered.com/app/394360/Hearts_of_Iron_IV/',
                'is_featured': False,
                'genres_list': ['Strateji'],
                'platforms_list': ['PC']
            },
            {
                'title': 'Crusader Kings III',
                'description': 'Hanedanınızın şanını koruyun ve nesiller boyu hükmedin. Crusader Kings III, orta çağda geçen derinlikli bir rol yapma ve büyük strateji deneyimidir. Soylu bir ailenin lideri olarak entrikalar kurun, evlilik ittifaklarıyla topraklarınızı genişletin, din savaşlarına katılın ve tahtınızı göz diken düşmanlara karşı hanedanınızın hayatta kalmasını sağlayın.',
                'release_date': datetime.date(2020, 9, 1),
                'rating_metacritic': 91,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1158310/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1158310/library_hero.jpg',
                'developer': 'Paradox Development Studio',
                'publisher': 'Paradox Interactive',
                'video_url': 'https://www.youtube.com/watch?v=xjn66Cl3pMA',
                'store_url': 'https://store.steampowered.com/app/1158310/Crusader_Kings_III/',
                'is_featured': False,
                'genres_list': ['Strateji', 'RYG (RPG)'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'Total War: Warhammer III',
                'description': 'Karanlık Kaos güçlerine karşı dünyayı savunun veya onları yöneterek evreni ateşe verin. Total War: Warhammer III, sıra tabanlı strateji haritası ile gerçek zamanlı taktiksel savaş mekaniklerini fantastik Warhammer dünyasında birleştiren devasa bir yapımlardır. Eşsiz ırkları yönetin ve muazzam ordularla zafere ulaşın.',
                'release_date': datetime.date(2022, 2, 17),
                'rating_metacritic': 85,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1142710/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1142710/library_hero.jpg',
                'developer': 'Creative Assembly',
                'publisher': 'SEGA',
                'video_url': 'https://www.youtube.com/watch?v=HAr7yUlM0Po',
                'store_url': 'https://store.steampowered.com/app/1142710/Total_War_WARHAMMER_III/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'Strateji'],
                'platforms_list': ['PC']
            },
            {
                'title': 'Age of Empires IV',
                'description': 'Tarihi savaşlara liderlik edin ve imparatorluğunuzu kurun. Age of Empires IV, gerçek zamanlı strateji dünyasının efsanevi serisini modern grafikler ve derin oynanış mekanikleriyle geri getiriyor. İngilizler, Moğollar, Osmanlılar ve Çinliler gibi tarihin en büyük medeniyetlerini yönetin, kaleler inşa edin ve ordularınızı zafere ulaştırın.',
                'release_date': datetime.date(2021, 10, 28),
                'rating_metacritic': 81,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1466860/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/1466860/library_hero.jpg',
                'developer': 'Relic Entertainment',
                'publisher': 'Xbox Game Studios',
                'video_url': 'https://www.youtube.com/watch?v=TTaCrP_U4ao',
                'store_url': 'https://store.steampowered.com/app/1466860/Age_of_Empires_IV_Anniversary_Edition/',
                'is_featured': False,
                'genres_list': ['Strateji'],
                'platforms_list': ['PC']
            },
            {
                'title': 'Assetto Corsa Competizione',
                'description': 'Gerçekçi GT3 yarış simülasyonu. Assetto Corsa Competizione, resmi Blancpain GT Series şampiyonasının olağanüstü atmosferini deneyimlemenizi sağlıyor. Lazerle taranmış hassas pistlerde, resmi sürücüler ve takımlarla en yüksek seviye sürüş dinamiklerini tecrübe edin.',
                'release_date': datetime.date(2019, 5, 29),
                'rating_metacritic': 77,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/805550/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/805550/library_hero.jpg',
                'developer': 'Kunos Simulazioni',
                'publisher': '505 Games',
                'video_url': 'https://www.youtube.com/watch?v=CYncAnd31Q8',
                'store_url': 'https://store.steampowered.com/app/805550/Assetto_Corsa_Competizione/',
                'is_featured': False,
                'genres_list': ['Yarış', 'Spor'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X']
            },
            {
                'title': 'DOOM Eternal',
                'description': 'Cehennem orduları dünyayı istila etti. Tek kurtarıcı sizsiniz. DOOM Eternal, boyutlar arası hızlı ve acımasız birinci şahıs nişancı aksiyonunu bir üst seviyeye taşıyor. Gelişmiş silahlarınız ve Slayer yeteneklerinizle iblisleri avlayın.',
                'release_date': datetime.date(2020, 3, 20),
                'rating_metacritic': 88,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/782330/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/782330/library_hero.jpg',
                'developer': 'id Software',
                'publisher': 'Bethesda Softworks',
                'video_url': 'https://www.youtube.com/watch?v=_oVwrpfo_QA',
                'store_url': 'https://store.steampowered.com/app/782330/DOOM_Eternal/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'Nişancı'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch']
            },
            {
                'title': 'Half-Life: Alyx',
                'description': 'Sanal gerçeklik dünyasının en büyük başyapıtı. Half-Life: Alyx, Half-Life ve Half-Life 2 arasındaki dönemde Combine istilasına karşı verilen mücadeleyi konu alıyor. Çevreyle derin etkileşim, bulmacalar ve sürükleyici nişancı oynanışı.',
                'release_date': datetime.date(2020, 3, 23),
                'rating_metacritic': 93,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/546560/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/546560/library_hero.jpg',
                'developer': 'Valve',
                'publisher': 'Valve',
                'video_url': 'https://www.youtube.com/watch?v=O2W0N3uKXmo',
                'store_url': 'https://store.steampowered.com/app/546560/HalfLife_Alyx/',
                'is_featured': False,
                'genres_list': ['Aksiyon', 'Nişancı'],
                'platforms_list': ['PC']
            },
            {
                'title': 'EA SPORTS FC 24',
                'description': 'Dünya oyununun yeni dönemi. EA SPORTS FC 24, futbol simülasyonu serüvenini yepyeni bir marka ve HyperMotionV gibi devrimsel teknolojilerle sürdürüyor. Dünyanın en büyük kulüplerinde ve liglerinde gerçekçi bir futbol tecrübesine adım atın.',
                'release_date': datetime.date(2023, 9, 29),
                'rating_metacritic': 76,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/2195250/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/2195250/library_hero.jpg',
                'developer': 'EA Vancouver',
                'publisher': 'EA Sports',
                'video_url': 'https://www.youtube.com/watch?v=-vL01jbgENE',
                'store_url': 'https://store.steampowered.com/app/2195250/EA_SPORTS_FC_24/',
                'is_featured': False,
                'genres_list': ['Spor'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch']
            },
            {
                'title': 'NBA 2K24',
                'description': 'Basketbol kültürünün kalbine yolculuk yapın. NBA 2K24, geliştirilmiş oynanış mekanikleri, geçmiş ve şimdiki NBA yıldızları ile MyCAREER gibi ikonik modları bir araya getiriyor. Sahaya çıkın ve yeteneklerinizi sergileyin.',
                'release_date': datetime.date(2023, 9, 8),
                'rating_metacritic': 68,
                'cover_image': 'https://cdn.akamai.steamstatic.com/steam/apps/2338770/library_600x900.jpg',
                'backdrop_image': 'https://cdn.akamai.steamstatic.com/steam/apps/2338770/library_hero.jpg',
                'developer': 'Visual Concepts',
                'publisher': '2K',
                'video_url': 'https://www.youtube.com/watch?v=BZvwJpvEjWE',
                'store_url': 'https://store.steampowered.com/app/2338770/NBA_2K24/',
                'is_featured': False,
                'genres_list': ['Spor'],
                'platforms_list': ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch']
            }
        ]

        for g_data in games_list:
            game, created = Game.objects.get_or_create(
                title=g_data['title'],
                defaults={
                    'description': g_data['description'],
                    'release_date': g_data['release_date'],
                    'rating_metacritic': g_data['rating_metacritic'],
                    'cover_image': g_data['cover_image'],
                    'backdrop_image': g_data['backdrop_image'],
                    'developer': g_data['developer'],
                    'publisher': g_data['publisher'],
                    'video_url': g_data['video_url'],
                    'store_url': g_data['store_url'],
                    'is_featured': g_data['is_featured']
                }
            )
            for g_name in g_data['genres_list']:
                game.genres.add(genres[g_name])
            for p_name in g_data['platforms_list']:
                game.platforms.add(platforms[p_name])
            self.stdout.write(f'  Oyun eklendi: {game.title}')

        # Create a superuser and some dummy reviews if none exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Süper kullanıcı oluşturuluyor (admin / admin)...')
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Süper kullanıcı oluşturuldu.')
        
        admin_user = User.objects.get(username='admin')
        
        # Add reviews to media
        self.stdout.write('Örnek değerlendirmeler ekleniyor...')
        
        # Create dummy users for reviews variety
        dummy_users = []
        for username in ['gamer12', 'pro_gamer', 'casual_player', 'retro_fan']:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com'}
            )
            if created:
                user.set_password('password123')
                user.save()
                Wishlist.objects.get_or_create(user=user)
            dummy_users.append(user)

        import random
        review_templates = [
            ("Grafikleri harika, hikayesi insanı içine çekiyor.", 9),
            ("Mekanikler çok akıcı ama optimizasyon biraz daha iyi olabilirdi.", 8),
            ("Saatlerce sıkılmadan oynadım, kesinlikle tavsiye ederim.", 10),
            ("Fiyatını sonuna kadar hak eden muazzam bir yapım.", 10),
            ("Biraz zor ama alıştıktan sonra elinizden bırakamıyorsunuz.", 9),
            ("Beklentilerimi tam olarak karşılamadı ama yine de fena değil.", 7),
            ("Atmosferi ve müzikleri tek kelimeyle muazzam.", 9),
            ("Bazı hatalar (bug) can sıkıyor ama oynanış zevkli.", 7),
            ("Tasarım kararları çok başarılı, oynamayan çok şey kaçırır.", 9),
            ("Kendi türünün en başarılı örneklerinden biri olmuş.", 8),
            ("Düşünmeden alabilirsiniz, oynadığım en iyi oyunlardan biri.", 10),
            ("Güzel bir deneyim sunuyor ama tekrar oynanabilirliği düşük.", 6),
            ("Hikaye anlatımı zayıf kalsa da aksiyonu çok iyi.", 8),
            ("Ses tasarımları ve çevre detayları inanılmaz derecede kaliteli.", 9),
            ("Zorlayıcı bulmacaları ve oynanış tarzı ile harika bir yapıt.", 8)
        ]

        for game in Game.objects.all():
            # Add 2 to 3 reviews per game
            num_reviews = random.randint(2, 3)
            selected_templates = random.sample(review_templates, num_reviews)
            
            for text, base_rating in selected_templates:
                rating = max(1, min(10, base_rating + random.randint(-1, 1)))
                user_choice = random.choice([admin_user, None] + dummy_users)
                
                Review.objects.create(
                    game=game,
                    user=user_choice,
                    text=text,
                    rating=rating
                )

        self.stdout.write(self.style.SUCCESS('Veri ekleme işlemi başarıyla tamamlandı!'))
