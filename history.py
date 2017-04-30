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



def write_log(date,action_list):
    log = []
    for action in action_list:
        log.append(action.action_dict)

    with open('./history/%s.json'%date, 'wb') as f:
        f.write(json.dumps(log, indent = 4))

def update_log(date, user_info):
    with open('./history/%d.json'%date, 'r') as f:
        log = json.load(f)

    for i in range(len(log)):
        user_data = user_info[i]
        log[i]["user_reps"] = user_data[0]
        log[i]["user_times"] = user_data[1]

    write_log(date, log)


def action_proportion(date_file):
    with open('./history/%s'%date_file, 'r') as f:
        log = json.loads(f.read())

    proportion = {}
    for action in log:
        if proportion.has_key(action['code']):
            proportion[action['code']] += 1
        else:
            proportion[action['code']] = 1
    return proportion

def latest_two():
    log_list = os.listdir('./history')
    tmp = [i for i in log_list if '.json' in i]
    if len(tmp) >= 2:
        first = tmp.pop()
        second = tmp.pop()
        return (first, second)
    elif len(tmp) == 1:
        return (tmp[0],None)
    else:
        return (None,None)

def action_weights():
    log_list = os.listdir('./history')
    log_files = [i for i in log_list if '.json' in i]
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
        print pool
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
        regular_count = list_count(action.action_dict["regular_times"])
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

def upgrade_level(action_code):
    log_list = os.listdir('./history')
    log_files = [i for i in log_list if '.json' in i]
    log_files.reverse()
    thread = 0
    for log_file in log_files:
        with open('./history/%s'%log_file, 'r') as f:
            log = json.loads(f.read())
            for action in log:
                if action['code'] == action_code:
                    if reps_quality is True:
                        thread += 1
                        if thread >= 4:
                            return True
    return False

if __name__ == '__main__':
    action_weights()































