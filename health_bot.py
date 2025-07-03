import streamlit as st
import requests

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide"
)

st.title("AI Health & Fitness Planner")
st.markdown("Generate personalized dietary and fitness plans and goals.")

groq_api_key = "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"

# User Inputs
st.header("👤 Your Profile")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
    dietary_preferences = st.multiselect(
        "Dietary Preferences",
        ["Vegetarian", "Vegan", "Jain", "Keto", "Gluten Free", "Low Carb", "Dairy Free"]
    )
    region = st.selectbox(
        "Preferred Indian Cuisine",
        ["North Indian", "South Indian", "East Indian", "West Indian", "North East Indian", "Mixed/No Preference"]
    )

with col2:
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0)
    sex = st.selectbox("Gender", ["Male", "Female", "Other"])
    fitness_goals = st.selectbox(
        "Fitness Goals",
        ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"]
    )

# Groq Query Function
def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return f"Error: {response.text}"
    return response.json()["choices"][0]["message"]["content"]

# Button Action
if st.button("🎯 Generate My Plan", use_container_width=True):
    with st.spinner("Creating your customized health and fitness plan..."):
        user_profile = f"""
        Age: {age}, Weight: {weight}kg, Height: {height}cm, Sex: {sex},
        Activity Level: {activity_level}, Dietary Preferences: {', '.join(dietary_preferences) or 'None'},
        Fitness Goals: {fitness_goals}, Preferred Cuisine Region: {region}
        """

        diet_prompt = f"""
Act as a professional Indian dietician. Based on the following profile:

{user_profile}

Generate a **7-day Indian meal plan** that:
- Uses foods and recipes from {region} cuisine.
- Avoids repeating meals across the week.
- Follows user's preferences (e.g., no onion/garlic for Jain, dairy-free etc.)
- Includes breakfast, lunch, dinner, and snacks.
- Mentions calories, protein, fat, carbs.
- Add hydration & fiber tips.
- At the end, add a "Common Guidance" section with advice and substitutes.
"""

        fitness_prompt = f"""
Act as a fitness coach. Based on this profile:

{user_profile}

Create a **weekly workout plan** that includes:
- Warm-ups, main workouts, cool-downs
- Each day's routine separately
- Explain purpose of each part
- Conclude with overall fitness tips and safety precautions
"""

        diet_response = query_groq(diet_prompt)
        fitness_response = query_groq(fitness_prompt)

        st.subheader("📋 7-Day Dietary Plan")
        st.write(diet_response)

        st.subheader("💪 Weekly Fitness Plan")
        st.write(fitness_response)
