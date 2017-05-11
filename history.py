#!/usr/bin/env python
# encoding: utf-8

import json
import os

class action_struct():
    def __init__(self):
        self.action_dict = {}
        self.action_dict['code'] = ""
        self.action_dict['image_link'] = ""
        self.action_dict['regular_reps'] = 0
        self.action_dict['regular_times'] = []
        self.action_dict['user_reps'] = 0
        self.action_dict['user_times'] = []
        self.action_dict['rest_time'] = 0

    def action_stream(self):
        return int(self.action_dict['code'].split('.')[0])

    def action_priority(self):
        return int(self.action_dict['code'].split('.')[1])

    def action_order(self):
        return int(self.action_dict['code'].split('.')[2])

    def show_action(self):
        print 'code : ', self.action_dict['code']
        print 'rest_time : ',self.action_dict['rest_time']
        print 'regular_reps : ' , self.action_dict['regular_reps']
        print 'regular_times : ', self.action_dict['regular_times']
        print 'user_reps : ', self.action_dict['user_reps']
        print 'user_times : '


def log_file_list(user):
    log_list = os.listdir('./history/%s'%user)
    log_files = [i for i in log_list if '.json' in i]
    return log_files

def write_log(user,date,action_list):
    log = []
    for action in action_list:
        log.append(action.action_dict)

    with open('./history/%s/%s.json'%(user,date), 'wb') as f:
        f.write(json.dumps(log, indent = 4))

def update_log(user,date, user_info):
    with open('./history/%d.json'%date, 'r') as f:
        log = json.load(f)

    for i in range(len(log)):
        user_data = user_info[i]
        log[i]["user_reps"] = user_data[0]
        log[i]["user_times"] = user_data[1]

    write_log(date, log)


def action_proportion(user,date_file):
    with open('./history/%s/%s'%(user,date_file), 'r') as f:
        log = json.loads(f.read())

    proportion = {}
    for action in log:
        if proportion.has_key(action['code']):
            proportion[action['code']] += 1
        else:
            proportion[action['code']] = 1
    return proportion

def action_proportion2(user,date_file):
    with open('./history/%s/%s'%(user,date_file), 'r') as f:
        log = json.loads(f.read())

    proportion = []
    for action in log:
        number = int(action['code'].split('.')[0])
        if number not in proportion:
            proportion.append(number)
    return proportion

def latest_two(user):
    tmp = log_file_list(user)
    if len(tmp) >= 2:
        first = tmp.pop()
        second = tmp.pop()
        return (first, second)
    elif len(tmp) == 1:
        return (tmp[0],None)
    else:
        return (None,None)

def action_weights(user):
    log_files = log_file_list(user)
    pool = {1:0,2:0,3:0,4:0,5:0}
    count = 0
    for log_file in log_files:
        action_prop = action_proportion(log_file)
        for key,value in action_prop.items():
            pool[int(key.split('.')[0])] += value
            count += value
    if count == 0:
        return {1:0.2,2:0.2,3:0.2,4:0.2,5:0.2}
    else:
        for key, value in pool.items():
            pool[key] = pool[key] / float(count)
        #print pool
        return pool

def list_count(li):
    count = 0
    for i in li:
        count += i
    return count

def reps_quality(action):
    if action.action_dict["user_reps"] < action.action_dict["regular_reps"]:
        return False
    else:
        regular_count = action.action_dict["regular_times"][0] * action.action_dict["regular_reps"]
        user_count = list_count(action.action_dict["user_times"])
        if user_count < regular_count:
            return False
        else:
            count = 0.0
            bias = 1.0 / float(len(action.action_dict["regular_times"]))
            for i in range(len(action.action_dict["regular_times"])):
                reg_times = action.action_dict["regular_times"][i]
                user_times = action.action_dict["user_times"][i]
                count += (bias * user_times/float(reg_times))
            return True

def upgrade_level(user,action_code):
    log_files = log_file_list(user)
    log_files.reverse()
    thread = 0
    stack = []
    for log_file in log_files:
        with open('./history/%s/%s'%(user,log_file), 'r') as f:
            log = json.loads(f.read())
            for action in log:
                if action['code'] == action_code:
                    stack.append(action)
    if len(stack) < 3:
        return False
    elif len(stack) < 8:
        return False
    else:
        for action in stack[-3:]:
            print action["user_reps"]
            print action["regular_reps"]
            if action["user_reps"] < action["regular_reps"]:
                return False
            mean = list_count(action["regular_times"])/len(action["regular_times"])
            if mean <  1.15 * action["regular_times"][0]:
                return False
        return True

def action_reps_record(user,action_code,times_count):
    log_files = log_file_list(user)
    container = []
    while 1:
        if log_files == []:
            break
        if len(container) == 3:
            break
        log_file_name = log_files.pop()
        with open('./history/%s/%s'%(user,log_file_name), 'r') as f:
            log = json.loads(f.read())
            for action in log:
                if action['code'] == action_code:
                    container.append((log_file_name.split('.')[0],action['user_times']))

    return container

def action_histgram(user):
    log_files = log_file_list(user)
    container = {}
    for log_file in log_files:
        with open('./history/%s'%log_file, 'r') as f:
            log = json.loads(f.read())
            for action in log:
                if not container.has_key(action['code']):
                    container[action['code']] = 1
                else:
                    container[action['code']] += 1

    for key, item in container.items():
        print "%s : %d"%(key, item)

def count_action_times(user,action_code):
    log_files = log_file_list(user)
    count = 0
    for log_file in log_files:
        with open('./history/%s/%s'%(user,log_file), 'r') as f:
            log = json.loads(f.read())
            for action in log:
                if action['code'] == action_code:
                    count += 1

    return count

def kick_action(user,action_code_list):
    max = 0
    tmp_code = ''
    for action_code in action_code_list:
        tmp_count = count_action_times(user,action_code)
        if max < tmp_count:
            max = tmp_count
            tmp_code = action_code
    action_code_list.remove(tmp_code)


if __name__ == '__main__':
    #action_weights()
    #print upgrade_level('4.2.4')
    action_histgram()





