import streamlit as st
from app.database import SessionLocal
from app.models import User

# Configure the look of the page
st.set_page_config(
    page_title="AI News Aggregator",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AI News Aggregator")
st.markdown("""
Welcome to the highest-signal tech newsletter on the internet. 

We aggregate the best breaking news from **Fireship, Wired AI, The Verge, and Matt Wolfe**, use AI to summarize the noise into actionable bullet points, and deliver it straight to your inbox.
""")

st.divider()

# Build the Email Capture Form
st.subheader("📬 Subscribe for Daily Updates")

with st.form("subscribe_form", clear_on_submit=True):
    user_email = st.text_input("Enter your email address:", placeholder="steve@apple.com")
    submitted = st.form_submit_button("Join the List")

    if submitted:
        if not user_email or "@" not in user_email or "." not in user_email:
            st.error("❌ Please enter a valid email address.")
        else:
            db = SessionLocal()
            try:
                # Check if the user is already in the database
                existing_user = db.query(User).filter(User.email == user_email).first()
                if existing_user:
                    st.warning("⚠️ You are already subscribed to the list!")
                else:
                    # Add the new user!
                    new_user = User(email=user_email)
                    db.add(new_user)
                    db.commit()
                    st.success("🎉 Success! You've been added to the intelligence feed.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
            finally:
                db.close()

st.divider()
st.caption("")