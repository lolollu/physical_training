def print_calendar(year,month,date = 1):
    month_dict = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July',
                  '8':'August','9':'September','10':'October','11':'November','12':'December'}
    
  
    if month in range(1,13) and date in range(1,31):
        month_str = str(month)
        if month_str in month_dict:
            month_str = month_dict[month_str]
    else:
        print('illegal')
        return -1
    
    
    print('%15s%8d'%(month_str,year))
    print('-'*33)
    print('Sun  Mon  Tue  Wed  Thu  Fri  Sat')
    
    
    first_day = get_start_day(year,month,1)
  
    month_num = days_of_month(year,month)

    each_day = 0
    for index in range(1,43):
    
        if index < first_day + 1:
            print(' '*5,end = '')
        else:
            if (index - 1) % 7 == 0:
                print('')
            each_day += 1
            if each_day > month_num:
                return False
            if each_day < 10:
                if each_day == date:
                    print('%-5s'%('--'),end = '')
                else:
                    print(' %-4d'%(each_day),end = '')
            else:
                if each_day == date:
                    print('%-5s'%('--'),end = '')
                else:
                    print('%-5d'%(each_day),end = '')
                
              

def get_start_day(year,month,date):
    total_days = 0
    #遍历年份
    for one_year in range(2010,year):
        if is_leap_year(one_year):
            total_days += 366
        else:
            total_days += 365
 
    for one_month in range(1,month):
        total_days += days_of_month(year,one_month)
  
    total_days += date

    
    day = (total_days % 7 + 5 - 1) % 7
    

    return day

def days_of_month(year,month):
    days = 0
    if month in (1,3,5,7,8,10,12):
        days = 31
    elif month in (4,6,9,11):
        days = 30
    elif is_leap_year(year):
        days = 29
    else:
        days = 28
    return days

def is_leap_year(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    return False

def main():
    print('*'*33)
    year = int(input('请输入年份：'))
    month = int(input('请输入月份：'))
    date = int(input('请输入号数：'))
    print('*'*33)

    print_calendar(year,month,date)
    

main()