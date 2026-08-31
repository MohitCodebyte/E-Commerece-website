"""
NOVA MART - Centralized Mock Data Store (Phase 1)
All business entities are modeled cleanly here.
In Phase 2, this module will be supplemented/replaced by database queries
through the repository interfaces without altering route or service contracts.
"""

from copy import deepcopy

# --- CATEGORIES ---
CATEGORIES = [
    {
        "id": "cat-electronics",
        "name": "Electronics",
        "slug": "electronics",
        "icon": "devices",
        "description": "Premium consumer electronics, audio gear, and accessories",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800",
        "product_count": 8,
        "is_featured": True,
    },
    {
        "id": "cat-fashion",
        "name": "Fashion & Apparel",
        "slug": "fashion",
        "icon": "apparel",
        "description": "Curated minimalist and street fashion for modern living",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBNGx_w12f3k9lM8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s800",
        "product_count": 4,
        "is_featured": True,
    },
    {
        "id": "cat-home",
        "name": "Home & Living",
        "slug": "home-living",
        "icon": "chair",
        "description": "Ergonomic furniture, ambient lighting, and desk essentials",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCrJiTelv8n7m6l5k4j3h2g1f0d9s8a7q6w5e4r3t2y1u=s800",
        "product_count": 3,
        "is_featured": True,
    },
    {
        "id": "cat-beauty",
        "name": "Beauty & Grooming",
        "slug": "beauty",
        "icon": "spa",
        "description": "Organic skincare and high-end personal care essentials",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBNGx_w12f3k9lM8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s800",
        "product_count": 2,
        "is_featured": False,
    },
    {
        "id": "cat-accessories",
        "name": "Accessories",
        "slug": "accessories",
        "icon": "watch",
        "description": "Smart wearables, wallets, and premium leather accessories",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800",
        "product_count": 3,
        "is_featured": True,
    },
]

# --- BRANDS ---
BRANDS = [
    {"id": "brand-novatech", "name": "NovaTech", "slug": "novatech", "logo": "smart_display", "is_verified": True},
    {"id": "brand-apexaudio", "name": "ApexAudio", "slug": "apexaudio", "logo": "headphones", "is_verified": True},
    {"id": "brand-vibewear", "name": "VibeWear", "slug": "vibewear", "logo": "checkroom", "is_verified": True},
    {"id": "brand-lumina", "name": "Lumina", "slug": "lumina", "logo": "lightbulb", "is_verified": True},
    {"id": "brand-soundpulse", "name": "SoundPulse", "slug": "soundpulse", "logo": "speaker", "is_verified": True},
    {"id": "brand-zenfit", "name": "ZenFit", "slug": "zenfit", "logo": "fitness_center", "is_verified": True},
    {"id": "brand-aurahome", "name": "AuraHome", "slug": "aurahome", "logo": "home", "is_verified": False},
]

# --- SELLERS ---
SELLERS = [
    {
        "id": "seller-1",
        "store_name": "TechZone Electronics",
        "slug": "techzone-electronics",
        "legal_name": "TechZone Retail Private Limited",
        "email": "seller@techzone.in",
        "phone": "+91 98765 43210",
        "address": "Unit 402, Pinnacle IT Park, Andheri East, Mumbai, Maharashtra - 400069",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400069",
        "gstin": "27AAAAA0000A1Z5",
        "pan": "AAAAA0000A",
        "bank_account": {
            "account_name": "TechZone Retail Pvt Ltd",
            "account_number": "918020045678912",
            "ifsc": "HDFC0001234",
            "bank_name": "HDFC Bank",
            "branch": "Andheri East"
        },
        "rating": 4.8,
        "total_reviews": 328,
        "commission_rate": 10.0,  # 10%
        "status": "active",  # active, pending, suspended
        "kyc_status": "verified",  # verified, pending, rejected
        "payout_balance": 84500.0,
        "lifetime_earnings": 492000.0,
        "banner": "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s1200",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuB2NOZ9Tw1k4m0Z5Y8n7m6l5k4j3h2g1f0d9s8a7q6w5e=s200",
        "joined_date": "2024-01-15",
    },
    {
        "id": "seller-2",
        "store_name": "UrbanStyle India",
        "slug": "urbanstyle-india",
        "legal_name": "UrbanStyle Fashion Labs LLP",
        "email": "seller@urbanstyle.in",
        "phone": "+91 98111 22334",
        "address": "12/A, Koramangala 4th Block, Bengaluru, Karnataka - 560034",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "560034",
        "gstin": "29BBBBB1111B1Z2",
        "pan": "BBBBB1111B",
        "bank_account": {
            "account_name": "UrbanStyle Fashion Labs",
            "account_number": "602410100987654",
            "ifsc": "ICIC0000456",
            "bank_name": "ICICI Bank",
            "branch": "Koramangala"
        },
        "rating": 4.6,
        "total_reviews": 184,
        "commission_rate": 12.0,  # 12%
        "status": "active",
        "kyc_status": "verified",
        "payout_balance": 32100.0,
        "lifetime_earnings": 185000.0,
        "banner": "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s1200",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuDv0Uxh_7m6l5k4j3h2g1f0d9s8a7q6w5e4r3t2y1u=s200",
        "joined_date": "2024-03-10",
    },
    {
        "id": "seller-3",
        "store_name": "SmartGadgets Direct",
        "slug": "smartgadgets-direct",
        "legal_name": "SmartGadgets Enterprise",
        "email": "seller@smartgadgets.in",
        "phone": "+91 99555 66778",
        "address": "B-44, Okhla Industrial Area Phase II, New Delhi - 110020",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110020",
        "gstin": "07CCCCC2222C1Z9",
        "pan": "CCCCC2222C",
        "bank_account": {
            "account_name": "SmartGadgets Enterprise",
            "account_number": "1009876543210",
            "ifsc": "SBIN0007890",
            "bank_name": "State Bank of India",
            "branch": "Okhla"
        },
        "rating": 4.2,
        "total_reviews": 42,
        "commission_rate": 10.0,
        "status": "pending",
        "kyc_status": "under_review",
        "payout_balance": 0.0,
        "lifetime_earnings": 0.0,
        "banner": "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s1200",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuB2NOZ9Tw1k4m0Z5Y8n7m6l5k4j3h2g1f0d9s8a7q6w5e=s200",
        "joined_date": "2024-07-01",
    }
]

# --- USERS (Customer, Seller, Super Admin) ---
USERS = [
    {
        "id": "user-cust-1",
        "name": "Aarav Sharma",
        "email": "customer@novamart.in",
        "password": "customer123",  # Demo credentials
        "role": "customer",
        "phone": "+91 98200 12345",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s200",
        "seller_id": None,
        "status": "active",
        "created_at": "2024-02-10",
        "addresses": [
            {
                "id": "addr-1",
                "label": "Home",
                "recipient": "Aarav Sharma",
                "phone": "+91 98200 12345",
                "street": "Flat 804, Oberoi Springs, Off Link Road",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": "400053",
                "is_default": True,
            },
            {
                "id": "addr-2",
                "label": "Office",
                "recipient": "Aarav Sharma (Work)",
                "phone": "+91 98200 12345",
                "street": "WeWork Enam Sambhav, BKC, Bandra East",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": "400051",
                "is_default": False,
            }
        ]
    },
    {
        "id": "user-cust-2",
        "name": "Priya Patel",
        "email": "priya@example.com",
        "password": "customer123",
        "role": "customer",
        "phone": "+91 98765 99887",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuBBLGR0hs9n8m7l6k5j4h3g2f1d0s9a8q7w6e5r4t3y2u=s200",
        "seller_id": None,
        "status": "active",
        "created_at": "2024-03-01",
        "addresses": [
            {
                "id": "addr-3",
                "label": "Home",
                "recipient": "Priya Patel",
                "phone": "+91 98765 99887",
                "street": "Flat 302, Prestige Tower, Indiranagar",
                "city": "Bengaluru",
                "state": "Karnataka",
                "pincode": "560038",
                "is_default": True,
            }
        ]
    },
    {
        "id": "user-seller-1",
        "name": "Rajesh Kumar",
        "email": "seller@techzone.in",
        "password": "seller123",  # Demo credentials
        "role": "seller",
        "phone": "+91 98765 43210",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuDv0Uxh_7m6l5k4j3h2g1f0d9s8a7q6w5e4r3t2y1u=s200",
        "seller_id": "seller-1",
        "status": "active",
        "created_at": "2024-01-15",
    },
    {
        "id": "user-seller-2",
        "name": "Ananya Rao",
        "email": "seller@urbanstyle.in",
        "password": "seller123",
        "role": "seller",
        "phone": "+91 98111 22334",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuCso59bPm1k4m0Z5Y8n7m6l5k4j3h2g1f0d9s8a7q6w5e=s200",
        "seller_id": "seller-2",
        "status": "active",
        "created_at": "2024-03-10",
    },
    {
        "id": "user-admin-1",
        "name": "Vikramaditya Singhania",
        "email": "admin@novamart.in",
        "password": "admin123",  # Demo credentials
        "role": "admin",
        "phone": "+91 99999 00000",
        "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuAS7hTLGp1k4m0Z5Y8n7m6l5k4j3h2g1f0d9s8a7q6w5e=s200",
        "seller_id": None,
        "status": "active",
        "created_at": "2023-12-01",
    }
]

# --- PRODUCTS ---
PRODUCTS = [
    {
        "id": "prod-1",
        "title": "Aura Pulse Studio Wireless Headphones",
        "slug": "aura-pulse-studio-wireless-headphones",
        "sku": "NM-TECH-001",
        "category_id": "cat-electronics",
        "category_name": "Electronics",
        "brand_id": "brand-apexaudio",
        "brand_name": "ApexAudio",
        "seller_id": "seller-1",
        "seller_name": "TechZone Electronics",
        "price": 14999.0,
        "compare_at_price": 18999.0,
        "cost_price": 10500.0,
        "discount_percent": 21,
        "stock": 45,
        "reserved_stock": 5,
        "low_stock_threshold": 10,
        "rating": 4.9,
        "review_count": 128,
        "badge": "Bestseller",
        "is_featured": True,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=800&q=80",
        ],
        "summary": "Flagship active noise-canceling wireless headphones featuring 40mm beryllium drivers, spatial audio, and 45-hour battery life.",
        "description": "Experience auditory perfection with the Aura Pulse Studio. Engineered for demanding audiophiles and professionals, these headphones deliver pristine highs, deep punchy sub-bass, and hybrid ANC that neutralizes up to 98% of ambient noise. Crafted with memory-foam ear cushions and aircraft-grade aluminum hinges.",
        "features": [
            "Hybrid Active Noise Cancellation (40dB depth)",
            "High-Resolution Audio certified with LDAC support",
            "45 Hours continuous playback on a single charge",
            "Multi-device seamless Bluetooth 5.3 pairing",
            "Ultra-soft memory foam with genuine protein leather"
        ],
        "specifications": {
            "Driver Size": "40mm Beryllium Drivers",
            "Frequency Response": "10Hz - 40,000Hz",
            "Battery Capacity": "850 mAh",
            "Charging Port": "USB Type-C (Fast Charge: 10 mins = 5 hrs)",
            "Weight": "250 grams",
            "Warranty": "2 Years Official Manufacturer Warranty"
        },
        "variants": [
            {"id": "var-1-1", "name": "Midnight Black", "color": "#0f172a", "stock": 25, "sku": "NM-TECH-001-BLK", "price": 14999.0},
            {"id": "var-1-2", "name": "Lunar Silver", "color": "#e2e8f0", "stock": 15, "sku": "NM-TECH-001-SLV", "price": 14999.0},
            {"id": "var-1-3", "name": "Electric Indigo", "color": "#4f46e5", "stock": 5, "sku": "NM-TECH-001-IND", "price": 15499.0},
        ]
    },
    {
        "id": "prod-2",
        "title": "ZenFit Apex Smart Fitness Tracker",
        "slug": "zenfit-apex-smart-fitness-tracker",
        "sku": "NM-TECH-002",
        "category_id": "cat-accessories",
        "category_name": "Accessories",
        "brand_id": "brand-zenfit",
        "brand_name": "ZenFit",
        "seller_id": "seller-1",
        "seller_name": "TechZone Electronics",
        "price": 4999.0,
        "compare_at_price": 6999.0,
        "cost_price": 3200.0,
        "discount_percent": 28,
        "stock": 80,
        "reserved_stock": 10,
        "low_stock_threshold": 15,
        "rating": 4.7,
        "review_count": 94,
        "badge": "Hot",
        "is_featured": True,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1579586337278-3f56b0d9e7b2?auto=format&fit=crop&w=800&q=80"
        ],
        "summary": "Ultra-lightweight AMOLED fitness tracker with continuous SpO2, heart-rate tracking, GPS route tracking, and 5ATM water resistance.",
        "description": "Transform your wellness journey with the ZenFit Apex. Featuring an edge-to-edge vibrant AMOLED display, over 120 sports tracking modes, sleep architecture diagnostics, and a rugged water-resistant chassis.",
        "features": [
            "1.47-inch Curved AMOLED Retina Display",
            "24/7 Heart Rate & Dynamic SpO2 Monitoring",
            "Built-in Precision GPS Tracking",
            "5ATM Water Resistance (50m dive proof)",
            "14-Day Battery Life on normal usage"
        ],
        "specifications": {
            "Display": "1.47-inch AMOLED, 368x194 px",
            "Sensors": "Optical Bio-Sensor, 6-Axis Gyro, Barometer",
            "Battery": "180 mAh Li-Polymer",
            "Connectivity": "Bluetooth 5.2 BLE",
            "Compatibility": "Android 8.0+ and iOS 12.0+",
            "Warranty": "1 Year Replacement Warranty"
        },
        "variants": [
            {"id": "var-2-1", "name": "Obsidian Black", "color": "#18181b", "stock": 45, "sku": "NM-TECH-002-BLK", "price": 4999.0},
            {"id": "var-2-2", "name": "Pacific Blue", "color": "#0284c7", "stock": 35, "sku": "NM-TECH-002-BLU", "price": 4999.0},
        ]
    },
    {
        "id": "prod-3",
        "title": "Minimalist Oversized Heavyweight Cotton Hoodie",
        "slug": "minimalist-oversized-heavyweight-cotton-hoodie",
        "sku": "NM-FASH-001",
        "category_id": "cat-fashion",
        "category_name": "Fashion & Apparel",
        "brand_id": "brand-vibewear",
        "brand_name": "VibeWear",
        "seller_id": "seller-2",
        "seller_name": "UrbanStyle India",
        "price": 2899.0,
        "compare_at_price": 3999.0,
        "cost_price": 1600.0,
        "discount_percent": 27,
        "stock": 60,
        "reserved_stock": 4,
        "low_stock_threshold": 12,
        "rating": 4.8,
        "review_count": 62,
        "badge": "Trending",
        "is_featured": True,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1509967419530-da38b4704bc6?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80"
        ],
        "summary": "450 GSM luxury brushed loopback French Terry fleece oversized hoodie tailored for clean architectural streetwear.",
        "description": "Crafted from 100% combed ring-spun cotton with custom double-needle stitch detailing. Pre-shrunk fabric ensures enduring shape after washing. Features a structured double-layer hood without drawstrings for a sleek silhouette.",
        "features": [
            "450 GSM Heavyweight French Terry Cotton",
            "Seamless drop-shoulder relaxed silhouette",
            "Kangaroo pocket with reinforced bartacks",
            "Pre-washed to eliminate post-purchase shrinkage",
            "Eco-friendly non-toxic reactive dyes"
        ],
        "specifications": {
            "Material": "100% Combed Organic Cotton",
            "Fit": "Modern Oversized Boxy Cut",
            "Care": "Machine wash cold inside out, tumble dry low",
            "Origin": "Tirupur, India"
        },
        "variants": [
            {"id": "var-3-1", "name": "Slate Charcoal / M", "color": "#334155", "size": "M", "stock": 20, "sku": "NM-FASH-001-M-GRY", "price": 2899.0},
            {"id": "var-3-2", "name": "Slate Charcoal / L", "color": "#334155", "size": "L", "stock": 25, "sku": "NM-FASH-001-L-GRY", "price": 2899.0},
            {"id": "var-3-3", "name": "Off White / L", "color": "#f8fafc", "size": "L", "stock": 15, "sku": "NM-FASH-001-L-WHT", "price": 2899.0},
        ]
    },
    {
        "id": "prod-4",
        "title": "AuraHome Ambient Arc Desk Lamp",
        "slug": "aurahome-ambient-arc-desk-lamp",
        "sku": "NM-HOME-001",
        "category_id": "cat-home",
        "category_name": "Home & Living",
        "brand_id": "brand-aurahome",
        "brand_name": "AuraHome",
        "seller_id": "seller-2",
        "seller_name": "UrbanStyle India",
        "price": 3499.0,
        "compare_at_price": 4999.0,
        "cost_price": 2100.0,
        "discount_percent": 30,
        "stock": 30,
        "reserved_stock": 2,
        "low_stock_threshold": 8,
        "rating": 4.6,
        "review_count": 41,
        "badge": "New",
        "is_featured": False,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1540932239986-30128078f3c5?auto=format&fit=crop&w=800&q=80"
        ],
        "summary": "Solid anodized aluminum minimalist desk lamp with touch-sensitive dimming and dual color temperature (2700K - 5500K).",
        "description": "Illuminate your desk workspace without eye fatigue. Equipped with flicker-free anti-blue-light LED beads, stepless dimming, and an integrated Qi 15W wireless charging base.",
        "features": [
            "Flicker-free CRI > 95 daylight simulation",
            "Stepless brightness slider with memory recall",
            "Built-in 15W Qi Wireless Fast Phone Charger Base",
            "Aerospace grade aluminum unibody build"
        ],
        "specifications": {
            "Power Consumption": "18W Max",
            "Luminous Flux": "800 Lumens",
            "Base Dimensions": "140mm diameter",
            "Height": "420mm",
            "Warranty": "1 Year Comprehensive Warranty"
        },
        "variants": [
            {"id": "var-4-1", "name": "Matte Space Gray", "color": "#475569", "stock": 20, "sku": "NM-HOME-001-GRY", "price": 3499.0},
            {"id": "var-4-2", "name": "Frosted Pearl", "color": "#f1f5f9", "stock": 10, "sku": "NM-HOME-001-WHT", "price": 3499.0},
        ]
    },
    {
        "id": "prod-5",
        "title": "SoundPulse Neo Portable Waterproof Speaker",
        "slug": "soundpulse-neo-portable-waterproof-speaker",
        "sku": "NM-TECH-003",
        "category_id": "cat-electronics",
        "category_name": "Electronics",
        "brand_id": "brand-soundpulse",
        "brand_name": "SoundPulse",
        "seller_id": "seller-1",
        "seller_name": "TechZone Electronics",
        "price": 3999.0,
        "compare_at_price": 5499.0,
        "cost_price": 2500.0,
        "discount_percent": 27,
        "stock": 50,
        "reserved_stock": 6,
        "low_stock_threshold": 10,
        "rating": 4.7,
        "review_count": 86,
        "badge": "Popular",
        "is_featured": True,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=800&q=80"
        ],
        "summary": "360-degree room-filling acoustic sound with dual passive radiators, IP67 submersible waterproofing, and 24-hour battery endurance.",
        "description": "Take studio sound anywhere from rooftop parties to seaside retreats. Built with military-grade rugged exterior shock bumpers and custom neodymium drivers.",
        "features": [
            "20W RMS High-Fidelity 360° Omnidirectional Audio",
            "IP67 Dustproof and Waterproof (floats on water)",
            "TWS Stereo Pairing with another SoundPulse Neo",
            "24 Hours Playtime with 5200 mAh Powerbank output"
        ],
        "specifications": {
            "Audio Output": "20W RMS (2x 10W Drivers)",
            "Bluetooth": "5.3 with AAC Codec",
            "Dimensions": "180 x 70 x 70 mm",
            "Weight": "560 grams",
            "Warranty": "1 Year Manufacturer Warranty"
        },
        "variants": [
            {"id": "var-5-1", "name": "Tactical Olive", "color": "#3f6212", "stock": 25, "sku": "NM-TECH-003-OLV", "price": 3999.0},
            {"id": "var-5-2", "name": "Stealth Black", "color": "#09090b", "stock": 25, "sku": "NM-TECH-003-BLK", "price": 3999.0},
        ]
    },
    {
        "id": "prod-6",
        "title": "NovaTech ProBook Ultra-Thin Laptop Stand",
        "slug": "novatech-probook-ultrathin-laptop-stand",
        "sku": "NM-TECH-004",
        "category_id": "cat-accessories",
        "category_name": "Accessories",
        "brand_id": "brand-novatech",
        "brand_name": "NovaTech",
        "seller_id": "seller-1",
        "seller_name": "TechZone Electronics",
        "price": 1899.0,
        "compare_at_price": 2499.0,
        "cost_price": 1100.0,
        "discount_percent": 24,
        "stock": 110,
        "reserved_stock": 8,
        "low_stock_threshold": 20,
        "rating": 4.9,
        "review_count": 156,
        "badge": "Top Rated",
        "is_featured": False,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80"
        ],
        "summary": "CNC machined aircraft aluminum foldable ergonomic laptop riser with silicone anti-slip buffers.",
        "description": "Optimize your posture and keep your workstation cool. Elevates your laptop to eye level across 6 adjustable angle settings.",
        "features": [
            "Precision CNC Aircraft-grade aluminum alloy",
            "Foldable ultra-thin design (slips into any laptop sleeve)",
            "6 Height adjustment levels from 15° to 45°",
            "Open ventilation design prevents laptop thermal throttling"
        ],
        "specifications": {
            "Material": "Sandblasted Aluminum Alloy",
            "Max Weight Capacity": "15 kg",
            "Folded Thickness": "4 mm",
            "Compatibility": "All Laptops 10 to 17 inches",
            "Warranty": "3 Years Durability Warranty"
        },
        "variants": [
            {"id": "var-6-1", "name": "Silver Chrome", "color": "#cbd5e1", "stock": 60, "sku": "NM-TECH-004-SLV", "price": 1899.0},
            {"id": "var-6-2", "name": "Space Gray", "color": "#475569", "stock": 50, "sku": "NM-TECH-004-GRY", "price": 1899.0},
        ]
    },
    {
        "id": "prod-7",
        "title": "Artisan Full-Grain Leather Weekender Duffle Bag",
        "slug": "artisan-full-grain-leather-weekender-duffle-bag",
        "sku": "NM-FASH-002",
        "category_id": "cat-fashion",
        "category_name": "Fashion & Apparel",
        "brand_id": "brand-vibewear",
        "brand_name": "VibeWear",
        "seller_id": "seller-2",
        "seller_name": "UrbanStyle India",
        "price": 7499.0,
        "compare_at_price": 9999.0,
        "cost_price": 4500.0,
        "discount_percent": 25,
        "stock": 25,
        "reserved_stock": 2,
        "low_stock_threshold": 5,
        "rating": 4.9,
        "review_count": 48,
        "badge": "Handcrafted",
        "is_featured": True,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80"
        ],
        "summary": "Handcrafted vegetable-tanned full-grain buffalo leather cabin duffle bag with solid brass hardware.",
        "description": "Engineered for weekend getaways and stylish daily commuting. Features reinforced leather carry handles, an adjustable padded shoulder strap, and an internal laptop compartment.",
        "features": [
            "100% Genuine vegetable-tanned full-grain leather",
            "Antique solid brass YKK zippers",
            "Padded interior sleeve for 15-inch laptops",
            "Water-resistant cotton twill interior lining"
        ],
        "specifications": {
            "Material": "Full-Grain Buffalo Leather",
            "Dimensions": "52 x 28 x 25 cm",
            "Capacity": "38 Liters",
            "Warranty": "5 Years Craftsmanship Guarantee"
        },
        "variants": [
            {"id": "var-7-1", "name": "Cognac Brown", "color": "#78350f", "stock": 15, "sku": "NM-FASH-002-BRN", "price": 7499.0},
            {"id": "var-7-2", "name": "Midnight Black", "color": "#09090b", "stock": 10, "sku": "NM-FASH-002-BLK", "price": 7499.0},
        ]
    },
    {
        "id": "prod-8",
        "title": "AeroStride Velocity Carbon Running Shoes",
        "slug": "aerostride-velocity-carbon-running-shoes",
        "sku": "NM-FASH-003",
        "category_id": "cat-fashion",
        "category_name": "Fashion & Apparel",
        "brand_id": "brand-vibewear",
        "brand_name": "VibeWear",
        "seller_id": "seller-2",
        "seller_name": "UrbanStyle India",
        "price": 6299.0,
        "compare_at_price": 7999.0,
        "cost_price": 3800.0,
        "discount_percent": 21,
        "stock": 40,
        "reserved_stock": 3,
        "low_stock_threshold": 10,
        "rating": 4.8,
        "review_count": 72,
        "badge": "Pro Choice",
        "is_featured": True,
        "is_active": True,
        "thumbnail": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
        "images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?auto=format&fit=crop&w=800&q=80"
        ],
        "summary": "Full-length carbon fiber propulsion plate with responsive nitrogen-infused dual-density midsole foam.",
        "description": "Built for marathon runners and tempo training. The breathable engineered monomesh upper keeps feet cool while the carbon plate provides maximum energy return with every stride.",
        "features": [
            "Full-length curved carbon fiber propulsion plate",
            "Nitrogen-infused ultra-responsive supercritical foam",
            "Ultralight engineered monomesh breathable upper",
            "High-traction zoned rubber outsole"
        ],
        "specifications": {
            "Weight": "198 grams (Size UK 9)",
            "Heel-to-Toe Drop": "8 mm",
            "Surface": "Road, Track",
            "Warranty": "6 Months Performance Warranty"
        },
        "variants": [
            {"id": "var-8-1", "name": "Inferno Red / UK 8", "color": "#dc2626", "stock": 12, "sku": "NM-FASH-003-8-RED", "price": 6299.0},
            {"id": "var-8-2", "name": "Inferno Red / UK 9", "color": "#dc2626", "stock": 18, "sku": "NM-FASH-003-9-RED", "price": 6299.0},
            {"id": "var-8-3", "name": "Stealth Black / UK 9", "color": "#09090b", "stock": 10, "sku": "NM-FASH-003-9-BLK", "price": 6299.0},
        ]
    }
]

# --- REVIEWS ---
REVIEWS = [
    {
        "id": "rev-1",
        "product_id": "prod-1",
        "product_title": "Aura Pulse Studio Wireless Headphones",
        "user_id": "user-cust-1",
        "user_name": "Aarav Sharma",
        "user_avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s200",
        "rating": 5,
        "title": "Unbelievable Sound Quality & ANC",
        "comment": "I've tried Bose and Sony, but the soundstage and instrument separation on the Aura Pulse is on another level. The build feels like a ₹30,000 pair of cans. Fast delivery by Nova Mart within 2 days in Mumbai!",
        "date": "2024-07-18",
        "verified_purchase": True,
        "helpful_count": 34,
        "seller_response": "Thank you Aarav! We take extreme pride in our precision acoustic calibration. Enjoy your music!",
        "status": "approved"  # approved, pending, flagged
    },
    {
        "id": "rev-2",
        "product_id": "prod-1",
        "product_title": "Aura Pulse Studio Wireless Headphones",
        "user_id": "user-cust-2",
        "user_name": "Priya Patel",
        "user_avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuBBLGR0hs9n8m7l6k5j4h3g2f1d0s9a8q7w6e5r4t3y2u=s200",
        "rating": 5,
        "title": "Best purchase for remote work",
        "comment": "The microphone clarity during Zoom meetings is crystal clear. Noise cancellation blocks out all street noise outside my apartment. 10/10 recommendation!",
        "date": "2024-07-22",
        "verified_purchase": True,
        "helpful_count": 18,
        "seller_response": None,
        "status": "approved"
    },
    {
        "id": "rev-3",
        "product_id": "prod-3",
        "product_title": "Minimalist Oversized Heavyweight Cotton Hoodie",
        "user_id": "user-cust-1",
        "user_name": "Aarav Sharma",
        "user_avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuDL9hkvls8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s200",
        "rating": 5,
        "title": "Thick luxury fabric, perfect boxy fit",
        "comment": "The French Terry cotton has substantial weight. Doesn't lose shape after washing. UrbanStyle nailed the drop shoulder fit.",
        "date": "2024-06-12",
        "verified_purchase": True,
        "helpful_count": 12,
        "seller_response": "Thanks Aarav! Our 450 GSM fleece is milled specifically for high durability.",
        "status": "approved"
    }
]

# --- ORDERS ---
ORDERS = [
    {
        "id": "ORD-2024-8901",
        "customer_id": "user-cust-1",
        "customer_name": "Aarav Sharma",
        "customer_email": "customer@novamart.in",
        "customer_phone": "+91 98200 12345",
        "shipping_address": {
            "recipient": "Aarav Sharma",
            "street": "Flat 804, Oberoi Springs, Off Link Road",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400053",
            "phone": "+91 98200 12345"
        },
        "order_date": "2024-08-20 14:32",
        "status": "delivered",  # pending, processing, shipped, delivered, cancelled, returned
        "payment_status": "paid",  # paid, pending, failed, refunded
        "payment_method": "UPI (Google Pay)",
        "subtotal": 14999.0,
        "tax": 2700.0,  # 18% GST
        "shipping_fee": 0.0,
        "discount": 1000.0,
        "coupon_code": "NOVA10",
        "total": 16699.0,
        "tracking_number": "DEL-EXP-982173491",
        "carrier": "Delhivery Express",
        "estimated_delivery": "2024-08-23",
        "delivered_date": "2024-08-22 17:45",
        "tracking_timeline": [
            {"status": "Order Placed", "time": "2024-08-20 14:32", "location": "Mumbai", "completed": True},
            {"status": "Payment Confirmed", "time": "2024-08-20 14:33", "location": "Gateway", "completed": True},
            {"status": "Processed & Packed", "time": "2024-08-21 09:15", "location": "TechZone Warehouse, Andheri", "completed": True},
            {"status": "Shipped in Transit", "time": "2024-08-21 16:30", "location": "Delhivery Hub, Mumbai", "completed": True},
            {"status": "Delivered", "time": "2024-08-22 17:45", "location": "Customer Doorstep", "completed": True},
        ],
        "items": [
            {
                "product_id": "prod-1",
                "product_title": "Aura Pulse Studio Wireless Headphones",
                "variant_name": "Midnight Black",
                "sku": "NM-TECH-001-BLK",
                "price": 14999.0,
                "quantity": 1,
                "seller_id": "seller-1",
                "seller_name": "TechZone Electronics",
                "commission_rate": 10.0,
                "commission_amount": 1499.9,
                "seller_net_earning": 13499.1,
                "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAuF1UtFRv-c7V47-kU4vC-u8rC4Uf8j3g9sLp1k4m0Z5Y=s800"
            }
        ]
    },
    {
        "id": "ORD-2024-8902",
        "customer_id": "user-cust-1",
        "customer_name": "Aarav Sharma",
        "customer_email": "customer@novamart.in",
        "customer_phone": "+91 98200 12345",
        "shipping_address": {
            "recipient": "Aarav Sharma",
            "street": "Flat 804, Oberoi Springs, Off Link Road",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400053",
            "phone": "+91 98200 12345"
        },
        "order_date": "2024-08-28 11:15",
        "status": "shipped",
        "payment_status": "paid",
        "payment_method": "Credit Card (Visa ending in 4242)",
        "subtotal": 5798.0,
        "tax": 1043.64,
        "shipping_fee": 150.0,
        "discount": 0.0,
        "coupon_code": None,
        "total": 6991.64,
        "tracking_number": "BLUEDART-88291039",
        "carrier": "Blue Dart Express",
        "estimated_delivery": "2024-09-02",
        "delivered_date": None,
        "tracking_timeline": [
            {"status": "Order Placed", "time": "2024-08-28 11:15", "location": "Mumbai", "completed": True},
            {"status": "Payment Confirmed", "time": "2024-08-28 11:16", "location": "Gateway", "completed": True},
            {"status": "Processed & Packed", "time": "2024-08-29 10:00", "location": "UrbanStyle Logistics, Bengaluru", "completed": True},
            {"status": "Shipped in Transit", "time": "2024-08-30 08:30", "location": "Blue Dart Air Hub, Bengaluru", "completed": True},
            {"status": "Delivered", "time": "Pending", "location": "Mumbai", "completed": False},
        ],
        "items": [
            {
                "product_id": "prod-3",
                "product_title": "Minimalist Oversized Heavyweight Cotton Hoodie",
                "variant_name": "Slate Charcoal / L",
                "sku": "NM-FASH-001-L-GRY",
                "price": 2899.0,
                "quantity": 2,
                "seller_id": "seller-2",
                "seller_name": "UrbanStyle India",
                "commission_rate": 12.0,
                "commission_amount": 695.76,
                "seller_net_earning": 5102.24,
                "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBNGx_w12f3k9lM8j7H6g5F4d3S2a1Q0w9E8r7T6y5U4i=s800"
            }
        ]
    },
    {
        "id": "ORD-2024-8903",
        "customer_id": "user-cust-2",
        "customer_name": "Priya Patel",
        "customer_email": "priya@example.com",
        "customer_phone": "+91 98765 99887",
        "shipping_address": {
            "recipient": "Priya Patel",
            "street": "Flat 302, Prestige Tower, Indiranagar",
            "city": "Bengaluru",
            "state": "Karnataka",
            "pincode": "560038",
            "phone": "+91 98765 99887"
        },
        "order_date": "2024-08-30 16:40",
        "status": "processing",
        "payment_status": "paid",
        "payment_method": "Net Banking (HDFC)",
        "subtotal": 4999.0,
        "tax": 899.82,
        "shipping_fee": 0.0,
        "discount": 500.0,
        "coupon_code": "FESTIVE25",
        "total": 5398.82,
        "tracking_number": "DEL-EXP-7721654",
        "carrier": "Delhivery Express",
        "estimated_delivery": "2024-09-04",
        "delivered_date": None,
        "tracking_timeline": [
            {"status": "Order Placed", "time": "2024-08-30 16:40", "location": "Bengaluru", "completed": True},
            {"status": "Payment Confirmed", "time": "2024-08-30 16:41", "location": "Gateway", "completed": True},
            {"status": "Processing in Warehouse", "time": "2024-08-31 09:00", "location": "TechZone Warehouse, Andheri", "completed": True},
            {"status": "Shipped in Transit", "time": "Pending", "location": "Logistics Hub", "completed": False},
            {"status": "Delivered", "time": "Pending", "location": "Indiranagar", "completed": False},
        ],
        "items": [
            {
                "product_id": "prod-2",
                "product_title": "ZenFit Apex Smart Fitness Tracker",
                "variant_name": "Obsidian Black",
                "sku": "NM-TECH-002-BLK",
                "price": 4999.0,
                "quantity": 1,
                "seller_id": "seller-1",
                "seller_name": "TechZone Electronics",
                "commission_rate": 10.0,
                "commission_amount": 499.9,
                "seller_net_earning": 4499.1,
                "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCrJiTelv8n7m6l5k4j3h2g1f0d9s8a7q6w5e4r3t2y1u=s800"
            }
        ]
    }
]

# --- COUPONS ---
COUPONS = [
    {
        "id": "cpn-1",
        "code": "NOVA10",
        "discount_type": "percentage",  # percentage or fixed
        "discount_value": 10.0,
        "max_discount": 2000.0,
        "min_order_amount": 2999.0,
        "expires_at": "2026-12-31",
        "is_active": True,
        "usage_count": 412,
        "description": "10% off on all orders above ₹2,999"
    },
    {
        "id": "cpn-2",
        "code": "FESTIVE25",
        "discount_type": "percentage",
        "discount_value": 25.0,
        "max_discount": 1000.0,
        "min_order_amount": 1999.0,
        "expires_at": "2026-10-31",
        "is_active": True,
        "usage_count": 289,
        "description": "Festive Season: 25% off up to ₹1,000"
    },
    {
        "id": "cpn-3",
        "code": "FREESHIP",
        "discount_type": "fixed",
        "discount_value": 150.0,
        "max_discount": 150.0,
        "min_order_amount": 999.0,
        "expires_at": "2026-12-31",
        "is_active": True,
        "usage_count": 750,
        "description": "Free standard shipping on orders above ₹999"
    }
]

# --- NOTIFICATIONS ---
NOTIFICATIONS = [
    {
        "id": "notif-1",
        "recipient_role": "customer",
        "recipient_id": "user-cust-1",
        "title": "Order Delivered Successfully",
        "message": "Your order ORD-2024-8901 has been delivered to Oberoi Springs, Mumbai.",
        "icon": "local_shipping",
        "type": "success",
        "created_at": "2024-08-22 17:46",
        "is_read": False,
        "link": "/customer/orders/ORD-2024-8901"
    },
    {
        "id": "notif-2",
        "recipient_role": "seller",
        "recipient_id": "user-seller-1",
        "title": "New Order Received #ORD-2024-8903",
        "message": "Priya Patel placed an order for ZenFit Apex Smart Fitness Tracker. Please pack and prepare for pickup.",
        "icon": "shopping_cart",
        "type": "info",
        "created_at": "2024-08-30 16:42",
        "is_read": False,
        "link": "/seller/orders/ORD-2024-8903"
    },
    {
        "id": "notif-3",
        "recipient_role": "seller",
        "recipient_id": "user-seller-1",
        "title": "Payout Processed: ₹45,000",
        "message": "Your withdrawal request has been transferred to HDFC Bank A/C ending 8912.",
        "icon": "account_balance_wallet",
        "type": "success",
        "created_at": "2024-08-25 11:30",
        "is_read": True,
        "link": "/seller/payouts"
    },
    {
        "id": "notif-4",
        "recipient_role": "admin",
        "recipient_id": "user-admin-1",
        "title": "New Vendor Application Submitted",
        "message": "SmartGadgets Direct has submitted their GSTIN & KYC documents for platform verification.",
        "icon": "verified_user",
        "type": "warning",
        "created_at": "2024-08-29 09:10",
        "is_read": False,
        "link": "/admin/customers"
    }
]

# --- PAYOUTS (Seller withdrawals) ---
PAYOUTS = [
    {
        "id": "PAY-2024-101",
        "seller_id": "seller-1",
        "seller_name": "TechZone Electronics",
        "amount": 45000.0,
        "status": "completed",  # pending, processing, completed, rejected
        "requested_at": "2024-08-24 10:00",
        "processed_at": "2024-08-25 11:30",
        "bank_account": "HDFC Bank (A/C ...8912)",
        "reference_id": "NEFT-UTR-7829104928"
    },
    {
        "id": "PAY-2024-102",
        "seller_id": "seller-1",
        "seller_name": "TechZone Electronics",
        "amount": 25000.0,
        "status": "processing",
        "requested_at": "2024-08-30 14:00",
        "processed_at": None,
        "bank_account": "HDFC Bank (A/C ...8912)",
        "reference_id": "PENDING_BANK_BATCH"
    },
    {
        "id": "PAY-2024-201",
        "seller_id": "seller-2",
        "seller_name": "UrbanStyle India",
        "amount": 18500.0,
        "status": "completed",
        "requested_at": "2024-08-20 09:30",
        "processed_at": "2024-08-21 15:45",
        "bank_account": "ICICI Bank (A/C ...7654)",
        "reference_id": "IMPS-UTR-9918230192"
    }
]

# --- INVENTORY LOGS ---
INVENTORY_LOGS = [
    {
        "id": "inv-log-1",
        "product_id": "prod-1",
        "product_title": "Aura Pulse Studio Wireless Headphones",
        "sku": "NM-TECH-001-BLK",
        "seller_id": "seller-1",
        "type": "adjustment",
        "quantity_change": +30,
        "previous_stock": 15,
        "new_stock": 45,
        "reason": "Restocked from manufacturer shipment Batch #82",
        "adjusted_by": "Rajesh Kumar (TechZone)",
        "date": "2024-08-15 11:00"
    },
    {
        "id": "inv-log-2",
        "product_id": "prod-1",
        "product_title": "Aura Pulse Studio Wireless Headphones",
        "sku": "NM-TECH-001-BLK",
        "seller_id": "seller-1",
        "type": "sale",
        "quantity_change": -1,
        "previous_stock": 46,
        "new_stock": 45,
        "reason": "Order Fulfillment #ORD-2024-8901",
        "adjusted_by": "System Automated",
        "date": "2024-08-20 14:32"
    }
]

# --- RETURNS & REFUNDS ---
RETURNS = [
    {
        "id": "RET-2024-01",
        "order_id": "ORD-2024-8870",
        "customer_id": "user-cust-2",
        "customer_name": "Priya Patel",
        "seller_id": "seller-1",
        "seller_name": "TechZone Electronics",
        "product_id": "prod-5",
        "product_title": "SoundPulse Neo Portable Waterproof Speaker",
        "reason": "Defective Audio Jack / Crackling noise on Bluetooth",
        "amount": 3999.0,
        "status": "approved",  # requested, approved, rejected, refund_issued
        "request_date": "2024-08-18",
        "resolution_date": "2024-08-20",
        "comments": "Return pickup arranged via Delhivery. Refund will credit within 3 banking days."
    }
]

# --- SUPPORT TICKETS ---
SUPPORT_TICKETS = [
    {
        "id": "TCK-1001",
        "user_id": "user-cust-1",
        "user_name": "Aarav Sharma",
        "email": "customer@novamart.in",
        "subject": "Inquiry regarding extended warranty on ApexAudio Headphones",
        "category": "Warranty & Servicing",
        "status": "resolved",  # open, in_progress, resolved
        "created_at": "2024-08-24 10:15",
        "messages": [
            {"sender": "customer", "message": "Hi, how do I register for the 2nd year manufacturer warranty on my Aura Pulse?", "time": "2024-08-24 10:15"},
            {"sender": "support", "message": "Hello Aarav, you can register directly at apex-audio.com/warranty with your Nova Mart invoice #ORD-2024-8901.", "time": "2024-08-24 11:30"}
        ]
    },
    {
        "id": "TCK-2001",
        "user_id": "user-seller-1",
        "user_name": "Rajesh Kumar (TechZone)",
        "email": "seller@techzone.in",
        "subject": "Request for GST invoice correction on monthly commission report",
        "category": "Billing & Payouts",
        "status": "in_progress",
        "created_at": "2024-08-28 14:00",
        "messages": [
            {"sender": "seller", "message": "Please update our registered GSTIN on the July commission tax credit invoice.", "time": "2024-08-28 14:00"},
            {"sender": "support", "message": "We have forwarded this to our accounts department. Updated credit note will be issued in 24 hours.", "time": "2024-08-29 09:20"}
        ]
    }
]


def get_mock_db():
    """Returns deep copies of all initial mock entities so demo changes don't corrupt baseline."""
    return {
        "categories": deepcopy(CATEGORIES),
        "brands": deepcopy(BRANDS),
        "sellers": deepcopy(SELLERS),
        "users": deepcopy(USERS),
        "products": deepcopy(PRODUCTS),
        "reviews": deepcopy(REVIEWS),
        "orders": deepcopy(ORDERS),
        "coupons": deepcopy(COUPONS),
        "notifications": deepcopy(NOTIFICATIONS),
        "payouts": deepcopy(PAYOUTS),
        "inventory_logs": deepcopy(INVENTORY_LOGS),
        "returns": deepcopy(RETURNS),
        "support_tickets": deepcopy(SUPPORT_TICKETS),
    }
