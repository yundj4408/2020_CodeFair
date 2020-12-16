import heapq
from collections import deque

class Node:
    """센서 노드 클래스"""
    def __init__(self, sensor_num):
        # 센서 번호
        self.data = sensor_num

        # 인접 노드 레퍼런스
        self.adjacent_node = {'north':None, 'south':None, 'east':None, 'west':None, 'up':None, 'down':None}
        self.direction_of_exit = {'north':False, 'south':False, 'east':False, 'west':False, 'up':False, 'down':False}
        

        # 다익스트라 변수
        self.distance = float('inf')
        self.weight = {'north':1, 'south':1, 'east':1, 'west':1, 'up':1, 'down':1}
        self.visited = False

        self.fire = False
        self.gass = False
        self.recheck = False

        # BFS 쓰기위한 변수
        self.state = 0  # 불 : F | 연기 : G | 출구 : E


class Map:
    """센서 맵 클래스"""
    def __init__(self):
        self.sensor_map = {}
        self.exit_node = {}
        self.fire_node = {}
        self.gass_node = {}

    def create_sensor_map(self, length_file, width_file, stairs_file, exit_file):
        """센서의 고유번호, 관계, 위치가 저장된 파일을 전달하면 그래프화 하고 sensor_map에 저장."""
        self.sensor_map = {}
        file_list = [length_file, width_file, stairs_file, exit_file]

        for file_name in file_list:

            with open(file_name) as sensor_file:

                for line in sensor_file:
                    
                    # 파일 입력받을 때 스플릿
                    raw_data = line.strip().split("-")
                    prev_sensor = None

                    for sensor_num in raw_data:
                        sensor_num = sensor_num.strip()

                        if sensor_num not in self.sensor_map:   # 센서 정보가 센서 딕셔너리에 없으면
                            current_sensor = Node(sensor_num)
                            self.sensor_map[sensor_num] = current_sensor
                        else:
                            current_sensor = self.sensor_map[sensor_num]


                        if file_name == "exit.txt": # 출구 센서 지정
                            current_sensor.state = 'E'
                            self.exit_node[sensor_num] = current_sensor


                        if prev_sensor is not None:

                            if file_name == "width.txt":# 가로 연결된 센서 
                                current_sensor.adjacent_node['west'] = prev_sensor
                                prev_sensor.adjacent_node['east'] = current_sensor

                            elif file_name == "length.txt":   # 세로 연결된 센서
                                current_sensor.adjacent_node['north'] = prev_sensor
                                prev_sensor.adjacent_node['south'] = current_sensor

                            elif file_name == "stairs.txt": # 계단 센서
                                current_sensor.adjacent_node['down'] = prev_sensor
                                prev_sensor.adjacent_node['up'] = current_sensor

                                # 계단 weight = 2로 설정
                                current_sensor.weight['down'] = 2
                                prev_sensor.weight['up'] = 2
                        
                        prev_sensor = current_sensor

    def adjacent_node_is(self, node):
        """인접노드 리턴"""
        adjacent = node.adjacent_node
        adjacent_node = {}

        for direction, node in adjacent.items():
            if adjacent[direction] is not None:
                adjacent_node[direction] = node

        return adjacent_node
        
    def set_state_to_0(self):
        """모든 노드 state 0으로"""
        for num in self.sensor_map:
            if self.sensor_map[num].state != 'E' and self.sensor_map[num].state != 'F' and self.sensor_map[num].state != 'G':
                self.sensor_map[num].state = 0

    def set_state(self):
        """각 노드 state 값 지정"""
        current_nodes = self.exit_node
        
        while current_nodes:
            temp = []
            for num in current_nodes:
                
                adjacent_nodes = self.adjacent_node_is(self.sensor_map[num])

                for ad_num in adjacent_nodes:
                    
                    if self.sensor_map[ad_num].state == 0:
                        temp.append(ad_num)

                        if self.sensor_map[num].state == 'E':
                            self.sensor_map[ad_num].state += 1
                        else:
                            self.sensor_map[ad_num].state = self.sensor_map[num].state + 1
                        
            current_nodes = temp

    def set_all_visited_false(self):
        """모든 노드의 방문표시 False로"""
        for node in self.sensor_map.values():
            node.visited = False

    def set_direction_of_exit_false(self, nodes):
        """입력받은 노드set의 출구방향 False로 설정"""
        for node in nodes.values():
            for direction in node.direction_of_exit.keys():
                node.direction_of_exit[direction] = False

    def set_recheck_false(self, nodes):
        for i in nodes.values():
            i.recheck = False

    def set_distance_dijkstra(self):
        """다익스트라 알고리즘으로 노드의 distance 설정"""
        for start_num in self.exit_node:
            self.set_all_visited_false()
            queue = []

            # 우선순위 큐에 들어가는 우선순위는 노드의 distance 값으로 한다.
            # 시작 노드를 큐에 넣고 distance는 0으로 한다. 큐에 넣었으니 visited = True로 한다.
            start_node = self.sensor_map[start_num]
            start_node.distance = 0
            heapq.heappush(queue, (start_node.distance, start_node.data))
            start_node.visited = True

            while queue:    # 큐가 빌 때 까지 -> 모든 노드를 방문할 때 까지

                # 현재 노드에 큐에서 우선순위가 가장 높은 큐를 넣는다.
                current_node = self.sensor_map[heapq.heappop(queue)[1]]

                # 현재 노드의 인접노드 중 방문하지 않은 노드를 불러온다.

                for adjacent_direction, adjacent_node in current_node.adjacent_node.items():
                    
                    if adjacent_node is not None and adjacent_node.visited is False and adjacent_node.fire is False and adjacent_node.distance > current_node.distance + current_node.weight[adjacent_direction]:
                        adjacent_node.distance = current_node.distance + current_node.weight[adjacent_direction]

                        heapq.heappush(queue, (adjacent_node.distance, adjacent_node.data))
                        adjacent_node.visited = True

    def direction_of_exit(self, search_node = None):    # 넘겨주는 값 : re_set_distance 리턴값
        """노드에서 어느방향으로 탈출해야 할 지 set"""
        if search_node is None:
            search_node = self.sensor_map

        self.set_direction_of_exit_false(search_node)

        for current_node in search_node.values():   # 현재 노드

            for direction, adjacent_node in self.adjacent_node_is(current_node).items(): # 현재 노드의 주변 노드

                if adjacent_node.distance < current_node.distance:
                    current_node.direction_of_exit[direction] = True

    def re_set_distance(self):
        """불이 감지됐을 떄 불에서부터 다시 계산한다."""
        # 확인한 노드 (리턴해야함)
        checked_node = {}

        # 불과 인접한 노드
        fire_ad_node = [] # 우선순위 큐

        for current_node in self.fire_node.values():
            for node in self.adjacent_node_is(current_node).values():
                if node.fire is False:
                    heapq.heappush(fire_ad_node, (node.distance, node.data))   
                    # fire_ad_node.append(node)

        while fire_ad_node:
            # for i in fire_ad_node:
            #     print("큐 안에 있는 노드", i[1], "distance", self.sensor_map[i[1]].distance)
            
            node_num = heapq.heappop(fire_ad_node)[1]
            node = self.sensor_map[node_num]
            # print("노드", node.data, "을 꺼냄")
            
            # node = fire_ad_node.popleft()
            node.recheck = True
            checked_node[node.data] = node
            ad_nodes = self.adjacent_node_is(node)


            for direction, ad_node in ad_nodes.items():
                # print("주변노드", ad_node.data, "distance", ad_node.distance)
                
                if node.distance < ad_node.distance and ad_node.recheck is False and ad_node.fire is False:
                    checked_node[ad_node.data] = ad_node
                    # print("검사할 노드", ad_node.data, "distance", ad_node.distance)
                    if ad_node.data not in fire_ad_node:
                        heapq.heappush(fire_ad_node, (ad_node.distance, ad_node.data))  
                        # fire_ad_node.append(ad_node)

                    node.distance += 2*node.weight[direction]
            
            print()

        print("sub graph :", checked_node.keys())
        self.set_recheck_false(checked_node)
        return checked_node

    def set_fire(self, sensor_num):
        """센서에서 불 감지 시 실행"""
        self.sensor_map[sensor_num].state = 'F'
        self.sensor_map[sensor_num].fire = True
        self.sensor_map[sensor_num].recheck = True      # re_set_distance에 필요
        self.sensor_map[sensor_num].distance = float('inf')
        self.fire_node[sensor_num] = self.sensor_map[sensor_num]

    def set_gass(self, sensor_num):
        """센서에서 가스 감지 시 실행"""
        self.sensor_map[sensor_num].state = 'G'
        self.sensor_map[sensor_num].gass = True
        self.gass_node[sensor_num] = self.sensor_map[sensor_num]

    def __str__(self):
        """센서맵의 센서들 문자열 리턴"""
        res_str = "|"

        for data in sorted(self.sensor_map.keys()):
            res_str += f" {data} |"

        return res_str