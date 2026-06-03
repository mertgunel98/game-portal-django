import urllib.request
import urllib.error
import json

candidates = {
    'EU4 (Xy4gM0Tz40c)': 'Xy4gM0Tz40c',
    'EU4 (k241hYt194U)': 'k241hYt194U',
    'EU5 (v3vM-J-W8q0)': 'v3vM-J-W8q0',
    'EU5 (8u1m_oX2n1M)': '8u1m_oX2n1M',
    'HoI4 (kU765r4B3XQ)': 'kU765r4B3XQ',
    'HoI4 (kY3E7QJ7x-w)': 'kY3E7QJ7x-w',
    'HoI4 (kU8Y33d5f4g)': 'kU8Y33d5f4g',
    'CK3 (0V5_3kLpW0M)': '0V5_3kLpW0M',
    'CK3 (-Uo7j_S0H3k)': '-Uo7j_S0H3k',
    'TW:W3 (S-t14_T5F-w)': 'S-t14_T5F-w',
    'TW:W3 (kYI_d1n3u_o)': 'kYI_d1n3u_o',
    'AoE4 (o68x-q8xT4Y)': 'o68x-q8xT4Y',
    'AoE4 (Q_3cM0Kz3Gk)': 'Q_3cM0Kz3Gk'
}

for name, video_id in candidates.items():
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"OK: {name} - Title: '{data.get('title')}'")
    except urllib.error.HTTPError as e:
        print(f"FAILED: {name} - HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"ERROR: {name} - {str(e)}")
