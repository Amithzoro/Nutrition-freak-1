import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# File names
FILENAME = "food_log.xlsx"
RECIPES_FILE = "recipes.json"

# Load recipes with error handling
def load_recipes():
    if not os.path.exists(RECIPES_FILE):
        st.error("❌ recipes.json not found. Please upload it.")
        return []
    try:
        with open(RECIPES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        st.error("❌ recipes.json is not valid JSON.")
        return []

# Load Excel food log
def load_log():
    if os.path.exists(FILENAME):
        try:
            return pd.read_excel(FILENAME)
        except Exception as e:
            st.warning(f"⚠️ Could not read {FILENAME}. Starting fresh. Error: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# Save food log
def save_log(df):
    try:
        df.to_excel(FILENAME, index=False)
        st.success(f"📂 Log updated in {FILENAME}")
    except Exception as e:
        st.error(f"❌ Error saving to Excel: {e}")

# Add meal
def add_meal(recipe, image_file):
    new_record = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Meal": recipe['title'],
        "Country": recipe.get("Country", "Unknown"),
        "Calories": recipe.get("Calories", 0),
        "Protein (g)": recipe.get("Protein", 0),
        "Carbs (g)": recipe.get("Carbs", 0),
        "Fat (g)": recipe.get("Fat", 0),
        "Fiber (g)": recipe.get("Fiber", 0),
        "Sugar (g)": recipe.get("Sugar", 0),
        "Sodium (mg)": recipe.get("Sodium", 0),
        "Ingredients": ', '.join(recipe.get("ingredients", [])),
        "Instructions": ' '.join(recipe.get("directions", [])),
        "Image": image_file.name if image_file else None
    }
    return new_record

# --- Streamlit UI ---
st.set_page_config(page_title="Global Nutrition Logger", page_icon="🌎")

st.title("🌎 Global Nutrition Logger")
st.write("Track your meals with recipe database, nutrition info & images.")

recipes = load_recipes()
log_df = load_log()

# Menu
menu = st.sidebar.radio("Menu", ["Add a Meal", "View Log"])

if menu == "Add a Meal":
    st.header("➕ Add a Meal")

    if recipes:
        food_names = [r['title'] for r in recipes]
        selected_food = st.selectbox("Select Food", food_names)
        recipe = next((r for r in recipes if r['title'] == selected_food), None)

        image_file = st.file_uploader("Upload Meal Image", type=["jpg", "jpeg", "png"])

        if st.button("Add Meal"):
            if recipe:
                record = add_meal(recipe, image_file)
                log_df = pd.concat([log_df, pd.DataFrame([record])], ignore_index=True)
                save_log(log_df)
                st.success(f"✅ {recipe['title']} logged successfully!")

                # Health tips
                st.subheader("💡 Health Tips")
                if record["Protein (g)"] < 15:
                    st.write("- Consider adding more lean protein for muscle repair.")
                if record["Carbs (g)"] > 70:
                    st.write("- High-carb meal. Balance with whole grains.")
                if record["Fiber (g)"] < 5:
                    st.write("- Add veggies/fruits for better fiber intake.")
    else:
        st.warning("⚠️ No recipes loaded. Please upload recipes.json file.")

elif menu == "View Log":
    st.header("📖 Food Log")
    if not log_df.empty:
        st.dataframe(log_df)
    else:
        st.info("No meals logged yet.")
