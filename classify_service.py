#!/usr/bin/env python3
"""
Clean Service Pattern classification for APIs.
Uses positive keyword scoring + category defaults so nothing falls to Other.
"""
import json

with open('/home/terexitarius/free-api-catalog/apis.json') as f:
    catalog = json.load(f)

apis = catalog['apis']

# Category -> default pattern mapping (every category has a home)
cat_default = {
    'weather': 'Dynamic Data',
    'cryptocurrency': 'Dynamic Data',
    'finance': 'Dynamic Data',
    'sports & fitness': 'Dynamic Data',
    'news': 'Dynamic Data',
    'tracking': 'Dynamic Data',
    'environment': 'Dynamic Data',
    'open data': 'Other',  # Falls through to keyword scan
    
    'geocoding': 'Geospatial',
    'transportation': 'Geospatial',
    
    'email': 'Communication',
    'social': 'Communication',
    
    'security': 'Analytics',
    
    'development': 'Service',
    'data validation': 'Service',
    'url shorteners': 'Service',
    'productivity': 'Service',
    'authentication & authorization': 'Service',
    
    'government': 'Government',
    
    'test data': 'Testing/Mock',
    
    'machine learning': 'AI/ML',
    
    'video': 'Content',
    'books': 'Content',
    'anime': 'Content',
    'games & comics': 'Content',
    'music': 'Content',
    'food & drink': 'Content',
    'animals': 'Content',
    'personality': 'Content',
    'entertainment': 'Content',
    'arts & design': 'Content',
    'photography': 'Content',
    
    'currency exchange': 'Financial',
    
    'health': 'Reference',
    'calendar': 'Reference',
    'business': 'Reference',
    'education': 'Reference',
    'science & math': 'Reference',
    'jobs': 'Reference',
    'phone': 'Reference',
}

# Positive keyword overrides (can upgrade from category default)
keyword_pattern = {
    'Service': [
        'qr code', 'qr-code', 'url shortener', 'shorten url', 'url ms',
        'lorem ipsum', 'fake data', 'dummy data', 'placeholder',
        'generator', 'create ', 'conversion', 'converter', 'compress ',
        'watermark', 'background removal', 'background rem',
        'paraphrase', 'summarize', 'pdf generat', 'invoice parser',
        'text-to-speech', 'speech to text', 'color palette',
        'gradient', 'vector', 'illustration', 'diagram',
        'password generator', 'uuid generator', 'short id',
    ],
    'Dynamic Data': [
        'real-time', 'real time', 'live data', 'live score',
        'weather', 'forecast', 'stock price', 'market data', 'ticker',
        'crypto price', 'bitcoin price', 'coin price',
        'news', 'headline', 'air quality', 'pollution',
        'flight status', 'train status', 'bus status', 'arrival', 'departure',
        'carbon intensity', 'solar irradiance',
        'standings', 'match result', 'game result', 'betting odds',
        'iss location', 'people in space', 'radar',
    ],
    'Communication': [
        'email', 'mail', 'smtp', 'sms', 'messaging',
        'notification', 'webhook',
        'discord', 'telegram', 'slack', 'whatsapp',
        'linkedin', 'reddit', 'tiktok', 'facebook', 'twitter',
        'instagram', 'social media', 'post ', 'publish', 'comment',
    ],
    'Analytics': [
        'monitor', 'tracking', 'metric', 'analytics', 'logging',
        'threat detection', 'vulnerability', 'malware', 'phishing',
        'reputation', 'risk scoring', 'fraud', 'abuse',
        'health check', 'uptime', 'status page',
    ],
    'AI/ML': [
        'machine learning', 'ai model', 'neural network',
        'text analysis', 'sentiment analysis',
        'object detection', 'face recognition',
        'named entity', 'tokenization', 'nlp',
    ],
    'Testing/Mock': [
        'mock api', 'fake endpoint', 'test data', 'sandbox',
        'echo server', 'httpbin', 'reqres', 'postman echo',
        'prototype', 'stub', 'testing api',
    ],
    'Geospatial': [
        'map ', 'geocoding', 'routing', 'navigation',
        'latitude', 'longitude', 'elevation', 'gis',
        'geolocation', 'address lookup', 'gps',
    ],
    'Government': [
        'census', 'federal', 'legislation', 'regulation',
        'patent', 'trademark', 'fbi', 'fema', 'epa',
        'police', 'criminal',
    ],
    'Financial': [
        'payment', 'transaction', 'trading', 'exchange', 'broker',
    ],
}

def classify(api):
    name = api.get('name', '').lower()
    desc = api.get('description', '').lower()
    cat = api.get('category', '').lower()
    text = f"{name} {desc} {cat}"
    
    # Check keyword matches first (can upgrade from category default)
    best_pattern = None
    best_score = 0
    for pattern, keywords in keyword_pattern.items():
        score = sum(3 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_pattern = pattern
    
    # If keywords found, use that
    if best_score > 0:
        return best_pattern
    
    # Fall back to category default
    return cat_default.get(cat, 'Reference')

# Classify
for api in apis:
    api['service_pattern'] = classify(api)

from collections import Counter
counts = Counter(a.get('service_pattern', 'Other') for a in apis)

print("Service Pattern distribution:")
for p, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {p}: {c}")

# Verify
print("\n=== VERIFICATION ===")
checks = [
    ('CoinGecko API', 'Dynamic Data'),
    ('Binance', 'Dynamic Data'),
    ('WeatherStack', 'Dynamic Data'),
    ('eBird', 'Content'),
    ('Motivational API', 'Content'),
    ('Gutenberg', 'Content'),
    ('TheMealDB', 'Content'),
    ('Nager.Date', 'Reference'),
    ('QR code', 'Service'),
    ('URL', 'Service'),
    ('JSONPlaceholder', 'Testing/Mock'),
    ('Twitter', 'Communication'),
    ('Finnhub', 'Dynamic Data'),
    ('FRED', 'Dynamic Data'),
    ('ExchangeRate', 'Financial'),
    ('OpenStreetMap', 'Geospatial'),
    ('FBI Wanted', 'Government'),
]

for name, expected in checks:
    matches = [a for a in apis if name.lower() in a['name'].lower()]
    for m in matches[:2]:
        status = "OK" if m.get('service_pattern') == expected else "MISMATCH"
        print(f"  {status} {m['name']}: {m.get('service_pattern')} (expected: {expected})")

# Save
catalog['service_patterns'] = dict(sorted(counts.items(), key=lambda x: -x[1]))
with open('/home/terexitarius/free-api-catalog/apis.json', 'w') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Write pattern files
import os
os.makedirs('/home/terexitarius/free-api-catalog/patterns', exist_ok=True)
by_pattern = {}
for a in apis:
    p = a.get('service_pattern', 'Reference')
    if p not in by_pattern:
        by_pattern[p] = []
    by_pattern[p].append(a)

for pattern, pattern_apis in sorted(by_pattern.items()):
    fname = pattern.lower().replace('/','_').replace(' ','_').replace('-','_').replace('#','')
    with open(f'/home/terexitarius/free-api-catalog/patterns/{fname}.json', 'w') as f:
        json.dump(pattern_apis, f, indent=2, ensure_ascii=False)

print(f"\nWrote {len(by_pattern)} pattern files to patterns/")
