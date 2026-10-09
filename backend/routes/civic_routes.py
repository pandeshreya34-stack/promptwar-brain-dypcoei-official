from flask import Blueprint, request, jsonify
from database import db
from models import CivicReport, Place

civic_bp = Blueprint('civic', __name__)

@civic_bp.route('/reports', methods=['GET', 'POST'])
def manage_reports():
    if request.method == 'GET':
        category = request.args.get('category')
        status = request.args.get('status')
        query = CivicReport.query
        if category and category != 'all':
            query = query.filter_by(category=category)
        if status and status != 'all':
            query = query.filter_by(status=status)

        reports = query.order_by(CivicReport.created_at.desc()).all()
        return jsonify({
            "total": len(reports),
            "reports": [r.to_dict() for r in reports],
            "demo_notice": "Civic report statuses are demonstration simulations. For live municipal escalation, submit tickets directly to PMC Care (pmc.gov.in / 1800 1030 222)."
        })

    # POST new report
    data = request.get_json() or {}
    category = data.get('category', '').strip()
    description = data.get('description', '').strip()
    address = data.get('address', '').strip()
    neighbourhood = data.get('neighbourhood', 'Pune').strip()
    image_url = data.get('image_url')
    lat = data.get('latitude')
    lng = data.get('longitude')
    is_anonymous = bool(data.get('is_anonymous', False))
    reporter_name = data.get('reporter_name', 'Pune Citizen').strip()

    if not category or not description or not address:
        return jsonify({"error": "Category, description, and address are required"}), 400

    report = CivicReport(
        category=category,
        description=description,
        image_url=image_url,
        latitude=lat,
        longitude=lng,
        address=address,
        neighbourhood=neighbourhood,
        status='Submitted',
        is_anonymous=is_anonymous,
        reporter_name=reporter_name if not is_anonymous else 'Anonymous Citizen',
        upvotes=1,
        is_demo=False
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "message": "Civic report registered successfully in community ledger",
        "report": report.to_dict(),
        "disclaimer": "This report is recorded in the SafeSteps Community demo ledger. Official PMC civic escalation requires authorization."
    }), 201

@civic_bp.route('/reports/<int:report_id>/status', methods=['PATCH'])
def update_report_status(report_id):
    report = CivicReport.query.get_or_404(report_id)
    data = request.get_json() or {}
    new_status = data.get('status')
    valid_statuses = ['Submitted', 'Under Review', 'In Progress', 'Resolved']

    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of {valid_statuses}"}), 400

    report.status = new_status
    db.session.commit()
    return jsonify({
        "message": f"Report status changed to {new_status}",
        "report": report.to_dict()
    })

@civic_bp.route('/reports/<int:report_id>/upvote', methods=['POST'])
def upvote_report(report_id):
    report = CivicReport.query.get_or_404(report_id)
    report.upvotes += 1
    db.session.commit()
    return jsonify({
        "message": "Upvote added to report",
        "upvotes": report.upvotes
    })

@civic_bp.route('/insights', methods=['GET'])
def get_insights():
    """Returns analytics data for Recharts on the community dashboard"""
    reports = CivicReport.query.all()
    places = Place.query.all()

    # Category breakdown of reports
    category_counts = {}
    for r in reports:
        category_counts[r.category] = category_counts.get(r.category, 0) + 1

    report_categories_data = [{"category": k, "count": v} for k, v in category_counts.items()]

    # Status distribution
    status_counts = {"Submitted": 0, "Under Review": 0, "In Progress": 0, "Resolved": 0}
    for r in reports:
        if r.status in status_counts:
            status_counts[r.status] += 1
    report_status_data = [{"status": k, "count": v} for k, v in status_counts.items()]

    # Neighbourhood distribution
    neighbourhood_counts = {}
    for r in reports:
        neighbourhood_counts[r.neighbourhood] = neighbourhood_counts.get(r.neighbourhood, 0) + 1
    neighbourhood_data = [{"neighbourhood": k, "issues": v} for k, v in sorted(neighbourhood_counts.items(), key=lambda x: x[1], reverse=True)[:6]]

    # Place category distribution
    place_cat_counts = {}
    for p in places:
        place_cat_counts[p.category] = place_cat_counts.get(p.category, 0) + 1
    places_chart_data = [{"category": k.capitalize(), "count": v} for k, v in place_cat_counts.items()]

    return jsonify({
        "total_reports": len(reports),
        "resolved_reports": status_counts["Resolved"],
        "in_progress_reports": status_counts["In Progress"],
        "total_verified_places": len(places),
        "report_categories_data": report_categories_data,
        "report_status_data": report_status_data,
        "neighbourhood_data": neighbourhood_data,
        "places_chart_data": places_chart_data
    })
