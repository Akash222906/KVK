import random
import datetime

DISTRICTS = [
    'Bardhaman', 'Birbhum', 'Bankura', 'Purulia', 'Hooghly',
    'Howrah', 'North 24 Parganas', 'South 24 Parganas', 'Nadia',
    'Murshidabad', 'Malda', 'Uttar Dinajpur', 'Dakshin Dinajpur',
    'Jalpaiguri', 'Darjeeling', 'Cooch Behar', 'Alipurduar',
    'Kalimpong', 'Paschim Medinipur', 'Purba Medinipur'
]

MARKET_PRICES = {
    'Rice':      {'msp': 2183, 'market': 2350, 'unit': 'quintal', 'trend': 'up'},
    'Wheat':     {'msp': 2275, 'market': 2400, 'unit': 'quintal', 'trend': 'stable'},
    'Jute':      {'msp': 5050, 'market': 5200, 'unit': 'quintal', 'trend': 'up'},
    'Potato':    {'msp': None, 'market': 1200, 'unit': 'quintal', 'trend': 'down'},
    'Mustard':   {'msp': 5650, 'market': 5800, 'unit': 'quintal', 'trend': 'up'},
    'Maize':     {'msp': 2090, 'market': 2150, 'unit': 'quintal', 'trend': 'stable'},
    'Tomato':    {'msp': None, 'market': 800,  'unit': 'quintal', 'trend': 'down'},
    'Onion':     {'msp': None, 'market': 1500, 'unit': 'quintal', 'trend': 'up'},
}

SCHEMES = [
    {
        'name': 'PM-KISAN',
        'full_name': 'Pradhan Mantri Kisan Samman Nidhi',
        'benefit': '₹6,000 per year in 3 installments',
        'eligibility': 'All small and marginal farmers with less than 2 hectares',
        'how_to_apply': 'Visit nearest CSC center or apply at pmkisan.gov.in',
        'category': 'Income Support'
    },
    {
        'name': 'Krishak Bandhu',
        'full_name': 'Krishak Bandhu Scheme (West Bengal)',
        'benefit': '₹10,000 per year per acre + ₹2 lakh death benefit',
        'eligibility': 'All farmers registered in West Bengal',
        'how_to_apply': 'Apply at local Krishak Bandhu office or Block Development Office',
        'category': 'State Scheme'
    },
    {
        'name': 'KCC',
        'full_name': 'Kisan Credit Card',
        'benefit': 'Credit up to ₹3 lakh at 4% interest per annum',
        'eligibility': 'All farmers, sharecroppers, tenant farmers',
        'how_to_apply': 'Apply at nearest bank branch with land records',
        'category': 'Credit'
    },
    {
        'name': 'PMFBY',
        'full_name': 'Pradhan Mantri Fasal Bima Yojana',
        'benefit': 'Crop insurance against natural calamities',
        'eligibility': 'All farmers growing notified crops',
        'how_to_apply': 'Apply through bank/insurance company before crop season',
        'category': 'Insurance'
    },
    {
        'name': 'PM-KUSUM',
        'full_name': 'Pradhan Mantri Kisan Urja Suraksha evam Utthan Mahabhiyan',
        'benefit': '60% subsidy on solar pumps',
        'eligibility': 'Farmers with own agricultural land',
        'how_to_apply': 'Apply through state nodal agency or agriculture department',
        'category': 'Solar/Energy'
    },
]

SEASONAL_ADVISORIES = {
    'Kharif': [
        'Prepare land for Aman paddy transplanting by June-July',
        'Apply balanced NPK fertilizer before transplanting',
        'Ensure proper irrigation during panicle initiation stage',
        'Monitor for Brown Plant Hopper and Stem Borer regularly',
        'Apply potash to strengthen stalks against lodging',
    ],
    'Rabi': [
        'Sow potato in October-November for optimal yield',
        'Apply mustard seed treatment before sowing',
        'Ensure adequate moisture during mustard flowering',
        'Protect potato crop from late blight in foggy conditions',
        'Harvest rabi crops before Nor\'wester season begins',
    ],
    'Summer': [
        'Summer vegetables need frequent light irrigation',
        'Mulching helps retain soil moisture and reduce weeding',
        'Protect crops from heat stress using shade nets',
        'Apply micronutrients for better fruit setting',
        'Harvest early morning to maintain produce quality',
    ]
}

def get_weather(district):
    month = datetime.datetime.now().month
    if month in [6, 7, 8, 9]:
        season, temp_base, rain_base, hum_base = 'Monsoon', 30, 200, 85
    elif month in [12, 1, 2]:
        season, temp_base, rain_base, hum_base = 'Winter', 18, 15, 65
    elif month in [3, 4, 5]:
        season, temp_base, rain_base, hum_base = 'Summer', 35, 40, 60
    else:
        season, temp_base, rain_base, hum_base = 'Post-Monsoon', 26, 60, 75

    current = {
        'district': district,
        'season': season,
        'temperature': round(temp_base + random.uniform(-2, 3), 1),
        'humidity': round(hum_base + random.uniform(-5, 5), 1),
        'rainfall': round(rain_base + random.uniform(-20, 30), 1),
        'wind_speed': round(random.uniform(8, 25), 1),
        'conditions': 'Partly Cloudy' if season == 'Monsoon' else 'Clear',
    }

    forecast = []
    days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    today = datetime.datetime.now().weekday()
    for i in range(7):
        day_idx = (today + i) % 7
        forecast.append({
            'day': days[day_idx],
            'max_temp': round(current['temperature'] + random.uniform(0, 4), 1),
            'min_temp': round(current['temperature'] - random.uniform(2, 6), 1),
            'rain_chance': random.randint(10, 90) if season == 'Monsoon' else random.randint(0, 30),
            'conditions': random.choice(['Sunny', 'Cloudy', 'Light Rain', 'Heavy Rain']) if season == 'Monsoon' else 'Clear',
        })

    return {'current': current, 'forecast': forecast}

def get_market_prices():
    prices = []
    for crop, data in MARKET_PRICES.items():
        fluctuation = random.uniform(-50, 80)
        prices.append({
            'crop': crop,
            'msp': data['msp'],
            'market_price': round(data['market'] + fluctuation, 0),
            'unit': data['unit'],
            'trend': data['trend'],
        })
    return prices

def get_advisory(season='Kharif'):
    return SEASONAL_ADVISORIES.get(season, SEASONAL_ADVISORIES['Kharif'])

def get_schemes():
    return SCHEMES

def get_districts():
    return DISTRICTS
