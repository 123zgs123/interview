import json
import cv2
path = "./boxes.json"

def get_object_position(path):
    '''
    :param path: 目标路径
    :return: 目标坐标的字典
    '''
    file = open(path, 'rb')
    filejson = json.load(file)
    out_dict = 0
    for sub_dict in filejson['boxes']:
        if sub_dict['name'] == 'box_b' and 'rectangle' in sub_dict.keys():
            out_dict = sub_dict['rectangle']
    return out_dict

def image_fill(oimage,dimage,object_position,same_ratio=False):
    '''
    :param oimage: 原始用于填充图像
    :param dimage: 待填充图像
    :param object_position: 待填充图像中待填充区域坐标,储存在字典中
    :param same_ratio: 是否等比例填充，默认为拉伸填充,填充方式为双线性插值
    :return: 填充完成的图像
    '''
    left_top = object_position['left_top']
    right_bottom = object_position['right_bottom']
    dheight = abs(left_top[0] - right_bottom[0]+1)
    dwidth = abs(left_top[1] - right_bottom[1]+1)
    if same_ratio:
        oheight, owidth = oimage.shape[:2]
        original_ratio = oheight/owidth
        destin_ratio = dheight/dwidth
        if (original_ratio >= 1 and original_ratio >= destin_ratio) or (original_ratio < 1 and original_ratio > destin_ratio):
            fill_image = cv2.resize(oimage,(round(original_ratio*dwidth),dwidth))
            dimage[left_top[0]:right_bottom[0] + 1, left_top[1]:right_bottom[1] + 1] = fill_image[:dheight+1]
        else:
            fill_image = cv2.resize(oimage,(dheight,round(dheight/original_ratio)))
            dimage[left_top[0]:right_bottom[0] + 1, left_top[1]:right_bottom[1] + 1] = fill_image[:,:dwidth + 1]

    else:
        dimage[left_top[0]:right_bottom[0] + 1, left_top[1]:right_bottom[1] + 1] = cv2.resize(oimage,(dheight,dwidth))
    return dimage


out_dict = get_object_position(path)
if out_dict:
    print(out_dict)
else:
    print('there is no targets that meet the conditions ')




