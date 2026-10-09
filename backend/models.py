from datetime import datetime
import json
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='citizen') # tourist, citizen, admin
    emergency_phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "emergency_phone": self.emergency_phone,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True) # history, food, cafe, hotel, facility, safety, hospital, transport
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    neighbourhood = db.Column(db.String(100), nullable=False, index=True)
    images = db.Column(db.Text, default='[]') # JSON array of image URLs
    opening_hours = db.Column(db.String(100), default='Open daily')
    last_verified = db.Column(db.String(50), default='October 2026')
    approximate_cost = db.Column(db.Integer, default=0) # 0 for free public places
    price_range = db.Column(db.String(50), default='Free / Public')
    currency = db.Column(db.String(10), default='₹')
    external_source_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=4.5)
    review_count = db.Column(db.Integer, default=10)
    accessibility_features = db.Column(db.Text, default='[]') # JSON array
    safety_features = db.Column(db.Text, default='[]') # JSON array
    reported_issues = db.Column(db.Text, default='[]') # JSON array
    sub_category = db.Column(db.String(50), nullable=True) # fort, hill, lake, heritage, cafe, restaurant, bakery, metro, bus, train
    menu_items = db.Column(db.Text, default='[]') # JSON array of {name, price, description, is_veg, bestseller, image_url}
    transit_connections = db.Column(db.Text, default='[]') # JSON array of {type, route_or_line, stop_or_station, fare, distance, image_url}
    data_source = db.Column(db.String(100), default='OpenStreetMap & Verified Seed')
    confidence_level = db.Column(db.String(50), default='High') # High, Moderate, Demo Seed
    trust_score = db.Column(db.Integer, default=85)
    trust_score_breakdown = db.Column(db.Text, default='{}') # JSON details

    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")

    def calculate_trust_score(self):
        """
        SafeSteps Transparent Weighted Trust Score Formula:
        - Review Confidence (20%): Based on review count & recency
        - Info Freshness (20%): Last verified timestamp confidence
        - Price Reliability (15%): Clarity & stability of reported pricing
        - Accessibility Coverage (15%): Documented ramps, restrooms, level access
        - Community Feedback (15%): Citizen upvotes & lack of unresolved flags
        - Safety Info Coverage (15%): Presence of verified safety checks (lighting, footfall, CCTV)
        """
        try:
            breakdown = json.loads(self.trust_score_breakdown or '{}')
        except:
            breakdown = {}

        rev_conf = breakdown.get('review_confidence', 80)
        freshness = breakdown.get('info_freshness', 85)
        price_rel = breakdown.get('price_reliability', 85)
        access_cov = breakdown.get('accessibility_coverage', 75)
        comm_feed = breakdown.get('community_feedback', 85)
        safety_cov = breakdown.get('safety_coverage', 80)

        weighted = (
            rev_conf * 0.20 +
            freshness * 0.20 +
            price_rel * 0.15 +
            access_cov * 0.15 +
            comm_feed * 0.15 +
            safety_cov * 0.15
        )
        self.trust_score = int(round(weighted))
        self.trust_score_breakdown = json.dumps({
            "review_confidence": rev_conf,
            "info_freshness": freshness,
            "price_reliability": price_rel,
            "accessibility_coverage": access_cov,
            "community_feedback": comm_feed,
            "safety_coverage": safety_cov,
            "is_demo_score": self.confidence_level == "Demo Seed" or "seed" in self.data_source.lower()
        })
        return self.trust_score

    def to_dict(self):
        try:
            imgs = json.loads(self.images or '[]')
        except:
            imgs = []
        try:
            access = json.loads(self.accessibility_features or '[]')
        except:
            access = []
        try:
            safety = json.loads(self.safety_features or '[]')
        except:
            safety = []
        try:
            issues = json.loads(self.reported_issues or '[]')
        except:
            issues = []
        try:
            menu = json.loads(self.menu_items or '[]')
        except:
            menu = []
        try:
            transit = json.loads(self.transit_connections or '[]')
        except:
            transit = []
        try:
            breakdown = json.loads(self.trust_score_breakdown or '{}')
        except:
            breakdown = {}

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "sub_category": self.sub_category,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "neighbourhood": self.neighbourhood,
            "images": imgs,
            "opening_hours": self.opening_hours,
            "last_verified": self.last_verified,
            "approximate_cost": self.approximate_cost,
            "price_range": self.price_range,
            "currency": self.currency,
            "external_source_url": self.external_source_url,
            "rating": round(self.rating, 1),
            "review_count": self.review_count,
            "accessibility_features": access,
            "safety_features": safety,
            "reported_issues": issues,
            "menu_items": menu,
            "transit_connections": transit,
            "data_source": self.data_source,
            "confidence_level": self.confidence_level,
            "trust_score": self.trust_score,
            "trust_score_breakdown": breakdown
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1 to 5
    comment = db.Column(db.Text, nullable=False)
    is_demo = db.Column(db.Boolean, default=True)
    helpful_votes = db.Column(db.Integer, default=0)
    reported_count = db.Column(db.Integer, default=0)
    moderation_status = db.Column(db.String(20), default='approved') # approved, pending, flagged
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_name": self.user_name,
            "rating": self.rating,
            "comment": self.comment,
            "is_demo": self.is_demo,
            "helpful_votes": self.helpful_votes,
            "reported_count": self.reported_count,
            "moderation_status": self.moderation_status,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

class CivicReport(db.Model):
    __tablename__ = 'civic_reports'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) # Pothole, Broken Streetlight, Garbage, Damaged Footpath, Accessibility Barrier, Waterlogging, Other
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    neighbourhood = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(30), default='Submitted') # Submitted -> Under Review -> In Progress -> Resolved
    is_anonymous = db.Column(db.Boolean, default=False)
    reporter_name = db.Column(db.String(100), default='Pune Citizen')
    upvotes = db.Column(db.Integer, default=1)
    is_demo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "description": self.description,
            "image_url": self.image_url,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "neighbourhood": self.neighbourhood,
            "status": self.status,
            "is_anonymous": self.is_anonymous,
            "reporter_name": "Anonymous Citizen" if self.is_anonymous else self.reporter_name,
            "upvotes": self.upvotes,
            "is_demo": self.is_demo,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

class SafetyContact(db.Model):
    __tablename__ = 'safety_contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False) # Helpline, Police, Hospital, Women
    is_emergency = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "phone": self.phone,
            "description": self.description,
            "category": self.category,
            "is_emergency": self.is_emergency
        }

class TrustedContact(db.Model):
    __tablename__ = 'trusted_contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True) # None for guest demo
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    relationship = db.Column(db.String(50), default='Family')
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "relationship": self.relationship,
            "is_primary": self.is_primary
        }

class SavedPlace(db.Model):
    __tablename__ = 'saved_places'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True) # None for guest demo
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    place = db.relationship('Place', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "notes": self.notes,
            "place": self.place.to_dict() if self.place else None,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }
