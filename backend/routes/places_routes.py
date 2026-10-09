import re
import json
from flask import Blueprint, request, jsonify
from database import db
from models import Place, Review, SavedPlace

places_bp = Blueprint('places', __name__)

import math

def calc_dist(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

@places_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = [
        {"id": "all", "name": "All Places", "icon": "MapPin", "count": Place.query.count()},
        {"id": "history", "name": "History & Heritage", "icon": "Landmark", "count": Place.query.filter_by(category="history").count()},
        {"id": "fort", "name": "Forts & Treks (किल्ले)", "icon": "Castle", "count": Place.query.filter((Place.category=="fort") | (Place.sub_category=="fort")).count()},
        {"id": "hill", "name": "Hills & Tekdis (टेकड्या)", "icon": "Mountain", "count": Place.query.filter((Place.category=="hill") | (Place.sub_category=="hill")).count()},
        {"id": "lake", "name": "Lakes & Water Bodies", "icon": "Waves", "count": Place.query.filter((Place.category=="lake") | (Place.sub_category=="lake")).count()},
        {"id": "food", "name": "Budget Food", "icon": "Utensils", "count": Place.query.filter_by(category="food").count()},
        {"id": "cafe", "name": "Cafes & Bakeries", "icon": "Coffee", "count": Place.query.filter_by(category="cafe").count()},
        {"id": "hotel", "name": "Hotels & Stays", "icon": "Hotel", "count": Place.query.filter_by(category="hotel").count()},
        {"id": "facility", "name": "Public Facilities", "icon": "Droplet", "count": Place.query.filter_by(category="facility").count()},
        {"id": "safety", "name": "Police & Safety", "icon": "Shield", "count": Place.query.filter_by(category="safety").count()},
        {"id": "hospital", "name": "Hospitals & Care", "icon": "Activity", "count": Place.query.filter_by(category="hospital").count()},
        {"id": "transport", "name": "Public Transport", "icon": "Bus", "count": Place.query.filter_by(category="transport").count()}
    ]
    return jsonify({"categories": categories})

@places_bp.route('/places', methods=['GET'])
def get_places():
    category = request.args.get('category', '').strip().lower()
    budget = request.args.get('budget', type=int)
    neighbourhood = request.args.get('neighbourhood', '').strip()
    accessible_only = request.args.get('accessible', '').lower() in ['true', '1']
    search_q = request.args.get('q', '').strip().lower()

    query = Place.query

    if category and category != 'all':
        if category in ['fort', 'hill', 'lake']:
            query = query.filter((Place.category == category) | (Place.sub_category == category))
        else:
            query = query.filter(Place.category == category)

    if budget is not None:
        query = query.filter(Place.approximate_cost <= budget)

    if neighbourhood:
        query = query.filter(Place.neighbourhood.ilike(f'%{neighbourhood}%'))

    places = query.all()

    # In-memory filtering for search & accessibility JSON
    results = []
    for p in places:
        data = p.to_dict()

        if accessible_only and len(data['accessibility_features']) == 0:
            continue

        if search_q:
            text_corpus = f"{p.name} {p.description} {p.address} {p.neighbourhood} {p.category} {p.sub_category or ''}".lower()
            if search_q not in text_corpus:
                continue

        results.append(data)

    return jsonify({
        "total": len(results),
        "places": results,
        "is_demo_data": True
    })

@places_bp.route('/places/<int:place_id>', methods=['GET'])
def get_place_detail(place_id):
    place = Place.query.get_or_404(place_id)
    reviews = Review.query.filter_by(place_id=place_id, moderation_status='approved').order_by(Review.created_at.desc()).all()

    data = place.to_dict()
    data['reviews'] = [r.to_dict() for r in reviews]

    # Calculate nearby heritage spots, nearby cafes, and nearby transit
    all_other_places = Place.query.filter(Place.id != place.id).all()
    heritage_candidates = []
    cafe_candidates = []
    transit_candidates = []

    for other in all_other_places:
        d = calc_dist(place.latitude, place.longitude, other.latitude, other.longitude)
        other_dict = other.to_dict()
        other_dict['distance_km'] = d

        # Heritage, forts, hills, lakes
        if other.category in ['history', 'fort', 'hill', 'lake'] or other.sub_category in ['fort', 'hill', 'lake', 'heritage']:
            heritage_candidates.append(other_dict)

        # Cafes & dining
        if other.category in ['food', 'cafe'] or other.sub_category in ['cafe', 'restaurant', 'bakery']:
            cafe_candidates.append(other_dict)

        # Transit (Metro, Bus, Train)
        if other.category == 'transport':
            transit_candidates.append(other_dict)

    heritage_candidates.sort(key=lambda x: x['distance_km'])
    cafe_candidates.sort(key=lambda x: x['distance_km'])
    transit_candidates.sort(key=lambda x: x['distance_km'])

    data['nearby_heritage_spots'] = heritage_candidates[:4]
    data['nearby_cafes'] = cafe_candidates[:4]
    data['nearby_transit'] = transit_candidates[:3]

    return jsonify({
        "place": data,
        "is_demo_data": True
    })

@places_bp.route('/search', methods=['GET'])
def natural_search():
    """
    Handles natural language queries such as:
    'Find historical places and affordable food under ₹500 near Shaniwar Wada, with a safer route'
    """
    raw_query = request.args.get('q', '').strip()
    if not raw_query:
        return jsonify({"places": [], "parsed_intent": {}, "message": "Query string is empty"})

    q_lower = raw_query.lower()

    # 1. Parse budget: looks for e.g. "under 500", "under ₹500", "< 300", "500 rs"
    budget_match = re.search(r'(?:under|below|<|upto|within|budget of)?\s*(?:₹|rs\.?|inr)?\s*(\d+)', q_lower)
    budget = None
    if budget_match and int(budget_match.group(1)) > 10:
        budget = int(budget_match.group(1))

    # 2. Parse categories
    target_categories = []
    if any(k in q_lower for k in ['fort', 'gad', 'sinhagad', 'torna', 'purandar']):
        target_categories.extend(['fort', 'history'])
    if any(k in q_lower for k in ['hill', 'tekdi', 'parvati', 'vetal', 'taljai']):
        target_categories.extend(['hill', 'nature'])
    if any(k in q_lower for k in ['lake', 'talav', 'khadakwasla', 'pashan', 'dam', 'water']):
        target_categories.extend(['lake', 'nature'])
    if any(k in q_lower for k in ['history', 'historical', 'wada', 'mahal', 'temple', 'heritage', 'chhatri']):
        target_categories.append('history')
    if any(k in q_lower for k in ['food', 'restaurant', 'thali', 'dinner', 'lunch', 'eat', 'paratha', 'meal', 'breakfast', 'misal']):
        target_categories.append('food')
    if any(k in q_lower for k in ['cafe', 'coffee', 'chai', 'tea', 'bakery', 'shrewsbury', 'bun maska', 'irani']):
        target_categories.append('cafe')
    if any(k in q_lower for k in ['hotel', 'stay', 'room', 'lodge']):
        target_categories.append('hotel')
    if any(k in q_lower for k in ['toilet', 'washroom', 'water', 'atm', 'facility', 'restroom']):
        target_categories.append('facility')
    if any(k in q_lower for k in ['safety', 'police', 'safe', 'chowki', 'cop']):
        target_categories.append('safety')
    if any(k in q_lower for k in ['hospital', 'clinic', 'doctor', 'medical', 'emergency']):
        target_categories.append('hospital')
    if any(k in q_lower for k in ['metro', 'bus', 'train', 'transport', 'station', 'pmpml', 'local']):
        target_categories.append('transport')

    # 3. Detect landmark anchors
    anchor_name = None
    if 'shaniwar wada' in q_lower:
        anchor_name = "Shaniwar Wada"
    elif 'deccan' in q_lower or 'fc road' in q_lower or 'jm road' in q_lower:
        anchor_name = "Deccan Gymkhana"
    elif 'viman nagar' in q_lower:
        anchor_name = "Viman Nagar"
    elif 'station' in q_lower or 'railway' in q_lower:
        anchor_name = "Pune Junction"

    # Query DB
    all_places = Place.query.all()
    matched = []

    for p in all_places:
        score = 0
        p_dict = p.to_dict()

        if target_categories:
            if p.category in target_categories or (p.sub_category and p.sub_category in target_categories):
                score += 5
        else:
            score += 1

        if budget is not None:
            if p.approximate_cost <= budget:
                score += 3
            else:
                score -= 3

        if anchor_name and (anchor_name.lower() in p.name.lower() or anchor_name.lower() in p.neighbourhood.lower() or anchor_name.lower() in p.address.lower()):
            score += 4

        # Keyword match bonus
        for word in q_lower.split():
            if len(word) > 3 and word in f"{p.name} {p.description}".lower():
                score += 1

        if score > 0:
            matched.append((score, p_dict))

    matched.sort(key=lambda x: x[0], reverse=True)
    results = [item[1] for item in matched]

    parsed_intent = {
        "budget_limit": budget,
        "categories": target_categories,
        "anchor_location": anchor_name,
        "suggested_route_preference": "safety-informed" if "safe" in q_lower else "fastest"
    }

    return jsonify({
        "query": raw_query,
        "parsed_intent": parsed_intent,
        "total": len(results),
        "places": results,
        "is_demo_data": True
    })

@places_bp.route('/reviews', methods=['GET', 'POST'])
def handle_reviews():
    if request.method == 'GET':
        place_id = request.args.get('place_id', type=int)
        query = Review.query
        if place_id:
            query = query.filter_by(place_id=place_id)
        reviews = query.filter_by(moderation_status='approved').order_by(Review.created_at.desc()).all()
        return jsonify({
            "total": len(reviews),
            "reviews": [r.to_dict() for r in reviews],
            "is_demo_data": True
        })

    # POST new review
    data = request.get_json() or {}
    place_id = data.get('place_id')
    user_name = data.get('user_name', 'Pune Visitor').strip()
    rating = data.get('rating', 5)
    comment = data.get('comment', '').strip()

    if not place_id or not comment:
        return jsonify({"error": "Place ID and review comment are required"}), 400

    place = Place.query.get(place_id)
    if not place:
        return jsonify({"error": "Place not found"}), 404

    # Spam / Duplicate basic check
    existing = Review.query.filter_by(place_id=place_id, user_name=user_name, comment=comment).first()
    if existing:
        return jsonify({"error": "Duplicate review detected"}), 400

    review = Review(
        place_id=place_id,
        user_name=user_name,
        rating=max(1, min(5, int(rating))),
        comment=comment,
        is_demo=False,
        helpful_votes=0,
        moderation_status='approved'
    )
    db.session.add(review)

    # Recalculate place rating and review count
    all_place_reviews = Review.query.filter_by(place_id=place_id, moderation_status='approved').all()
    place.review_count = len(all_place_reviews) + 1
    total_stars = sum(r.rating for r in all_place_reviews) + review.rating
    place.rating = total_stars / place.review_count
    place.calculate_trust_score()

    db.session.commit()

    return jsonify({
        "message": "Review submitted successfully and reflected in trust indicators",
        "review": review.to_dict()
    }), 201

@places_bp.route('/reviews/<int:review_id>/vote', methods=['POST'])
def vote_review(review_id):
    review = Review.query.get_or_404(review_id)
    review.helpful_votes += 1
    db.session.commit()
    return jsonify({"message": "Helpful vote recorded", "helpful_votes": review.helpful_votes})

@places_bp.route('/reviews/<int:review_id>/report', methods=['POST'])
def report_review(review_id):
    review = Review.query.get_or_404(review_id)
    review.reported_count += 1
    if review.reported_count >= 3:
        review.moderation_status = 'flagged'
    db.session.commit()
    return jsonify({"message": "Review flagged for community moderation", "status": review.moderation_status})

@places_bp.route('/saved-places', methods=['GET', 'POST', 'DELETE'])
def saved_places():
    if request.method == 'GET':
        saved = SavedPlace.query.order_by(SavedPlace.created_at.desc()).all()
        return jsonify({
            "saved_places": [s.to_dict() for s in saved]
        })

    if request.method == 'POST':
        data = request.get_json() or {}
        place_id = data.get('place_id')
        notes = data.get('notes', '')
        if not place_id:
            return jsonify({"error": "Place ID required"}), 400

        existing = SavedPlace.query.filter_by(place_id=place_id).first()
        if existing:
            return jsonify({"message": "Place already saved", "saved": existing.to_dict()}), 200

        saved = SavedPlace(place_id=place_id, notes=notes)
        db.session.add(saved)
        db.session.commit()
        return jsonify({"message": "Place saved", "saved": saved.to_dict()}), 201

    if request.method == 'DELETE':
        place_id = request.args.get('place_id', type=int)
        if not place_id:
            return jsonify({"error": "Place ID required"}), 400
        saved = SavedPlace.query.filter_by(place_id=place_id).first()
        if saved:
            db.session.delete(saved)
            db.session.commit()
        return jsonify({"message": "Place removed from saved"})
