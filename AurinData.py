"""
Author:
    Team2
Members:
    Jiachuan Yu(867000), jiachuany
    Mengyu Zhou(780956), mengyuz2
    Chenxi Hou(811596), chou1
    Surong Zhu(859160), surongz
    Sicong Ma(884092), Sicongm

"""

#This document is use the data from AURIN, combine useful data as a dictionary \
#transform it to the type of string and write it into a json file named "aurin-melb-out.json".
import json

class AurinData():
    def processMelAge(self):
        melbSuburbFile = open('/Users/mengyu_zhou/Desktop/aurin-melb.json','r')
        melbSuburbJson = json.load(melbSuburbFile)
        features = melbSuburbJson['features']
        properties = []
        dic = {}
        for feature in features:
            properties.append(feature['properties'])
        for property in properties:
            dic[property['sa2_name16']]=property['median_tot_prsnl_inc_weekly']

        with open('/Users/mengyu_zhou/Desktop/aurin-melb-out.json','w') as f:
            f.write(json.dumps(dic))
            print('done')

if __name__ == '__main__':
    MelAge = AurinData()
    MelAge.processMelAge()
        
