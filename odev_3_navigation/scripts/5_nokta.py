#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class PatrolMission:
    def __init__(self):
        # Action client tanımlaması
        self.nav_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Move base sunucusu bekleniyor...")
        self.nav_client.wait_for_server()
        rospy.loginfo("Sunucuya bağlanıldı. Görev başlıyor.")

    def go_to_target(self, pos_x, pos_y, orient_w):
        hedef = MoveBaseGoal()
        hedef.target_pose.header.frame_id = "map"
        hedef.target_pose.header.stamp = rospy.Time.now()
        
        # Pozisyon ayarları
        hedef.target_pose.pose.position.x = pos_x
        hedef.target_pose.pose.position.y = pos_y
        
        # Yönelim ayarları
        hedef.target_pose.pose.orientation.w = orient_w
        
        self.nav_client.send_goal(hedef)
        
        is_finished = self.nav_client.wait_for_result()
        if not is_finished:
            rospy.logerr("Hedefe ulaşılamadı veya sunucu çöktü!")
            rospy.signal_shutdown("Hata oluştu!")
            return None
        else:
            return self.nav_client.get_result()

def run_mission():
    rospy.init_node('turtlebot_auto_patrol', anonymous=True)
    
    robot_controller = PatrolMission()
    
    # Gidilecek rotalar (x, y, w) formatı
    rotalar = [
        [0.0, 1.5, 1.0],
        [0.5, 0.5, 1.0],
        [1.5, 0.0, 1.0],
        [0.5, -0.5, 1.0],
        [-0.5, 0.0, 1.0]
    ]
    
    sayac = 1
    for hedef_noktasi in rotalar:
        x_val = hedef_noktasi[0]
        y_val = hedef_noktasi[1]
        w_val = hedef_noktasi[2]
        
        rospy.loginfo("Hedef {} gönderiliyor -> X: {}, Y: {}".format(sayac, x_val, y_val))
        durum = robot_controller.go_to_target(x_val, y_val, w_val)
        
        if durum:
            rospy.loginfo("--- Hedef {} tamamlandı! ---".format(sayac))
            rospy.sleep(1.2) # Diğer hedefe geçmeden önce kısa bir bekleme
            
        sayac += 1

if __name__ == '__main__':
    try:
        run_mission()
    except rospy.ROSInterruptException:
        rospy.logwarn("Görev kullanıcı tarafından sonlandırıldı.")
