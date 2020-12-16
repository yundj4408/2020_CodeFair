import heapq
from collections import deque


class Node:
    """센서 노드 클래스"""

    def __init__(self, sensor_num):
        # 센서 번호
        self.data = sensor_num

        # 인접 노드 레퍼런스
        self.adjacent_node = {'north': None, 'south': None, 'east': None, 'west': None, 'up': None, 'down': None}
        self.direction_of_exit = {'north': False, 'south': False, 'east': False, 'west': False, 'up': False, 'down': False}
        self.forward = None
        self.backward = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        # 다익스트라 알고리즘 쓰기위한 변수
        self.distance = float('inf')
        self.weight = {'north': 1, 'south': 1, 'east': 1, 'west': 1, 'up': 1, 'down': 1}
        self.visited = False
        self.fire = False
        self.gass = False
        self.exit_diret = []
        self.exit_diret_num = 0

    def set_exit_diret_num(self):
        for boolean in self.direction_of_exit.values():
            if boolean:
                self.exit_diret_num += 1

class Map:
    """센서 맵 클래스"""

    def __init__(self):
        self.sensor_map = {}
        self.exit_node = {}
        self.fire_node = {}
        self.fire_place_num = []

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
                        sensor_num = int(sensor_num.strip())

                        if sensor_num not in self.sensor_map:  # 센서 정보가 센서 딕셔너리에 없으면
                            current_sensor = Node(sensor_num)
                            self.sensor_map[sensor_num] = current_sensor
                        else:
                            current_sensor = self.sensor_map[sensor_num]

                        if file_name == "exit.txt":  # 출구 센서 지정
                            current_sensor.state = 'E'
                            self.exit_node[sensor_num] = current_sensor

                        if prev_sensor is not None:

                            if file_name == "width.txt":  # 가로 연결된 센서
                                current_sensor.adjacent_node['west'] = prev_sensor
                                prev_sensor.adjacent_node['east'] = current_sensor

                            elif file_name == "length.txt":  # 세로 연결된 센서
                                current_sensor.adjacent_node['north'] = prev_sensor
                                prev_sensor.adjacent_node['south'] = current_sensor

                            elif file_name == "stairs.txt":  # 계단 센서
                                current_sensor.adjacent_node['down'] = prev_sensor
                                prev_sensor.adjacent_node['up'] = current_sensor

                                # 계단 weight = 2로 설정
                                current_sensor.weight['down'] = 2
                                prev_sensor.weight['up'] = 2

                        prev_sensor = current_sensor

    """DKA"""

    def adjacent_node_is(self, node):
        """인접노드 리턴
        입력 : 노드 주소
        리턴 : {node_num: node_address, ...}"""
        adjacent = node.adjacent_node
        adjacent_node = {}

        for direction, diret_node in adjacent.items():
            if adjacent[direction] is not None and diret_node is not True:
                adjacent_node[diret_node.data] = diret_node

        return adjacent_node

    def all_adjacent_node(self):
        """모든 노드의 연결된 노드를 이중 리스트로 출력해줌"""
        all_adjacent_node = []

        for node in self.sensor_map.values():

            temp = []
            for node_num in self.adjacent_node_is(node).keys():
                temp.append(node_num)
            all_adjacent_node.append(temp)

        return all_adjacent_node

    def set_state_to_0(self):
        """모든 노드 state 0으로"""
        for num in self.sensor_map:
            if self.sensor_map[num].state != 'E' and self.sensor_map[num].state != 'F' and self.sensor_map[
                num].state != 'G':
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

    """JSA"""

    # def set_direction_of_exit_false(self, nodes):
    #     """입력받은 노드set의 출구방향 False로 설정"""
    #     for node in nodes.values():
    #         for direction in node.direction_of_exit.keys():
    #             node.direction_of_exit[direction] = False

    def set_recheck_false(self, nodes):
        for i in nodes.values():
            i.recheck = False

    def set_all_visited_false(self):
        """모든 노드의 방문표시 False로"""
        for node in self.sensor_map.values():
            node.visited = False

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

            while queue:  # 큐가 빌 때 까지 -> 모든 노드를 방문할 때 까지

                # 현재 노드에 큐에서 우선순위가 가장 높은 큐를 넣는다.
                current_node = self.sensor_map[heapq.heappop(queue)[1]]

                # 현재 노드의 인접노드 중 방문하지 않은 노드를 불러온다.

                for adjacent_direction, adjacent_node in current_node.adjacent_node.items():

                    if adjacent_node is not None and adjacent_node.visited is False and adjacent_node.fire is False and adjacent_node.distance > current_node.distance + \
                            current_node.weight[adjacent_direction]:
                        adjacent_node.distance = current_node.distance + current_node.weight[adjacent_direction]

                        heapq.heappush(queue, (adjacent_node.distance, adjacent_node.data))
                        adjacent_node.visited = True

    def direction_of_exit(self, search_node=None):  # 넘겨주는 값 : re_set_distance 리턴값
        """노드에서 어느방향으로 탈출해야 할 지 set"""
        if search_node is None:
            search_node = self.sensor_map

        #self.set_direction_of_exit_false(search_node)

        for current_num, current_node in search_node.items():  # 현재 노드

            for direction, adjacent_node in self.adjacent_node_is(current_node).items():  # 현재 노드의 주변 노드

                if adjacent_node.distance < current_node.distance:
                    current_node.direction_of_exit[direction] = True
                    current_node.exit_diret_num += 1

    def set_direction_of_exit_false(self, node):
        """입력받은 노드set의 출구방향 False로 설정"""

        for direction in node.direction_of_exit.keys():
            node.direction_of_exit[direction] = False

    def set_fire(self, sensor_num):
        """센서에서 불 감지 시 실행"""
        self.sensor_map[sensor_num].state = 'F'
        self.sensor_map[sensor_num].fire = True
        self.sensor_map[sensor_num].recheck = True  # re_set_distance에 필요
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


def fire_test(Map, fire_node_num, send_node_num1, send_node_num2):
    queue = []
    del_list = []
    self = Map
    fire_start = fire_node_num
    send1 = send_node_num1
    send2 = send_node_num2

    node = self.sensor_map  # {}
    node[fire_node_num].distance = float('inf')

    if fire_node_num not in self.fire_place_num:
        self.fire_place_num.append(fire_node_num)

    for ad_node_num in self.adjacent_node_is(node[send2]).keys():
        if ad_node_num != send1 and ad_node_num not in self.fire_place_num:
            queue.insert(0, ad_node_num)

    for current_node_num in queue:
        substract = []
        node_list = []
        shortest_node_num = []

        for ad_node_num in self.adjacent_node_is(node[current_node_num]).keys():
            node_list.append(ad_node_num)

            if ad_node_num != send2:
                substract.append(node[ad_node_num].distance - node[current_node_num].distance)
            else:
                substract.append(float('inf'))

        if min(substract) != -1 or node[current_node_num].exit_diret_num != substract.count(-1):
           #node[current_node_num].exit_diret = []
            self.set_direction_of_exit_false(node[current_node_num])
            shortest_distance_node_index = [current_node_num for current_node_num, value in enumerate(substract) if
                                            value == min(substract)]

            for k in shortest_distance_node_index:
                shortest_node_num.append(node_list[k])

            if node[current_node_num].adjacent_node['north'] is not None and node[current_node_num].adjacent_node['north'].data in shortest_node_num:
                node[current_node_num].adjacent_node['north'] = True
            if node[current_node_num].adjacent_node['south'] is not None and node[current_node_num].adjacent_node['south'].data in shortest_node_num:
                node[current_node_num].adjacent_node['south'] = True
            if node[current_node_num].adjacent_node['east'] is not None and node[current_node_num].adjacent_node['east'].data in shortest_node_num:
                node[current_node_num].adjacent_node['east'] = True
            if node[current_node_num].adjacent_node['west'] is not None and node[current_node_num].adjacent_node['west'].data in shortest_node_num:
                node[current_node_num].adjacent_node['west'] = True
            if node[current_node_num].adjacent_node['up'] is not None and node[current_node_num].adjacent_node['up'].data in shortest_node_num:
                node[current_node_num].adjacent_node['up'] = True
            if node[current_node_num].adjacent_node['down'] is not None and node[current_node_num].adjacent_node['down'].data in shortest_node_num:
                node[current_node_num].adjacent_node['down'] = True

            node[current_node_num].set_exit_diret_num()
        else:
            del_list.append(current_node_num)

    for i in del_list:
        queue.remove(i)

    for i in queue:
        fire_test(Map,fire_start, send2, i)