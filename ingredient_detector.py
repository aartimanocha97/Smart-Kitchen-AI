

from pathlib import Path
from ultralytics import YOLO
from main import INGREDIENTS

MODEL_PATH = Path(__file__).parent / "best.pt"

model = YOLO(str(MODEL_PATH))


YOLO_TO_INGREDIENT = {
    "apple": "apple",
    "banana": "banana",
    "beetroot": "beetroot",
    "bitter_gourd": "bitter gourd",
    "bottle_gourd": "bottle gourd",
    "cabbage": "cabbage",
    "capsicum": "capsicum",
    "carrot": "carrot",
    "cauliflower": "cauliflower",
    "cherry": "cherry",
    "chilli": "green chilli",
    "coconut": "coconut",
    "cucumber": "cucumber",
    "eggplant": "eggplant",
    "ginger": "ginger",
    "grape": "grapes",
    "green_orange": "orange",
    "kiwi": "kiwi",
    "maize": "corn",
    "mango": "mango",
    "melon": "melon",
    "okra": "okra",
    "onion": "onion",
    "orange": "orange",
    "peach": "peach",
    "pear": "pear",
    "peas": "peas",
    "pineapple": "pineapple",
    "pomegranate": "pomegranate",
    "potato": "potato",
    "radish": "radish",
    "strawberry": "strawberry",
    "tomato": "tomato",
    "turnip": "turnip",
    "watermelon": "watermelon",
}


def detect_ingredients(image_path):

    results = model.predict(
        source=image_path,
        conf=0.20,
        imgsz=640,
        iou=0.45,
        max_det=100,
        augment=True,
        verbose=False
    )

    detected_items = []
    detection_details = []

    valid_ingredients = set(INGREDIENTS.values())

    for result in results:
        for box in result.boxes:

            class_id = int(box.cls[0])
            label = result.names[class_id].lower()
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int, box.xyxy[0].tolist()
            )

            ingredient = YOLO_TO_INGREDIENT.get(label)

            detection_details.append(
                f"{label} | {confidence:.2%} | "
                f"Box: {(x1, y1, x2, y2)}"
            )

            if not ingredient:
                continue

            canonical = INGREDIENTS.get(
                ingredient.lower(),
                ingredient.lower()
            )

            if canonical in valid_ingredients:
                if canonical not in detected_items:
                    detected_items.append(canonical)

    print("\n========== YOLO DETECTION REPORT ==========")

    for detail in detection_details:
        print(detail)

    if not detection_details:
        print("No objects detected.")

    print("Recognized ingredients:", detected_items)
    print("===========================================\n")

    return detected_items
