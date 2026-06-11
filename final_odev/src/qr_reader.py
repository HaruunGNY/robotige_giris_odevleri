#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KTÜN Robotiğe Giriş - Final Projesi
QR Kod Okuyucu ve Doğrulayıcı Düğümü (qr_reader.py)

Bu düğüm, robotun kamerasından gelen görüntüleri (/camera/rgb/image_raw) dinler.
Task Manager'dan gelen tetikleme (Service Call) ile o anki görüntü üzerinde 
OpenCV QRCodeDetector kullanarak QR kodu tarar ve içeriğini döndürür.
"""

import rospy
import cv2
import os
from sensor_msgs.msg import Image
from std_srvs.srv import Trigger, TriggerResponse
from cv_bridge import CvBridge, CvBridgeError

try:
    from pyzbar import pyzbar
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

class QrReaderNode:
    def __init__(self):
        rospy.init_node("qr_reader_node", anonymous=False)
        
        self.bridge = CvBridge()
        self.latest_image = None
        self.detector = cv2.QRCodeDetector()
        
        # Kamera konusuna abone oluyoruz
        # TurtleBot3 Waffle kamerasının renkli görüntü konusu: /camera/rgb/image_raw
        self.image_sub = rospy.Subscriber(
            "/camera/rgb/image_raw", 
            Image, 
            self.image_callback
        )
        
        # QR okumayı tetiklemek için bir servis sunuyoruz
        self.service = rospy.Service(
            "/read_qr", 
            Trigger, 
            self.handle_read_qr
        )
        
        if PYZBAR_AVAILABLE:
            rospy.loginfo("[QR Reader] Düğüm pyzbar kütüphanesi ile başlatıldı. Görüntü bekleniyor...")
        else:
            rospy.logwarn("[QR Reader] pyzbar kütüphanesi yüklü değil! OpenCV kullanılacak (QUIRC hatası verebilir). "
                          "Yüklemek için: sudo apt-get install python3-pyzbar")

    def image_callback(self, msg):
        try:
            # ROS Image mesajını OpenCV formatına dönüştürüyoruz
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr("[QR Reader] CvBridge hatası: %s", str(e))

    def handle_read_qr(self, req):
        response = TriggerResponse()
        
        if self.latest_image is None:
            response.success = False
            response.message = "KAMERA_GORUNTUSU_YOK"
            rospy.logwarn("[QR Reader] Hata: Henüz kameradan bir görüntü alınamadı.")
            return response
            
        # Görüntüyü gri tonlamaya çevirerek QR dedektörün başarımını arttırıyoruz
        gray_img = cv2.cvtColor(self.latest_image, cv2.COLOR_BGR2GRAY)
        
        # Hata ayıklama için kameranın gördüğü resmi kaydedelim
        debug_path = os.path.join(
            os.path.dirname(__file__), "..", "debug_cam.png"
        )
        cv2.imwrite(debug_path, self.latest_image)
        rospy.loginfo(f"[QR Reader] Kamera görüntüsü hata ayıklama için kaydedildi: {debug_path}")
        
        # QR Kodunu algıla ve çöz
        data = None
        if PYZBAR_AVAILABLE:
            rospy.loginfo("[QR Reader] QR kodu pyzbar ile çözülüyor...")
            barcodes = pyzbar.decode(gray_img)
            for barcode in barcodes:
                if barcode.type == 'QRCODE':
                    data = barcode.data.decode("utf-8")
                    break
        else:
            rospy.logwarn("[QR Reader] pyzbar yüklü değil, OpenCV ile çözülüyor...")
            data, bbox, rectified_image = self.detector.detectAndDecode(gray_img)
        
        if data:
            response.success = True
            response.message = data
            rospy.loginfo("[QR Reader] QR Kod başarıyla okundu: %s", data)
        else:
            response.success = False
            response.message = "QR_OKUNAMADI"
            rospy.logwarn("[QR Reader] Görüntüde geçerli bir QR kod algılanamadı.")
            
        return response

if __name__ == "__main__":
    try:
        node = QrReaderNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("[QR Reader] Düğüm durduruluyor.")
