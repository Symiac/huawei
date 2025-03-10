import numpy as np
def dijkstra(graph, src,crossPool,roadPool):
    # 判断图是否为空，如果为空直接退出
    if graph is None:
        return None
    nodes = [i for i in range(len(graph))]  # 获取图中所有节点
    visited=[]  # 表示已经路由到最短路径的节点集合
    map_cross = []
    for cross in crossPool:
        map_cross.append(cross)

    if src in nodes:
        visited.append(src)
        nodes.remove(src)
    else:
        return None
    distance = {src: 0}  # 记录源节点到各个节点的距离
    for i in nodes:
        distance[i] = graph[src][i]  # 初始化
    path = {src: []}  # 记录源节点到每个节点的路径
    k = pre = src
    while nodes:
        mid_distance = graph.max()*graph.shape[0]*(graph.shape[1]-1)
        for v in visited:
            for d in nodes:
                new_distance = distance[v] + graph[v][d]
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    k = d
                    pre = v
        distance[k] = mid_distance  # 最短路径
        p=0
        for i in crossPool[map_cross[pre]].allRoad:
            if i != -1:
                if roadPool[i].fromCrossId==map_cross[k] or roadPool[i].toCrossId ==map_cross[k]:
                    p=i
        path[k] = [i for i in path[pre]]
        path[k].append(p)
        visited.append(k)
        nodes.remove(k)
    path={map_cross[p]:path[p] for p in path}
    return path
def calPlace(cross,crossPool,roadPool,now_placew):
    cross.pos=(now_placew[0],now_placew[1])
    absPlace=[(0,1),(1,0),(0,-1),(-1,0)]
    for i in cross.allRoad:
        if i == -1:
            continue
        else:
            index=cross.allRoad.index(i)
            road=roadPool[i]
            indexNext=road.fromCrossId if road.fromCrossId!=cross.id else road.toCrossId
            new_place=(absPlace[index][0]+now_placew[0],absPlace[index][1]+now_placew[1])
            next_index=crossPool[indexNext].allRoad.index(i)
            if (next_index-index)%4 !=2:
                crossPool[indexNext].moveAllRoad(i,index-2)
            if crossPool[indexNext].pos == ():
                calPlace(crossPool[indexNext], crossPool, roadPool,new_place)



if __name__ == "__main__":
    import random
    a=[[random.randint(0,100) for i in range(64)] for i in range(64)]
    for i in range(64):
        a[i][i]=0
    a=np.array(a,dtype="int32")
    dis, path = dijkstra(a,0)
#sys.path.extend(['F:\\2019\\learn_python', 'F:\\2019\\learn_python\\huawei\\SDK_python\\CodeCraft-2019\\src\\huaweiUtil', 'F:/2019/learn_python'])
