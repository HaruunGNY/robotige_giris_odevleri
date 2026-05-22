#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from ros_noetic_odev.srv import DikdortgenAlan, DikdortgenAlanResponse

def handle_alani_hesapla(req):
    """
    İstemciden gelen width (en) ve height (boy) değerlerini alıp alanı hesaplar.
    Sonucu (area) geri döndürür.
    """
    alan = req.en * req.boy
    rospy.loginfo("Hesaplama İsteği Alındı -> En: %.2f, Boy: %.2f | Sonuç (Alan): %.2f", req.en, req.boy, alan)
    return DikdortgenAlanResponse(alan)

def dikdortgen_alani_hesapla_sunucu():
    """
    'calculate_rectangle_area' adında bir servis başlatır ve gelen istekleri dinler.
    """
    rospy.init_node('alan_sunucu')
    
    # Servisi tanımlıyoruz
    s = rospy.Service('dikdortgen_alani_hesapla', DikdortgenAlan, handle_alani_hesapla)
    
    rospy.loginfo("Dikdörtgen Alanı Hesaplama Servisi Başlatıldı. İstekler bekleniyor...")
    rospy.spin()

if __name__ == "__main__":
    try:
        dikdortgen_alani_hesapla_sunucu()
    except rospy.ROSInterruptException:
        pass
