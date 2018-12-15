from watson_developer_cloud import VisualRecognitionV3, WatsonApiException
import glob
import cv2
import time

KEY = open("apikey.ini").read()
# If service instance provides IAM API key authentication
service = VisualRecognitionV3(
    "2018-03-19",
    # url is optional, and defaults to the URL below.
    url="https://gateway.watsonplatform.net/visual-recognition/api",
    iam_apikey=KEY,
)


# 画像のパスを投げて顔のjsonデータを返す
def detect_face(face_path):
    try:
        with open(face_path, "rb") as image_file:
            return service.detect_faces(images_file=image_file).get_result()
            # return json.dumps(face_result, indent=2)
    except WatsonApiException as ex:
        print(ex)


# 認識したjsonを投げて切り取った画像をフォルダに分けて配置する
def trimming(img_path, json_data):
    try:
        # ファイル名の取得
        file_name = img_path.replace("./image/original/", "")
        image = json_data["images"][0]
        # 画像の読み込み
        raw_img = cv2.imread(img_path)
        if image["faces"]:
            dir_path = "./image/face_img/"
            max_y = []
            max_x = []
            for face in image["faces"]:
                rect = face["face_location"]
                x = rect["left"]
                y = rect["top"]
                h = rect["height"]
                w = rect["width"]
                max_y.append(y + h)
                max_x.append(x + w)
            # y座標準拠の最大幅の顔を切り取り
            face_cut = raw_img[y : max(max_y), x : max_x[max_y.index(max(max_y))]]
        else:
            dir_path = "./image/error/"
            face_cut = raw_img
        # 画像の書き込み
        cv2.imwrite(dir_path + file_name, face_cut)
    except:
        pass


if __name__ == "__main__":
    # 画像のリストを取得
    img_path_list = glob.glob("./image/original/*.jpg")
    img_path_list.sort()
    for i, img_path in enumerate(img_path_list):
        face_json = detect_face(img_path)
        trimming(img_path, face_json)
        print("{}/{} trimming!!!".format(i + 1, len(img_path_list)))
        time.sleep(1)

