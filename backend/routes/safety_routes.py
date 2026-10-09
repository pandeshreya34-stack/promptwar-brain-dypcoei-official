from flask import Blueprint, request, jsonify
from database import db
from models import SafetyContact, TrustedContact, Place
import math

safety_bp = Blueprint('safety', __name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@safety_bp.route('/safety-contacts', methods=['GET'])
def get_safety_contacts():
    category = request.args.get('category')
    query = SafetyContact.query
    if category:
        query = query.filter_by(category=category)
    contacts = query.all()
    return jsonify({
        "contacts": [c.to_dict() for c in contacts],
        "important_note": "For immediate police or medical assistance, dial 112 or 1091 immediately."
    })

@safety_bp.route('/trusted-contacts', methods=['GET', 'POST', 'DELETE'])
def manage_trusted_contacts():
    if request.method == 'GET':
        contacts = TrustedContact.query.all()
        return jsonify({
            "contacts": [c.to_dict() for c in contacts]
        })

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        relationship = data.get('relationship', 'Family')
        is_primary = data.get('is_primary', False)

        if not name or not phone:
            return jsonify({"error": "Name and phone number are required"}), 400

        contact = TrustedContact(
            name=name,
            phone=phone,
            relationship=relationship,
            is_primary=is_primary
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({
            "message": "Trusted contact added successfully",
            "contact": contact.to_dict()
        }), 201

    if request.method == 'DELETE':
        cid = request.args.get('id', type=int)
        if not cid:
            return jsonify({"error": "Contact ID required"}), 400
        contact = TrustedContact.query.get_or_404(cid)
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Trusted contact removed"})

@safety_bp.route('/nearby-emergency', methods=['GET'])
def nearby_emergency():
    """Returns nearest police stations and hospitals to user's coordinate"""
    try:
        lat = float(request.args.get('lat', 18.5204))
        lng = float(request.args.get('lng', 73.8567))
    except ValueError:
        lat, lng = 18.5204, 73.8567

    safety_places = Place.query.filter(Place.category.in_(['safety', 'hospital'])).all()
    results = []

    for p in safety_places:
        dist = round(haversine_distance(lat, lng, p.latitude, p.longitude), 2)
        p_data = p.to_dict()
        p_data['distance_km'] = dist
        results.append(p_data)

    results.sort(key=lambda x: x['distance_km'])

    return jsonify({
        "user_coords": {"lat": lat, "lng": lng},
        "nearby": results[:6]
    })

@safety_bp.route('/sos-trigger', methods=['POST'])
def trigger_sos():
    """
    Transparent SOS endpoint.
    Per prompt guidelines:
    'The SOS button must never falsely claim to contact police or dispatch help unless a real authorized integration exists.
    If emergency integration is unavailable, immediately offer the official phone-call option and explain the limitation.'
    """
    data = request.get_json() or {}
    lat = data.get('lat')
    lng = data.get('lng')
    user_name = data.get('user_name', 'User')

    contacts = TrustedContact.query.all()
    trusted_phones = [c.phone for c in contacts]

    sms_text = f"EMERGENCY ALERT: {user_name} needs assistance in Pune. "
    if lat and lng:
        sms_text += f"Location: https://maps.google.com/?q={lat},{lng} ({lat:.4f}, {lng:.4f}). "
    sms_text += "Please call back or dial Pune Police 112 / 1091."

    return jsonify({
        "status": "simulation_ready",
        "integration_available": False,
        "disclosure": "Direct police computer dispatch API is not connected. To dispatch police or medical services, tap to dial 112 or 1091 directly below.",
        "official_numbers": [
            {"label": "National Emergency", "phone": "112"},
            {"label": "Pune Women Damini Squad", "phone": "1091"},
            {"label": "National Women Support", "phone": "181"},
            {"label": "Ambulance", "phone": "108"}
        ],
        "prepared_sms_body": sms_text,
        "trusted_contacts": [c.to_dict() for c in contacts]
    })
