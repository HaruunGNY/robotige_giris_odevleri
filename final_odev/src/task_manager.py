#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KTÜN Robotiğe Giriş - Final Projesi
Görev Yöneticisi Düğümü (task_manager.py)

Bu düğüm, sistemin beynidir (Durum Makinesi). mission.yaml içindeki hedefleri sırayla
move_base aksiyon sunucusuna gönderir, hedefe ulaştığında qr_reader servisinden
QR kodu okumasını ister, hata yönetimini uygular ve sonunda başarım durum raporu sunar.
"""

import rospy
import actionlib
import yaml
import os
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_srvs.srv import Trigger
from geometry_msgs.msg import PoseWithCovarianceStamped

class TaskManagerNode:
    def __init__(self):
        rospy.init_node("task_manager_node", anonymous=False)
        rospy.loginfo("[Task Manager] Düğüm başlatılıyor...")

        # Servislerin ve aksiyonların hazır olmasını bekleme
        self.move_base_client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("[Task Manager] move_base aksiyon sunucusu bekleniyor...")
        self.move_base_client.wait_for_server()
        rospy.loginfo("[Task Manager] move_base sunucusu hazır.")

        rospy.loginfo("[Task Manager] QR okuyucu servisi bekleniyor (/read_qr)...")
        rospy.wait_for_service("/read_qr")
        self.qr_client = rospy.ServiceProxy("/read_qr", Trigger)
        rospy.loginfo("[Task Manager] QR okuyucu servisi hazır.")

        # Parametre sunucusundan görev bilgilerini çekme
        # Eğer parametre yoksa doğrudan varsayılan YAML dosyasından yükleme yapalım
        if rospy.has_param("/locations"):
            self.locations = rospy.get_param("/locations")
            self.mission_data = {}
            for loc in self.locations:
                self.mission_data[loc] = rospy.get_param(f"/{loc}")
        else:
            # Yedek plan: Dosyadan doğrudan yükleme
            config_path = os.path.join(
                os.path.dirname(__file__), "..", "config", "mission.yaml"
            )
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
                self.locations = data["locations"]
                self.mission_data = data
            rospy.loginfo("[Task Manager] Görev bilgileri yerel mission.yaml dosyasından yüklendi.")

        # Raporlama için veri yapısı
        self.report = {}
        for loc in self.locations:
            self.report[loc] = "PENDING"

    def send_navigation_goal(self, location_name, retry_count=1):
        """move_base ile robotu hedefe yönlendirir, başarısızlık durumunda tekrar dener."""
        goal_data = self.mission_data[location_name]["goal"]
        
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        
        # Koordinatları ata
        goal.target_pose.pose.position.x = goal_data["x"]
        goal.target_pose.pose.position.y = goal_data["y"]
        goal.target_pose.pose.position.z = goal_data["z"]
        
        goal.target_pose.pose.orientation.x = goal_data.get("qx", 0.0)
        goal.target_pose.pose.orientation.y = goal_data.get("qy", 0.0)
        goal.target_pose.pose.orientation.z = goal_data.get("qz", 0.0)
        goal.target_pose.pose.orientation.w = goal_data.get("qw", 1.0)
        
        for attempt in range(retry_count + 1):
            rospy.loginfo(
                f"[Task Manager] {location_name} konumuna gidiliyor... (Deneme {attempt + 1}/{retry_count + 1})"
            )
            
            self.move_base_client.send_goal(goal)
            
            # 90 saniye zaman aşımı (timeout)
            finished_within_time = self.move_base_client.wait_for_result(rospy.Duration(90.0))
            
            if finished_within_time:
                state = self.move_base_client.get_state()
                if state == actionlib.GoalStatus.SUCCEEDED:
                    rospy.loginfo(f"[Task Manager] Hedef noktaya ulaşıldı: {location_name}")
                    return True
                else:
                    rospy.logwarn(f"[Task Manager] Hedefe gidilemedi. Durum kodu: {state}")
            else:
                rospy.logerr(f"[Task Manager] Hedef zaman aşımına uğradı (90 saniye)!")
                self.move_base_client.cancel_goal()
                
        return False

    def verify_qr_code(self, location_name, max_retries=2):
        """QR kodunu okur ve hedeflenen konum ismiyle eşleşip eşleşmediğini doğrular."""
        expected_qr = self.mission_data[location_name]["qr_expected"]
        
        for attempt in range(max_retries + 1):
            rospy.loginfo(
                f"[Task Manager] QR okuma tetiklendi... (Deneme {attempt + 1}/{max_retries + 1})"
            )
            
            try:
                # Servis çağrısı
                res = self.qr_client()
                if res.success:
                    decoded_data = res.message
                    if decoded_data == expected_qr:
                        rospy.loginfo(f"[Task Manager] Görev noktası doğrulandı ({decoded_data})")
                        return "SUCCESS"
                    else:
                        rospy.logwarn(
                            f"[Task Manager] QR okuma hatalı! Beklenen: {expected_qr}, Okunan: {decoded_data}. Yeniden deneniyor..."
                        )
                else:
                    rospy.logwarn(f"[Task Manager] QR okunamadı! Yeniden deneniyor...")
            except rospy.ServiceException as e:
                rospy.logerr(f"[Task Manager] Servis çağrı hatası: {e}")
                
            # Yeniden denemeden önce kısa bir süre bekle
            rospy.sleep(1.0)
            
        rospy.logerr(f"[Task Manager] QR doğrulama başarısız oldu. Görev noktası ATLANDI.")
        return "SKIPPED"

    def print_final_report(self):
        """Görev bitiminde şık bir başarım raporu sunar."""
        print("\n" + "="*50)
        print("         🏁 GÖREV TAMAMLANDI - FİNAL RAPORU 🏁         ")
        print("="*50)
        
        success_count = 0
        skipped_count = 0
        fail_count = 0
        
        for loc, status in self.report.items():
            if status == "SUCCESS":
                status_str = "✅ BAŞARILI (SUCCESS)"
                success_count += 1
            elif status == "SKIPPED":
                status_str = "🟡 ATLANDI (SKIPPED)"
                skipped_count += 1
            else:
                status_str = "❌ BAŞARISIZ (FAIL)"
                fail_count += 1
            print(f"📍 {loc:<20} : {status_str}")
            
        print("-"*50)
        total = len(self.report)
        print(f"Toplam Nokta : {total}")
        print(f"Başarılı     : {success_count}")
        print(f"Atlanan      : {skipped_count}")
        print(f"Başarısız    : {fail_count}")
        
        success_rate = (success_count / float(total)) * 100
        print(f"Başarım Oranı: %{success_rate:.1f}")
        print("="*50 + "\n")

    def run(self):
        rospy.loginfo("[Task Manager] Görev akışı başlatılıyor. AMCL lokalizasyonu hazır olmalıdır.")
        
        # İlk AMCL lokalizasyon kontrolü (opsiyonel ama sistemi garantiye alır)
        rospy.sleep(2.0)
        
        for loc in self.locations:
            # 1. Hedefe Git
            nav_success = self.send_navigation_goal(loc, retry_count=1)
            
            if nav_success:
                # 2. QR Kod Doğrula
                qr_status = self.verify_qr_code(loc, max_retries=2)
                self.report[loc] = qr_status
            else:
                self.report[loc] = "FAIL"
                rospy.logerr(f"[Task Manager] {loc} konumuna ulaşılamadı. Sonraki hedefe geçiliyor.")
                
            rospy.sleep(1.0)
            
        self.print_final_report()

if __name__ == "__main__":
    try:
        node = TaskManagerNode()
        node.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("[Task Manager] Düğüm kesildi.")
