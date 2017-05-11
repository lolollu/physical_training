#!/usr/bin/env python
# encoding: utf-8

import json
import sqlite3

def json_writer(dicts,dst):
    j = json.dumps(dicts)
    with open(dst,'wb') as f:
        f.write(j)

def json_loader(src):
    with open(src,'r') as f:
        dicts = json.loads(f.read())
    return dicts

def init_action_relations(csv):
    db = sqlite3.connect('./action_relations.db')
    db.execute('''CREATE TABLE RELATION
             (ID INTEGER PRIMARY KEY NOT NULL,
             CURRENT TEXT NOT NULL,
             PREVIOUS TEXT)
             ''')

    with open(csv,'r') as f:
        content = f.readlines()

    for i in range(len(content)):
        line = content[i]
        current, previous = line.split(',')
        previous = previous.replace('\r\n','')
        command = "INSERT INTO RELATION (ID, CURRENT, PREVIOUS) VALUES (%d,'%s','%s')"%(i,current,previous)
        print command
        db.execute(command)
        db.commit()

def get_next_action(action_code):
    connect = sqlite3.connect('./action_relations.db')
    cu = connect.execute("SELECT CURRENT FROM RELATION WHERE PREVIOUS = '%s'"%action_code)
    container = []
    for row in cu:
        #print row[0]
        container.append(row[0])
    return container

def get_previos_action(action_code):
    connect = sqlite3.connect('./action_relations.db')
    cu = connect.execute("SELECT PREVIOUS FROM RELATION WHERE CURRENT = '%s'"%action_code)
    for row in cu :
        return row[0]

def detect_edge(start,pool,edge_pool):
    new_set = get_next_action(start)
    if new_set != []:
        for n in new_set:
            if n in pool:
                tmp = detect_edge(n,pool,edge_pool)
                if tmp is not None:
                    edge_pool.append(tmp)
            else:
                return n
    else:
        return start

def avaliable_upgrade_codes(code_list):
    if code_list == []:
        return []
    action_pool = []
    stream_count = []
    for code in code_list:
        code_stream = code.split('.')[0]
        if code_stream not in stream_count:
            stream_count.append(code_stream)
        action_pool.append(code)
        now = code
        while True:
            pre_action = get_previos_action(now)
            if pre_action != "%s.1.1"%code_stream:
                if pre_action not in action_pool:
                    action_pool.append(pre_action)
                now = pre_action
            else:
                break
        action_pool.append("%s.1.1"%code_stream)
    count_list = []
    for stream in stream_count:
        h = []
        detect_edge('%s.1.1'%stream,action_pool,h)
        count_list += h
    return count_list

def show_profile():
    dicts = json_loader('./user_profile.json')
    for key,value in dicts.items():
        if key == 'levels':
            print key , " :"
            for level in value:
                print level
        else:
            print "{key} : {value}".format(key=key , value=value)

if __name__ == '__main__':
    #print get_next_action('1.4.11')
    print avaliable_upgrade_codes(["1.1.9","1.2.9","1.3.7","1.5.9","2.1.3","2.2.3","3.1.6","3.2.6","4.1.3","4.2.4","5.1.6","5.2.5"])
    #print type(get_previos_action('1.1.1'))
    #show_profile()
