
from ultralytics import YOLO

# Load our pretrained AI model
model = YOLO("yolo11n.pt")

# Ask AI to detect objects in a sample image
results = model.predict(
    source="https://ultralytics.com/images/bus.jpg",
    save=True,
    conf=0.25
)

# Print the objects detected
for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        object_name = result.names[class_id]
        confidence = float(box.conf[0]) * 100

        print(f"{object_name}: {confidence:.1f}% confidence")

print("Detection test completed!")
