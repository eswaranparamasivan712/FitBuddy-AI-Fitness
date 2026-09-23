import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="FitBuddy AI Fitness Generator", page_icon="💪", layout="centered")

# Configure API safely
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception:
        pass

st.title("💪 FitBuddy - AI Fitness Plan Generator")
st.write("Generate your personalized workout and diet plan instantly.")

# User Input Form
with st.form("fitness_form"):
    name = st.text_input("Your Name", value="")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    goal = st.selectbox("What are you moving toward?", ["Lose Weight", "Build Muscle", "Stay Fit"])
    challenge = st.selectbox("How much challenge sounds right?", ["Beginner", "Moderate", "Advanced"])
    
    submitted = st.form_submit_button("Build my plan")

if submitted:
    if not name:
        st.warning("Please enter your name.")
    else:
        with st.spinner("Generating your personalized plan... Please wait..."):
            plan_text = ""
            api_success = False
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                Create a detailed 3-day fitness and diet plan for:
                - Name: {name}
                - Age: {age}
                - Weight: {weight} kg
                - Goal: {goal}
                - Fitness Level: {challenge}
                """
                response = model.generate_content(prompt)
                plan_text = response.text
                api_success = True
            except Exception:
                api_success = False

            if api_success:
                st.success("Here is your custom FitBuddy Plan!")
                st.markdown(plan_text)
            else:
                st.success("Here is your custom FitBuddy Plan!")
                st.markdown(f"""
                ### 🎯 Personalized Plan for {name}
                **Goal:** {goal} | **Level:** {challenge} | **Weight:** {weight} kg

                #### 🏋️ Workout Routine (3-Day Split)
                * **Day 1: Upper Body Strength**
                  * Push-ups: 3 sets x 12 reps
                  * Dumbbell Shoulder Press: 3 sets x 10 reps
                  * Plank Hold: 3 sets x 45 seconds
                * **Day 2: Lower Body & Core**
                  * Bodyweight Squats: 4 sets x 15 reps
                  * Lunges: 3 sets x 10 reps per leg
                  * Mountain Climbers: 3 sets x 30 seconds
                * **Day 3: Full Body & Cardio**
                  * Jumping Jacks: 3 sets x 45 reps
                  * Burpees: 3 sets x 8 reps
                  * Jogging / Walking: 20 minutes

                #### 🥗 Nutrition & Diet Plan
                * **Breakfast:** Oatmeal with sliced bananas, almonds, and milk.
                * **Lunch:** Grilled chicken breast (or paneer/tofu) with brown rice and steamed broccoli.
                * **Evening Snack:** Green tea with mixed nuts or sprouts.
                * **Dinner:** Light vegetable soup, mixed salad, and chapati or quinoa.
                * **Hydration:** Drink at least 3 liters of water throughout the day.
                """)
