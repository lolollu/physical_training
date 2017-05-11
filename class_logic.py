#!/usr/bin/env python
# encoding: utf-8

import history
import relations
import user_info
import time
import random
import datetime
import os
import sys
import daily_guide


def get_new_action(action_code,potential_upgrade):
    new_action = relations.get_previos_action(action_code)
    if new_action == '':
        new_action = random.choice(potential_upgrade)
    return new_action

def main_part_logic(user,main_list):
    potential_upgrade = relations.avaliable_upgrade_codes(main_list)
    while True:
        if len(main_list) <= 3:
            break
        else:
            #main_list.remove(random.choice(main_list))
            history.kick_action(user,main_list)

    if len(main_list) == 2:
        main_list.append(get_new_action(random.choice(main_list),potential_upgrade))

    elif len(main_list) == 1:
        new_one = relations.get_previos_action(main_list[0])
        if new_one == u'':
            start = main_list[0]
            while True:
                print start
                new_one = relations.get_next_action(start)
                for new in new_one:
                    main_list.append(new)
                if len(main_list) >= 3:
                    break
                else:
                    start = new
    return main_list

def secondary_part_logic(user,second_list):
    potential_upgrade = relations.avaliable_upgrade_codes(second_list)
    while True:
        if len(second_list) <= 2:
            break
        else:
            #second_list.remove(random.choice(second_list))
            history.kick_action(user,second_list)

    if len(second_list) == 1:
        second_list.append(get_new_action(second_list[0],potential_upgrade))
    return second_list

def day_class(user):
    user_profile = user_info.load_info()
    parts = []
    #get the weighted parts
    part1 = [1,2,3]
    part2 = [3,4,5]
    last_first, last_second = history.latest_two(user)
    if last_first is not None:
        first_prop = history.action_proportion2(user,last_first)
        print first_prop
        for number in first_prop:
            if number in part1:
                part1.remove(number)
            if number in part2:
                part2.remove(number)
    if 3 in part1:
        rand_number = random.random()
        if rand_number <= 0.666667:
            part1.remove(3)
            parts.append(part1[0])
        else:
            parts.append(3)
    else:
        parts.append(random.choice(part1))
    if 3 in parts:
        part2.remove(3)
    parts.append(random.choice(part2))

    print 'Parts : ', parts

    #get actions order list
    action_codes = user_profile.levels
    container = [[],[]]
    for action_code in action_codes:
        if int(action_code.split('.')[0]) == parts[0]:
            if history.upgrade_level(user,action_code):
                next_action = relations.get_next_action(action_code)
                for n in next_action:
                    container[0].append(n)
                user_info.update_level([action_code], next_action)
            else:
                container[0].append(action_code)
        elif int(action_code.split('.')[0]) == parts[1]:
            if history.upgrade_level(user,action_code):
                next_action = relations.get_next_action(action_code)
                for n in next_action:
                    container[1].append(n)
                user_info.update_level([action_code], next_action)
            else:
                container[1].append(action_code)

    container[0] = sorted(container[0], key=lambda value: int(value.split('.')[1]))
    container[1] = sorted(container[1], key=lambda value: int(value.split('.')[1]))

    full = []
    action_list = []

    full += main_part_logic(user,container[0])
    full += secondary_part_logic(user,container[1])

    for code in full:
        action = history.action_struct()
        action.action_dict['code'] = code
        action.action_dict['regular_reps'] = 6
        action.action_dict['regular_times'] = [8]
        action.action_dict['rest_time'] = 25
        action_list.append(action.action_dict)

    #print time.strftime('%Y%m%d')
    print '~~~~~~~~~~~~~~~~~~~~~~'
    for action in action_list:
        history.show_action(action)
        action_history = history.action_reps_record(user,action['code'],3)
        for i in action_history:
            print i
        print '----------------------'
    return action_list

def write_log(user,date,actions,history_count):
    src = './history/%s/%s.txt'%(user,date)
    with open(src, 'wb') as f:
        f.write('*** %s *** | ***%d***\n'%(date,history_count))
        f.write('~~~~~~~~~~~~~~~~~~~~\n')
        for action in actions:
            action_history = history.action_reps_record(user,action['code'],3)
            f.write('Code : %s\n'%action['code'])
            #f.write('Rest Time : %d\n'%action.action_dict['rest_time'] )
            f.write('Regular Reps :%2d | Regular Times Each Rep :%2d\n'%(action['regular_reps'],
                                                                             action['regular_times'][0]))
            #f.write(reg_times)
            reps = ''
            for i in range(action['regular_reps']):
                reps += "  __ |"
            #f.write('*User Reps : \n')
            f.write('\n')
            f.write('*User Times : %s\n'%reps)
            history_content = 'History   :  %d times in total\n'%history.count_action_times(user,action['code'])
            for date, one in action_history:
                line = '%s      '%date
                for i in one:
                    line += '  %2d |'%i
                line += '\n'
                history_content += line
            f.write(history_content)
            f.write('_________________________________________________\n')

def latest_day(user,day):
    today = int(time.strftime("%Y%m%d",time.localtime()))
    log_list = os.listdir('./history/%s'%user)
    log_files = [i for i in log_list if '.json' in i]
    log_files = [i.split('.')[0] for i in log_files ]
    latest = log_files.pop()
    time_array = time.strptime(latest,"%Y%m%d")
    time_stamp = int(time.mktime(time_array))
    date_array = datetime.datetime.utcfromtimestamp(time_stamp) + datetime.timedelta(hours = 8)
    next_day = date_array + datetime.timedelta(days = 1)
    next_day = int(next_day.strftime("%Y%m%d"))
    if day == 'today':
        return str(today)
    else:
        return next_day

if __name__ == '__main__':
    try:
        user = sys.argv[1]
    except:
        user = None
    next_day = latest_day(user,None)
    actions = day_class(user)
    action_code_list = [i['code'] for i in actions]
    history_count = len(history.log_file_list(user)) + 1
    #write_log(user,next_day,actions,history_count)
    daily_guide.gen_pdf(user,next_day, actions, history_count)
    history.write_log(user,next_day,actions)
    #image_guide.create_image(user,next_day,action_code_list)







