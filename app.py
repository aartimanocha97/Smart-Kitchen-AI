
import streamlit as st
from pathlib import Path

from main import recommend_recipes, INGREDIENTS
from ingredient_detector import detect_ingredients

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Kitchen AI",
    page_icon="🍳",
    layout="centered"
)

st.title("Smart Kitchen AI")
st.write(
    "Upload a food photo or enter ingredients manually "
    "to discover recipes you can make!"
)

# ---------------- SESSION STATE ----------------

if "detected_ingredients" not in st.session_state:
    st.session_state.detected_ingredients = []

if "selected_ingredients" not in st.session_state:
    st.session_state.selected_ingredients = []

# ---------------- IMAGE UPLOAD ----------------

st.subheader("Detect Ingredients from an Image")

uploaded_file = st.file_uploader(
    "Upload a food image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Image",
        width="stretch"
    )

    if st.button("Detect Ingredients"):

        image_path = Path("uploaded_ingredients.jpg")
        image_path.write_bytes(uploaded_file.getvalue())

        with st.spinner("Detecting ingredients..."):

            detected = detect_ingredients(str(image_path))

            st.session_state.detected_ingredients = detected

            valid_options = set(INGREDIENTS.values())

            st.session_state.selected_ingredients = [
                ingredient
                for ingredient in detected
                if ingredient in valid_options
            ]

        st.rerun()

# ---------------- CONFIRM INGREDIENTS ----------------

st.subheader("Confirm Your Ingredients")

if st.session_state.detected_ingredients:
    st.write("AI detected:")
    st.write(", ".join(st.session_state.detected_ingredients))

all_ingredients = sorted(set(INGREDIENTS.values()))

selected_ingredients = st.multiselect(
    "Select the ingredients you have:",
    options=all_ingredients,
    key="selected_ingredients"
)

# ---------------- MANUAL INGREDIENT INPUT ----------------

st.subheader("Add Ingredients Manually")

manual_input = st.text_input(
    "Enter additional ingredients separated by commas",
    placeholder="Example: potato, onion, tomato"
)

# ---------------- RECIPE RECOMMENDATIONS ----------------

if st.button("🍽️ Find Recipes", type="primary"):

    manual_ingredients = [
        item.strip()
        for item in manual_input.split(",")
        if item.strip()
    ]

    final_ingredients = list(set(
        selected_ingredients + manual_ingredients
    ))

    if not final_ingredients:
        st.warning("Please select or enter at least one ingredient.")

    else:

        with st.spinner("Finding the best recipes for you..."):

            recommendations = recommend_recipes(final_ingredients)

        st.divider()
        st.header("🍲 Recommended Recipes")

        if not recommendations:

            st.info(
                "No matching recipes found. "
                "Try adding more ingredients!"
            )

        else:

            st.success(
                f"Found {len(recommendations)} matching recipes!"
            )

            for index, recipe in enumerate(recommendations, start=1):

                recipe_name = recipe.get("name", "Unnamed Recipe")

                with st.expander(
                    f"🍽️ {index}. {recipe_name} "
                    f"— {recipe.get('score', 0)}% match",
                    expanded=(index == 1)
                ):

                    # -------- RECIPE INFORMATION --------

                    st.subheader("📋 Recipe Information")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            f"**Cuisine:** "
                            f"{recipe.get('cuisine', 'N/A')}"
                        )
                        st.write(
                            f"**Diet:** "
                            f"{recipe.get('diet', 'N/A')}"
                        )
                        st.write(
                            f"**Difficulty:** "
                            f"{recipe.get('difficulty', 'N/A')}"
                        )

                    with col2:
                        st.write(
                            f"**Preparation:** "
                            f"{recipe.get('prep_time_min', 'N/A')} min"
                        )
                        st.write(
                            f"**Cooking:** "
                            f"{recipe.get('cook_time_min', 'N/A')} min"
                        )
                        st.write(
                            f"**Servings:** "
                            f"{recipe.get('servings', 'N/A')}"
                        )

                    st.divider()

                    # -------- INGREDIENT MATCHING --------

                    st.subheader("Ingredient Matching")

                    st.write(
                        "**Available ingredients:** "
                        + ", ".join(recipe.get("matched", []))
                    )

                    missing = recipe.get("missing", [])

                    if missing:
                        st.write(
                            "**Ingredients you still need:** "
                            + ", ".join(missing)
                        )
                    else:
                        st.success(
                            "You have all the required ingredients!"
                        )

                    st.divider()

                    # -------- COMPLETE INGREDIENT LIST --------

                    st.subheader("🥕 Complete Ingredients")

                    for item in recipe.get("ingredients", []):

                        name = item.get("name", "Unknown")
                        qty = item.get("qty", "")
                        unit = item.get("unit", "")
                        optional = item.get("optional", False)

                        quantity = f"{qty} {unit}".strip()

                        if optional:
                            st.write(
                                f"• {name} — {quantity} (Optional)"
                            )
                        else:
                            st.write(
                                f"• {name} — {quantity}"
                            )

                    st.divider()

                    # -------- COOKING INSTRUCTIONS --------

                    st.subheader("👩‍🍳 How to Prepare")

                    steps = recipe.get("steps", [])

                    if steps:

                        for step_number, step in enumerate(
                            steps, start=1
                        ):
                            st.write(f"**Step {step_number}:** {step}")

                    else:
                        st.info(
                            "Cooking instructions are not available "
                            "for this recipe."
                        )
