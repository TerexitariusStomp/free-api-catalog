#!/usr/bin/env python3
"""
Clean, simple functional pattern classification.
Each API gets ONE pattern based on its primary function.
"""
import json, os

with open('/home/terexitarius/free-api-catalog/apis.json') as f:
    catalog = json.load(f)

apis = catalog['apis']

# ===== PATTERN DEFINITIONS =====
# Each pattern = (positive_keywords, priority_category_defaults)
PATTERNS = {
    'Service': [
        # Things that CREATE, GENERATE, TRANSFORM, or OPERATE on input
        'qr code', 'qr-code', 'url shortener', 'url shortening', 'shorten url',
        'url ms', 'link shortener', 'short link',
        'color palette', 'color generator', 'gradient', 'color converter',
        'lorem ipsum', 'fake data', 'dummy data', 'placeholder', 'mock data',
        'generate', 'generator', 'created', 'creation', 'create',
        'convert ', 'converter', 'compression', 'compress ',
        'watermark', 'background removal', 'resiz', 'crop',
        'paraphrase', 'summarize', 'summarize', 'pdf creation',
        'text-to-speech', 'speech to text', 'word cloud',
        'password ', 'uuid ', 'hash', 'encrypt', 'decrypt',
        'screenshot', 'pdf generation', 'invoice ',
        'translation', 'translate ', 'ocr', 'object recognition',
        'vector', 'svg', 'illustration', 'diagram',
    ],
    'Dynamic Data': [
        # Regularly or real-time updated data feeds
        'weather', 'forecast', 'meteorological', 'climate', 'meteo',
        'stock price', 'market data', 'ticker', 'stockmarket', 'trading data',
        'bitcoin price', 'crypto price', 'exchange rate', 'currency rate',
        'news', 'headline', 'article feed', 'rss feed',
        'air quality', 'pollution', 'pm2.5',
        'flight status', 'flight tracking', 'train status', 'bus status',
        'arrival', 'departure', 'delay', 'schedule',
        'score', 'standings', 'match result', 'game score', 'live score',
        'betting odds', 'live odds',
        'real-time', 'real time', 'live data', 'live ',
        'carbon intensity', 'grid load', 'energy',
        'iss location', 'people in space', 'radar',
        'seismic', 'earthquake', 'tsunami',
    ],
    'Platform': [
        # APIs for managing/posting to external platforms
        'manage ', 'update ', 'delete resource', 'create ', 'crud',
        'dashboard', 'board', 'project management',
        'cms', 'wordpress', 'drupal', 'jira', 'notion',
        'airtable', 'clickup', 'trello', 'asana',
        'shopify', 'woocommerce', 'magento',
        'inventory', 'order', 'fulfillment',
        'crm', 'salesforce', 'hubspot',
        'create issue', 'create post', 'publish post',
        'user management', 'manage users', 'manage content',
    ],
    'Communication': [
        # Sending/receiving messages
        'email', 'mail', 'smtp', 'sms', 'messaging', 'chat ', 'chat bot',
        'notification', 'push notification', 'webhook',
        'discord', 'telegram', 'slack', 'whatsapp', 'signal',
        'twitter', 'tweet', 'facebook', 'linkedin', 'instagram',
        'post ', 'publish', 'share', 'comment', 'social media',
        'call ', 'phone', 'sip', 'voip',
    ],
    'Geospatial': [
        # Location-based services
        'map ', 'map api', 'geocoding', 'geocode', 'reverse geocode',
        'routing', 'navigation', 'direction', 'gps',
        'latitude', 'longitude', 'coordinate',
        'elevation', 'altitude', 'topography',
        'public transport', 'transit', 'bus', 'train', 'subway', 'metro',
        'address lookup', 'geolocation', 'geo location',
        'gis',
    ],
    'Analytics': [
        # Monitoring, scanning, metrics
        'monitor', 'monitoring', 'tracking', 'metric', 'analytics',
        'logging', 'observability', 'health check', 'uptime', 'status page',
        'threat detection', 'vulnerability', 'malware', 'phishing',
        'reputation', 'fraud', 'abuse', 'risk scoring',
        'scan ', 'scanner', 'audit',
    ],
    'AI/ML': [
        # Machine learning and AI
        'machine learning', 'ai model', 'deep learning', 'neural',
        'text analysis', 'sentiment analysis', 'classification model',
        'face recognition', 'object detection', 'image recognition',
        'language model', 'tokenization', 'named entity', 'nlp',
        'recommendation engine', 'prediction model', 'forecast model',
    ],
    'Government': [
        # Official public data
        'census', 'government', 'federal', 'national statistics',
        'legislation', 'regulation', 'patent', 'trademark', 'copyright',
        'fbi', 'fema', 'epa', 'noaa', 'nasa', 'usda',
        'police', 'criminal', 'compliance',
        'public record', 'official data',
    ],
    'Testing': [
        # Mock/testing endpoints
        'mock', 'fake endpoint', 'test data', 'sandbox',
        'echo server', 'httpbin', 'reqres', 'postman echo',
        'testing api', 'prototype', 'stub',
    ],
    'Identity': [
        # Authentication and identity
        'authentication', 'authorization', 'oauth', 'otp',
        'two-factor', 'mfa', 'passkey', 'biometric',
        'kyc', 'identity verification',
    ],
}

# Category defaults (when no keywords match, assign category to pattern)
CAT_DEFAULTS = {
    'weather': 'Dynamic Data',
    'cryptocurrency': 'Dynamic Data',
    'finance': 'Dynamic Data',
    'news': 'Dynamic Data',
    'sports & fitness': 'Dynamic Data',
    'tracking': 'Dynamic Data',
    'environment': 'Dynamic Data',
    'email': 'Communication',
    'social': 'Communication',
    'url shorteners': 'Service',
    'data validation': 'Service',
    'development': 'Service',
    'test data': 'Testing',
    'machine learning': 'AI/ML',
    'geocoding': 'Geospatial',
    'transportation': 'Geospatial',
    'security': 'Analytics',
    'government': 'Government',
    'video': 'Reference',
    'books': 'Reference',
    'anime': 'Reference',
    'games & comics': 'Reference',
    'music': 'Reference',
    'food & drink': 'Reference',
    'animals': 'Reference',
    'personality': 'Reference',
    'entertainment': 'Reference',
    'art & design': 'Reference',
    'photography': 'Reference',
    'health': 'Reference',
    'calendar': 'Reference',
    'science & math': 'Reference',
    'currency exchange': 'Reference',
    'business': 'Reference',
    'education': 'Reference',
    'jobs': 'Reference',
    'tracking': 'Dynamic Data',
    'open data': 'Reference',
    'authentication & authorization': 'Identity',
    'phone': 'Communication',
    'bioinformatics': 'Reference',
    'astrology': 'Reference',
    'language': 'Reference',
    'multi-service': 'Service',
    'sports betting': 'Dynamic Data',
    'translation': 'Service',
    'audio': 'Reference',
    'vehicle': 'Reference',
    'shopping': 'Platform',
    'blockchain': 'Dynamic Data',
    'open source projects': 'Reference',
}

def classify_api(api):
    """Classify an API into ONE functional pattern."""
    name = api.get('name', '').lower()
    desc = api.get('description', '').lower().strip()
    cat = api.get('category', '').lower()
    text = f"{name} {desc}"
    
    # Score each pattern based on keyword matches (longer keyword = higher priority)
    scores = {}
    for pattern, keywords in PATTERNS.items():
        score = 0
        for kw in keywords:
            if kw in text:
                # Longer keywords are more specific (higher weight)
                score += len(kw.split()) * 2
        scores[pattern] = score
    
    # Find best scoring pattern
    best_pattern = None
    best_score = 0
    for pattern, score in scores.items():
        if score > best_score:
            best_score = score
            best_pattern = pattern
    
    # If keywords found, use that pattern
    if best_score >= 3:  # At least one significant keyword match
        return best_pattern
    
    # Otherwise, use category default
    return CAT_DEFAULTS.get(cat, 'Reference')

# Classify all APIs
for api in apis:
    api['service_pattern'] = classify_api(api)

# Count and report
from collections import Counter
counts = Counter(api.get('service_pattern', 'Reference') for api in apis)

print("=== SERVICE PATTERN DISTRIBUTION ===")
for pattern, count in sorted(counts.items(), key=lambda x: -x[1]):
    pct = count / len(apis) * 100
    print(f"  {pattern}: {count} ({pct:.1f}%)")

# Verify specific cases
print("\n=== VERIFICATION (spot checks) ===")
checks = [
    ('coingecko', 'Dynamic Data'),
    ('binance', 'Dynamic Data'),
    ('weather', 'Dynamic Data'),
    ('finnhub', 'Dynamic Data'),
    ('fred', 'Dynamic Data'),
    ('ebird', 'Reference'),
    ('motivational', 'Reference'),
    ('pokemon', 'Reference'),
    ('meal', 'Reference'),
    ('qr ', 'Service'),
    ('short', 'Service'),
    ('url ', 'Service'),
    ('color', 'Service'),
    ('lorem', 'Service'),
    ('converter', 'Service'),
    ('email', 'Communication'),
    ('telegram', 'Communication'),
    ('twitter', 'Communication'),
    ('map ', 'Geospatial'),
    ('nominatim', 'Geospatial'),
    ('overpass', 'Geospatial'),
    ('mock', 'Testing'),
    ('httpbin', 'Testing'),
    ('jsonplaceholder', 'Testing'),
    ('fbi', 'Government'),
    ('patent', 'Government'),
    ('census', 'Government'),
    ('exchange rate', 'Dynamic Data'),
    ('exchangerate', 'Dynamic Data'),
    ('currency rate', 'Dynamic Data'),
    ('nager.date', 'Reference'),
    ('exchange rate', 'Reference'),
    ('exchangerate', 'Reference'),
]

for keyword, expected in checks:
    matches = [a for a in apis if keyword in a['name'].lower() or keyword in a.get('url', '').lower()][:2]
    for m in matches:
        status = "OK" if m.get('service_pattern') == expected else "FAIL"
        print(f"  {status} [{m.get('service_pattern','?')}] {m['name']} (expected: {expected})")

# Save with patterns
catalog['service_patterns'] = dict(sorted(counts.items(), key=lambda x: -x[1]))
with open('/home/terexitarius/free-api-catalog/apis.json', 'w') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Generate pattern files
os.makedirs('/home/terexitarius/free-api-catalog/patterns', exist_ok=True)
by_pattern = {}
for api in apis:
    p = api.get('service_pattern', 'Reference')
    if p not in by_pattern:
        by_pattern[p] = []
    by_pattern[p].append(api)

for pattern, pattern_apis in sorted(by_pattern.items(), key=lambda x: -len(x[1])):
    fname = pattern.lower().replace('/', '_').replace(' ', '_').replace('-', '_')
    with open(f'/home/terexitarius/free-api-catalog/patterns/{fname}.json', 'w') as f:
        json.dump(pattern_apis, f, indent=2, ensure_ascii=False)

print(f"\nWrote {len(by_pattern)} pattern files to patterns/")
for p, aps in sorted(by_pattern.items(), key=lambda x: -len(x[1])):
    print(f"  {p}: {len(aps)}")
