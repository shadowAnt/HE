import os
import re

label = []
faceDR = open("../faces/faceDR")
for line in faceDR:
    wlabels = {}
    tokens = re.split(r'[( )]', line)
    if len(tokens) < 10:
        wlabels["No"] = tokens[1]
        wlabels["sex"] = 'male'
        wlabels["age"] = 'adult'
        wlabels["race"] = 'white'
        wlabels["face"] = 'serious'
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
    a=0
    for i in list:
        sex.append(label[i]["sex"])
        age.append(label[i]["age"])
        race.append(label[i]["race"])
        face.append(label[i]["face"])
        # print(i+1223, sex[a], age[a], race[a], face[a])
        a = a+1
    sexSet = {}
    ageSet = {}
    raceSet = {}
    faceSet = {}
    for i in set(sex):
        sexSet[sex.count(i)] = i
    for i in set(age):
        ageSet[age.count(i)] = i
    for i in set(race):
        raceSet[race.count(i)] = i
    for i in set(face):
        faceSet[face.count(i)] = i
    # print(sexSet)
    ans.append(sexSet[sorted(sexSet.keys())[-1]])
    ans.append(ageSet[sorted(ageSet.keys())[-1]])
    ans.append(raceSet[sorted(raceSet.keys())[-1]])
    ans.append(faceSet[sorted(faceSet.keys())[-1]])
    return ans

def showReal(index):
    real = []
    faceDS = open("../faces/faceDS")
    for line in faceDS:
        tokens = re.split(r'[( )]', line)
        if index + 3223 == int(tokens[1]):
            if len(tokens) < 10:
                real.append('male')
                real.append('adult')
                real.append('white')
                real.append('serious')
                continue
            real.append(tokens[5])
            real.append(tokens[10])
            real.append(tokens[14])
            real.append(tokens[18])
    return real

if __name__ == "__main__":
    # a = list(range(100))
    # print(getLabel(a))
    print(showReal(0))