# Ödev 1: Turtlesim Konum Dinleyici ve Hareket Yönetimi (Python)

Bu paket, ROS (Robot Operating System) eğitimleri kapsamında verilmiş Turtlesim Konum Okuma (Subscriber) ve Hareket Kontrol (Publisher) ödevini içermektedir. Turtlesim simülasyonundaki kaplumbağanın `/turtle1/pose` konusundan (topic) anlık konum verisi saniyede bir kez ekrana yazdırılmakta, aynı anda `/turtle1/cmd_vel` konusu üzerinden aralıksız hız komutları gönderilerek kaplumbağa hareket ettirilmektedir.

## 🚀 Nasıl Çalıştırılır?

Aşağıdaki komutları sırasıyla ayrı terminal sekmelerinde çalıştırın:

1. ROS çekirdeğini başlatın:
```bash
roscore
```

2. Turtlesim simülasyonunu başlatın:
```bash
rosrun turtlesim turtlesim_node
```

3. Yönetici Python düğümünü başlatın:
```bash
rosrun odev_1_turtlesim kaplumbaga_takip_ve_hareket.py
```
