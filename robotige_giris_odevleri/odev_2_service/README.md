# Ödev 2: Dikdörtgen Alanı Hesaplama Servisi (Python)

Bu paket, istemcinin (Client) Terminal aracılığıyla gönderdiği En (`en`) ve Boy (`boy`) parametrelerini alarak, dikdörtgenin alanını (`alan`) hesaplayan ve istemciye sonucu geri döndüren bir ROS **Service** uygulaması içerir. Özel servis dosyası (`DikdortgenAlan.srv`) kullanılmıştır.

## 🚀 Nasıl Çalıştırılır ve Test Edilir?

Aşağıdaki komutları sırasıyla ayrı terminal sekmelerinde çalıştırın:

1. ROS Çekirdeğini (Master) Başlatın:
```bash
roscore
```

2. Alan Hesaplayıcı Server'ı Çalıştırın:
```bash
rosrun odev_2_service alan_sunucu.py
```

3. Client'ı çalıştırıp test edin (Ör: En=5.2, Boy=10.0):
```bash
rosrun odev_2_service alan_istemci.py 5.2 10.0
```

Alternatif Test (rosservice call ile):
```bash
rosservice call /dikdortgen_alani_hesapla "en: 5.2
boy: 10.0"
```
