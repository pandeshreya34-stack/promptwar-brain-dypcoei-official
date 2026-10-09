import sys
sys.stdout.reconfigure(encoding='utf-8')
from app import create_app

def run_tests():
    app = create_app()
    client = app.test_client()

    print("\n--- 1. Testing Health Endpoint ---")
    res = client.get('/api/health')
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print("Health Status:", res.get_json())

    print("\n--- 2. Testing Categories ---")
    res = client.get('/api/categories')
    assert res.status_code == 200
    cats = res.get_json()['categories']
    print(f"Categories loaded: {len(cats)} categories")

    print("\n--- 3. Testing Places & Trust Score ---")
    res = client.get('/api/places')
    assert res.status_code == 200
    places = res.get_json()['places']
    print(f"Total places loaded: {len(places)}")
    sample_place = places[0]
    print(f"Sample Place: {sample_place['name']} ({sample_place['category']}) - Trust Score: {sample_place['trust_score']}/100")
    assert 'trust_score_breakdown' in sample_place

    print("\n--- 4. Testing Natural-Language Search ---")
    nl_query = "Find historical places and affordable food under ₹500 near Shaniwar Wada, with a safer route"
    res = client.get(f'/api/search?q={nl_query}')
    assert res.status_code == 200
    search_data = res.get_json()
    print("Parsed Intent:", search_data['parsed_intent'])
    print(f"Search Results Count: {search_data['total']}")
    assert search_data['total'] > 0

    print("\n--- 5. Testing Route Planner ---")
    res = client.post('/api/routes', json={
        "origin_lat": 18.5195,
        "origin_lng": 73.8553,
        "dest_lat": 18.5284,
        "dest_lng": 73.8505,
        "mode": "walking",
        "preference": "safety-informed",
        "origin_name": "Shaniwar Wada",
        "dest_name": "Pataleshwar Cave Temple"
    })
    assert res.status_code == 200
    route_data = res.get_json()
    print(f"Route Preference: {route_data['preference_title']}")
    print(f"Distance: {route_data['distance_km']} km, Duration: ~{route_data['duration_minutes']} mins")
    print(f"Explanation: {route_data['explanation'][:80]}...")
    print(f"Waypoints: {len(route_data['waypoints'])} coordinates")

    print("\n--- 6. Testing Itinerary Planner ---")
    res = client.get('/api/itinerary')
    assert res.status_code == 200
    samples = res.get_json()['sample_itineraries']
    print(f"Sample itineraries: {len(samples)} options")

    res_custom = client.post('/api/itinerary', json={
        "start_location": "Deccan Gymkhana",
        "available_hours": 5,
        "total_budget": 500,
        "people_count": 2,
        "categories": ["history", "food"],
        "transport_mode": "metro_bus",
        "accessible_only": False
    })
    assert res_custom.status_code == 200
    custom_itn = res_custom.get_json()['itinerary']
    print(f"Custom Plan: {custom_itn['title']} | Stops: {custom_itn['total_stops']} | Est Cost/Person: ₹{custom_itn['estimated_cost_per_person']}")

    print("\n--- 7. Testing Safety Contacts & SOS Trigger ---")
    res = client.get('/api/safety-contacts')
    assert res.status_code == 200
    contacts = res.get_json()['contacts']
    print(f"Safety Contacts: {len(contacts)}")
    helpline_nums = [c['phone'] for c in contacts]
    assert '112' in helpline_nums
    assert '1091' in helpline_nums

    res_sos = client.post('/api/sos-trigger', json={
        "lat": 18.5204,
        "lng": 73.8567,
        "user_name": "Radhika"
    })
    assert res_sos.status_code == 200
    sos_data = res_sos.get_json()
    print(f"SOS Disclosure Status: {sos_data['status']}")
    print(f"SMS Prepared: {sos_data['prepared_sms_body'][:60]}...")

    print("\n--- 8. Testing Civic Reports & Insights ---")
    res_rep = client.post('/api/reports', json={
        "category": "Broken Streetlight",
        "description": "Flickering streetlight near FC road junction",
        "address": "Goodluck Chowk",
        "neighbourhood": "Deccan Gymkhana",
        "is_anonymous": False,
        "reporter_name": "Aarav"
    })
    assert res_rep.status_code == 201
    rep_id = res_rep.get_json()['report']['id']

    # Patch status
    res_patch = client.patch(f'/api/reports/{rep_id}/status', json={"status": "In Progress"})
    assert res_patch.status_code == 200
    print(f"Report status successfully advanced to: {res_patch.get_json()['report']['status']}")

    # Insights
    res_in = client.get('/api/insights')
    assert res_in.status_code == 200
    insights = res_in.get_json()
    print(f"Total reports: {insights['total_reports']}, Resolved: {insights['resolved_reports']}, Verified places: {insights['total_verified_places']}")

    print("\n--- 9. Testing Voice & AI Assistant ---")
    # English
    res_en = client.post('/api/assistant/chat', json={"message": "Show food under ₹200", "language": "en"})
    assert res_en.status_code == 200
    print("EN Reply:", res_en.get_json()['reply'][:70], "...")

    # Marathi
    res_mr = client.post('/api/assistant/chat', json={"message": "मला पुण्यात स्वस्त जेवणाची ठिकाणे दाखवा", "language": "mr"})
    assert res_mr.status_code == 200
    print("MR Reply:", res_mr.get_json()['reply'][:70], "...")

    # Hindi
    res_hi = client.post('/api/assistant/chat', json={"message": "पुणे में ऐतिहासिक स्थल बताओ", "language": "hi"})
    assert res_hi.status_code == 200
    print("HI Reply:", res_hi.get_json()['reply'][:70], "...")

    # Emergency Detection
    res_em = client.post('/api/assistant/chat', json={"message": "I am in danger! Please help me emergency!", "language": "en"})
    assert res_em.status_code == 200
    em_data = res_em.get_json()
    assert em_data['is_emergency'] is True
    print("Emergency Detection Triggered Successfully:", em_data['reply'][:70], "...")

    print("\n==========================================")
    print(" ALL 9 BACKEND TEST SUITES PASSED! 100% ")
    print("==========================================\n")

if __name__ == '__main__':
    run_tests()
