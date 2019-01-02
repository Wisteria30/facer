import glob
import cv2

img_path_list = glob.glob("../image/valu_cutout_face_over128/*.jpg")
img_path_list.sort()
for i, img_path in enumerate(img_path_list):
    try:
        raw_img = cv2.imread(img_path)
        imp_file = img_path.replace("../image/valu_cutout_face_over128/", "")
        if raw_img.shape[0] >= 224 and raw_img.shape[1] >= 224:
            dir_path = "../image/valu_cutout_face_over224/"
        else:
            dir_path = "../image/less224/"
        cv2.imwrite(dir_path + imp_file, raw_img)
        print("{}/{} {} filtering!!!".format(i + 1, len(img_path_list), dir_path))
    except:
        print("{}/{} error!!!".format(i + 1, len(img_path_list)))
