#!/usr/bin/env python
# encoding: utf-8

import json

src = r'./user_profile.json'

class user_struct():
    def __init__(self):
        self.name = ""
        self.age = 0
        self.strength = 0
        self.weight = 0
        self.height = 0
        self.levels = []
        self.action_weights = {}

def json_writer(dicts,dst):
    j = json.dumps(dicts)
    with open(dst,'wb') as f:
        f.write(j)

def json_loader(src):
    with open(src,'r') as f:
        dicts = json.load(f)
        #dicts = json.loads(f.read())
    return dicts

def update_level(current_level, next_level):
    user_profile = json_loader(src)
    for i in current_level:
        user_profile[levels].remove(i)
    for i in next_level:
        user_profile['levels'].append(i)

    json_writer(user_profile,src)


def load_info():
    user = user_struct()
    user_dicts = json_loader(src)
    user.name = user_dicts["name"]
    user.age = user_dicts["age"]
    user.strength = user_dicts["strength"]
    user.weight = user_dicts['weight']
    user.levels = user_dicts['levels']
    user.action_weights = user_dicts['action_weights']
    return user

if __name__ == "__main__":
    load_info()

