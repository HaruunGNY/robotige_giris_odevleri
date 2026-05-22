#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Robotiğe Giriş Dersi - Ödev 5: PID Denetleyici ile Mesafe Kontrolü
Bu düğüm, robotun önündeki duvara tam olarak belirlenen mesafede pürüzsüz
ve sarsıntısız bir şekilde durmasını sağlamak için PID kontrol algoritmasını kullanır.
"""

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class OtonomPidMesafeDenetleyici:
    def __init__(self):
        # Düğümü özgün bir isimle başlatıyoruz
        rospy.init_node('duvar_mesafe_pid_dugumu', anonymous=True)
        
        # Hız komutlarını yayınlayacak Publisher nesnesi
        self.hiz_komut_yayici = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Lidar sensörünü dinleyeceğimiz Subscriber nesnesi
        self.lazer_sensor_abonesi = rospy.Subscriber('/scan', LaserScan, self.lazer_veri_isleme)
        
        # PID Kazanç Katsayıları (P, I, D)
        # Kp: Oransal katsayı - Hata ile doğru orantılı tepki verir
        # Ki: İntegral katsayısı - Zamanla biriken kalıcı hatayı sıfırlar
        # Kd: Türevsel katsayı - Hatanın değişim hızına bakarak salınımı sönümler
        self.Kp = 0.50
        self.Ki = 0.01
        self.Kd = 0.10
        
        # Çalışma Parametreleri
        self.istenen_guvenli_mesafe = 0.35    # Robotun durması istenen hedef mesafe (metre)
        self.olculen_aktif_mesafe = 0.0       # Sensörden okunan anlık mesafe
        self.veri_akisi_hazir = False          # Lidar verisi gelip gelmediğini kontrol eden bayrak
        
        # PID Durum Değişkenleri
        self.gecmis_hata_degeri = 0.0
        self.integral_toplama_haznesi = 0.0
        
        # Döngü Hızı (10 Hz = 0.1 saniye aralıklarla çalışır)
        self.rate = rospy.Rate(10)
        self.dongu_kilitli = False
        
        rospy.loginfo("==============================================")
        rospy.loginfo("PID Mesafe Denetleyicisi Hazır Hale Getirildi.")
        rospy.loginfo("İstenen Hedef Mesafe: {} metre".format(self.istenen_guvenli_mesafe))
        rospy.loginfo("==============================================")

    def lazer_veri_isleme(self, veri):
        """
        Lidar verilerini işleyen callback. Sadece tam ön cephedeki (dar bir açı olan 10 derecelik alan)
        mesafeleri filtreleyerek en yakın mesafeyi belirler.
        """
        # Robotun tam önündeki 10 derecelik koniyi tarıyoruz
        on_cephe_konisi = veri.ranges[0:5] + veri.ranges[355:360]
        
        # Geçersiz ölçümleri filtreliyoruz
        temiz_veriler = []
        for m in on_cephe_konisi:
            if 0.05 < m < 8.0:
                temiz_veriler.append(m)
                
        if temiz_veriler:
            self.olculen_aktif_mesafe = min(temiz_veriler)
            self.veri_akisi_hazir = True

    def kontrol_dongusu(self):
        """
        PID hesaplamalarını yapan ve motor hızlarını kontrol eden ana döngü.
        """
        cmd_hiz_paket = Twist()
        dt_zaman = 0.1         # 10 Hz çalışma hızı için zaman adımı (saniye)
        hata_toleransi = 0.02   # +- 2 cm tolerans (deadband) aralığı
        
        while not rospy.is_shutdown():
            # Eğer hedefe ulaşıldı ve sistem kilitlendi ise hız vermeyi durdur
            if self.dongu_kilitli:
                self.rate.sleep()
                continue
                
            if self.veri_akisi_hazir:
                # Anlık hata (Sapma) hesaplanır
                anlik_sapma = self.olculen_aktif_mesafe - self.istenen_guvenli_mesafe
                
                # Tolerans aralığına girildi mi kontrol edilir
                if abs(anlik_sapma) < hata_toleransi:
                    cmd_hiz_paket.linear.x = 0.0
                    cmd_hiz_paket.angular.z = 0.0
                    self.hiz_komut_yayici.publish(cmd_hiz_paket)
                    
                    rospy.loginfo("--------------------------------------------------")
                    rospy.loginfo("HEDEF MESAFEYE ULAŞILDI! Mevcut Uzaklık: {:.3f}m".format(self.olculen_aktif_mesafe))
                    rospy.loginfo("PID Görevi Başarıyla Tamamlandı. Sistem Kilitlendi.")
                    rospy.loginfo("--------------------------------------------------")
                    
                    self.dongu_kilitli = True
                else:
                    # ORANSAL BİLEŞEN (Proportional)
                    P_tepki = self.Kp * anlik_sapma
                    
                    # İNTEGRAL BİLEŞEN (Integral)
                    self.integral_toplama_haznesi += anlik_sapma * dt_zaman
                    I_tepki = self.Ki * self.integral_toplama_haznesi
                    
                    # TÜREVSEL BİLEŞEN (Derivative)
                    hata_degisimi = (anlik_sapma - self.gecmis_hata_degeri) / dt_zaman
                    D_tepki = self.Kd * hata_degisimi
                    
                    # Toplam Kontrol Çıktısı
                    hesaplanan_hiz = P_tepki + I_tepki + D_tepki
                    
                    # Robotun fiziksel limitleri aşmaması için hızı sınırlandırıyoruz (Satürasyon)
                    # Waffle modeli için maksimum güvenli doğrusal hız 0.22 m/s civarındadır
                    hesaplanan_hiz = max(min(hesaplanan_hiz, 0.20), -0.20)
                    
                    # Robot hareket komutunu doldur
                    cmd_hiz_paket.linear.x = hesaplanan_hiz
                    cmd_hiz_paket.angular.z = 0.0
                    self.hiz_komut_yayici.publish(cmd_hiz_paket)
                    
                    # Geçmiş hatayı güncelle
                    self.gecmis_hata_degeri = anlik_sapma
                    
                    rospy.loginfo("Aktif Mesafe: {:.3f}m | Hata: {:.3f}m | Çıkış Hızı: {:.3f} m/s".format(
                        self.olculen_aktif_mesafe, anlik_sapma, hesaplanan_hiz
                    ))
                    
            self.rate.sleep()

if __name__ == '__main__':
    try:
        # Sınıfı örnekleyip denetleyiciyi aktif ediyoruz
        denetleyici = OtonomPidMesafeDenetleyici()
        denetleyici.kontrol_dongusu()
    except rospy.ROSInterruptException:
        rospy.loginfo("PID kontrol düğümü sonlandırıldı.")
