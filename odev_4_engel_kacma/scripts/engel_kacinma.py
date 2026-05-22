#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Robotiğe Giriş Dersi - Ödev 4: Lidar ile Engellerden Kaçınma
Bu düğüm, TurtleBot3 robotunun Lidar (LaserScan) verilerini analiz ederek 
önündeki engellerden kaçmasını ve güvenli bir şekilde hareket etmesini sağlar.
"""

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class OtonomEngelSavar:
    def __init__(self):
        # Düğüm adını özgün ve belirgin şekilde başlatıyoruz
        rospy.init_node('engel_kacinma_yoneticisi', anonymous=True)
        
        # Robotun hız komutlarını yayınlayacağı Publisher
        self.motor_guc_yayinci = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Lidar sensör verilerini dinleyeceğimiz Subscriber
        self.lazer_tarama_dinleyici = rospy.Subscriber('/scan', LaserScan, self.lazer_sensor_okuma)
        
        # Göndereceğimiz hız mesajını tanımlıyoruz
        self.hareket_komutlari = Twist()
        
        # Parametreler (Kolayca ayarlanabilmesi için)
        self.guvenlik_siniri = 0.5    # Engel algılama kritik mesafesi (metre)
        self.hedef_ileri_hiz = 0.2    # Engel yokken düz gitme hızı (m/s)
        self.aci_donus_hizi = 0.2     # Engel varken dönüş hızı (rad/s)
        
        rospy.loginfo("==============================================")
        rospy.loginfo("Otonom Engel Savar Sistemi Başarıyla Başlatıldı.")
        rospy.loginfo("Kritik Güvenlik Sınırı: {} metre".format(self.guvenlik_siniri))
        rospy.loginfo("==============================================")

    def lazer_sensor_okuma(self, sensor_verisi):
        """
        Lidar sensöründen gelen verileri işleyen geri çağırma (callback) fonksiyonu.
        Ön cephedeki (sol 40 derece ve sağ 40 derece) mesafeleri analiz eder.
        """
        # Sol ve sağ açılardaki mesafe verilerini alıyoruz
        sol_aci_verileri = sensor_verisi.ranges[0:40]
        sag_aci_verileri = sensor_verisi.ranges[320:360]
        
        # Ön bölgeyi temsil edecek şekilde listeleri birleştiriyoruz
        on_bolge_taramasi = sol_aci_verileri + sag_aci_verileri
        
        # Sıfır veya geçersiz (örneğin sonsuz) değerleri eliyoruz
        filtreli_mesafe_listesi = []
        for mesafe in on_bolge_taramasi:
            if 0.05 < mesafe < 8.0:
                filtreli_mesafe_listesi.append(mesafe)
        
        # Önümüzdeki en yakın engelin mesafesini buluyoruz
        if filtreli_mesafe_listesi:
            en_yakin_cisim_mesafesi = min(filtreli_mesafe_listesi)
        else:
            en_yakin_cisim_mesafesi = float('inf')
            
        # Reaktif karar mekanizması
        if en_yakin_cisim_mesafesi > self.guvenlik_siniri:
            # Önümüz açık, doğrusal hareket et
            self.hareket_komutlari.linear.x = self.hedef_ileri_hiz
            self.hareket_komutlari.angular.z = 0.0
            rospy.logdebug("Yol temiz. İlerleniyor... En yakın engel: {:.2f}m".format(en_yakin_cisim_mesafesi))
        else:
            # Önümüzde engel var! Dur ve kendi ekseninde dön
            self.hareket_komutlari.linear.x = 0.0
            self.hareket_komutlari.angular.z = self.aci_donus_hizi
            rospy.logwarn("Engel algılandı! Dönüş yapılıyor. Mesafe: {:.2f}m".format(en_yakin_cisim_mesafesi))
            
        # Karar verilen hız değerlerini robota yayınlıyoruz
        self.motor_guc_yayinci.publish(self.hareket_komutlari)

if __name__ == '__main__':
    try:
        # Sınıfı örnekleyerek çalışmayı başlatıyoruz
        kontrolcu = OtonomEngelSavar()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Engel savar düğümü kapatıldı.")
