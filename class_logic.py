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

def get_new_action(action_code,potential_upgrade):
    new_action = relations.get_previos_action(action_code)
    if new_action == '':
        new_action = random.choice(potential_upgrade)
    return new_action

def main_part_logic(main_list):
    potential_upgrade = relations.avaliable_upgrade_codes(main_list)
    while True:
        if len(main_list) <= 3:
            break
        else:
            main_list.remove(random.choice(main_list))
    '''
    if len(main_list) == 3:
        main_list.remove(random.choice(main_list))
        rand_select = random.choice(main_list)
        main_list.append(get_new_action(rand_select,potential_upgrade))

    elif len(main_list) == 2:
        rand_select = random.choice(main_list)
        main_list.append(get_new_action(rand_select,potential_upgrade))
    '''
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

def secondary_part_logic(second_list):
    potential_upgrade = relations.avaliable_upgrade_codes(second_list)
    while True:
        if len(second_list) <= 2:
            break
        else:
            second_list.remove(random.choice(second_list))
    if len(second_list) == 2:
        return second_list
    elif len(second_list) == 1:
        second_list.append(get_new_action(second_list[0],potential_upgrade))
    return second_list

def day_class():
    user_profile = user_info.load_info()
    parts = []
    #get the weighted parts
    part1 = [1,2,3]
    part2 = [3,4,5]
    last_first, last_second = history.latest_two()
    if last_first is not None:
        first_prop = history.action_proportion2(last_first)
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

    '''
    #get the two parts
    last_first, last_second = history.latest_two()
    if last_first is not None:
        first_prop = history.action_proportion(last_first)
        for key,value in first_prop.items():
            try:
                streams.remove(int(key.split('.')[0]))
            except:
                pass

    current_weights_pool = history.action_weights()
    container = []
    for key,value in current_weights_pool.items():
        if abs(user_profile.action_weights[str(key)] - value) > 0.005:
            container.append((int(key),user_profile.action_weights[str(key)] - value))

    parts = []
    if container != []:
        container = sorted(container, key=lambda value: value[1])

        lenght = len(container)
        for i in range(lenght):
            if container[lenght - i -1][0] in streams:
                parts.append(container[lenght - i -1][0])
        while 1:
            if len(parts) >2:
                parts.pop()
            else:
                break
        while 1:
            if len(parts) < 2:
                select = random.choice(streams)
                parts.append(select)
                streams.remove(select)
            else:
                break
    else:
        while 1:
            if len(parts) < 2:
                select = random.choice(streams)
                parts.append(select)
                streams.remove(select)
            else:
                break
    '''
    print 'Parts : ', parts

    #get actions order list
    action_codes = user_profile.levels
    container = [[],[]]
    for action_code in action_codes:
        if int(action_code.split('.')[0]) == parts[0]:
            if history.upgrade_level(action_code):
                next_action = relations.get_next_action(action_code)
                for n in next_action:
                    container[0].append(n)
                user_info.update_level([action_code], next_action)
            else:
                container[0].append(action_code)
        elif int(action_code.split('.')[0]) == parts[1]:
            if history.upgrade_level(action_code):
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

    full += main_part_logic(container[0])
    full += secondary_part_logic(container[1])

    for code in full:
        action = history.action_struct()
        action.action_dict['code'] = code
        action.action_dict['regular_reps'] = 6
        action.action_dict['regular_times'] = [8]
        action.action_dict['rest_time'] = 25
        action_list.append(action)

    #print time.strftime('%Y%m%d')
    print '~~~~~~~~~~~~~~~~~~~~~~'
    for action in action_list:
        action.show_action()
        action_history = history.action_reps_record(action.action_dict['code'],3)
        for i in action_history:
            print i
        print '----------------------'
    return action_list

def write_log(date,actions,history_count):
    src = './history/%s.txt'%date
    with open(src, 'wb') as f:
        f.write('*** %s *** | ***%d***\n'%(date,history_count))
        f.write('~~~~~~~~~~~~~~~~~~~~\n')
        for action in actions:
            action_history = history.action_reps_record(action.action_dict['code'],3)
            f.write('Code : %s\n'%action.action_dict['code'])
            #f.write('Rest Time : %d\n'%action.action_dict['rest_time'] )
            f.write('Regular Reps : %d   |   Regular Times Each Rep : %d\n'%(action.action_dict['regular_reps'],
                                                                             action.action_dict['regular_times'][0]))
            '''
            reg_times = ''
            for i in action.action_dict['regular_times']:
                reg_times += '%d    '%i
            reg_times = 'Regular Times each rep : %d\n'%action.action_dict['regular_times'][0]
            '''
            #f.write(reg_times)
            reps = ''
            for i in range(action.action_dict['regular_reps']):
                reps += "  ___ |"
            #f.write('*User Reps : \n')
            f.write('\n')
            f.write('*User Times : %s\n'%reps)
            history_content = 'History   :\n'
            for date, one in action_history:
                line = '%s      '%date
                for i in one:
                    line += '  %3d |'%i
                line += '\n'
                history_content += line
            f.write(history_content)
            f.write('_______________________________________________________________________\n')
        f.write('Notes:')

def latest_day(day):
    today = int(time.strftime("%Y%m%d",time.localtime()))
    log_list = os.listdir('./history')
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
        day = sys.argv[1]
    except:
        day = None
    next_day = latest_day(day)
    actions = day_class()
    history_count = len(history.log_file_list()) + 1
    write_log(next_day,actions,history_count)
    history.write_log(next_day,actions)






