#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nmea_msgs.msg import Sentence
from std_msgs.msg import Header

class NMEAPublisher(Node):
    def __init__(self):
        super().__init__('nmea_publisher_node')
        
        # 발행자 설정
        self.publisher_ = self.create_publisher(Sentence, '/ntrip_nmea', 10)
        
        # 타이머 설정 (1Hz)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.get_logger().info('NMEA Publisher Node has been started')
    
    def timer_callback(self):
        # NMEA 메시지 생성
        nmea_sentence = Sentence()
        
        # 헤더 설정
        nmea_sentence.header = Header()
        nmea_sentence.header.stamp = self.get_clock().now().to_msg()
        nmea_sentence.header.frame_id = ""
        
        # NMEA 문장 설정 (원하는 위치 선택)
        nmea_sentence.sentence = "$GPGGA,085723.919,3554.842,N,12848.203,E,1,12,1.0,0.0,M,0.0,M,,*6B\r\n" # 대가대
        # nmea_sentence.sentence = "$GPGGA,065201.798,3717.326,N,12706.431,E,1,12,1.0,0.0,M,0.0,M,,*69\r\n" # 용인운전면허시험장
        # nmea_sentence.sentence = "$GPGGA,121305.984,3314.565,N,12625.487,E,1,12,1.0,0.0,M,0.0,M,,*65\r\n" # 제주도
        # nmea_sentence.sentence = "$GPGGA,055110.532,3318.337,N,12618.855,E,1,12,1.0,0.0,M,0.0,M,,*60\r\n" # 신화월드
        
        # 메시지 발행
        self.publisher_.publish(nmea_sentence)
        self.get_logger().info(f'Published NMEA Sentence: {nmea_sentence.sentence.strip()}')

def main(args=None):
    rclpy.init(args=args)
    
    nmea_publisher = NMEAPublisher()
    
    try:
        rclpy.spin(nmea_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        # 노드 종료
        nmea_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
