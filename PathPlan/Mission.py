'''
#################### PATH PLAN TEAM ####################

## ABOUT
- 각 미션 별로 제어팀에게 경로 정보가 담긴 packet을 넘겨줌

# +---+-------- packet[5] ----------+
# | 0 | mission number              |
# +---+-----------------------------+ 
# | 1 | coordinates of the targets  |
# +---+-----------------------------+
# | 2 | (depends on mission)        |
# +---+-----------------------------+
# | 3 | (depends on mission)        |
# +---+-----------------------------+
# | 4 | is school zone?             |
# +---+-----------------------------+


## INPUT & OUTPUT
- input: pathplan.py에서 표지판에 따른 YOLO 값 >> mission = Mission(1), mission.getpath()
- output: 각 미션 별 packet

'''

########### IMPORT MODULE ###########
from Lane_Detection import Lane_Detection
from Combine import Combine
from Path_Planning import Path_Planning
# from YOLO import yolo
import time
#####################################

########## IMPORT INSTANCE ##########
# lane_detection = Lane_Detection()
# combine = Combine()
# yolo = yolo()
#####################################



class Mission:
    def __init__(self, mission_num):
        self._mission_num = mission_num  # 기본값은 0
        self.packet = [mission_num, [(0,0)], None, None, 0]  # default
        self._path_planning = Path_Planning(mission_num)

    def get_packet(self):
        if self._mission_num == 0:
            self._path_tracking
        elif self._mission_num == 1:
            self._static_obstacle
        elif self._mission_num == 2:
            self._dynamic_obstacle
        elif self._mission_num == 3:
            self._non_signal_straight
        elif self._mission_num == 4:
            self._non_signal_left
        elif self._mission_num == 5:
            self._non_signal_right
        elif self._mission_num == 6:
            self._signal_left
        elif self._mission_num == 7:
            self._signal_straight
        elif self._mission_num == 8:
            self._parking

        return self.packet

    ############### MISSON ###############

    ## 0. 직선 주행(기본 주행)
    def _path_tracking(self):
        self.packet[1] = self._path_planning.get_path()
        self.packet[4] = yolo.is_school_zone()

    ## 1. 정적 장애물 미션
    def _static_obstacle(self):
        self.packet[1] = self._path_planning.get_path()

    ## 2. 동적 장애물 미션
    def _dynamic_obstacle(self):
        self.packet[1] = self._path_planning.get_path()
        yolo = YOLO()
        self.packet[4] = yolo.is_school_zone()

    ## 3. 비신호 직진 미션
    def _non_signal_straight(self):
        self.packet[1] = self._path_planning.get_path()

    ## 4. 비신호 좌회전 미션
    def _non_signal_left(self):
        self.packet[1] = self._path_planning.get_path()

    ## 5. 비신호 우회전 미션
    def _non_signal_right(self):
        self.packet[1] = self._path_planning.get_path()

    ## 6. 신호 좌회전 미션
    def _signal_left(self):
        self.packet[1] = self._path_planning.get_path()
        lane_detection = Lane_Detection()
        self.packet[2] = lane_detection.get_stop_line()  # 정지선까지 거리
        yolo = YOLO()
        self.packet[3] = yolo.traffic_light()  # 좌회전신호 판단 >> 주행 가능: 1, 멈춤: 0
        self.packet[4] = yolo.is_school_zone()

    ## 7. 신호 직진 미션
    def _signal_straight(self):
        self.packet[1] = self._path_planning.get_path()
        lane_detection = Lane_Detection()
        self.packet[2] = lane_detection.get_stop_line()  # 정지선까지 거리
        yolo = YOLO()
        self.packet[3] = yolo.traffic_light()  # 적색 신호 판단 >> 주행 가능: 1, 멈춤: 0

    ## 8. 주차 미션
    def _parking(self):
        self.packet[1] = self._path_planning.get_path()

    #####################################