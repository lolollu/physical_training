#!/usr/bin/env python
# encoding: utf-8

import time
import datetime
#import PIL
import history
import sys

week_name = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']


class date_struct():
    def __init__(self, date):
        #print date
        time_string = time.strptime(date,"%Y%m%d")
        time_stamp = int(time.mktime(time_string))
        date_array = datetime.datetime.utcfromtimestamp(time_stamp) + datetime.timedelta(hours=8)
        self.week =  date_array.strftime("%a")
        self.month = int(date_array.strftime("%m"))
        self.year = int(date_array.strftime("%Y"))
        self.day = int(date_array.strftime("%d"))



def all_days(last, first):
    d1 = datetime.date(int(last[:4]),int(last[4:6]),int(last[6:]))
    d2 = datetime.date(int(first[:4]),int(first[4:6]),int(first[6:]))
    return (d1-d2).days

if __name__ == '__main__':
    try:
        user = sys.argv[1]
    except:
        print 'input user name'
        sys.exit()

    log_files = history.log_file_list(user)
    log_files.reverse()
    current_month = 0

    with open('./history/%s/attendence.txt'%user,'wb') as attendence:
        week_line = week_name[:]
        week_line.reverse()
        current_week_line = week_line[:]
        period = all_days(log_files[0].split('.')[0],log_files[-1].split('.')[0])
        attendence.write("%d times in %d days\n"%(len(log_files),period))
        while log_files != []:
            log_file = log_files.pop()
            date = log_file.split('.')[0]
            date_srt = date_struct(date)
            if date_srt.month != current_month:
                current_month = date_srt.month
                attendence.write("\n%d | %s\n"%(date_srt.year,month_name[date_srt.month-1]))
                for day in week_name:
                    attendence.write("%s "%day)
                attendence.write('\n')
            while current_week_line != []:
                this_day = current_week_line.pop()
                if date_srt.week != this_day:
                    attendence.write("    ")
                else:
                    attendence.write("%3d "%date_srt.day)
                    break
            #print current_week_line
            if current_week_line == []:
                current_week_line = week_line[:]
                attendence.write('\n')
            #if date_srt.week == "Sat":
            #    attendence.write('\n')

        #print log_files
    with open('./history/%s/attendence.txt'%user,'r') as attendence:
        print attendence.read()









