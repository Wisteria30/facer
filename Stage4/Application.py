from PIL import Image, ImageDraw, ImageFont
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import requests
import sys


# Face APIで顔の認識
def detect_face(img_path, api_key):
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": api_key,
    }
    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"

    data = open(img_path, "rb")
    response = requests.post(face_api_url, headers=headers, data=data)
    print(response.json())
    return response.json()


# jsonから顔座標の取得
def getRectangle(faceDictionary):
    rect = faceDictionary["faceRectangle"]
    left = rect["left"]
    top = rect["top"]
    bottom = left + rect["height"]
    right = top + rect["width"]
    return (left, top, bottom, right)


# 画像を学習用にデータ変換して予測
def predict(images, model):
    model = model
    imgs = []
    imgs.append([img_to_array(img.resize((224, 224))) / 255 for img in images])
    return model.predict(imgs)


if __name__ == "__main__":
    img_path = sys.argv[1]
    with open("../apikey.ini", "r") as f:
        api_key = f.read()
        f.close()
    faces = detect_face(img_path, api_key)
    raw_img = load_img(img_path)
    model = load_model("../model/my_model.h5")
    rectangles = predict_face = []
    for face in faces:
        rect = getRectangle(face)
        rectangles.append(rect)
        crop_img = raw_img.crop(rect)
        predict_face.append(crop_img)
    # 予測
    predicts_result = predict(predict_face, model)
    # 描画系
    draw = ImageDraw.Draw(raw_img)
    for i, rect in enumerate(rectangles):
        draw.line(
            (
                (rect[0], rect[1]),
                (rect[2], rect[1]),
                (rect[2], rect[3]),
                (rect[0], rect[3]),
                (rect[0], rect[1]),
            ),
            fill=(255, 255, 0),
            width=10,
        )
        # 何かしらのフォントを指定(Macのものなので適宜変更)
        fnt = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
        draw.text(
            (rect[0], rect[3]), str(*predicts_result[i]), font=fnt, fill=(255, 0, 0)
        )
    raw_img.show()
