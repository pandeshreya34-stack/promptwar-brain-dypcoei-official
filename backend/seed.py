import json
from database import db
from models import Place, Review, CivicReport, SafetyContact, User

def seed_database():
    if Place.query.first():
        print("Database already contains SEHER Pune places.")
        return
    print("Seeding SEHER Pune places, forts, hills, lakes, cafes with menus, transit vehicles...")

    # 1. Official Safety Contacts
    contacts = [
        SafetyContact(
            name="National Emergency Unified Number",
            department="Govt of India / Maharashtra Police & Emergency",
            phone="112",
            description="Unified emergency helpline for Police, Fire, and Ambulance across Pune and Maharashtra.",
            category="Helpline",
            is_emergency=True
        ),
        SafetyContact(
            name="Pune Women's Safety Helpline (Damini Squad)",
            department="Pune City Police Women Safety Cell",
            phone="1091",
            description="Dedicated 24/7 Pune police helpline connected to Damini Rapid Patrol Squads across city zones.",
            category="Women",
            is_emergency=True
        ),
        SafetyContact(
            name="National Women Helpline (WCD)",
            department="Ministry of Women and Child Development",
            phone="181",
            description="Toll-free 24-hour telecom service providing support, legal counsel, and shelter assistance to women in distress.",
            category="Women",
            is_emergency=True
        ),
        SafetyContact(
            name="Ambulance & Medical Emergency",
            department="Maharashtra Emergency Medical Services (MEMS)",
            phone="108",
            description="Free 24/7 emergency response service for medical emergencies, accidents, and trauma transfer.",
            category="Hospital",
            is_emergency=True
        ),
        SafetyContact(
            name="Pune City Police Control Room",
            department="Pune City Police Headquarters, Sadhu Vaswani Road",
            phone="020-26122880",
            description="Direct line to Pune Police Central Dispatch and city patrol coordination.",
            category="Police",
            is_emergency=False
        ),
        SafetyContact(
            name="Sassoon Hospital Trauma Center",
            department="Sassoon General Hospital, Sangamvadi",
            phone="020-26128000",
            description="Premier government tertiary care hospital and 24/7 trauma emergency care in Pune.",
            category="Hospital",
            is_emergency=True
        )
    ]
    for c in contacts:
        db.session.add(c)

    # 2. Comprehensive Pune Places Dataset
    places_data = [
        # ==========================================
        # FORTS (किल्ले)
        # ==========================================
        {
            "name": "Sinhagad Fort",
            "category": "history",
            "sub_category": "fort",
            "description": "Legendary hill fortress situated 30 km southwest of Pune on the Sahyadri ranges. Famously conquered by Maratha military leader Tanaji Malusare in the 1670 Battle of Sinhagad. Features Kalyan Darwaza, Pune Darwaza, Tanaji's Samadhi, Lokmanya Tilak's bungalow, and legendary local pitla bhakri & kanda bhaji.",
            "latitude": 18.3664,
            "longitude": 73.7558,
            "address": "Sinhagad Ghat Road, Thoptewadi, Pune 411025",
            "neighbourhood": "Sinhagad / Haveli",
            "images": [
                "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "05:00 AM – 06:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 50,
            "price_range": "₹50 (Vehicle Entry) / Free Walking Trek",
            "currency": "₹",
            "external_source_url": "https://pune.gov.in",
            "rating": 4.7,
            "review_count": 8900,
            "accessibility_features": ["Motorable ghat road up to top parking", "Stone rest pavilions along ridge"],
            "safety_features": ["Forest checkpost and security at base", "High daytime footfall of trekkers", "Guard rails along steep cliffs"],
            "reported_issues": ["Monsoon slippery stones along cliff edge", "Heavy weekend traffic on ghat road"],
            "data_source": "Archeological Survey of India & Maharashtra Forest Dept",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Authentic Pitla Bhakri with Thecha", "price": 120, "description": "Fresh hot jowar bhakri with gram flour pitla, spicy green mirchi thecha, and fresh onion curd", "is_veg": True, "bestseller": True},
                {"name": "Crispy Kanda Bhaji", "price": 60, "description": "Golden deep-fried spiced onion pakoras served steaming hot in the mountain breeze", "is_veg": True, "bestseller": True},
                {"name": "Matka Dahi (Earthen Pot Curd)", "price": 40, "description": "Rich thick local curd set in authentic miniature clay pot", "is_veg": True, "bestseller": True},
                {"name": "Taak (Spiced Buttermilk)", "price": 25, "description": "Fresh churned buttermilk with roasted cumin and coriander", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML Bus Route 50 (Swargate to Sinhagad Base)", "fare": "₹35", "details": "Direct electric buses every 30 minutes from Swargate Bus Stand to Donje Phata (Sinhagad base)."},
                {"type": "shared", "title": "Shared Jeep / Sumo from Donje Base", "fare": "₹60 per seat", "details": "Ferries visitors from base parking up the winding 9km ghat road to top fort gate."}
            ],
            "breakdown": {"review_confidence": 96, "info_freshness": 95, "price_reliability": 90, "accessibility_coverage": 65, "community_feedback": 95, "safety_coverage": 85}
        },
        {
            "name": "Torna Fort (Prachandagad)",
            "category": "history",
            "sub_category": "fort",
            "description": "The first fort captured by 16-year-old Chhatrapati Shivaji Maharaj in 1646, establishing the foundation of Hindavi Swarajya. Standing at 1,403 meters (highest in Pune district), Torna features massive Zunjar Machi and Budhla Machi fortifications, Mengai temple, and breathtaking Sahyadri views.",
            "latitude": 18.2764,
            "longitude": 73.6231,
            "address": "Velhe Taluka, Pune District 412212",
            "neighbourhood": "Velhe / Sahyadris",
            "images": [
                "https://images.unsplash.com/photo-1548013146-72479768bbaa?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "Open 24 hours (Daylight trekking recommended 06:00 AM – 06:00 PM)",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Entry (Trekking route)",
            "currency": "₹",
            "external_source_url": "https://maharashtratourism.gov.in",
            "rating": 4.8,
            "review_count": 4200,
            "accessibility_features": ["Moderate to challenging trekking route", "Base village homestays"],
            "safety_features": ["Velhe Police Station 4km at base", "Active trekking groups on weekends", "Clear trail markings"],
            "reported_issues": ["Steep rock patches near Bini Darwaza", "No night illumination"],
            "data_source": "Maharashtra Tourism & Trekker Federation",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Velhe Village Rustic Thali", "price": 150, "description": "Home-cooked jowar bhakri, gavran chicken or batata rassa, thecha, and dal", "is_veg": False, "bestseller": True},
                {"name": "Lemon Sharbat & Poha at Ridge Base", "price": 40, "description": "Fresh lemon mint energy drink and hot Maharashtrian kanda poha", "is_veg": True, "bestseller": True}
            ],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML Bus from Swargate to Velhe Village", "fare": "₹55", "details": "Direct state/PMPML buses depart Swargate terminal to Velhe village base."}
            ],
            "breakdown": {"review_confidence": 92, "info_freshness": 90, "price_reliability": 95, "accessibility_coverage": 50, "community_feedback": 94, "safety_coverage": 80}
        },
        {
            "name": "Purandar Fort",
            "category": "history",
            "sub_category": "fort",
            "description": "Historic twin fort (Purandar and Vajragad) nestled at 1,372 meters. Birthplace of Chhatrapati Sambhaji Maharaj and site of the historic 1665 Treaty of Purandar. Features Kedareshwar Temple, Bini Darwaza, Delhi Gate, and sprawling military cantonment grounds with cedar and pine trees.",
            "latitude": 18.2778,
            "longitude": 73.9789,
            "address": "Saswad, Purandar Taluka, Pune 412301",
            "neighbourhood": "Saswad / Purandar",
            "images": [
                "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "09:00 AM – 05:00 PM daily (ID proof mandatory for entry)",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Entry (Valid Govt ID Required)",
            "currency": "₹",
            "external_source_url": "https://asi.nic.in",
            "rating": 4.6,
            "review_count": 3100,
            "accessibility_features": ["Motorable road up to NCC Academy base", "Paved stone steps to lower ramparts"],
            "safety_features": ["Indian Armed Forces checkpoint at gate", "Clean military zone security", "Regular forest patrols"],
            "reported_issues": ["Entry closes promptly at 5:00 PM"],
            "data_source": "Ministry of Defence & Archaeological Survey of India",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "bus", "title": "MSRTC / PMPML Bus from Swargate to Saswad", "fare": "₹40", "details": "Bus to Saswad depot, followed by local auto-rickshaw to Purandar fort base."}
            ],
            "breakdown": {"review_confidence": 94, "info_freshness": 95, "price_reliability": 100, "accessibility_coverage": 70, "community_feedback": 92, "safety_coverage": 95}
        },

        # ==========================================
        # HILLS & TEKDIS (टेकड्या)
        # ==========================================
        {
            "name": "Parvati Hill & Temple Complex",
            "category": "history",
            "sub_category": "hill",
            "description": "Iconic hillock in the heart of southern Pune rising 2,100 feet above sea level. Ascend 103 well-laid stone steps to visit the historic 17th-century Devdeveshwar temple built by Peshwa Balaji Baji Rao, the Peshwa Museum, Kartikeya temple, and enjoy a stunning 360-degree panoramic view of the Pune city skyline.",
            "latitude": 18.4975,
            "longitude": 73.8485,
            "address": "Parvati Paytha, Sadashiv Peth, Pune 411009",
            "neighbourhood": "Parvati / Sadashiv Peth",
            "images": [
                "https://images.unsplash.com/photo-1609137144822-261c16827f80?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "05:00 AM – 08:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Entry (Peshwa Museum ₹20)",
            "currency": "₹",
            "external_source_url": "https://pmc.gov.in",
            "rating": 4.6,
            "review_count": 6800,
            "accessibility_features": ["Gradual wide stone steps with railings", "Seating platforms halfway up hill"],
            "safety_features": ["High family and senior citizen foot traffic morning & evening", "Parvati Police Chowki at base", "Illuminated pathways until 9 PM"],
            "reported_issues": ["103 steps require moderate fitness for seniors"],
            "data_source": "PMC Heritage Cell & Devdeveshwar Sansthan",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Swargate Station", "fare": "₹15", "details": "1.5 km from Swargate underground metro station. Direct autos available at ₹40."},
                {"type": "pmpml", "title": "PMPML Bus Stop: Parvati Paytha", "fare": "₹10", "details": "Buses from PMC, Deccan, and Swargate stop directly at the foothills."}
            ],
            "breakdown": {"review_confidence": 95, "info_freshness": 96, "price_reliability": 100, "accessibility_coverage": 75, "community_feedback": 95, "safety_coverage": 94}
        },
        {
            "name": "Vetal Tekdi (ARAI Hill)",
            "category": "history",
            "sub_category": "hill",
            "description": "The green lungs and highest natural point in Pune city limits (2,600 feet). Spanning lush wilderness between Kothrud and Senapati Bapat Road, Vetal Tekdi offers peaceful trails for morning walkers, birdwatchers, yoga practitioners, and sunset lovers. Home to the Vetoba temple, quarries, and peacocks.",
            "latitude": 18.5244,
            "longitude": 73.8188,
            "address": "ARAI Post, Paud Road / SB Road, Pune 411038",
            "neighbourhood": "Kothrud / SB Road",
            "images": [
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "05:00 AM – 07:30 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Public Reserve",
            "currency": "₹",
            "external_source_url": "https://forest.maharashtra.gov.in",
            "rating": 4.7,
            "review_count": 5400,
            "accessibility_features": ["Paved trail from ARAI gate", "Multiple access gates (MIT, SB Road, Law College)"],
            "safety_features": ["Thousands of regular morning & evening fitness enthusiasts", "Kothrud Police beat patrols", "Forest department personnel"],
            "reported_issues": ["Avoid remote solitary off-trails after sunset"],
            "data_source": "Maharashtra Forest Dept & Vetal Tekdi Bachao Samiti",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Ideal Colony / Vanaz Station", "fare": "₹15", "details": "2 km from Aqua line metro stations on Paud Road."},
                {"type": "pmpml", "title": "PMPML Buses to SB Road / MIT Kothrud", "fare": "₹10", "details": "Short walking distance from MIT college gate or Symbiosis SB Road."}
            ],
            "breakdown": {"review_confidence": 94, "info_freshness": 94, "price_reliability": 100, "accessibility_coverage": 70, "community_feedback": 96, "safety_coverage": 90}
        },
        {
            "name": "Taljai Hills & Eco Reserve",
            "category": "history",
            "sub_category": "hill",
            "description": "Dense reserve forest and serene biodiversity hill park in southern Pune. Features quiet walking circuits shaded by trees, a historic Taljai Devi temple, butterfly gardens, peacocks roaming freely in early mornings, and a fresh open-air gym.",
            "latitude": 18.4795,
            "longitude": 73.8445,
            "address": "Taljai Forest Area, Sahakar Nagar, Pune 411009",
            "neighbourhood": "Sahakar Nagar / Dhankawadi",
            "images": [
                "https://images.unsplash.com/photo-1511497584788-87676104235f?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "05:00 AM – 10:00 AM, 04:30 PM – 07:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Public Park",
            "currency": "₹",
            "external_source_url": "https://pmc.gov.in",
            "rating": 4.6,
            "review_count": 3900,
            "accessibility_features": ["Paved jogging paths", "Benches along tree canopy"],
            "safety_features": ["Gated security at park entry", "Family crowds during designated walking hours", "Sahakar Nagar police chowki 800m away"],
            "reported_issues": ["Park gates close strictly at 10 AM and 7 PM to protect wildlife"],
            "data_source": "Pune Municipal Corporation Garden Dept",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML Bus to Sahakar Nagar Terminal", "fare": "₹15", "details": "Buses terminate 400m from the Taljai entrance gate."}
            ],
            "breakdown": {"review_confidence": 92, "info_freshness": 93, "price_reliability": 100, "accessibility_coverage": 80, "community_feedback": 94, "safety_coverage": 92}
        },

        # ==========================================
        # LAKES & WATER BODIES (तलाव / धरणे)
        # ==========================================
        {
            "name": "Khadakwasla Dam & Lake Promenade",
            "category": "history",
            "sub_category": "lake",
            "description": "Pune's primary drinking water lifeline and favorite weekend sunset getaway. Built in 1879 across the Mutha River near the National Defence Academy (NDA). Features a lively lakefront promenade with roasted sweet corn (bhutta), bhelpuri, kulfi, and panoramic reflections of the Sinhagad hills over the vast lake.",
            "latitude": 18.4385,
            "longitude": 73.7635,
            "address": "Sinhagad Road, Khadakwasla, Pune 411024",
            "neighbourhood": "Khadakwasla / NDA",
            "images": [
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "06:00 AM – 08:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 50,
            "price_range": "Free Entry / Snacks ₹30–₹80",
            "currency": "₹",
            "external_source_url": "https://irrigation.maharashtra.gov.in",
            "rating": 4.5,
            "review_count": 8200,
            "accessibility_features": ["Paved sidewalk along Sinhagad road", "Accessible roadside viewing promenade"],
            "safety_features": ["NDA & Military security in vicinity", "Khadakwasla Police Chowki at chowk", "Warning buoys prohibiting deep swimming"],
            "reported_issues": ["Swimming in deep reservoir is strictly prohibited and dangerous"],
            "data_source": "Maharashtra Water Resources Dept & Pune Police",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Coal-Roasted Butta (Spiced Corn on the Cob)", "price": 40, "description": "Tender corn roasted on burning coals with fresh lemon, butter, and chili salt", "is_veg": True, "bestseller": True},
                {"name": "Puneri Sukka Bhel & Pani Puri", "price": 50, "description": "Crispy puffed rice with sev, onions, spicy mint chutney, and raw mango", "is_veg": True, "bestseller": True},
                {"name": "Malai Kulfi on Stick", "price": 40, "description": "Authentic chilled cardamom and pistachio milk kulfi", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML Direct Bus 50/51 from Swargate & Deccan", "fare": "₹25", "details": "Frequent direct electric bus service stops right at Khadakwasla Chowk promenade."}
            ],
            "breakdown": {"review_confidence": 95, "info_freshness": 95, "price_reliability": 95, "accessibility_coverage": 85, "community_feedback": 92, "safety_coverage": 88}
        },
        {
            "name": "Pashan Lake & Bird Sanctuary",
            "category": "history",
            "sub_category": "lake",
            "description": "Historic man-made lake constructed in the British era to supply water to Pashan and Governor's house. Surrounded by wetlands, bamboo clusters, and walking paths. A famous refuge for migratory birds like painted storks, purple moorhens, and herons.",
            "latitude": 18.5348,
            "longitude": 73.7845,
            "address": "Pashan Lake Road, Pashan, Pune 411021",
            "neighbourhood": "Pashan",
            "images": [
                "https://images.unsplash.com/photo-1511497584788-87676104235f?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "06:00 AM – 11:00 AM, 04:00 PM – 07:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Entry",
            "currency": "₹",
            "external_source_url": "https://pmc.gov.in",
            "rating": 4.3,
            "review_count": 2900,
            "accessibility_features": ["Level walkway along the western bank", "Birdwatching viewing decks"],
            "safety_features": ["PMC security guard at main entrance", "Fenced lake perimeter"],
            "reported_issues": ["Monsoon water hyacinth weed cleanup periodically underway"],
            "data_source": "PMC Environment Dept & Birdwatchers of Pune",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML Bus to Pashan Circle", "fare": "₹15", "details": "Buses from Pune Station and Shivajinagar to Pashan / Baner stop 600m away."}
            ],
            "breakdown": {"review_confidence": 90, "info_freshness": 92, "price_reliability": 100, "accessibility_coverage": 80, "community_feedback": 90, "safety_coverage": 86}
        },

        # ==========================================
        # HISTORICAL HERITAGE (वारसा स्थळे)
        # ==========================================
        {
            "name": "Shaniwar Wada",
            "category": "history",
            "sub_category": "heritage",
            "description": "Historic 18th-century fortification in the heart of Pune, built in 1732 as the seat of the Peshwa prime ministers of the Maratha Empire. Features sprawling stone ramparts, Delhi Gate, lotus fountain ruins, and landscaped gardens.",
            "latitude": 18.5195,
            "longitude": 73.8553,
            "address": "Shaniwar Peth, Pune, Maharashtra 411030",
            "neighbourhood": "Shaniwar Peth",
            "images": [
                "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "09:30 AM – 05:30 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 25,
            "price_range": "₹25 (Indian) / ₹300 (Foreign)",
            "currency": "₹",
            "external_source_url": "https://asi.nic.in",
            "rating": 4.4,
            "review_count": 4820,
            "accessibility_features": ["Step-free garden pathways", "Wide entrance gate", "Seating benches available"],
            "safety_features": ["ASI official security personnel at gates", "Faraskhana Police Station 300m away", "High pedestrian density during daylight", "Well-lit outer perimeter on Bajirao Road"],
            "reported_issues": ["Uneven stone steps leading to rampart viewing decks"],
            "data_source": "Archeological Survey of India & OpenStreetMap",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro PMC / Kasba Peth Station", "fare": "₹15", "details": "400m walk from PMC Metro Station on Purple line."},
                {"type": "pmpml", "title": "PMPML Shaniwar Wada Bus Terminal", "fare": "₹10", "details": "Major transit hub with direct buses connecting all Pune corners."}
            ],
            "breakdown": {"review_confidence": 92, "info_freshness": 90, "price_reliability": 95, "accessibility_coverage": 70, "community_feedback": 88, "safety_coverage": 85}
        },
        {
            "name": "Lal Mahal",
            "category": "history",
            "sub_category": "heritage",
            "description": "Reconstructed red palace commemorating Chhatrapati Shivaji Maharaj's early life in Pune, where he famously vanquished Mughal general Shaista Khan. Features detailed pictorial galleries and a statue of young Shivaji with Rajmata Jijau.",
            "latitude": 18.5186,
            "longitude": 73.8569,
            "address": "Kasba Peth, Near Shaniwar Wada, Pune 411011",
            "neighbourhood": "Kasba Peth",
            "images": [
                "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "09:00 AM – 01:00 PM, 04:00 PM – 08:00 PM",
            "last_verified": "October 2026",
            "approximate_cost": 5,
            "price_range": "₹5 Entry",
            "currency": "₹",
            "external_source_url": "https://pmc.gov.in",
            "rating": 4.2,
            "review_count": 1350,
            "accessibility_features": ["Ground floor exhibition gallery ramp", "Accessible ticketing booth"],
            "safety_features": ["Located on busy central Kasba Peth road", "CCTV surveillance inside premises", "PMC staff on duty during open hours"],
            "reported_issues": [],
            "data_source": "Pune Municipal Corporation & OpenStreetMap",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Kasba Peth Station", "fare": "₹15", "details": "300m walk across Shivaji Road from Kasba Peth Metro."}
            ],
            "breakdown": {"review_confidence": 88, "info_freshness": 92, "price_reliability": 98, "accessibility_coverage": 80, "community_feedback": 86, "safety_coverage": 84}
        },
        {
            "name": "Pataleshwar Cave Temple",
            "category": "history",
            "sub_category": "heritage",
            "description": "8th-century rock-cut monolithic cave temple dedicated to Lord Shiva, carved out of single basalt rock during the Rashtrakuta period. Includes a circular Nandi mandapa supported by giant stone pillars and shady banyan trees.",
            "latitude": 18.5284,
            "longitude": 73.8505,
            "address": "Jangali Maharaj Road, Shivajinagar, Pune 411005",
            "neighbourhood": "Shivajinagar",
            "images": [
                "https://images.unsplash.com/photo-1609137144822-261c16827f80?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "08:00 AM – 05:30 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Entry",
            "currency": "₹",
            "external_source_url": "https://asi.nic.in",
            "rating": 4.5,
            "review_count": 2980,
            "accessibility_features": ["Paved path from JM Road main gate", "Rest areas with stone benches"],
            "safety_features": ["Facing prominent, well-lit JM Road", "Shivajinagar Police Station 400m away", "Regular student and family foot traffic"],
            "reported_issues": ["Steep rock-cut steps down into the inner courtyard"],
            "data_source": "ASI Monument Record & OSM",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Shivajinagar Station", "fare": "₹15", "details": "600m from Shivajinagar multi-modal transit hub."},
                {"type": "pmpml", "title": "PMPML JM Road Bus Stop", "fare": "₹10", "details": "Buses stop directly outside Pataleshwar gate."}
            ],
            "breakdown": {"review_confidence": 90, "info_freshness": 90, "price_reliability": 100, "accessibility_coverage": 65, "community_feedback": 92, "safety_coverage": 88}
        },
        {
            "name": "Mahadji Shinde Chhatri",
            "category": "history",
            "sub_category": "heritage",
            "description": "Exquisite memorial dedicated to the Maratha commander Mahadji Shinde, constructed in Anglo-Rajasthani architectural style with intricate carvings, painted ceilings, stained glass windows, and a Shiva temple.",
            "latitude": 18.4965,
            "longitude": 73.8997,
            "address": "Wanawadi, Pune 411040",
            "neighbourhood": "Wanawadi",
            "images": [
                "https://images.unsplash.com/photo-1548013146-72479768bbaa?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "07:00 AM – 08:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 20,
            "price_range": "₹20 Entry",
            "currency": "₹",
            "external_source_url": "https://scindiaheritage.com",
            "rating": 4.3,
            "review_count": 820,
            "accessibility_features": ["Level courtyard entry", "Seated shaded areas"],
            "safety_features": ["Enclosed heritage campus with security guard", "Wanawadi Cantonment area with regular patrols"],
            "reported_issues": ["Steps to the inner sanctum temple hall"],
            "data_source": "Pune Heritage Cell & OSM",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML Bus to Shinde Chhatri Stop", "fare": "₹15", "details": "Buses from Swargate and Pune Station stop right at Wanawadi main road."}
            ],
            "breakdown": {"review_confidence": 84, "info_freshness": 85, "price_reliability": 90, "accessibility_coverage": 70, "community_feedback": 82, "safety_coverage": 80}
        },
        {
            "name": "Mahatma Phule Wada",
            "category": "history",
            "sub_category": "heritage",
            "description": "Historic residence of social reformers Mahatma Jyotirao Phule and Savitribai Phule, pioneer champions of girls' education and women's rights in India. Features preserved personal artifacts, photographs, and courtyard.",
            "latitude": 18.5085,
            "longitude": 73.8647,
            "address": "Ganj Peth, Pune 411042",
            "neighbourhood": "Ganj Peth",
            "images": [
                "https://images.unsplash.com/photo-1599839575945-a9e5af0c3fa5?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "09:00 AM – 06:00 PM (Closed Mondays)",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Free Entry",
            "currency": "₹",
            "external_source_url": "https://pmc.gov.in",
            "rating": 4.6,
            "review_count": 940,
            "accessibility_features": ["Ground floor ramp into memorial hall", "Tactile educational panels"],
            "safety_features": ["Dedicated state memorial curators", "CCTV coverage inside museum courtyard", "Close to commercial Bhavani Peth market"],
            "reported_issues": [],
            "data_source": "Maharashtra Directorate of Archaeology",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML Bus to Ganj Peth", "fare": "₹10", "details": "Short hop from Swargate or Pune Station."}
            ],
            "breakdown": {"review_confidence": 88, "info_freshness": 90, "price_reliability": 100, "accessibility_coverage": 85, "community_feedback": 94, "safety_coverage": 85}
        },

        # ==========================================
        # CAFES & RESTAURANTS WITH MENUS (कॅफे आणि उपहारगृहे)
        # ==========================================
        {
            "name": "Vaishali Restaurant",
            "category": "food",
            "sub_category": "restaurant",
            "description": "Pune's legendary and most celebrated garden cafe on FC Road since 1971. The beloved meeting point for college students, professors, artists, and families. Famous across India for its SPDP, Mysore Masala Dosa, and frothy South Indian filter coffee in a vibrant open courtyard.",
            "latitude": 18.5222,
            "longitude": 73.8415,
            "address": "1218/1, Fergusson College Road, Shivajinagar, Pune 411004",
            "neighbourhood": "FC Road",
            "images": [
                "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "07:00 AM – 11:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 200,
            "price_range": "₹150–₹350 per person",
            "currency": "₹",
            "external_source_url": "https://vaishalipune.com",
            "rating": 4.7,
            "review_count": 9200,
            "accessibility_features": ["Ground floor entrance with ramp access", "Spacious garden courtyard seating"],
            "safety_features": ["Active FC Road with 24/7 security & CCTV", "Deccan Police Chowki 200m away", "Zero tolerance harassment policy, extremely safe for solo women"],
            "reported_issues": ["Peak evening waiting queue (15–20 minutes)"],
            "data_source": "Direct Venue & Pune Heritage Food Survey",
            "confidence_level": "High",
            "menu_items": [
                {"name": "SPDP (Sev Potato Dahi Puri)", "price": 110, "description": "Vaishali's world-famous dish: Crisp puris stuffed with spiced boiled potatoes, chilled sweetened curd, tangy tamarind, and crunchy nylon sev", "is_veg": True, "bestseller": True},
                {"name": "Mysore Masala Dosa", "price": 140, "description": "Crispy golden crepe smeared with spicy red garlic-chili paste, stuffed with spiced potato masala and dollop of white butter", "is_veg": True, "bestseller": True},
                {"name": "South Indian Filter Coffee", "price": 65, "description": "Authentic aromatic Chicory-infused coffee frothed in traditional brass dabarah and tumbler", "is_veg": True, "bestseller": True},
                {"name": "Special Cheese Pav Bhaji", "price": 170, "description": "Rich mashed spiced vegetable gravy topped with melted cheddar cheese and buttered pav", "is_veg": True, "bestseller": True},
                {"name": "Onion Tomato Uttappam", "price": 130, "description": "Thick fluffy fermented rice pancake topped with fresh diced tomatoes, onions, and curry leaves", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Deccan Gymkhana Station", "fare": "₹15", "details": "400m walk from Deccan Gymkhana Metro Station."},
                {"type": "pmpml", "title": "PMPML Goodluck Chowk Stop", "fare": "₹10", "details": "100m from bus stops connecting all Pune routes."}
            ],
            "breakdown": {"review_confidence": 98, "info_freshness": 96, "price_reliability": 95, "accessibility_coverage": 85, "community_feedback": 98, "safety_coverage": 96}
        },
        {
            "name": "Cafe Goodluck",
            "category": "cafe",
            "sub_category": "cafe",
            "description": "Legendary Irani cafe established in 1935 at Goodluck Chowk. Renowned for bun maska, Irani chai, keema pav, caramel custard, and bustling intellectual conversations with students and artists across generations.",
            "latitude": 18.5173,
            "longitude": 73.8418,
            "address": "Fergusson College Road, Deccan Gymkhana, Pune 411004",
            "neighbourhood": "Deccan Gymkhana",
            "images": [
                "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "07:00 AM – 11:30 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 150,
            "price_range": "₹100–₹250 per person",
            "currency": "₹",
            "external_source_url": "https://cafegoodluck.in",
            "rating": 4.5,
            "review_count": 5200,
            "accessibility_features": ["Ground level corner entrance", "Wide front seating area"],
            "safety_features": ["Iconic junction with 24/7 visibility", "Deccan Police chowki within 100m", "Bustling crowds at all hours"],
            "reported_issues": [],
            "data_source": "Heritage & Community Survey",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Bun Maska (Warm Bun with Generous Butter)", "price": 55, "description": "Soft fresh Iranian bun sliced and generously slathered with pure salted Amul butter", "is_veg": True, "bestseller": True},
                {"name": "Irani Special Chai", "price": 35, "description": "Slow-brewed thick creamy Irani tea with condensed milk and subtle aromatic spices", "is_veg": True, "bestseller": True},
                {"name": "Mutton Keema Ghotala with Pav", "price": 220, "description": "Spicy minced mutton cooked with eggs, onions, and garam masala, served with warm pav", "is_veg": False, "bestseller": True},
                {"name": "Caramel Custard", "price": 90, "description": "Silky egg custard pudding with golden burnt caramel glaze", "is_veg": False, "bestseller": True},
                {"name": "Chicken Tikka Roll", "price": 180, "description": "Juicy charcoal-grilled chicken tikka rolled in flaky rumali roti with mint chutney", "is_veg": False, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Deccan Gymkhana Station", "fare": "₹15", "details": "Directly accessible via 250m walk from metro exit."},
                {"type": "pmpml", "title": "Goodluck Chowk PMPML Stop", "fare": "₹10", "details": "At the doorstep of the cafe."}
            ],
            "breakdown": {"review_confidence": 95, "info_freshness": 95, "price_reliability": 95, "accessibility_coverage": 85, "community_feedback": 96, "safety_coverage": 95}
        },
        {
            "name": "Vohuman Cafe",
            "category": "cafe",
            "sub_category": "cafe",
            "description": "Celebrated Irani breakfast paradise near Pune Railway Station, established by Late Uncle Hormuz Irani. Famous for mouth-watering cheese omelettes loaded with melted Amul cheese, soft bun maska, and strong tea in a friendly, no-frills setting.",
            "latitude": 18.5305,
            "longitude": 73.8765,
            "address": "Millennium Star, Near Ruby Hall Clinic, Dhole Patil Road, Pune 411001",
            "neighbourhood": "Dhole Patil Road / Station",
            "images": [
                "https://images.unsplash.com/photo-1525610553991-2bede1a236e2?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "06:00 AM – 07:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 160,
            "price_range": "₹100–₹250 per person",
            "currency": "₹",
            "external_source_url": "https://instagram.com/vohumancafe",
            "rating": 4.6,
            "review_count": 6400,
            "accessibility_features": ["Ground floor entrance with level flooring", "Spacious outdoor & indoor tables"],
            "safety_features": ["Opposite Ruby Hall Clinic with 24/7 hospital security", "Station Police beat nearby", "Very well-lit commercial avenue"],
            "reported_issues": [],
            "data_source": "Verified Food Directory",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Double Cheese Omelette", "price": 160, "description": "Fluffy 2-egg omelette overflowing with melted Amul cheese block, served with buttered toast", "is_veg": False, "bestseller": True},
                {"name": "Bun Maska with Jam", "price": 65, "description": "Classic Iranian bun loaded with butter and mixed fruit jam", "is_veg": True, "bestseller": True},
                {"name": "Irani Tea (Kadak Chai)", "price": 35, "description": "Signature strong, milky tea brewed to perfection", "is_veg": True, "bestseller": True},
                {"name": "Cheese Toast", "price": 95, "description": "Golden grilled bread with crispy melted cheese crust and pepper", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Ruby Hall Clinic Station", "fare": "₹15", "details": "100m from Ruby Hall Clinic Metro Station on Aqua line."},
                {"type": "train", "title": "Pune Junction Railway Station", "fare": "₹10", "details": "600m from Pune Station main concourse."}
            ],
            "breakdown": {"review_confidence": 96, "info_freshness": 95, "price_reliability": 96, "accessibility_coverage": 90, "community_feedback": 95, "safety_coverage": 94}
        },
        {
            "name": "Kayani Bakery",
            "category": "cafe",
            "sub_category": "bakery",
            "description": "Pune's most iconic Parsi heritage bakery founded in 1955 on East Street, Camp. Internationally renowned for melt-in-the-mouth buttery Shrewsbury biscuits, spongy mawa cakes, and brazil nut cookies.",
            "latitude": 18.5135,
            "longitude": 73.8785,
            "address": "6, East Street, Camp, Pune 411001",
            "neighbourhood": "Camp / East Street",
            "images": [
                "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "07:30 AM – 01:00 PM, 03:30 PM – 08:00 PM (Closed Sundays)",
            "last_verified": "October 2026",
            "approximate_cost": 250,
            "price_range": "₹150–₹350 takeaway",
            "currency": "₹",
            "external_source_url": "https://kayanibakerypune.com",
            "rating": 4.6,
            "review_count": 8100,
            "accessibility_features": ["Street-level shop front", "Wide pedestrian sidewalk on East Street"],
            "safety_features": ["Pune Cantonment Board patrolled area", "CCTV on busy East Street shopping district"],
            "reported_issues": ["Shrewsbury biscuits sell out early; cash or UPI preferred"],
            "data_source": "Camp Heritage Survey & Verified Seed",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Legendary Shrewsbury Biscuits (500g box)", "price": 260, "description": "Authentic rich butter shortbread biscuits that melt on your tongue. Pune's #1 edible souvenir", "is_veg": True, "bestseller": True},
                {"name": "Mawa Cake (Freshly Baked)", "price": 180, "description": "Rich, moist cardamom-scented cake made with evaporated milk solid (mawa)", "is_veg": True, "bestseller": True},
                {"name": "Walnut Cake Bar", "price": 220, "description": "Dense butter sponge cake loaded with premium walnuts", "is_veg": True, "bestseller": False},
                {"name": "Ginger Biscuits (250g)", "price": 140, "description": "Crunchy spicy ginger biscuits perfect with afternoon chai", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "pmpml", "title": "PMPML East Street / Camp Stop", "fare": "₹10", "details": "Direct bus connectivity from Swargate and Pune Station."}
            ],
            "breakdown": {"review_confidence": 98, "info_freshness": 96, "price_reliability": 98, "accessibility_coverage": 85, "community_feedback": 96, "safety_coverage": 95}
        },
        {
            "name": "Bedekar Tea Stall & Misal",
            "category": "food",
            "sub_category": "restaurant",
            "description": "The quintessential home of authentic Puneri Misal since 1948 in Narayan Peth. Known for its distinct mildly-sweet and fragrant spiced sample (tarri), fresh farsan, served traditionally with sliced white bread instead of pav.",
            "latitude": 18.5165,
            "longitude": 73.8510,
            "address": "418, Narayan Peth, Munjabacha Bol, Pune 411030",
            "neighbourhood": "Narayan Peth",
            "images": [
                "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "07:30 AM – 07:00 PM (Closed Mondays)",
            "last_verified": "October 2026",
            "approximate_cost": 120,
            "price_range": "₹80–₹160 per person",
            "currency": "₹",
            "external_source_url": "https://bedekarmisal.com",
            "rating": 4.4,
            "review_count": 5100,
            "accessibility_features": ["Ground floor shop entrance in historic Peth lane"],
            "safety_features": ["Safe bustling traditional commercial peth locality", "Vishrambaug Wada police chowki 300m away"],
            "reported_issues": ["Narrow peth lane; two-wheeler or walking recommended"],
            "data_source": "Old Pune Culinary Archives & Verified Seed",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Authentic Puneri Misal with Bread Slice", "price": 110, "description": "Crispy farsan, sprouted matki, and spiced gravy (tarri) accompanied by two slices of soft white bread", "is_veg": True, "bestseller": True},
                {"name": "Solkadhi (Kokum & Coconut Digestif)", "price": 45, "description": "Chilled pink digestive drink made from wild kokum fruit extract, garlic, and freshly squeezed coconut milk", "is_veg": True, "bestseller": True},
                {"name": "Kanda Poha", "price": 50, "description": "Flattened rice tempered with mustard, turmeric, green chilies, onions, and topped with grated coconut", "is_veg": True, "bestseller": False},
                {"name": "Masala Taak", "price": 30, "description": "Cooling spiced buttermilk with ginger and fresh coriander", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Kasba Peth / Budhwar Peth Station", "fare": "₹15", "details": "500m walk through the vibrant traditional peth streets."}
            ],
            "breakdown": {"review_confidence": 92, "info_freshness": 94, "price_reliability": 96, "accessibility_coverage": 75, "community_feedback": 92, "safety_coverage": 90}
        },
        {
            "name": "Sujata Mastani",
            "category": "food",
            "sub_category": "cafe",
            "description": "Originators of Pune's legendary royal dessert 'Mastani' since 1968, named after Peshwa Bajirao's queen Mastani. A decadent, thick, pure milk ice-cream shake garnished with generous dry fruits, tutti frutti, and a scoop of rich homemade ice cream.",
            "latitude": 18.5132,
            "longitude": 73.8515,
            "address": "Alka Talkies Chowk / Sadashiv Peth, Pune 411030",
            "neighbourhood": "Sadashiv Peth",
            "images": [
                "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "11:00 AM – 11:30 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 150,
            "price_range": "₹120–₹220 per glass",
            "currency": "₹",
            "external_source_url": "https://sujatamastani.com",
            "rating": 4.6,
            "review_count": 7800,
            "accessibility_features": ["Ground level counter and parlour seating"],
            "safety_features": ["Prominent Alka Chowk junction with heavy footfall until midnight", "Very bright street illumination"],
            "reported_issues": [],
            "data_source": "Pune Heritage Brands Directory",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Special Mango Mastani", "price": 150, "description": "Sujata's signature: Thick Alphonso mango shake topped with a rich mango ice-cream scoop, cashews, almonds, and pistachios", "is_veg": True, "bestseller": True},
                {"name": "Kesar Pista Mastani", "price": 160, "description": "Royal saffron and roasted pistachio thick milk shake with saffron ice cream", "is_veg": True, "bestseller": True},
                {"name": "Sitaphal Mastani (Seasonal)", "price": 170, "description": "Fresh custard apple fruit pulp whipped into velvety chilled cream with nuts", "is_veg": True, "bestseller": True},
                {"name": "Chocolate Brownie Mastani", "price": 180, "description": "Dutch cocoa shake layered with brownie bits, chocolate fudge, and nuts", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Deccan Gymkhana / Alka Chowk", "fare": "₹15", "details": "300m walk from Sambhaji Park & Alka Chowk metro exits."}
            ],
            "breakdown": {"review_confidence": 96, "info_freshness": 96, "price_reliability": 96, "accessibility_coverage": 85, "community_feedback": 96, "safety_coverage": 96}
        },
        {
            "name": "Asha Dining Hall",
            "category": "food",
            "sub_category": "restaurant",
            "description": "Celebrated Pune culinary institution serving authentic, hygienic unlimited Maharashtrian vegetarian thalis since 1949, including Varan Bhat, Puran Poli, spiced vegetables, and refreshing Taak.",
            "latitude": 18.5202,
            "longitude": 73.8415,
            "address": "Apte Road, Deccan Gymkhana, Pune 411004",
            "neighbourhood": "Deccan Gymkhana",
            "images": [
                "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "11:30 AM – 03:00 PM, 07:30 PM – 10:30 PM",
            "last_verified": "October 2026",
            "approximate_cost": 300,
            "price_range": "₹200–₹400 per person",
            "currency": "₹",
            "external_source_url": "https://ashadining.com",
            "rating": 4.5,
            "review_count": 3100,
            "accessibility_features": ["Ground floor entry with small curb", "Family-friendly spacious seating"],
            "safety_features": ["Very well-lit commercial Apte Road", "High family footfall until late evening", "Deccan Police Chowki within 250m"],
            "reported_issues": ["Peak weekend waiting queues (15–20 mins)"],
            "data_source": "Direct Venue & Community Verified",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Unlimited Authentic Maharashtrian Thali", "price": 320, "description": "Complete traditional feast: Varan Bhat with pure ghee, hot Puran Poli, 2 regional sabzis, spicy Aamti, Koshimbir, hot puris, and chilled Taak", "is_veg": True, "bestseller": True},
                {"name": "Puran Poli with Ghee (Per Piece Add-on)", "price": 60, "description": "Sweet chana dal and jaggery stuffed flatbread drenched in homemade pure desi ghee", "is_veg": True, "bestseller": True},
                {"name": "Ukdiche Modak (Pack of 2)", "price": 90, "description": "Steamed rice flour dumplings stuffed with grated fresh coconut, jaggery, cardamom, and nutmeg", "is_veg": True, "bestseller": True}
            ],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Deccan Gymkhana Station", "fare": "₹15", "details": "400m from Deccan Metro exit on Apte Road."}
            ],
            "breakdown": {"review_confidence": 94, "info_freshness": 92, "price_reliability": 92, "accessibility_coverage": 80, "community_feedback": 95, "safety_coverage": 90}
        },
        {
            "name": "Chaitanya Parathas",
            "category": "food",
            "sub_category": "restaurant",
            "description": "Pune student staple on FC Road offering over 40 varieties of hot, stuffed North Indian parathas served with white butter, curd, and dal makhani in generous, affordable portions.",
            "latitude": 18.5262,
            "longitude": 73.8410,
            "address": "Fergusson College Road, Shivajinagar, Pune 411004",
            "neighbourhood": "FC Road",
            "images": [
                "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "11:30 AM – 11:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 250,
            "price_range": "₹200–₹400 per person",
            "currency": "₹",
            "external_source_url": "https://chaitanyaparathas.com",
            "rating": 4.4,
            "review_count": 3890,
            "accessibility_features": ["Ground level dining area", "Nearby pedestrian sidewalk with ramps"],
            "safety_features": ["Extremely active FC Road student corridor", "Constant police patrols and CCTV on FC Road", "Safe for solo women dining even late at night"],
            "reported_issues": ["Limited car parking, public transit/walking recommended"],
            "data_source": "Verified Seed & Student Forum",
            "confidence_level": "High",
            "menu_items": [
                {"name": "Paneer Cheese Corn Paratha Combo", "price": 220, "description": "Gigantic hot stuffed paratha served with homemade white butter, fresh curd, and rich slow-cooked Dal Makhani", "is_veg": True, "bestseller": True},
                {"name": "Aloo Methi Garlic Paratha", "price": 160, "description": "Crispy spiced potato and fenugreek paratha with pickles and curd", "is_veg": True, "bestseller": True},
                {"name": "Thick Sweet Punjabi Lassi", "price": 80, "description": "Chilled sweet churned yogurt topped with thick malai layer", "is_veg": True, "bestseller": False}
            ],
            "transit_connections": [
                {"type": "metro", "title": "Pune Metro Deccan Station", "fare": "₹15", "details": "500m walk along FC Road commercial promenade."}
            ],
            "breakdown": {"review_confidence": 92, "info_freshness": 94, "price_reliability": 94, "accessibility_coverage": 80, "community_feedback": 92, "safety_coverage": 94}
        },

        # ==========================================
        # PUBLIC TRANSIT VEHICLES & HUBS (सार्वजनिक वाहतूक)
        # ==========================================
        {
            "name": "Pune Metro — Purple & Aqua Line (Maha Metro)",
            "category": "transport",
            "sub_category": "metro",
            "description": "Modern, air-conditioned, rapid transit network serving Pune and Pimpri-Chinchwad. Features sleek 3-coach trains with dedicated ladies coaches, automated ticketing, tactile paving for the visually impaired, elevators at all stations, and CCTV surveillance.",
            "latitude": 18.5320,
            "longitude": 73.8525,
            "address": "Shivajinagar Metro Terminal / Vanaz / PCMC / Swargate, Pune",
            "neighbourhood": "Shivajinagar / Central",
            "images": [
                "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "06:00 AM – 10:30 PM daily (Trains every 7-10 mins)",
            "last_verified": "October 2026",
            "approximate_cost": 20,
            "price_range": "₹10–₹35 per ticket",
            "currency": "₹",
            "external_source_url": "https://punemetrorail.org",
            "rating": 4.8,
            "review_count": 5200,
            "accessibility_features": [
                "100% barrier-free step-free boarding",
                "Elevators from street level to platform",
                "Tactile guiding paths for visually impaired",
                "Wheelchair locking zones inside trains",
                "Braille signage and audio announcements in Marathi, Hindi & English"
            ],
            "safety_features": [
                "Dedicated Reserved Ladies Coaches on all trains",
                "Maharashtra Security Force (MSF) security screening at all gates",
                "Emergency SOS talkback intercom buttons inside every coach",
                "360-degree high-definition CCTV coverage across entire network",
                "Bright LED illumination at all stations"
            ],
            "reported_issues": [],
            "data_source": "Maha Metro Pune Corporation",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "metro", "title": "Lines: Purple Line (PCMC to Swargate) & Aqua Line (Vanaz to Ramwadi)", "fare": "₹10 to ₹35", "details": "Seamless interchange at District Court Station."}
            ],
            "breakdown": {"review_confidence": 98, "info_freshness": 98, "price_reliability": 98, "accessibility_coverage": 98, "community_feedback": 98, "safety_coverage": 99}
        },
        {
            "name": "PMPML Rainbow BRTS & Electric City Buses",
            "category": "transport",
            "sub_category": "bus",
            "description": "Pune Mahanagar Parivahan Mahamandal Ltd (PMPML) operating modern zero-emission Electric Buses (Olectra/Tata) and Rainbow Bus Rapid Transit (BRTS) dedicated corridors connecting Swargate, Katraj, Hadapsar, Deccan, Viman Nagar, and Hinjawadi IT Park. Affordable daily passes available.",
            "latitude": 18.5015,
            "longitude": 73.8580,
            "address": "Swargate / Deccan / Katraj / Pune Station Terminals, Pune",
            "neighbourhood": "Citywide",
            "images": [
                "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "05:00 AM – 11:45 PM daily (Night buses on select routes)",
            "last_verified": "October 2026",
            "approximate_cost": 15,
            "price_range": "₹5–₹40 per ticket / Day Pass ₹50",
            "currency": "₹",
            "external_source_url": "https://pmpml.org",
            "rating": 4.3,
            "review_count": 7800,
            "accessibility_features": [
                "Low-floor wheelchair accessible ramps on electric e-buses",
                "Level platform boarding on Rainbow BRTS corridors",
                "Reserved seating for women and senior citizens"
            ],
            "safety_features": [
                "Tejaswini Women-Only Special Buses during peak hours",
                "GPS tracking and panic buttons on smart e-buses",
                "CCTV cameras inside bus cabins"
            ],
            "reported_issues": ["Peak office hours crowding on non-BRT arterial routes"],
            "data_source": "PMPML Official Transport Portal",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "bus", "title": "Over 350 city bus routes across PMC and PCMC", "fare": "₹5 to ₹40", "details": "Universal PMPML daily travel pass available for ₹50 at conductors."}
            ],
            "breakdown": {"review_confidence": 92, "info_freshness": 94, "price_reliability": 96, "accessibility_coverage": 85, "community_feedback": 88, "safety_coverage": 90}
        },
        {
            "name": "Pune Suburban EMU Local Train (Pune — Lonavala)",
            "category": "transport",
            "sub_category": "train",
            "description": "Central Railway Suburban electric multiple unit (EMU) local train service running from Pune Junction and Shivajinagar to Khadki, Dehu Road, Talegaon, and Lonavala. Ultra-affordable and punctual commuter link with ladies' special compartments.",
            "latitude": 18.5289,
            "longitude": 73.8744,
            "address": "Pune Junction Railway Station, Agarkar Nagar, Pune 411001",
            "neighbourhood": "Camp / Station",
            "images": [
                "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "04:30 AM – 12:30 AM daily",
            "last_verified": "October 2026",
            "approximate_cost": 15,
            "price_range": "₹10–₹20 per ticket",
            "currency": "₹",
            "external_source_url": "https://indianrailways.gov.in",
            "rating": 4.4,
            "review_count": 6200,
            "accessibility_features": [
                "Elevator and ramps to platforms at Pune Junction and Shivajinagar",
                "Accessible ticketing counters"
            ],
            "safety_features": [
                "Railway Protection Force (RPF) and GRP police squads",
                "Dedicated Ladies Compartments with night RPF escort",
                "CCTV monitoring on station concourses"
            ],
            "reported_issues": [],
            "data_source": "Central Railway Division Pune",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [
                {"type": "train", "title": "Pune Junction to Lonavala Suburban Line (64 km)", "fare": "₹15", "details": "Runs 44 daily services connecting Khadki, Pimpri, Chinchwad, Talegaon, and Lonavala."}
            ],
            "breakdown": {"review_confidence": 94, "info_freshness": 94, "price_reliability": 98, "accessibility_coverage": 85, "community_feedback": 90, "safety_coverage": 92}
        },

        # ==========================================
        # POLICE & SAFETY (पोलीस आणि सुरक्षा)
        # ==========================================
        {
            "name": "Faraskhana Police Station & Women Assistance Cell",
            "category": "safety",
            "sub_category": "police",
            "description": "Central historic police station serving Old Pune (Budhwar Peth, Shaniwar Wada area). Hosts a dedicated Women’s Help Desk and Damini Squad patrol station.",
            "latitude": 18.5172,
            "longitude": 73.8560,
            "address": "Budhwar Peth, Near Shaniwar Wada, Pune 411002",
            "neighbourhood": "Budhwar Peth",
            "images": [
                "https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "24/7 Open",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Public Police Station",
            "currency": "₹",
            "external_source_url": "https://punepolice.gov.in",
            "rating": 4.5,
            "review_count": 340,
            "accessibility_features": ["Ground floor public assistance counter", "Ramp at front entrance"],
            "safety_features": ["Armed police personnel 24/7", "Dedicated woman police officer on duty", "Direct emergency dispatch base"],
            "reported_issues": [],
            "data_source": "Pune City Police Official Portal & OSM",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [],
            "breakdown": {"review_confidence": 92, "info_freshness": 96, "price_reliability": 100, "accessibility_coverage": 85, "community_feedback": 90, "safety_coverage": 99}
        },
        {
            "name": "Deccan Gymkhana Police Station",
            "category": "safety",
            "sub_category": "police",
            "description": "Key police station covering FC Road, JM Road, Prabhat Road, and Law College Road. Very responsive to student and female tourist safety concerns.",
            "latitude": 18.5160,
            "longitude": 73.8400,
            "address": "Prabhat Road, Deccan Gymkhana, Pune 411004",
            "neighbourhood": "Deccan Gymkhana",
            "images": [
                "https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "24/7 Open",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Public Police Station",
            "currency": "₹",
            "external_source_url": "https://punepolice.gov.in",
            "rating": 4.6,
            "review_count": 410,
            "accessibility_features": ["Ground floor visitor room", "Paved parking access"],
            "safety_features": ["Constant patrol cars and mobile beat staff", "Immediate proximity to college campuses", "Dedicated women's assistance cell"],
            "reported_issues": [],
            "data_source": "Pune Police Directory",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [],
            "breakdown": {"review_confidence": 94, "info_freshness": 95, "price_reliability": 100, "accessibility_coverage": 85, "community_feedback": 92, "safety_coverage": 99}
        },

        # ==========================================
        # HOSPITALS (रुग्णालये)
        # ==========================================
        {
            "name": "Sassoon General Hospital & Trauma Centre",
            "category": "hospital",
            "sub_category": "hospital",
            "description": "Large state government teaching hospital affiliated with B. J. Medical College. Comprehensive 24/7 trauma care, emergency medicine, women’s obstetric wing, and ICU.",
            "latitude": 18.5265,
            "longitude": 73.8722,
            "address": "Station Road, Sangamvadi, Pune 411001",
            "neighbourhood": "Sangamvadi",
            "images": [
                "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "24/7 Emergency",
            "last_verified": "October 2026",
            "approximate_cost": 0,
            "price_range": "Govt Subsidized / Free Emergency",
            "currency": "₹",
            "external_source_url": "https://bjmcpune.org",
            "rating": 4.0,
            "review_count": 2100,
            "accessibility_features": ["Dedicated ambulance bay and stretcher ramps", "Multiple wheelchair access ramps", "Broad elevators"],
            "safety_features": ["24/7 hospital security police post on site", "CCTV monitoring across triage and wards", "Well-connected to Pune Station and main roads"],
            "reported_issues": ["Heavy OPD wait times during day hours"],
            "data_source": "Maharashtra Health Dept & OSM",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [],
            "breakdown": {"review_confidence": 88, "info_freshness": 95, "price_reliability": 100, "accessibility_coverage": 92, "community_feedback": 82, "safety_coverage": 94}
        },
        {
            "name": "Sahyadri Super Speciality Hospital (Deccan)",
            "category": "hospital",
            "sub_category": "hospital",
            "description": "Top-tier multispeciality hospital on Karve Road providing 24/7 cardiac, trauma, critical care, pediatric, and round-the-clock pharmacy services.",
            "latitude": 18.5079,
            "longitude": 73.8347,
            "address": "Plot No. 30 C, Erandwane, Karve Road, Pune 411004",
            "neighbourhood": "Erandwane / Deccan",
            "images": [
                "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "24/7 Emergency & Pharmacy",
            "last_verified": "October 2026",
            "approximate_cost": 800,
            "price_range": "Private Healthcare / Insurance cashless",
            "currency": "₹",
            "external_source_url": "https://sahyadrihospitals.com",
            "rating": 4.4,
            "review_count": 2850,
            "accessibility_features": ["Barrier-free automatic entrance doors", "Dedicated patient transfer elevators", "Wheelchairs readily available at entrance"],
            "safety_features": ["Round-the-clock private security and surveillance", "Direct emergency triage desk", "Well-lit main Karve Road location"],
            "reported_issues": [],
            "data_source": "Verified Seed",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [],
            "breakdown": {"review_confidence": 92, "info_freshness": 94, "price_reliability": 88, "accessibility_coverage": 96, "community_feedback": 90, "safety_coverage": 96}
        },

        # ==========================================
        # PUBLIC TOILETS & WATER (स्वच्छता व पिण्याचे पाणी)
        # ==========================================
        {
            "name": "PMC Smart Public Toilet & Water ATM (Deccan)",
            "category": "facility",
            "sub_category": "facility",
            "description": "Modern Pune Municipal Corporation automated hygiene facility featuring clean gender-segregated cubicles, sanitary napkin vending, disabled ramp, and chilled RO drinking water dispenser.",
            "latitude": 18.5175,
            "longitude": 73.8435,
            "address": "Deccan Gymkhana Bus Station Complex, Pune 411004",
            "neighbourhood": "Deccan Gymkhana",
            "images": [
                "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=80"
            ],
            "opening_hours": "06:00 AM – 11:00 PM daily",
            "last_verified": "October 2026",
            "approximate_cost": 5,
            "price_range": "₹5 per use / RO Water ₹1/litre",
            "currency": "₹",
            "external_source_url": "https://pmc.gov.in/swachh",
            "rating": 4.2,
            "review_count": 310,
            "accessibility_features": ["Gradual ramp access", "Wide ADA-compliant cabin with support grab bars", "Tactile pavement on entry"],
            "safety_features": ["Full-time female and male attendants", "Exterior CCTV surveillance on bus depot", "Emergency bell inside accessible cubicle"],
            "reported_issues": [],
            "data_source": "PMC Swachh Pune Initiative & OSM",
            "confidence_level": "High",
            "menu_items": [],
            "transit_connections": [],
            "breakdown": {"review_confidence": 85, "info_freshness": 95, "price_reliability": 100, "accessibility_coverage": 95, "community_feedback": 88, "safety_coverage": 90}
        }
    ]

    for p in places_data:
        place = Place(
            name=p["name"],
            category=p["category"],
            sub_category=p.get("sub_category"),
            description=p["description"],
            latitude=p["latitude"],
            longitude=p["longitude"],
            address=p["address"],
            neighbourhood=p["neighbourhood"],
            images=json.dumps(p["images"]),
            opening_hours=p["opening_hours"],
            last_verified=p["last_verified"],
            approximate_cost=p["approximate_cost"],
            price_range=p["price_range"],
            currency=p["currency"],
            external_source_url=p["external_source_url"],
            rating=p["rating"],
            review_count=p["review_count"],
            accessibility_features=json.dumps(p["accessibility_features"]),
            safety_features=json.dumps(p["safety_features"]),
            reported_issues=json.dumps(p["reported_issues"]),
            menu_items=json.dumps(p.get("menu_items", [])),
            transit_connections=json.dumps(p.get("transit_connections", [])),
            data_source=p["data_source"],
            confidence_level=p["confidence_level"],
            trust_score_breakdown=json.dumps(p["breakdown"])
        )
        place.calculate_trust_score()
        db.session.add(place)

    db.session.commit()

    # 3. Add Sample Reviews for Places
    sample_reviews = [
        ("Sinhagad Fort", "Aditya Kulkarni", 5, "Trekking up to Sinhagad in the early morning fog is unbeatable! The pitla bhakri and kanda bhaji at the top are world class. Wide stairs, plenty of families, and strong mobile connectivity near Tanaji memorial."),
        ("Parvati Hill & Temple Complex", "Prerana Deshpande", 5, "Climbing the 103 stone steps in the morning gives the most peaceful sunrise view over all of Pune! Very safe with plenty of morning fitness walkers and police chowki at the bottom."),
        ("Khadakwasla Dam & Lake Promenade", "Mihir Joshi", 5, "Hot coal-roasted butta and sukka bhel by the water as the sunset turns orange! PMPML direct bus from Swargate makes it very easy to reach."),
        ("Vaishali Restaurant", "Rhea Sengupta", 5, "The SPDP and filter coffee are sacred rituals of Pune! Always safe, bustling with cheerful student crowds, and extremely respectful staff."),
        ("Vohuman Cafe", "Varun Patil", 5, "Double cheese omelette with bun maska and hot Irani chai right next to Ruby Hall metro station. Fast service and authentic breakfast."),
        ("Shaniwar Wada", "Ananya Deshmukh", 5, "Visited with family. Beautiful stone gates and very clean gardens. Delhi gate is majestic. The area outside has good police presence and plenty of auto-rickshaws."),
        ("Pune Metro — Purple & Aqua Line (Maha Metro)", "Tanvi Agarwal", 5, "World-class metro transit! Spotless coaches, elevators at every gate, CCTV coverage, and ladies' dedicated coaches make night travel completely secure and fast.")
    ]

    for place_name, user, rating, comment in sample_reviews:
        p = Place.query.filter_by(name=place_name).first()
        if p:
            r = Review(
                place_id=p.id,
                user_name=user,
                rating=rating,
                comment=comment,
                is_demo=True,
                helpful_votes=15,
                reported_count=0,
                moderation_status='approved'
            )
            db.session.add(r)

    # 4. Civic Reports
    reports_data = [
        {
            "category": "Broken Streetlight",
            "description": "Streetlight pole #14 near Goodluck Chowk corner flickers and goes dark after 8 PM, making the pedestrian crossing dim.",
            "image_url": "https://images.unsplash.com/photo-1517646287270-a5a9ca602e5c?w=800&auto=format&fit=crop&q=80",
            "latitude": 18.5178,
            "longitude": 73.8422,
            "address": "Fergusson College Road, Deccan Gymkhana",
            "neighbourhood": "Deccan Gymkhana",
            "status": "In Progress",
            "is_anonymous": False,
            "reporter_name": "Radhika Sharma",
            "upvotes": 28
        },
        {
            "category": "Pothole",
            "description": "Deep pothole forming on the lane towards Shaniwar Wada western parking gate after recent monsoon showers.",
            "image_url": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=800&auto=format&fit=crop&q=80",
            "latitude": 18.5198,
            "longitude": 73.8548,
            "address": "Bajirao Road Junction, Shaniwar Peth",
            "neighbourhood": "Shaniwar Peth",
            "status": "Under Review",
            "is_anonymous": False,
            "reporter_name": "Siddharth Gaikwad",
            "upvotes": 19
        },
        {
            "category": "Damaged Footpath",
            "description": "Missing paver blocks and broken curb creating a trip hazard for elderly pedestrians near BMCC college corner.",
            "image_url": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?w=800&auto=format&fit=crop&q=80",
            "latitude": 18.5240,
            "longitude": 73.8360,
            "address": "BMCC Road, Shivajinagar",
            "neighbourhood": "Shivajinagar",
            "status": "Resolved",
            "is_anonymous": False,
            "reporter_name": "Citizen Safety Volunteer",
            "upvotes": 35
        }
    ]

    for r in reports_data:
        report = CivicReport(
            category=r["category"],
            description=r["description"],
            image_url=r["image_url"],
            latitude=r["latitude"],
            longitude=r["longitude"],
            address=r["address"],
            neighbourhood=r["neighbourhood"],
            status=r["status"],
            is_anonymous=r["is_anonymous"],
            reporter_name=r["reporter_name"],
            upvotes=r["upvotes"],
            is_demo=True
        )
        db.session.add(report)

    # 5. Demo Citizen User
    demo_user = User.query.filter_by(username="sehercitizen").first()
    if not demo_user:
        demo_user = User(
            username="sehercitizen",
            email="citizen@seherpune.org",
            role="citizen",
            emergency_phone="+91 98765 43210"
        )
        demo_user.set_password("pune2026")
        db.session.add(demo_user)

    db.session.commit()
    print("SEHER Database seeding completed successfully with forts, hills, lakes, cafes, and menus.")

if __name__ == '__main__':
    from flask import Flask
    from config import Config
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()
