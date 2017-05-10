#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import os

root = './action_images/'
root_t = './action_image_lib/'
hist_dst = './history/'
'''
for i in range(1,6):
    path = os.path.join(root,str(i))
    file_list = os.listdir(path)
    path_t = os.path.join(root_t,str(i))
    for file in file_list:
        src = os.path.join(path,file)
        dst = os.path.join(path_t, file)
        image = Image.open(src)
        image = image.resize((360,240),Image.ANTIALIAS)
        image.save(dst)
'''

def create_image(user,date,action_code_list):
    image_size = (360,240*len(action_code_list))
    full_image = Image.new('RGB', image_size)
    for i in range(len(action_code_list)):
        action_code = action_code_list[i]
        sub_name = action_code.split('.')[0]
        sub_image_src = os.path.join(root_t,sub_name,"%s.jpg"%action_code)
        sub_image = Image.open(sub_image_src)
        full_image.paste(sub_image,(0,i*240))
    full_image.save(os.path.join(hist_dst,user,'%s.jpg'%date))


if __name__ == '__main__':
    date = "20170511"
    action_code_list = ['2.1.3','2.2.3','2.1.2','5.1.6','5.2.5']
    create_image(date, action_code_list)
