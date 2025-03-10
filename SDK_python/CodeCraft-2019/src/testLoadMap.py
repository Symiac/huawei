from huaweiUtil import loadData
from Model import Car,Cross,Road
import numpy as np




def loadMap(crossPath,roadPath):
    crossPool=loadCrossPool(crossPath)
    roadPool=loadRoadPool(roadPath)
    return (crossPool,roadPool)

def loadCrossPool(crossPath):
    global k
    datas=loadData.loadData(crossPath)
    crossPool=[]

    for data in datas:
        cross=Cross.Cross(data[0],data[1],data[2],data[3],data[4])
        crossPool.append(cross)
        #(self,id,nRoadId,eRoadId,sRoadId,wRoadId)
    crossdict={cross.id:cross for cross in crossPool}
    k=crossdict
    return crossdict
def loadRoadPool(roadPath):
    datas=loadData.loadData(roadPath)
    roadPool=[]
    print(datas)
    for d in datas:
        road=Road.Road(d[0],d[1],d[2],d[3],d[4],d[5],d[6])
        roadPool.append(road)
    roadDic={road.id:road for road in roadPool}
    return roadDic

def loadCar(carPath):
    datas = loadData.loadData(carPath)
    carPool = []
    print(datas)
    for d in datas:
        road = Car.Car(d[0], d[1], d[2], d[3], d[4])
        carPool.append(road)
    carDic={car.id : car for car in carPool}
    return carDic


def graph(crossPool,roadPool):
    length=len(crossPool)
    max=-1
    tgraph=np.zeros((length,length))
    map=[]
    for i in range(length):
        for j in range(length):
            if crossPool[i].nRoadId != -1:
                pass
    pass


# 生成地图
def get_map(crosses, roads):
    length = len(crosses)
    graph_list=np.zeros((length,length),dtype="int32")
    graph_list[:]=9999
    map=[]
    for cross in crosses:
        map.append(cross)
    for i in range(len(crosses)):
        for j in range(len(crosses)):
            if i == j:
                graph_list[i][j] = 0
            else:
                for k in crosses[map[i]].allRoad:
                    if k is not -1:
                        road=roads[k]
                        previousCross = road.fromCrossId
                        nextCross = road.toCrossId
                        if road.isDuplex == 1:
                            if sorted([previousCross,nextCross]) == sorted([crosses[map[i]].id,crosses[map[j]].id]):
                                graph_list[i][j] = road.length
                        elif previousCross == crosses[map[i]].id and nextCross == crosses[map[j]].id:
                             graph_list[i][j] = road.length
                        else:
                            pass
    return graph_list







def dumpAnswer(path,cars):
    with open(path,"w") as f:
        for car in cars:
            tempStr=str(cars[car].id)+" ,"+str(cars[car].bestStartTime)+" ,"+" ,".join([str(i) for i in cars[car].path])
            tempStr="("+tempStr+")\r"
            f.writelines(tempStr)




crossPool,roadPool = loadMap("../1-map-training-1/cross.txt","../1-map-training-1/road.txt")
car =loadCar("../1-map-training-1/car.txt")
#car.sort(key=lambda c:c.plantTime,reverse=False)
# for c in car:
#     print(c)

# now_pos=[0,0]



from huaweiUtil import alg
mapp = get_map(crossPool, roadPool)
map_cross=[]
for cross in crossPool:
        map_cross.append(cross)

path={}
import time
a=time.time()

for c in range(len(crossPool)):
    path.update({map_cross[c]:alg.dijkstra(mapp, c,crossPool,roadPool)})
now_time=6
for c in car:
    car[c].addAnswer(path)
    roadLength=0
    minSpeed=1000
    for i in car[c].path:
        roadLength+=roadPool[i].length
        minSpeed=min(roadPool[i].speed,minSpeed)
    car[c].bestStartTime = now_time
    now_time += int(roadLength/minSpeed)

dumpAnswer("./answer.txt",car)

print(path)

