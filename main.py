
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Load ingredient database
with open(BASE_DIR / "ingredients.json", "r", encoding="utf-8") as file:
    INGREDIENT_DATABASE = json.load(file)

# Load recipe database
with open(BASE_DIR / "recipes.json", "r", encoding="utf-8") as file:
    RECIPE_DATABASE = json.load(file)

RECIPES = RECIPE_DATABASE["recipes"]

# Ingredient names and aliases used by the image detector
INGREDIENTS = {}

for category, items in INGREDIENT_DATABASE["categories"].items():
    for ingredient, aliases in items.items():
        canonical = ingredient.strip().lower()
        INGREDIENTS[canonical] = canonical

        if isinstance(aliases, list):
            for alias in aliases:
                INGREDIENTS[alias.strip().lower()] = canonical

# Build a dictionary of ingredient names and their aliases
INGREDIENT_ALIASES = INGREDIENTS

for category, items in INGREDIENT_DATABASE["categories"].items():
    for ingredient, aliases in items.items():
        canonical = ingredient.strip().lower()
        INGREDIENT_ALIASES[canonical] = canonical

        if isinstance(aliases, list):
            for alias in aliases:
                INGREDIENT_ALIASES[alias.strip().lower()] = canonical


def normalize_ingredients(user_ingredients):
    """Convert ingredient names and aliases to canonical names."""
    normalized = []

    for ingredient in user_ingredients:
        name = str(ingredient).strip().lower()

        if name:
            canonical = INGREDIENT_ALIASES.get(name, name)

            if canonical not in normalized:
                normalized.append(canonical)

    return normalized


def recommend_recipes(user_ingredients):
    """Rank recipes according to the required ingredients available."""
    available = set(normalize_ingredients(user_ingredients))
    recommendations = []

    for recipe in RECIPES:
        required = []
        optional = []

        for item in recipe.get("ingredients", []):
            name = item["name"].strip().lower()

            # Water is treated as an implicit ingredient
            if name == "water":
                continue

            if item.get("optional", False):
                optional.append(name)
            else:
                required.append(name)

        matched = [name for name in required if name in available]
        missing = [name for name in required if name not in available]
        optional_matched = [name for name in optional if name in available]

        if not required:
            score = 100.0
        else:
            score = (len(matched) / len(required)) * 100

        # Only recommend recipes matching at least one available ingredient
        if matched or optional_matched:
            recommendations.append({
                **recipe,
                "score": round(score, 1),
                "matched": matched + optional_matched,
                "missing": missing,
                "optional_matched": optional_matched,
            })

    recommendations.sort(
        key=lambda recipe: (
            -recipe["score"],
            len(recipe["missing"]),
            recipe.get("prep_time_min", 0)
            + recipe.get("cook_time_min", 0)
        )
    )

    return recommendations
