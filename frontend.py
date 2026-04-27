import streamlit as st
from app.database import SessionLocal
from app.models import User

st.set_page_config(page_title="AI Tech Intelligence", page_icon="🚀", layout="centered")

st.title("🚀 AI Tech Intelligence")
st.markdown("Welcome to the highest-signal tech newsletter on the internet. Choose your feeds below.")
st.divider()

st.subheader("📬 Subscribe for Daily Updates")

with st.form("subscribe_form", clear_on_submit=True):
    user_email = st.text_input("Enter your email address:", placeholder="steve@apple.com")
    
    st.markdown("**Customize your intelligence feed:**")
    # Add checkboxes for the specific feeds
    feed_fireship = st.checkbox("Fireship (Developer News)", value=True)
    feed_wired = st.checkbox("Wired AI (Tech Trends)", value=True)
    feed_verge = st.checkbox("The Verge (Consumer Tech)", value=True)
    feed_matt = st.checkbox("Matt Wolfe (AI Tools)", value=True)

    submitted = st.form_submit_button("Join the List")

    if submitted:
        if not user_email or "@" not in user_email or "." not in user_email:
            st.error("❌ Please enter a valid email address.")
        else:
            try:
                db = SessionLocal()
                
                existing_user = db.query(User).filter(User.email == user_email).first()
                if existing_user:
                    st.warning("👋 You're already on the list! We'll keep you updated.")
                else:
                    # Compile choices
                    chosen_feeds = []
                    if feed_fireship: chosen_feeds.append("1")
                    if feed_wired: chosen_feeds.append("2")
                    if feed_verge: chosen_feeds.append("3")
                    if feed_matt: chosen_feeds.append("4")
                    
                    pref_string = ",".join(chosen_feeds)
                    
                    new_user = User(email=user_email, preferences=pref_string)
                    db.add(new_user)
                    db.commit()
                    
                    st.success("🎉 You're in! Check your inbox for the next update.")
                    st.balloons() 

            except Exception as e:
                print(f"DEBUG ERROR: {e}") 
                
                st.error("🔌 Connectivity hiccup! Please try again in a moment.")
                
            finally:
                if 'db' in locals():
                    db.close()