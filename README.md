# Smart Kitchen AI 

An AI-powered ingredient detection and recipe recommendation system that
helps users discover recipes using ingredients they already have.

## Overview

Smart Kitchen AI combines computer vision with a rule-based
recommendation system. Users can upload a food image or enter
ingredients manually. The application detects supported food items from
the image, lets users confirm their ingredients, and recommends recipes
based on ingredient availability.

## Problem Statement

People often have ingredients at home but are unsure what they can
prepare with them. This project aims to make recipe discovery easier by
connecting available ingredients with suitable recipes.

## Key Features

-   **Image-based ingredient detection:** Uses a pretrained YOLO model
    to identify supported food items in an uploaded image.
-   **Manual ingredient selection:** Users can select ingredients from
    the available catalogue.
-   **Ingredient confirmation:** Users can review and adjust the
    detected ingredients before requesting recommendations.
-   **Recipe recommendations:** Matches available ingredients against
    the recipe database.
-   **Match percentage:** Displays the proportion of a recipe's required
    ingredients that the user has.
-   **Missing ingredient information:** Shows which required ingredients
    are still needed.
-   **Recipe details:** Displays cuisine, diet type, difficulty,
    preparation time, cooking time, servings, ingredient quantities, and
    cooking steps.

## How It Works

1.  The user uploads a food image or selects ingredients manually.
2.  The pretrained YOLO model predicts supported food classes in the
    uploaded image.
3.  Detected labels are mapped to the project's ingredient names.
4.  The user confirms or edits the ingredient selection and can add more
    ingredients manually.
5.  The recommendation module compares the selected ingredients with the
    recipes stored in `recipes.json`.
6.  Recipes are scored and ranked, and the application displays matching
    recipes with available and missing ingredients.

## Recommendation Logic

The recommendation module uses rule-based ingredient matching; it is not
a separately trained recipe recommendation model.

The match score is calculated as:

\[ `\text{Match Score}`{=tex} =
`\frac{\text{Number of matched required ingredients}}`{=tex}
{`\text{Total number of required ingredients}`{=tex}} `\times 100`{=tex}
\]

Optional ingredients are handled separately and are not counted as
required ingredients in this score. Recommendations are ranked using the
match score, missing ingredients, and preparation/cooking time.

## Technology Stack

  Technology         Purpose
  ------------------ ----------------------------------------
  Python             Main programming language
  Streamlit          Interactive web application interface
  Ultralytics YOLO   Pretrained object-detection model
  JSON               Storage for ingredient and recipe data
  pathlib            File path handling

## Project Structure

``` text
Smart-Kitchen-AI/
├── app.py
├── main.py
├── ingredient_detector.py
├── ingredients.json
├── recipes.json
├── best.pt
├── test_detection.py
├── .gitignore
└── README.md
```

## Dataset Information

The project uses two JSON data files:

-   `ingredients.json` --- ingredient catalogue, including ingredient
    names and aliases.
-   `recipes.json` --- recipe records containing recipe information,
    ingredients, quantities, and preparation steps.

The ingredient catalogue contains 448 entries, and the recipe database
contains 106 recipes. The image detector supports 35 food-related
classes. These counts describe different parts of the system: the
detector does not recognize all 448 catalogue entries.

## Installation and Setup

### 1. Clone the repository

``` bash
git clone https://github.com/aartimanocha97/Smart-Kitchen-AI.git
cd Smart-Kitchen-AI
```

### 2. Create and activate a virtual environment (recommended)

On macOS or Linux:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required packages

``` bash
python -m pip install --upgrade pip
python -m pip install streamlit ultralytics
```

### 4. Run the application

``` bash
python -m streamlit run app.py
```

Streamlit will provide a local URL to open the application in your
browser.

## Model File

The application loads the YOLO weights from `best.pt` in the project
directory. Keep this file in the same directory as
`ingredient_detector.py`, as the code resolves the model path relative
to that file.

## Limitations

-   Ingredient detection is limited to the classes supported by the
    pretrained model.
-   Detection quality can be affected by lighting, image quality,
    overlapping objects, object size, and visually similar foods.
-   The user may need to confirm or correct image detections.
-   Recipe recommendations depend on the ingredients and recipe
    information available in the JSON files.
-   The recommendation module uses rule-based matching rather than a
    trained recommendation algorithm.

## Future Improvements

-   Expand the range of detectable ingredients.
-   Improve detection performance across different lighting and
    background conditions.
-   Add more recipes and richer recipe metadata.
-   Add filters for cuisine, dietary preference, difficulty, and
    preparation time.
-   Evaluate ingredient detection and recommendation quality using a
    documented test dataset and suitable metrics.

## Author

**Aarti Manocha**

## Repository

[Smart Kitchen AI on
GitHub](https://github.com/aartimanocha97/Smart-Kitchen-AI)
