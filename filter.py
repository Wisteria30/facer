import glob
import cv2

img_path_list = glob.glob("./image/face_img/*.jpg")
img_path_list.sort()
for i, img_path in enumerate(img_path_list):
    try:
        raw_img = cv2.imread(img_path)
        imp_file = img_path.replace("./image/face_img/", "")
        if raw_img.shape[0] >= 64 and raw_img.shape[1] >= 64:
            dir_path = "./image/over64/"
        else:
            dir_path = "./image/less64/"
        cv2.imwrite(dir_path + imp_file, raw_img)
        print("{}/{} {} filtering!!!".format(i + 1, len(img_path_list), dir_path))
    except:
        print("{}/{} error!!!".format(i + 1, len(img_path_list)))
