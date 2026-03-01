import streamlit as st
import requests
import json
import google.generativeai as genai
import pandas as pd
import time

# ============================================
# CONFIGURATION - PUT YOUR API KEYS HERE
# ============================================
SERP_API_KEY = "7f1fd2837f4837d1055543644026df101b0c8d0a1bdf13a2e3adcb84579414a0"
GEMINI_API_KEY = "AIzaSyCrcx-mIdgnAZxgItU5a8IQti4K5diJnjY"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ============================================
# PAGE SETUP
# ============================================
st.set_page_config(
    page_title="LeadIntel — AI Cold Email Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# PREMIUM CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {
        background: #0a0a0f;
        color: #e0e0e0;
    }
    
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b3520, #ff6b3510);
        border: 1px solid #ff6b3540;
        color: #ff6b35;
        padding: 0.35rem 1rem;
        border-radius: 50px;
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -1px;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #ff6b35, #ff8c42, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.05rem;
        color: #888;
        margin-top: 0.8rem;
        margin-bottom: 0;
    }
    
    .search-container {
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .stTextInput > div > div > input {
        background: #1a1a2a !important;
        border: 1px solid #2a2a3a !important;
        color: #fff !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b35 !important;
        box-shadow: 0 0 0 2px #ff6b3520 !important;
    }
    
    .stTextInput > label {
        color: #888 !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.75rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ff6b35, #ff8c42) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px #ff6b3540 !important;
    }
    
    .stButton > button:not([kind="primary"]) {
        background: #1a1a2a !important;
        color: #ff6b35 !important;
        border: 1px solid #ff6b3540 !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .metrics-row {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        flex: 1;
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 14px;
        padding: 1.3rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #ff6b3540;
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        margin: 0;
    }
    
    .metric-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #666;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }
    
    .biz-header {
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0 1rem;
    }
    
    .biz-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #fff;
        margin: 0;
    }
    
    .biz-meta {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.3rem;
    }
    
    .sentiment-badge {
        display: inline-block;
        padding: 0.3rem 0.9rem;
        border-radius: 50px;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .sentiment-positive { background: #22c55e15; color: #22c55e; border: 1px solid #22c55e30; }
    .sentiment-mixed { background: #f59e0b15; color: #f59e0b; border: 1px solid #f59e0b30; }
    .sentiment-negative { background: #ef444415; color: #ef4444; border: 1px solid #ef444430; }
    
    .summary-text {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: #999;
        line-height: 1.7;
        padding: 1rem 0;
        border-bottom: 1px solid #1e1e2e;
        margin-bottom: 1.5rem;
    }
    
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #fff;
        margin: 1.5rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .dot-red { background: #ef4444; box-shadow: 0 0 10px #ef444460; }
    .dot-green { background: #22c55e; box-shadow: 0 0 10px #22c55e60; }
    .dot-blue { background: #3b82f6; box-shadow: 0 0 10px #3b82f660; }
    .dot-orange { background: #ff6b35; box-shadow: 0 0 10px #ff6b3560; }
    
    .pain-card {
        background: #1a0a0a;
        border: 1px solid #ef444425;
        border-left: 3px solid #ef4444;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.2s ease;
    }
    .pain-card:hover { background: #1f0e0e; transform: translateX(3px); }
    .pain-title { font-family: 'DM Sans'; font-size: 0.95rem; font-weight: 600; color: #ef4444; margin: 0; }
    .pain-detail { font-family: 'DM Sans'; font-size: 0.85rem; color: #999; margin: 0.3rem 0; line-height: 1.5; }
    .pain-meta { font-family: 'Space Mono'; font-size: 0.65rem; color: #555; }
    
    .praise-card {
        background: #0a1a0e;
        border: 1px solid #22c55e25;
        border-left: 3px solid #22c55e;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.2s ease;
    }
    .praise-card:hover { background: #0e1f12; transform: translateX(3px); }
    .praise-title { font-family: 'DM Sans'; font-size: 0.95rem; font-weight: 600; color: #22c55e; margin: 0; }
    .praise-detail { font-family: 'DM Sans'; font-size: 0.85rem; color: #999; margin: 0.3rem 0; line-height: 1.5; }
    .praise-meta { font-family: 'Space Mono'; font-size: 0.65rem; color: #555; }
    
    .opportunity-box {
        background: linear-gradient(135deg, #ff6b3510, #ffd70010);
        border: 1px solid #ff6b3530;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin: 1.5rem 0;
    }
    .opportunity-label { font-family: 'Space Mono'; font-size: 0.7rem; color: #ff6b35; letter-spacing: 2px; text-transform: uppercase; margin: 0 0 0.5rem; }
    .opportunity-text { font-family: 'DM Sans'; font-size: 1rem; color: #ddd; line-height: 1.6; margin: 0; }
    
    .email-card {
        background: #12121a;
        border: 1px solid #1e1e2e;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .email-card:hover { border-color: #ff6b3540; }
    .email-approach { font-family: 'Space Mono'; font-size: 0.7rem; color: #ff6b35; letter-spacing: 2px; text-transform: uppercase; margin: 0 0 0.8rem; }
    .email-subject { font-family: 'DM Sans'; font-size: 1rem; font-weight: 600; color: #fff; margin: 0 0 0.8rem; padding-bottom: 0.8rem; border-bottom: 1px solid #1e1e2e; }
    .email-body { font-family: 'DM Sans'; font-size: 0.9rem; color: #bbb; line-height: 1.8; white-space: pre-wrap; }
    
    .tag-high { display: inline-block; background: #ef444420; color: #ef4444; padding: 0.15rem 0.5rem; border-radius: 4px; font-family: 'Space Mono'; font-size: 0.6rem; letter-spacing: 1px; text-transform: uppercase; }
    .tag-medium { display: inline-block; background: #f59e0b20; color: #f59e0b; padding: 0.15rem 0.5rem; border-radius: 4px; font-family: 'Space Mono'; font-size: 0.6rem; letter-spacing: 1px; text-transform: uppercase; }
    .tag-low { display: inline-block; background: #3b82f620; color: #3b82f6; padding: 0.15rem 0.5rem; border-radius: 4px; font-family: 'Space Mono'; font-size: 0.6rem; letter-spacing: 1px; text-transform: uppercase; }
    
    .divider { border: none; border-top: 1px solid #1e1e2e; margin: 2rem 0; }
    
    .footer { text-align: center; padding: 2rem 0; font-family: 'DM Sans'; color: #444; font-size: 0.85rem; }
    .footer strong { color: #ff6b35; }
    .footer .tagline { font-family: 'Space Mono'; font-size: 0.7rem; color: #333; letter-spacing: 2px; text-transform: uppercase; margin-top: 0.5rem; }
    
    section[data-testid="stSidebar"] { background: #0d0d14; border-right: 1px solid #1e1e2e; }
    
    .score-bar-container { background: #1a1a2a; border-radius: 8px; height: 8px; margin: 0.8rem 0; overflow: hidden; }
    .score-bar { height: 100%; border-radius: 8px; transition: width 1s ease; }
    
    .how-it-works { display: flex; justify-content: center; gap: 0; margin: 1.5rem 0 0.5rem; padding: 0 2rem; }
    .step-item { text-align: center; flex: 1; }
    .step-num { display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; background: linear-gradient(135deg, #ff6b35, #ff8c42); border-radius: 50%; font-family: 'Space Mono'; font-size: 0.8rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
    .step-text { font-family: 'DM Sans'; font-size: 0.8rem; color: #666; }
    .step-arrow { color: #333; font-size: 1.2rem; line-height: 32px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { background: #1a1a2a !important; border-radius: 8px !important; color: #888 !important; font-family: 'DM Sans' !important; padding: 0.5rem 1.2rem !important; }
    .stTabs [aria-selected="true"] { background: #ff6b35 !important; color: #fff !important; }
    
    .stProgress > div > div > div { background: linear-gradient(135deg, #ff6b35, #ffd700) !important; }
    .stDownloadButton > button { background: #12121a !important; color: #ff6b35 !important; border: 1px solid #ff6b3540 !important; border-radius: 10px !important; font-family: 'DM Sans' !important; }
</style>
""", unsafe_allow_html=True)


# ============================================
# HERO
# ============================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ AI-Powered Intelligence</div>
    <p class="hero-title">Lead<span>Intel</span></p>
    <p class="hero-subtitle">Know their pain before you email them. Analyze any business's reviews<br>and generate hyper-personalized cold emails in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="how-it-works">
    <div class="step-item"><div class="step-num">1</div><div class="step-text">Enter Business</div></div>
    <div class="step-item"><div class="step-arrow">→</div></div>
    <div class="step-item"><div class="step-num">2</div><div class="step-text">AI Scrapes Reviews</div></div>
    <div class="step-item"><div class="step-arrow">→</div></div>
    <div class="step-item"><div class="step-num">3</div><div class="step-text">Extracts Pain Points</div></div>
    <div class="step-item"><div class="step-arrow">→</div></div>
    <div class="step-item"><div class="step-num">4</div><div class="step-text">Custom Cold Email</div></div>
</div>
""", unsafe_allow_html=True)


# ============================================
# FUNCTIONS
# ============================================
def scrape_reviews(business_name, city=""):
    try:
        search_query = f"{business_name} {city}".strip()
        params = {"engine": "google_maps", "q": search_query, "api_key": SERP_API_KEY, "type": "search"}
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        
        if "local_results" not in data or len(data["local_results"]) == 0:
            return None, "No business found on Google Maps"
        
        place = data["local_results"][0]
        business_info = {
            "name": place.get("title", business_name),
            "rating": place.get("rating", "N/A"),
            "reviews_count": place.get("reviews", 0),
            "address": place.get("address", "N/A"),
            "type": place.get("type", "N/A"),
            "phone": place.get("phone", "N/A"),
        }
        
        review_params = {"engine": "google_maps_reviews", "place_id": place.get("place_id", ""), "api_key": SERP_API_KEY, "sort_by": "newestFirst"}
        review_response = requests.get("https://serpapi.com/search", params=review_params)
        review_data = review_response.json()
        
        reviews = []
        if "reviews" in review_data:
            for review in review_data["reviews"]:
                reviews.append({"text": review.get("snippet", ""), "rating": review.get("rating", 0), "date": review.get("date", ""), "user": review.get("user", {}).get("name", "Anonymous")})
        
        business_info["reviews"] = reviews
        return business_info, None
    except Exception as e:
        return None, f"Error: {str(e)}"


def analyze_reviews(business_info):
    reviews_text = "\n\n".join([f"Review {i} (Rating: {r['rating']}/5): {r['text']}" for i, r in enumerate(business_info["reviews"], 1)])
    if not reviews_text.strip():
        return None, "No review text found"
    
    prompt = f"""You are a business intelligence analyst. Analyze these Google Maps reviews for "{business_info['name']}".

REVIEWS:
{reviews_text}

Respond in EXACTLY this JSON format (no markdown, no backticks, just pure JSON):
{{
    "overall_sentiment": "positive/negative/mixed",
    "sentiment_score": 75,
    "pain_points": [
        {{"issue": "Short title", "detail": "One line with specific examples from reviews", "severity": "high/medium/low", "mention_count": 3}}
    ],
    "praises": [
        {{"strength": "Short title", "detail": "One line with specific examples from reviews", "frequency": "frequent/occasional"}}
    ],
    "business_summary": "2-3 sentence summary",
    "biggest_opportunity": "Single biggest improvement based on reviews"
}}

Find 3-5 pain points and 3-5 praises. Score 0-100. Be specific with review quotes."""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(result_text), None
    except Exception as e:
        return None, f"AI error: {str(e)}"


def generate_cold_emails(business_info, analysis, sender_company, sender_service):
    pain_text = "\n".join([f"- {p['issue']}: {p['detail']}" for p in analysis.get("pain_points", [])])
    praise_text = "\n".join([f"- {p['strength']}: {p['detail']}" for p in analysis.get("praises", [])])
    
    prompt = f"""Write 3 cold email variations for this business.

BUSINESS: {business_info['name']} | RATING: {business_info['rating']}/5 ({business_info['reviews_count']} reviews) | TYPE: {business_info['type']}
PAIN POINTS: {pain_text}
STRENGTHS: {praise_text}
OPPORTUNITY: {analysis.get('biggest_opportunity', 'N/A')}
SENDER: {sender_company} ({sender_service})

EMAIL 1 - PAIN POINT (subtly reference weakness)
EMAIL 2 - STRENGTH AMPLIFIER (praise strength, offer to scale)
EMAIL 3 - CURIOSITY HOOK (create intrigue)

Rules: Under 80 words, peer-to-peer tone, don't say "I read your reviews", one CTA, include subject line.

JSON format (no markdown, no backticks):
{{"email_1": {{"approach": "Pain Point", "subject": "...", "body": "..."}}, "email_2": {{"approach": "Strength Amplifier", "subject": "...", "body": "..."}}, "email_3": {{"approach": "Curiosity Hook", "subject": "...", "body": "..."}}}}"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        # Try direct parse first
        try:
            return json.loads(result_text), None
        except json.JSONDecodeError:
            # Fix common JSON issues from Gemini
            import re
            # Try to extract JSON between first { and last }
            match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if match:
                cleaned = match.group(0)
                # Replace smart quotes
                cleaned = cleaned.replace('\u2018', "'").replace('\u2019', "'")
                cleaned = cleaned.replace('\u201c', '"').replace('\u201d', '"')
                try:
                    return json.loads(cleaned), None
                except:
                    pass
            
            # Last resort: ask Gemini to fix it
            fix_prompt = f"Fix this broken JSON and return ONLY valid JSON, nothing else:\n{result_text}"
            fix_response = model.generate_content(fix_prompt)
            fix_text = fix_response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(fix_text), None
    except Exception as e:
        return None, f"Email error: {str(e)}"


# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown('<p style="font-family: DM Sans; font-size: 1.2rem; font-weight: 700; color: #fff;">⚡ LeadIntel</p>', unsafe_allow_html=True)
    sender_company = st.text_input("Your Company", value="imaPRO")
    sender_service = st.text_input("Your Service", value="digital marketing & lead generation")
    st.markdown('<hr style="border-color: #1e1e2e">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])


# ============================================
# SEARCH
# ============================================
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    business_name = st.text_input("BUSINESS NAME", placeholder="e.g., Barbeque Nation")
with col2:
    city = st.text_input("CITY", placeholder="e.g., Lucknow")
analyze_button = st.button("⚡ Analyze & Generate Emails", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# RESULTS
# ============================================
if analyze_button and business_name:
    with st.spinner("🔎 Finding business on Google Maps..."):
        business_info, error = scrape_reviews(business_name, city)
    
    if error:
        st.error(f"❌ {error}")
    elif business_info:
        st.markdown(f'<div class="biz-header"><p class="biz-name">{business_info["name"]}</p><p class="biz-meta">📍 {business_info.get("address", "N/A")} · {business_info.get("type", "N/A")}</p></div>', unsafe_allow_html=True)
        
        reviews_found = len(business_info.get('reviews', []))
        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-card"><p class="metric-value">⭐ {business_info['rating']}</p><p class="metric-label">Rating</p></div>
            <div class="metric-card"><p class="metric-value">{business_info['reviews_count']}</p><p class="metric-label">Total Reviews</p></div>
            <div class="metric-card"><p class="metric-value">{reviews_found}</p><p class="metric-label">Scraped</p></div>
            <div class="metric-card"><p class="metric-value">📍</p><p class="metric-label">{business_info.get('type', 'Business')}</p></div>
        </div>
        """, unsafe_allow_html=True)
        
        if reviews_found == 0:
            st.warning("⚠️ No reviews found. LeadIntel works best with local businesses.")
        else:
            with st.spinner("🧠 AI analyzing reviews..."):
                analysis, error = analyze_reviews(business_info)
            
            if error:
                st.error(f"❌ {error}")
            elif analysis:
                score = analysis.get("sentiment_score", 50)
                sentiment = analysis.get("overall_sentiment", "mixed")
                sent_class = "sentiment-positive" if score >= 70 else "sentiment-mixed" if score >= 40 else "sentiment-negative"
                bar_color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
                
                st.markdown(f"""
                <div style="margin: 1rem 0;">
                    <span class="sentiment-badge {sent_class}">{sentiment.upper()} · {score}/100</span>
                    <div class="score-bar-container"><div class="score-bar" style="width: {score}%; background: {bar_color};"></div></div>
                </div>
                <div class="summary-text">{analysis.get('business_summary', '')}</div>
                """, unsafe_allow_html=True)
                
                col_pain, col_praise = st.columns(2)
                with col_pain:
                    st.markdown('<div class="section-header"><span class="dot dot-red"></span> Pain Points</div>', unsafe_allow_html=True)
                    for pp in analysis.get("pain_points", []):
                        sev = pp.get("severity", "medium")
                        st.markdown(f'<div class="pain-card"><p class="pain-title">{pp["issue"]}</p><p class="pain-detail">{pp["detail"]}</p><span class="tag-{sev}">{sev}</span> <span class="pain-meta">· ~{pp.get("mention_count", 1)} mentions</span></div>', unsafe_allow_html=True)
                
                with col_praise:
                    st.markdown('<div class="section-header"><span class="dot dot-green"></span> Praises</div>', unsafe_allow_html=True)
                    for pr in analysis.get("praises", []):
                        st.markdown(f'<div class="praise-card"><p class="praise-title">{pr["strength"]}</p><p class="praise-detail">{pr["detail"]}</p><span class="praise-meta">{pr.get("frequency", "occasional")}</span></div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="opportunity-box"><p class="opportunity-label">🎯 Biggest Opportunity</p><p class="opportunity-text">{analysis.get("biggest_opportunity", "N/A")}</p></div>', unsafe_allow_html=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-header"><span class="dot dot-orange"></span> Personalized Cold Emails</div>', unsafe_allow_html=True)
                
                with st.spinner("✍️ Generating emails..."):
                    emails, error = generate_cold_emails(business_info, analysis, sender_company, sender_service)
                
                if error:
                    st.error(f"❌ {error}")
                elif emails:
                    tabs = st.tabs(["🔴 Pain Point", "🟢 Strength Amplifier", "🟡 Curiosity Hook"])
                    for i, (tab, key) in enumerate(zip(tabs, ["email_1", "email_2", "email_3"])):
                        with tab:
                            email = emails.get(key, {})
                            st.markdown(f'<div class="email-card"><p class="email-approach">{email.get("approach", "")}</p><p class="email-subject">Subject: {email.get("subject", "")}</p><p class="email-body">{email.get("body", "")}</p></div>', unsafe_allow_html=True)
                            st.button(f"📋 Copy Email {i+1}", key=f"copy_{key}")
                
                st.session_state['last_analysis'] = {'business_info': business_info, 'analysis': analysis, 'emails': emails if emails else {}}


# ============================================
# BULK UPLOAD
# ============================================
if uploaded_file:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="dot dot-blue"></span> Bulk Analysis</div>', unsafe_allow_html=True)
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.dataframe(df.head(), use_container_width=True)
        
        name_col = next((col for col in df.columns if "name" in col.lower() or "business" in col.lower()), None)
        city_col = next((col for col in df.columns if "city" in col.lower() or "location" in col.lower()), None)
        
        if name_col and st.button("⚡ Analyze All", type="primary"):
            results = []
            progress = st.progress(0)
            status = st.empty()
            
            for idx, row in df.iterrows():
                biz_name, biz_city = row[name_col], row[city_col] if city_col else ""
                status.text(f"Analyzing {idx+1}/{len(df)}: {biz_name}...")
                progress.progress((idx + 1) / len(df))
                
                business_info, err = scrape_reviews(biz_name, biz_city)
                if err or not business_info or not business_info.get("reviews"):
                    results.append({"Business": biz_name, "Status": "❌ No reviews", "Pain Points": "", "Score": ""})
                    continue
                
                analysis, err = analyze_reviews(business_info)
                if err or not analysis:
                    results.append({"Business": biz_name, "Status": "❌ Failed", "Pain Points": "", "Score": ""})
                    continue
                
                emails, _ = generate_cold_emails(business_info, analysis, sender_company, sender_service)
                results.append({
                    "Business": biz_name, "Rating": business_info.get("rating", ""),
                    "Score": analysis.get("sentiment_score", ""), "Status": "✅ Done",
                    "Pain Points": "; ".join([p["issue"] for p in analysis.get("pain_points", [])]),
                    "Email Subject": emails.get("email_1", {}).get("subject", "") if emails else ""
                })
                time.sleep(1)
            
            status.text("✅ Complete!")
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            st.download_button("📥 Download Results", results_df.to_csv(index=False), "leadintel_results.csv", "text/csv")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============================================
# FOOTER
# ============================================
st.markdown('<div class="footer">Built by <strong>imaPRO</strong> · LeadIntel v1.0<div class="tagline">Know their pain before you email them</div></div>', unsafe_allow_html=True)
