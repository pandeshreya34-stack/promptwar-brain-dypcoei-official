import re
from flask import Blueprint, request, jsonify
from models import Place

assistant_bp = Blueprint('assistant', __name__)

EMERGENCY_KEYWORDS = [
    'emergency', 'help', 'danger', 'police', 'ambulance', 'sos', 'attack', 'threat', 'stalk',
    'मदत', 'पोलीस', 'आपत्कालीन', 'दवाखाना', 'धोका',
    'मदद', 'खतरा', 'इमरजेंसी', 'अस्पताल', 'सुरक्षा'
]

@assistant_bp.route('/assistant/chat', methods=['POST'])
def assistant_chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    language = data.get('language', 'en') # 'en', 'hi', 'mr'

    if not message:
        return jsonify({"reply": "How can I assist you with exploring Pune safely today?", "is_emergency": False})

    msg_lower = message.lower()

    # 1. IMMEDIATE Emergency check: Prompt requirement:
    # "For emergencies, show official contact options directly. Never make users wait for an AI-generated answer before accessing emergency numbers."
    if any(k in msg_lower for k in EMERGENCY_KEYWORDS) and any(alert in msg_lower for alert in ['emergency', 'sos', 'help me', 'danger', 'threat', 'attack', 'stalked', '112', '1091', 'मदत', 'धोका', 'खतरा']):
        if language == 'mr':
            reply = "⚠️ आपत्कालीन सहाय्य: कृपया त्वरित ११२ किंवा १०९१ (पुणे महिला हेल्पलाईन) वर संपर्क साधा. जवळचे पोलीस ठाणे आणि रुग्णालय खालील त्वरित बटणांवर उपलब्ध आहेत."
        elif language == 'hi':
            reply = "⚠️ आपातकालीन सहायता: कृपया तुरंत 112 या 1091 (पुणे महिला हेल्पलाइन) पर कॉल करें। नजदीकी पुलिस स्टेशन और अस्पताल नीचे दिए गए हैं।"
        else:
            reply = "⚠️ IMMEDIATE EMERGENCY ALERT: Please call 112 or 1091 (Pune Women's Safety Helpline) immediately. Nearest verified police stations and emergency hospitals are displayed below."

        return jsonify({
            "reply": reply,
            "is_emergency": True,
            "emergency_contacts": [
                {"name": "National Emergency", "phone": "112"},
                {"name": "Pune Women Helpline (Damini Squad)", "phone": "1091"},
                {"name": "Ambulance", "phone": "108"},
                {"name": "Women Support Helpline", "phone": "181"}
            ],
            "recommended_places": []
        })

    # 2. Marathi queries
    if language == 'mr' or any(word in message for word in ['पुण्यात', 'ठिकाणे', 'जेवण', 'दाखवा', 'ऐतिहासिक', 'स्वस्त']):
        if 'जेवण' in message or 'खाद्य' in message or 'स्वस्त' in message:
            places = Place.query.filter_by(category='food').all()
            reply = "पुण्यातील बजेट-फ्रेंडली जेवणासाठी 'आशा डायनिंग हॉल' (डेक्कन, अस्सल थाळी ₹३००) आणि 'चैतन्य पराठा' (एफसी रोड, ₹२५०) हे उत्तम व सुरक्षित पर्याय आहेत."
        elif 'ऐतिहासिक' in message or 'इतिहास' in message:
            places = Place.query.filter_by(category='history').all()
            reply = "पुण्यातील प्रमुख ऐतिहासिक ठिकाणे: शनिवार वाडा (शनिवार पेठ, ₹२५), लाल महाल (कस्बा पेठ, ₹५), आणि पाताळेश्वर लेणी (जंगली महाराज रस्ता, मोफत प्रवेश)."
        elif 'रुग्णालय' in message or 'दवाखाना' in message:
            places = Place.query.filter_by(category='hospital').all()
            reply = "पुण्यातील प्रमुख २४/७ रुग्णालये: ससून सर्वोपचार रुग्णालय (स्टेशन रस्ता) आणि सह्याद्री सुपर स्पेशालिटी हॉस्पिटल (कर्वे रस्ता)."
        else:
            places = Place.query.limit(3).all()
            reply = "मी सेफस्टेप्स पुणे व्हॉइस सहाय्यक आहे. तुम्हाला ऐतिहासिक ठिकाणे, स्वस्त जेवण, सुरक्षित मार्ग किंवा महिला सुरक्षा केंद्राबद्दल माहिती हवी आहे का?"

        return jsonify({
            "reply": reply,
            "is_emergency": False,
            "recommended_places": [p.to_dict() for p in places[:3]]
        })

    # 3. Hindi queries
    if language == 'hi' or any(word in message for word in ['पुणे', 'खाना', 'सस्ता', 'दिखाओ', 'इतिहास']):
        if 'खाना' in message or 'सस्ता' in message or 'भोजन' in message:
            places = Place.query.filter_by(category='food').all()
            reply = "पुणे में किफायती और सुरक्षित भोजन के लिए: 'आशा डाइनिंग हॉल' (डेक्कन, प्रामाणिक थाली ₹300) और 'चैतन्य पराठा' (एफसी रोड, ₹250)."
        elif 'इतिहास' in message or 'ऐतिहासिक' in message:
            places = Place.query.filter_by(category='history').all()
            reply = "पुणे के प्रमुख ऐतिहासिक स्थल: शनिवार वाड़ा (₹25), लाल महल (₹5), और पातालेश्वर गुफा मंदिर (जेएम रोड, निःशुल्क प्रवेश)।"
        elif 'अस्पताल' in message or 'डॉक्टर' in message:
            places = Place.query.filter_by(category='hospital').all()
            reply = "पुणे में 24/7 आपातकालीन अस्पताल: ससून जनरल हॉस्पिटल (स्टेशन रोड) और सह्याद्री अस्पताल (कर्वे रोड)।"
        else:
            places = Place.query.limit(3).all()
            reply = "मैं सेफस्टेप्स पुणे सहायक हूँ। मैं आपको ऐतिहासिक स्थल, बजट भोजन, और सुरक्षित नेविगेशन खोजने में मदद कर सकता हूँ।"

        return jsonify({
            "reply": reply,
            "is_emergency": False,
            "recommended_places": [p.to_dict() for p in places[:3]]
        })

    # 4. English queries
    if any(k in msg_lower for k in ['food', 'eat', 'thali', 'cheap', 'budget', 'under 200', 'under 500']):
        places = Place.query.filter_by(category='food').all()
        reply = "Here are top-rated budget-friendly dining options in Pune: Sambar Aromas (Viman Nagar, ₹1–₹200), Chaitanya Parathas (FC Road, ₹200–₹400), and Asha Dining Hall (Deccan, ₹200–₹400 unlimited authentic thali)."
    elif any(k in msg_lower for k in ['history', 'historical', 'heritage', 'monument', 'fort', 'wada']):
        places = Place.query.filter_by(category='history').all()
        reply = "Must-visit Pune heritage landmarks: Shaniwar Wada (18th-century Peshwa seat, ₹25), Lal Mahal (Kasba Peth, ₹5), Pataleshwar Rock-Cut Caves (JM Road, Free), and Mahatma Phule Wada (Ganj Peth, Free)."
    elif any(k in msg_lower for k in ['hospital', 'doctor', 'clinic', 'medical']):
        places = Place.query.filter_by(category='hospital').all()
        reply = "Verified 24/7 medical centers: Sassoon General Hospital (Station Road, govt trauma care) and Sahyadri Super Speciality Hospital (Karve Road, Deccan)."
    elif any(k in msg_lower for k in ['safe', 'safety', 'route', 'walk']):
        places = Place.query.filter(Place.category.in_(['safety', 'transport'])).all()
        reply = "For safer transit in Pune, utilize our Safety-Informed Route planner which sticks to well-illuminated corridors (such as FC Road & JM Road) and verified Metro purple line stations with 24/7 security."
    elif any(k in msg_lower for k in ['hotel', 'stay', 'lodge']):
        places = Place.query.filter_by(category='hotel').all()
        reply = "Safe hotel accommodations with verified security and high trust scores include Hotel Shreyas on Apte Road (Deccan) and Sagar Plaza near Pune Station."
    else:
        places = Place.query.order_by(Place.trust_score.desc()).limit(3).all()
        reply = f"I found several high-trust verified locations in Pune matching your interests. You can explore them on the map or ask me for specific budget recommendations (e.g. 'Show food under ₹200' or 'Historical places')."

    return jsonify({
        "reply": reply,
        "is_emergency": False,
        "recommended_places": [p.to_dict() for p in places[:4]]
    })
