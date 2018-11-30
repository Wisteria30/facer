import cognitive_face as CF
import requests
import cv2
import tempfile
from matplotlib import pyplot as plt


KEY = (
    {"key"}
)  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = (
    "https://westus.api.cognitive.microsoft.com/face/v1.0/"
)  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = "https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg"
# img_url = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/220px-Lenna_%28test_image%29.png"
faces = CF.face.detect(img_url)


def imread_web(url):
    # 画像をリクエストする
    response = requests.get(url)
    img = None
    # Tempfileを作成して即読み込む
    with tempfile.NamedTemporaryFile(dir="./") as fp:
        fp.write(response.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img


raw_img = imread_web(img_url)
for face in faces:
    rect = face["faceRectangle"]
    x = rect["left"]
    y = rect["top"]
    h = rect["height"]
    w = rect["width"]
    face_cut = raw_img[y : y + h, x : x + w]
    face_cut = cv2.cvtColor(face_cut, cv2.COLOR_BGR2RGB)

# cv2.imwrite("hoge.jpg", face_cut)
plt.imshow(face_cut)
plt.show()
