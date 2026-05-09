#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import rospy
from ros_noetic_odev.srv import DikdortgenAlan, DikdortgenAlanRequest

def alan_hesapla_istemci(en, boy):
    """
    Server'a bağlanarak verilen en ve boy değerleri için alan hesaplaması talep eder.
    """
    # Servisin aktif olmasını bekliyoruz
    rospy.wait_for_service('dikdortgen_alani_hesapla')
    
    try:
        # Servise bağlanmak için bir proxy (aracı) oluşturuyoruz
        alan_hesapla = rospy.ServiceProxy('dikdortgen_alani_hesapla', DikdortgenAlan)
        
        # İsteği gönderip cevabı alıyoruz
        cevap = alan_hesapla(en, boy)
        return cevap.alan
        
    except rospy.ServiceException as e:
        rospy.logerr("Servis çağrısı başarısız oldu: %s", e)

if __name__ == "__main__":
    # Komut satırından 2 argüman (width ve height) gelmesini bekliyoruz
    if len(sys.argv) == 3:
        try:
            w = float(sys.argv[1])
            h = float(sys.argv[2])
        except ValueError:
            print("Lütfen sayısal değerler girin! Örnek kullanım: rosrun ros_noetic_odev alan_istemci.py 5.2 10.0")
            sys.exit(1)
    else:
        print("Hatalı parametre sayısı!")
        print("Kullanım: rosrun ros_noetic_odev alan_istemci.py <en> <boy>")
        print("Örnek: rosrun ros_noetic_odev alan_istemci.py 5.2 10.0")
        sys.exit(1)
        
    # ROS Düğümünü client olarak başlatıyoruz
    rospy.init_node('alan_istemci', anonymous=True)
    
    print("İstek gönderiliyor: En={}, Boy={}".format(w, h))
    hesaplanan_alan = alan_hesapla_istemci(w, h)
    
    # Sonucu ekrana yazdırıyoruz
    if hesaplanan_alan is not None:
        print("Sunucudan Gelen Sonuç (Alan): {:.2f}".format(hesaplanan_alan))
