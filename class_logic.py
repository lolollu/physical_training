#!/usr/bin/env python
# encoding: utf-8

import history
import relations
import user_info
import time
import random
import time
import datetime
import os

def analyse_history():
    pass

def actions_filter(parts,levels):
    levels_container = []
    for level in levels:
        part = int(level.split('.')[0])
        if part in parts:
            container.append(level)
    for key,value in container:
        pass

def sub_stream_filter(level_list):
    container = {}
    for level in level_list:
        sub_stream = int(level.split('.')[1])

def get_new_action(action_code,potential_upgrade):
    new_action = relations.get_previos_action(action_code)
    if new_action == '':
        new_action = random.choice(potential_upgrade)
    return new_action

def main_part_logic(main_list):
    potential_upgrade = relations.avaliable_upgrade_codes(main_list)
    while True:
        if len(main_list) <= 4:
            break
        else:
            main_list.remove(random.choice(main_list))
    if len(main_list) == 4:
        main_list.remove(random.choice(main_list))
        rand_select = random.choice(main_list)
        main_list.append(get_new_action(rand_select,potential_upgrade))
    elif len(main_list) == 3:
        rand_select = random.choice(main_list)
        main_list.append(get_new_action(rand_select,potential_upgrade))
    elif len(main_list) == 2:
        tmp = []
        for action_code in main_list:
            tmp.append(get_new_action(action_code,potential_upgrade))
        main_list = [main_list[0],tmp[0],main_list[1],tmp[0]]
    elif len(main_list) == 1:
        new_one = get_previos_action(main_list[0])
        if pre == u'':
            start = main_list[0]
            while True:
                print start
                new_one =  get_next_action(start)
                for new in new_one:
                    main_list.append(new)
                if len(main_list) == 4:
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
    elif len(main_list) == 1:
        second_list.append(get_new_action(main_list[0],potential_upgrade))
    return second_list

def day_class():
    user_profile = user_info.load_info()
    streams = [1,2,3,4,5]
    parts = []
    #get the two parts
    last_first, last_second = history.latest_two()
    if last_first is not None:
        first_prop = history.action_proportion(last_first)
        for key,value in first_prop.items():
            try:
                streams.remove(int(key.split('.')[0]))
            except:
                pass
        '''
        if last_second is not None:
            second_prop = history.action_proportion(last_second)
            chance = random.randint(0,1)
            key = second_prop.items()[chance][0]
            streams.remove(int(key.split('.')[0]))
        '''

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
    if len(container) >=2:
        parts = [container[0][0],container[1][0]]
    elif len(container) == 1:
        first = container[0][0]
        try:
            streams.remove(first)
        except:
            pass
        parts = [first,random.choice[streams]]
    else:
        parts.append(random.choice(streams))
        streams.remove(parts[0])
        parts.append(random.choice(streams))

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
        action.action_dict['regular_reps'] = 3
        action.action_dict['regular_times'] = [12,12,12]
        action.action_dict['rest_time'] = 25
        action_list.append(action)

    print time.strftime('%Y%m%d')
    print '~~~~~~~~~~~~~~~~~~~~~~'
    for action in action_list:
        action.show_action()
        print '----------------------'
    return action_list

def write_log(date,actions):
    src = './history/%s.txt'%date
    with open(src, 'wb') as f:
        f.write('*** %s ***\n'%date)
        f.write('~~~~~~~~~~~~~~~~~~~~\n')
        for action in actions:
            f.write('Code : %s\n'%action.action_dict['code'])
            f.write('Rest Time : %d\n'%action.action_dict['rest_time'] )
            f.write('Regular Reps : %d\n'%action.action_dict['regular_reps'])
            reg_times = ''
            for i in action.action_dict['regular_times']:
                reg_times += '%d    '%i
            reg_times = 'Regular Times : '+reg_times+ '\n'
            f.write(reg_times)
            f.write('*User Reps : \n')
            f.write('*User Times : \n')
            f.write('--------------------------------\n')
        f.write('Notes:')

def latest_day():
    today = int(time.strftime("%Y%m%d",time.localtime()))
    log_list = os.listdir('./history')
    log_files = [i for i in log_list if '.json' in i]
    log_files = [i.split('.')[0] for i in log_files ]
    latest = log_files.pop()
    time_array = time.strptime(latest,"%Y%m%d")
    time_stamp = int(time.mktime(time_array))
    date_array = datetime.datetime.utcfromtimestamp(time_stamp)
    next_day = date_array + datetime.timedelta(days = 2)
    next_day = int(next_day.strftime("%Y%m%d"))
    return str(today) if today >= next_day else next_day

if __name__ == '__main__':
    next_day = latest_day()
    actions = day_class()
    write_log(next_day,actions)
    history.write_log(next_day,actions)






