#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def yonetici_node():
    # Sınıf tabanlı değil, fonksiyon tabanlı ve global değişkenlerle daha amatör/öğrenci tarzında ama sağlam kod.
    rospy.init_node('kaplumbaga_yonetici', anonymous=False)
    
    # Global state değişkenleri
    global son_gosterim_zamani
    son_gosterim_zamani = rospy.get_time()

    def konum_dinleyici(gelen_veri):
        global son_gosterim_zamani
        su_an = rospy.get_time()
        
        # 1 saniyelik gecikme kontrolü
        if (su_an - son_gosterim_zamani) >= 1.0:
            rospy.loginfo("Turtlesim pozisyonu X=%.2f Y=%.2f Açı=%.2f", 
                          gelen_veri.x, gelen_veri.y, gelen_veri.theta)
            son_gosterim_zamani = su_an

    # Abone olma
    rospy.Subscriber('/turtle1/pose', Pose, konum_dinleyici)
    
    # Yayıncı oluşturma
    hareket_yayinci = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    hiz_ayar = rospy.Rate(10) # 10 Hz
    
    hareket_komutu = Twist()
    hareket_komutu.linear.x = 0.5   # İleri hız
    hareket_komutu.angular.z = 0.2  # Dönme hızı
    
    rospy.loginfo("Kaplumbağa yöneticisi aktifleşti! Hareket ve konum dinleme başlıyor...")
    
    while not rospy.is_shutdown():
        hareket_yayinci.publish(hareket_komutu)
        hiz_ayar.sleep()

if __name__ == '__main__':
    try:
        yonetici_node()
    except rospy.ROSInterruptException:
        pass
