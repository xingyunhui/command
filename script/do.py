#!/usr/bin/python
#coding=utf-8

import xlrd
import sys
import json
import math
#import chardet

reload(sys)
sys.setdefaultencoding('utf8')



def getGeo():

    data = xlrd.open_workbook('/Users/heran/Downloads/111.xlsx')
    file = open("geo1.txt","w+")

    table = data.sheets()[0]

    nrows = table.nrows

    ncols = table.ncols

    print "rows total : " + str(nrows)
    print "cols total : " + str(ncols)

    for i in range(4,902):
        name = table.cell(i,0).value
        print i
        print table.cell(i,7).value
        print table.cell(i,8).value
        print table.cell(i,9).value
        #x = double(table.cell(i,7).value) + double(table.cell(i,8).value)/60 + double(table.cell(i,9).value)/3600
        #y = double(table.cell(i,4).value) + double(table.cell(i,5).value)/60 + double(table.cell(i,6).value)/3600
        #x = (float)table.cell(i,8).value  + (float)table.cell(i,9).value/60 + (float)table.cell(i,9).value/3600
        #y = (float)table.cell(i,5).value  + (float)table.cell(i,6).value/60 + (float)table.cell(i,9).value/3600
        x = table.cell(i,29).value
        y = table.cell(i,28).value
        print "name : %s, x : %s, y : %s " %(name,x,y)
        file.write("%s %s %s\n" %(name,x,y))
    file.close()

def getJson():
    json_result = {}
    json_result["title"] = u"油田指挥图"
    try:
       geo = open("geo1.txt", "r+")
       result = open("result_google.json","w+")
       relation = open("wc1.txt","r+")
       nodeList = getNode(geo)
       edgeList = getEdge(relation)
       json_result["nodes"] = nodeList
       json_result["edges"] = edgeList
       json_str = json.dumps(json_result,ensure_ascii=False)
       result.write(json_str)
    finally:
        geo.close()
        result.close()

def getNode(geo):
    list = []
    colors = xlrd.open_workbook('/Users/heran/Downloads/22.XLS')
    table = colors.sheets()[0]
    for line in geo:
        data = line.split(" ")
        dict = {}
        dict["label"] = data[0]
        dict["attributes"] = {}
        dict["x"], dict["y"] = getBaiDuPosition(float(data[1]),float(data[2].replace('\n','')))
        #dict["x"] = data[1]
        #dict["y"] = data[2].replace('\n','')
        dict["id"] = data[0]
        dict["size"] = 10

        dict["focusNodeAdjacency"] = "true"
        if '#' in data[0] :
            dict['symbol'] = "triangle"
            dict["color"] = '#000000'
        else :
            dict['symbol'] = "circle"
            dict["color"] = getColor(data[0],table)
        list.append(dict)
    return list

def getBaiDuPosition(x,y):
    z = math.sqrt(x*x + y*y) + 0.00002 *math.sin(y* math.pi * 3000.0 / 180.0)
    theta = math.atan2(y,x) + 0.000003*math.cos(x* math.pi * 3000.0 / 180.0)
    baidux = z * math.cos(theta) + 0.0065
    baiduy = z * math.sin(theta) + 0.006
    return baidux,baiduy


def getEdge(relation):
    list = []
    for line in relation:
        data = line.split(" ")
        if(len(data)==2):
            dict = {}
            dict["sourceID"] = data[0]
            dict["targetID"] = data[1].replace('\n','').decode('utf8')
        #print eval("u"+"\'"+data[1].replace('\n','').decode('utf8')+"\'")
        #print dict
            dict["size"] = 1
            list.append(dict)
    return list

def getColor(name,table):
    nrows = table.nrows
    ncols = table.ncols
    #print "rows total : " + str(nrows)
    #print "cols total : " + str(ncols)
    for i in range(1,nrows):
        if table.cell(i,0).value.lower() == name.lower():
            return table.cell(i,1).value
    print "color not find " + name
    return "#F06292"



def readRealation():

    file = open('wc1.txt',"a+")
    data = xlrd.open_workbook('/Users/heran/Downloads/fanwei.xlsx')
    table = data.sheets()[0]

    nrows = table.nrows
    ncols = table.ncols
    print "rows total : " + str(nrows)
    print "cols total : " + str(ncols)
    for i in range(1,nrows):

        wells = table.cell(i,0).value
        camera = table.cell(i,1).value
        if(wells==''):
            wells = table.cell(i-1,0).value
            if(wells==''):
                wells = table.cell(i-2,0).value
                if(wells==''):
                    wells = table.cell(i-3,0).value
        #print wells,camera
        # if wells == None:
        #     if i == 87 or i == 91 or i == 96 or i == 101 or i == 103 or i == 106 or i == 108 or i == 116 or i == 120 or i == 142 or i == 152 or i == 154 or i == 159 or i == 161 or i == 163 or i == 166 or i == 171 or i == 179 or i == 184 or i == 192 or i == 197 or i == 199 or i == 205 or i == 207 or i == 209 or i == 214:
        #         wells = table.cell(i-1,1).value
        #     elif i == 109  or i == 117 or i == 164 or i == 172 :
        #         wells = table.cell(i - 2 ,1).value
        if wells == None:
            file.write("  %s" %(camera))
        else:
            wellList = wells.split(",")
            for j in range(0,len(wellList)):
                file.write("%s %s\n" %(wellList[j] , camera))

        #print "well %s , cameras %s " %(well,cameras)
        #if cameras == None:
        #    file.write("%s" %(well))
        #else:
        #    cameraList = cameras.split(",")
        #    for j in range(0,len(cameraList)):
                #file.write("%s %s\n" %(well,cameraList[j]))


    file.close()


if __name__ == "__main__":
    # readRealation()
    getJson()
    #getGeo()
    #print getBaiDuPosition(1,2)

