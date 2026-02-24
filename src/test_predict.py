from PIL import Image
from src.predict import predict_food
from src.nutrition import get_nutrition


img = Image.open(r'C:\Machine_Learning_Projects\foodsnap_ai\src\test_img.jpg')
food, conf = predict_food(img)
nutrition = get_nutrition(food)

print("Predicted Food:", food)
print("Confidence:", conf)
print("Nutritions: ", nutrition)