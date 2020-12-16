import heapq
import queue
import time

start = time.time()  # 시작 시간 저장
"""
pylint main.py ->분석도구 명령어
"""

class Map(object):
    def __init__(self):
        self.fire_place_num = []
        self.exit = [1, 3]  # 탈출구인 노드 num 들
        self.all_node_num = 21
        self.node = []  # 모든 노드들
        self.check = []
        self.all_node = []  # 모든 노드번호들 넣을곳 추후 탈출구 노드를 제외하고 화살표 방향을 정할때 씀
        self.now_distance = []  # 방향구하는거 쓸떄 비교에 쓰임
        self.initiation_smoke_values = []  # 각 노드별 초기 연기 데이터 값


map = Map()
count = -1

class Node(object):
    def __init__(self, num):
        # self.location = np.array([x,y,z])
        self.index = num
        self.forward = None
        self.backward = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.distance = float('inf')
        self.temp_distance = 0
        self.direction = [0, 0, 0, 0, 0, 0]  # 상, 하, 좌, 우, 위, 아래
        self.exit_diret = 0  # <- 자료형 뭐고?
        self.exit_diret_num = []
        self.visited_place = []

    def set_index(self, num):
        self.index = num

    def set_distance(self, num):
        if (self.distance > num):
            self.distance = num

    def set_exit_diret_num(self, list):
        self.exit_diret_num = list


def AddNode():  # count는 node num을 지정해주기 위해 사용
    global count
    count += 1
    return Node(count)


def find_linked_node(Node):  # 입력 Node와 연결된 노드 Num을 index_list에 넣음
    dir = Node.direction
    index_list = []
    if dir[0] == 1:
        index_list.append(Node.forward.index)
    if dir[1] == 1:
        index_list.append(Node.backward.index)
    if dir[2] == 1:
        index_list.append(Node.left.index)
    if dir[3] == 1:
        index_list.append(Node.right.index)
    if dir[4] == 1:
        index_list.append(Node.up.index)
    if dir[5] == 1:
        index_list.append(Node.down.index)
    return index_list


def dijkstra(start, linked_node_list):  
    # 모든 노드간 가중치가 1
    # 이는 추후 바꿀수 있으며 모든 가중치가 1이기에 출발 노드에서 모든 노드까지의 거리 측정가능
    distances = {node: float('inf') for node in range(84)}
    distances[start] = 0

    queue = []
    heapq.heappush(queue, [distances[start], start])

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if distances[current_node] < current_distance:
            continue

        for adjacent in linked_node_list[current_node]:
            distance = current_distance + 1

            if distance < distances[adjacent]:
                distances[adjacent] = distance
                heapq.heappush(queue, [distance, adjacent])
    return distances


def set_weight(node, exit):  # 다익스트라를 통해 탈출구에서 모든 노드까지의 거리를 구한후 비교해서 최솟값 넣기
    for e in exit:
        result = dijkstra(e, linked_node_list)
        for i in range(0, map.all_node_num):
            node[i].set_distance(result[i])

def fire_in_node(start_node_num, node, linked_node_list):
    queue = []
    temp = []
    sub_graph = []
    queue.append(start_node_num)

    while queue:
        check = 0
        prev_node_num = queue.pop()
        check_node_list = []    # 시작 노드 주변노드

        for i in linked_node_list[prev_node_num]:
            check_node_list.append(i)

        for j in check_node_list:
            ad_node_list = []
            for k in linked_node_list[j]:
                if k != prev_node_num:
                    ad_node_list.append(k)

            if node[prev_node_num].distance < node[j].distance:
                sub_graph.append(j)
                queue.append(j)

            elif node[prev_node_num].distance > node[j].distance:
                for k in ad_node_list:
                    temp.append(node[k].distance)

                for k in range(1, len(temp)):
                    if temp[k-1] != temp[k]:
                        check = 1

                if check == 0:
                    sub_graph.append(j)
                    queue.append(j)

    return sub_graph


def fire_test(fire_node_num, send_node_num1, send_node_num2, node, linked_node_list):
    print("fire test")
    queue = []
    del_list = []
    fire_start = fire_node_num
    send1 = send_node_num1
    send2 = send_node_num2
    node[fire_node_num].distance = float('inf')

    if fire_node_num not in map.fire_place_num:
        map.fire_place_num.append(fire_node_num)
    for i in linked_node_list[send2]:
        if i != send1 and i not in map.exit:  # not in fire_place_num:
            queue.insert(0, i)

    for i in queue:
        substract = []
        node_list = []
        shortest_node_num = []
        # temp_exit_diret = 0

        for j in linked_node_list[i]:
            node_list.append(j)

            if j != send2:
                substract.append(node[j].distance - node[i].distance)

            else:
                substract.append(float('inf'))

        # print(node_list)
        shortest_distance_node_index = [i for i, value in enumerate(substract) if value == min(substract)]
        temp_exit_diret = node[i].exit_diret

        if (min(substract) != -1 or node[i].exit_diret_num != shortest_distance_node_index) and min(substract) != float(
                'inf'):
            node[i].exit_diret = 0

            if send2 not in node[i].visited_place:
                node[i].visited_place.append(send2)
                print('7')
            # node[i].distance += 2

            node[i].set_exit_diret_num(shortest_distance_node_index)
            for k in shortest_distance_node_index:
                shortest_node_num.append(node_list[k])

            if node[i].forward != None and node[i].forward.index in shortest_node_num:
                if node[i].forward.index not in node[i].visited_place:
                    node[i].exit_diret += 32

            if node[i].backward != None and node[i].backward.index in shortest_node_num:
                if node[i].backward.index not in node[i].visited_place:
                    node[i].exit_diret += 16
            if node[i].right != None and node[i].right.index in shortest_node_num:
                if node[i].right.index not in node[i].visited_place:
                    node[i].exit_diret += 4

            if node[i].left != None and node[i].left.index in shortest_node_num:
                if node[i].left.index not in node[i].visited_place:
                    node[i].exit_diret += 8
            if node[i].up != None and node[i].up.index in shortest_node_num:
                if node[i].up.index not in node[i].visited_place:
                    node[i].exit_diret += 2
            if node[i].down != None and node[i].down.index in shortest_node_num:
                if node[i].down.index not in node[i].visited_place:
                    node[i].exit_diret += 1

        else:
            del_list.append(i)

    for i in del_list:
        queue.remove(i)

    for i in queue:
        fire_test(fire_start, send2, i, node, linked_node_list)

def create_sensor_map(length_file, width_file, stairs_file):
    """센서의 고유번호, 관계, 위치가 저장된 파일을 전달하면 그래프화 하고 sensor_map에 저장."""
    sensor_map = []
    file_list = [length_file, width_file, stairs_file]

    for file_name in file_list:

        with open(file_name) as sensor_file:

            for line in sensor_file:

                # 파일 입력받을 때 스플릿
                raw_data = line.strip().split("-")
                prev_sensor = None

                for sensor_num in raw_data:
                    sensor_num = int(sensor_num.strip())

                    if sensor_num not in sensor_map:  # 센서 정보가 센서 딕셔너리에 없으면
                        current_sensor = map.node[sensor_num]
                        sensor_map.append(sensor_num)
                    else:
                        current_sensor = map.node[sensor_num]
                    # print(current_sensor)
                    # print(prev_sensor)
                    # if file_name == "exit.txt":  # 출구 센서 지정
                    #     current_sensor.state = 'E'
                    #     exit_node[sensor_num] = current_sensor

                    if prev_sensor is not None:
                        if file_name == "./width.txt":  # 가로 연결된 센서
                            current_sensor.left = prev_sensor
                            prev_sensor.right = current_sensor
                            current_sensor.direction[2] = 1
                            prev_sensor.direction[3] = 1
                        elif file_name == "./length.txt":  # 세로 연결된 센서
                            current_sensor.forward = prev_sensor
                            prev_sensor.backward = current_sensor
                            current_sensor.direction[0] = 1
                            prev_sensor.direction[1] = 1
                        elif file_name == "./stairs.txt":  # 계단 센서
                            current_sensor.down = prev_sensor
                            prev_sensor.up = current_sensor
                            current_sensor.direction[5] = 1
                            prev_sensor.direction[4] = 1
                            # 계단 weight = 2로 설정
                            # current_sensor.weight['down'] = 2
                            # prev_sensor.weight['up'] = 2

                    prev_sensor = current_sensor


def find_exit(all_node, node, linked_node_list):
    for i in all_node:
        substract = []
        shortest_node_num = []
        for j in linked_node_list[i]:
            substract.append(node[j].distance - node[i].distance)
        shortest_distance_node_index = [i for i, value in enumerate(substract) if value == min(substract)]
        node[i].set_exit_diret_num(shortest_distance_node_index)
        for k in shortest_distance_node_index:
            shortest_node_num.append(linked_node_list[i][k])  # output = shortest node_num
            # print("aa->",shortest_node_num)
        if node[i].forward != None and node[i].forward.index in shortest_node_num:
            node[i].exit_diret += 32
        if node[i].backward != None and node[i].backward.index in shortest_node_num:
            node[i].exit_diret += 16
        if node[i].right != None and node[i].right.index in shortest_node_num:
            node[i].exit_diret += 4
        if node[i].left != None and node[i].left.index in shortest_node_num:
            node[i].exit_diret += 8
        if node[i].up != None and node[i].up.index in shortest_node_num:
            node[i].exit_diret += 2
        if node[i].down != None and node[i].down.index in shortest_node_num:
            node[i].exit_diret += 1


if __name__ == "__main__":

    map = Map()

    for i in range(0,map.all_node_num):
        map.node.append(AddNode())

    create_sensor_map('./length.txt', './width.txt', './stairs.txt')

    # 다익스트라 알고리즘
    # linked_node_list[인접노드를 찾을 노드 num] = [인접 node num들]
    linked_node_list = []
    for i in range(0,map.all_node_num):
        linked_node_list.append([])
        for j in find_linked_node(map.node[i]):
            linked_node_list[i].append(j)

    set_weight(map.node, map.exit)  # 모든 노드에서 가장 가까운 탈출구까지 거리 구하는 함수

    for i in range(0,map.all_node_num):  # 각 노드들이 가진 거리들 출력
        map.now_distance.append(map.node[i].distance)
        print(i, ':', map.node[i].distance, end=" ")
    print()


    # 화재전 노드 방향 연결
    for i in range(0,map.all_node_num):
        map.all_node.append(i)
    for j in map.exit:
        map.all_node.remove(j)

    find_exit(map.all_node, map.node, linked_node_list)
    for i in range(0,map.all_node_num):
        print(i, '->', map.node[i].exit_diret)
    # print("node21 visited_place",node[21].visited_place)

    fire_test(6, 6, 6, map.node, linked_node_list)
    print("fire in 2")
    for i in range(0,map.all_node_num):
        print(i, '->', map.node[i].exit_diret)
    # #print("node21 visited_place", node[21].visited_place)

    # fire_test(11, 11, 11, map.node, linked_node_list)
    # print("fire in 18")
    # for i in range(map.all_node_num):
    #     print(i, '->', map.node[i].exit_diret)
    # # print("node21 visited_place", node[21].visited_place)
    #
    # fire_test(3, 3, 3, map.node, linked_node_list)
    # print("fire in 20")
    # for i in range(map.all_node_num):
    #     print(i, '->', map.node[i].exit_diret)
    # # #print("node21 visited_place", node[21].visited_place)
    #
    # fire_test(16, 16, 16, map.node, linked_node_list)
    # print("fire in 20")
    # for i in range(map.all_node_num):
    #     print(i, '->', map.node[i].exit_diret)

    print("asdasd"+fire_in_node(7,map.node,linked_node_list))
    #print("node21 visited_place", node[21].visited_place)

'''
node = 그래프 상의 모든 노드들 (object)
linked_node_list = 모든 노드들이 각자 자신과 연결된 노드 번호를 가지고 있는 table 
exit = 탈출구가 있는 노드 

해야하는것: distance가 작은값으로 방향 표시하게 해야함
           불이랑 연기 났을때 방향 표시가 바뀌게 해야함
'''