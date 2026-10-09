from flask import Blueprint, request, jsonify
from models import Place

itinerary_bp = Blueprint('itinerary', __name__)

SAMPLE_ITINERARIES = [
    {
        "id": "pune-heritage-500",
        "title": "Pune Heritage Day under ₹500",
        "tagline": "Discover historic Maratha strongholds and legendary culinary stops without breaking the bank.",
        "target_budget": 500,
        "duration_hours": 6,
        "places_sequence": [
            {
                "place_name": "Shaniwar Wada",
                "approx_time": "10:00 AM - 11:30 AM",
                "estimated_cost": 25,
                "reason": "Iconic seat of the Maratha Peshwas with immense historical significance and modest ₹25 ticket."
            },
            {
                "place_name": "Lal Mahal",
                "approx_time": "11:45 AM - 12:45 PM",
                "estimated_cost": 5,
                "reason": "Directly across the road from Shaniwar Wada; minimal ₹5 entry with pictorial gallery of Chhatrapati Shivaji Maharaj."
            },
            {
                "place_name": "Asha Dining Hall",
                "approx_time": "01:15 PM - 02:30 PM",
                "estimated_cost": 300,
                "reason": "Authentic unlimited thali in safe, hygienic Deccan locality. Fills you up for the entire afternoon."
            },
            {
                "place_name": "Pataleshwar Cave Temple",
                "approx_time": "03:00 PM - 04:30 PM",
                "estimated_cost": 0,
                "reason": "Cool monolithic rock temple on JM Road; 100% free public access and peaceful green courtyard."
            }
        ],
        "total_estimated_cost_per_person": 330,
        "budget_remaining": 170,
        "transport_tip": "Use Pune Metro Purple Line (PMC Station to Deccan Gymkhana) or PMPML buses (₹10-₹15 per trip)."
    },
    {
        "id": "budget-food-trail",
        "title": "Pune Budget Food Exploration",
        "tagline": "Taste legendary Irani tea, student parathas, and authentic filter coffee across vibrant student lanes.",
        "target_budget": 450,
        "duration_hours": 5,
        "places_sequence": [
            {
                "place_name": "Goodluck Cafe",
                "approx_time": "08:30 AM - 10:00 AM",
                "estimated_cost": 120,
                "reason": "Historic Bun Maska and Irani Chai at Pune's most celebrated heritage crossroads."
            },
            {
                "place_name": "Pataleshwar Cave Temple",
                "approx_time": "10:30 AM - 11:45 AM",
                "estimated_cost": 0,
                "reason": "Refreshing cultural walk right next to JM Road food corridors."
            },
            {
                "place_name": "Chaitanya Parathas",
                "approx_time": "12:30 PM - 02:00 PM",
                "estimated_cost": 220,
                "reason": "Gigantic hot parathas loaded with butter, curd, and dal — supreme student favourite."
            }
        ],
        "total_estimated_cost_per_person": 340,
        "budget_remaining": 110,
        "transport_tip": "All stops are within walking or short auto distance in the Deccan / Shivajinagar belt."
    },
    {
        "id": "family-friendly-outing",
        "title": "Family-Friendly Pune Outing",
        "tagline": "Relaxed, safe, and family-approved heritage walk with guaranteed seating and hygienic facilities.",
        "target_budget": 800,
        "duration_hours": 7,
        "places_sequence": [
            {
                "place_name": "Shaniwar Wada",
                "approx_time": "09:30 AM - 11:30 AM",
                "estimated_cost": 50,
                "reason": "Spacious gardens with plenty of resting shade and verified security at the gates."
            },
            {
                "place_name": "PMC Smart Public Toilet & Water ATM (Deccan)",
                "approx_time": "12:00 PM - 12:15 PM",
                "estimated_cost": 10,
                "reason": "Verified clean sanitation stop and RO drinking water refill for children and elders."
            },
            {
                "place_name": "Asha Dining Hall",
                "approx_time": "12:30 PM - 02:00 PM",
                "estimated_cost": 600,
                "reason": "Comfortable family seating with traditional nutritious Maharashtrian cuisine."
            },
            {
                "place_name": "Mahadji Shinde Chhatri",
                "approx_time": "03:30 PM - 05:00 PM",
                "estimated_cost": 40,
                "reason": "Peaceful architectural gem in Wanawadi with open courtyards and intricate carvings."
            }
        ],
        "total_estimated_cost_per_person": 700,
        "budget_remaining": 100,
        "transport_tip": "Auto-rickshaw or app cab recommended for family comfort between Deccan and Wanawadi."
    },
    {
        "id": "student-weekend-exploration",
        "title": "Student Weekend Exploration",
        "tagline": "Ultra-low-cost Pune discovery designed for students, hostellers, and young explorers.",
        "target_budget": 250,
        "duration_hours": 4,
        "places_sequence": [
            {
                "place_name": "Mahatma Phule Wada",
                "approx_time": "10:00 AM - 11:30 AM",
                "estimated_cost": 0,
                "reason": "Free inspiring memorial honoring pioneers of social reform and education."
            },
            {
                "place_name": "Goodluck Cafe",
                "approx_time": "12:00 PM - 01:15 PM",
                "estimated_cost": 110,
                "reason": "Pocket-friendly Irani bun maska and lively campus ambiance."
            },
            {
                "place_name": "Chaitanya Parathas",
                "approx_time": "01:30 PM - 02:45 PM",
                "estimated_cost": 130,
                "reason": "Shared paratha combos keep meal cost under ₹130 per person."
            }
        ],
        "total_estimated_cost_per_person": 240,
        "budget_remaining": 10,
        "transport_tip": "Hop on the Pune Metro Purple Line with your student travel card."
    },
    {
        "id": "accessible-city-outing",
        "title": "Accessible City Outing",
        "tagline": "Curated for wheelchair users and mobility-assisted travellers with step-free access and modern facilities.",
        "target_budget": 600,
        "duration_hours": 5,
        "places_sequence": [
            {
                "place_name": "Shivajinagar Metro & Suburban Station",
                "approx_time": "10:00 AM - 10:45 AM",
                "estimated_cost": 25,
                "reason": "100% barrier-free transit with elevators, tactile pavers, and wide accessible faregates."
            },
            {
                "place_name": "Mahatma Phule Wada",
                "approx_time": "11:15 AM - 12:45 PM",
                "estimated_cost": 0,
                "reason": "Ground floor ramp access into the historic memorial hall."
            },
            {
                "place_name": "PMC Smart Public Toilet & Water ATM (Deccan)",
                "approx_time": "01:00 PM - 01:20 PM",
                "estimated_cost": 5,
                "reason": "Certified ramped entrance, wide ADA cabin with grab bars, and emergency assistance bell."
            },
            {
                "place_name": "Hotel Shreyas",
                "approx_time": "01:30 PM - 03:00 PM",
                "estimated_cost": 350,
                "reason": "Elevator access, ramped lobby, and accessible ground-floor dining room."
            }
        ],
        "total_estimated_cost_per_person": 380,
        "budget_remaining": 220,
        "transport_tip": "Accessible Pune Metro stations offer step-free train boarding."
    }
]

@itinerary_bp.route('/itinerary', methods=['GET', 'POST'])
def itinerary_planner():
    if request.method == 'GET':
        sample_id = request.args.get('sample_id')
        if sample_id:
            for s in SAMPLE_ITINERARIES:
                if s["id"] == sample_id:
                    return jsonify({"itinerary": s})
            return jsonify({"error": "Sample itinerary not found"}), 404

        return jsonify({
            "sample_itineraries": SAMPLE_ITINERARIES
        })

    # POST: Custom budget planner
    data = request.get_json() or {}
    start_location = data.get('start_location', 'Deccan Gymkhana')
    available_hours = float(data.get('available_hours', 5))
    total_budget = int(data.get('total_budget', 500))
    people_count = max(1, int(data.get('people_count', 1)))
    preferred_categories = data.get('categories', ['history', 'food'])
    transport_mode = data.get('transport_mode', 'metro_bus')
    accessible_only = data.get('accessible_only', False)

    per_person_budget = total_budget // people_count

    # Select fitting places
    query = Place.query
    if preferred_categories:
        query = query.filter(Place.category.in_(preferred_categories))

    candidate_places = query.order_by(Place.rating.desc()).all()

    selected = []
    cumulative_cost = 0

    for p in candidate_places:
        p_dict = p.to_dict()
        if accessible_only and len(p_dict['accessibility_features']) == 0:
            continue

        cost = p_dict['approximate_cost']
        if cumulative_cost + cost <= per_person_budget and len(selected) < min(4, int(available_hours)):
            cumulative_cost += cost
            selected.append({
                "place_id": p.id,
                "name": p.name,
                "category": p.category,
                "neighbourhood": p.neighbourhood,
                "approximate_cost": cost,
                "trust_score": p.trust_score,
                "rating": p.rating,
                "recommendation_reason": f"High trust rating ({p.trust_score}/100) and fits budget threshold."
            })

    budget_remaining = per_person_budget - cumulative_cost

    custom_plan = {
        "title": f"Custom Plan from {start_location} ({people_count} Person{'s' if people_count > 1 else ''})",
        "start_location": start_location,
        "available_hours": available_hours,
        "total_budget": total_budget,
        "budget_per_person": per_person_budget,
        "estimated_cost_per_person": cumulative_cost,
        "budget_remaining_per_person": budget_remaining,
        "transport_mode": transport_mode,
        "recommended_stops": selected,
        "total_stops": len(selected),
        "notes": "Estimates exclude auto-rickshaw/taxi fares and personal shopping. Prices last verified October 2026."
    }

    return jsonify({"itinerary": custom_plan})
