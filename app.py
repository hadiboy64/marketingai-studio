import streamlit as st
from google import genai

st.set_page_config(
    page_title="MarketingAI Studio",
    page_icon="📢",
    layout="wide",
)
# Secrets se API Key auto-read karna
api_key = st.secrets.get("GEMINI_API_KEY")

st.sidebar.title("🤖 MarketingAI Config")
if api_key:
    st.sidebar.success("✅ System Ready (API Connected)")
else:
    st.sidebar.error("⚠️ API Key not configured in Secrets.")

st.sidebar.info("Built for local small businesses & Pakistani e-commerce brands.")

st.title("📢 MarketingAI Studio")
st.caption("AI-Powered Content & Social Media Strategy Assistant for Local Businesses")
st.markdown("---")

tab1, tab2 = st.tabs(["🚀 Rapid Campaign", "📅 30-Day Content Calendar"])

# Helper function streaming text ke liye
def stream_text(response):
    for chunk in response:
        if chunk.text:
            yield chunk.text

# --- TAB 1: RAPID CAMPAIGN ---
with tab1:
    st.subheader("Generate Quick Marketing Package")
    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("Product / Business Name:", value="Handmade Beaded Bag")
        business_type = st.selectbox("Business Category:", ["Fashion & Apparel", "Handmade & Crafts", "Food & Restaurant", "Electronics & Gadgets", "Services / Other"])

    with col2:
        offer_details = st.text_input("Special Offer / Promotion Details:", value="20% Discount for Friday Sale")
        target_audience = st.text_input("Target Audience / City:", value="Young Women & Students in Karachi")

    st.markdown("---")

    if st.button("🚀 Generate Marketing Package", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the left sidebar.")
        else:
            with st.spinner("Generating rapid marketing campaign..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    You are an expert digital marketing manager specializing in small business growth in Pakistan.
                    Create a concise, high-converting marketing package for:

                    - **Product/Business Name:** {product_name}
                    - **Category:** {business_type}
                    - **Special Offer:** {offer_details}
                    - **Target Audience/Location:** {target_audience}

                    Output format (Keep it brief, engaging, and fast):
                    ### 1. 📲 Social Media Captions (3 Options, Roman Urdu + English)
                    ### 2. 🏷️ High-Reach Hashtags (12 hashtags)
                    ### 3. 🎬 15-Second Reel / TikTok Script
                    ### 4. 💬 WhatsApp Business Broadcast Message
                    """

                    response = client.models.generate_content_stream(
                        model="gemini-3-flash-preview",
                        contents=prompt,
                    )
                    st.write_stream(stream_text(response))

                except Exception as e:
                    st.error(f"Error generating content: {e}")

# --- TAB 2: 30-DAY CONTENT CALENDAR ---
with tab2:
    st.subheader("30-Day Strategic Content Calendar (80/20 Rule)")
    
    col_cal1, col_cal2 = st.columns(2)
    with col_cal1:
        cal_business = st.text_input("Business / Product Name for Calendar:", value="KIXORA.PK")
        cal_platform = st.multiselect("Platforms:", ["Instagram", "Facebook", "TikTok", "LinkedIn"], default=["Instagram", "Facebook"])
    
    with col_cal2:
        cal_audience = st.text_input("Target Audience Details:", value="Gen Z & Young Professionals in Pakistan")

    if st.button("📅 Generate 30-Day Content Strategy", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the left sidebar.")
        else:
            with st.spinner("Streaming 30-day strategy table..."):
                try:
                    client = genai.Client(api_key=api_key)
                    calendar_prompt = f"""
                    Act as an expert social media content strategist. Create a 30-day content strategy for:
                    - **Business/Product Name:** {cal_business}
                    - **Target Audience:** {cal_audience}
                    - **Target Platforms:** {', '.join(cal_platform)}

                    **Guidelines:**
                    - Strictly follow the 80/20 rule: 80% non-promotional (Educational, Entertaining, BTS, Social Proof, UGC) and 20% promotional.
                    - Mix English and Roman Urdu.
                    - Output as a structured Markdown Table:
                      | Day | Content Pillar | Content Type | Content Idea | Caption (Roman Urdu/Eng) | CTA |
                    """

                    response = client.models.generate_content_stream(
                        model="gemini-3-flash-preview",
                        contents=calendar_prompt,
                    )
                    st.write_stream(stream_text(response))

                except Exception as e:
                    st.error(f"Error generating calendar: {e}")
