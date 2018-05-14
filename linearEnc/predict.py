import os
import re

label = []
faceDR = open("../faces/faceDR")
for line in faceDR:
    wlabels = {}
    tokens = re.split(r'[( )]', line)
    if len(tokens) < 10:
        wlabels["No"] = tokens[1]
        wlabels["sex"] = '0'
        wlabels["age"] = '0'
        wlabels["race"] = '0'
        wlabels["face"] = '0'
        label.append(wlabels)
        continue
    wlabels["No."] = tokens[1]
    wlabels["sex"] = tokens[5]
    wlabels["age"] = tokens[10]
    wlabels["race"] = tokens[14]
    wlabels["face"] = tokens[18]
    label.append(wlabels)

def getLabel(list):
    sex = []
    age = []
    race = []
    face = []
    ans = []
    for i in list:
        sex.append(label[i]["sex"])
        age.append(label[i]["age"])
        race.append(label[i]["race"])
        face.append(label[i]["face"])
    sexSet = {}
    ageSet = {}
    raceSet = {}
    faceSet = {}
    for i in set(sex):
        sexSet[i] = sex.count(i)
    for i in set(age):
        ageSet[i] = age.count(i)
    for i in set(race):
        raceSet[i] = race.count(i)
    for i in set(face):
        faceSet[i] = face.count(i)
    ans.append(sorted(sexSet.keys())[-1])
    ans.append(sorted(ageSet.keys())[-1])
    ans.append(sorted(raceSet.keys())[-1])
    ans.append(sorted(faceSet.keys())[-1])
    return ans

def showReal(index):
    real = []
    faceDS = open("../faces/faceDS")
    for line in faceDS:
        tokens = re.split(r'[( )]', line)
        if len(tokens) < 10:
            real.append('0')
            real.append('0')
            real.append('0')
            real.append('0')
            continue
        if index+3223 == int(tokens[1]):
            real.append(tokens[5])
            real.append(tokens[10])
            real.append(tokens[14])
            real.append(tokens[18])
    return real

if __name__ == "__main__":
    # a = list(range(100))
    # print(getLabel(a))
    print(showReal(0))