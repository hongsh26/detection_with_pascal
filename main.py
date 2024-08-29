import xml.etree.ElementTree as ET
import os
import cv2
import argparse

parser = argparse.ArgumentParser(description="Do you want to see original image?")

parser.add_argument('--original', '-o', action='store_true', help='want to see them')
args = parser.parse_args()

path = 'data/VOCdevkit/VOC2012/JPEGImages'
image_list = os.listdir(path)
image_list = image_list[:5]

xml_list = []

def showImage(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ESC 누르면 다음 사진 확인 가능
for image in image_list:
    img = cv2.imread(os.path.join(path, image))
    if (args.original):
        showImage('original', img)
    xml_list.append(image[:11] + '.xml')

object_list = []
for xml in xml_list:
    tree = ET.parse(os.path.join('data/VOCdevkit/VOC2012/Annotations', xml))
    root = tree.getroot()
    file_name = root.find('filename').text
    image_path = os.path.join(path, file_name)
    for obj in tree.findall('object'):
        name = obj.find('name').text

        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        position = (xmin, ymin, xmax, ymax)
        object_dict = {'name': name, 'position': position, 'xml': file_name}
        object_list.append(object_dict)

for xml in xml_list:
    file = xml[:11]
    li = [obj for obj in object_list if obj['xml'][:11] == file]
    image_path = os.path.join(path, li[0]['xml'][:11] + '.jpg')
    image = cv2.imread(image_path)
    image_copy = image.copy()
    for obj in li:
        image_copy = cv2.rectangle(image_copy, (obj['position'][0], obj['position'][1]),
                                   (obj['position'][2], obj['position'][3]), (200, 255, 0), 2)
    showImage('image', image_copy)