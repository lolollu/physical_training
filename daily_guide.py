#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import history

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('msyh', './fonts/msyh.ttf'))


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
import time

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

def write_lines(user,date,actions,history_count):
    lines = []
    lines.append('*** %s *** | ***%d***'%(date,history_count))
    lines.append('')
    lines.append('~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for action in actions:
        action_history = history.action_reps_record(user,action['code'],3)
        lines.append('Code : %s'%action['code'])
        #f.write('Rest Time : %d\n'%action.action_dict['rest_time'] )
        lines.append('Regular Reps :%2d | Regular Times Each Rep :%2d'%(action['regular_reps'],
                                                                             action['regular_times'][0]))
        reps = ''
        for i in range(action['regular_reps']):
            reps += "       |"
        #f.write('*User Reps : \n')
        lines.append('History   :  %d times in total'%history.count_action_times(user,action['code']))
        lines.append('*User Times : %s'%reps)
        for date, one in action_history:
            line = '%s      '%date
            for i in one:
                if i>=10:
                    line += '  %d |'%i
                else:
                    line += '   %2d |'%i
            lines.append(line)
        lines.append('_______________________________________________________________________________________________________________')
    lines.append('Notes:')
    return lines


def gen_pdf(user,date,actions,history_count):
    pdf_file = canvas.Canvas('./history/%s/%s.pdf'%(user,date), pagesize = landscape(A4))
    width,height = landscape(A4)
    log_lines = write_lines(user,date,actions, history_count)
    text_object = pdf_file.beginText()
    text_object.setTextOrigin(60,height-52)
    text_object.setFont("msyh",11)
    for line in log_lines:
        text_object.textOut(line)
        text_object.moveCursor(0,12)
    text_object.setFillColorRGB(0.4,0,1)
    pdf_file.drawText(text_object)
    for i in range(len(actions)):
        action_code = actions[i]['code']
        sub_name = action_code.split('.')[0]
        sub_image_src = os.path.join(root_t,sub_name,"%s.jpg"%action_code)
        pdf_file.drawImage(sub_image_src, 460,431-i*96.3,145,82)

    pdf_file.save()

if __name__ == '__main__':
    date = "20170511"
    action_code_list = ['2.1.3','2.2.3','2.1.2','5.1.6','5.2.5']
    create_image(date, action_code_list)
