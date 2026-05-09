# Ödev 3: Turtlebot3 5 Noktaya Otonom Navigasyon

Bu proje, Turtlebot3'ü Gazebo simülasyon ortamında, daha önceden kaydedilmiş bir harita üzerinde belirlenen 5 farklı noktaya otonom olarak gönderen bir ROS uygulamasıdır.

## Kurulum ve Çalıştırma

Projeyi çalıştırmak için sırasıyla aşağıdaki adımları izleyin. Her bir komutu **yeni bir terminal sekmesinde** çalıştırmanız gerekmektedir.

### 1. Gazebo Simülasyonunu Başlatma
```bash
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

### 2. Navigasyonu ve Haritayı Başlatma
Simülasyon açıldıktan sonra, navigasyon düğümlerini ve daha önceden çıkardığınız haritayı (`map.yaml`) sisteme yüklemek için:
```bash
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$(rospack find odev_3_navigation)/maps/map.yaml
```

*Not: RViz açıldığında robotun konumu yanlış görünüyorsa, üst menüdeki "2D Pose Estimate" aracını kullanarak robotun haritadaki ilk konumunu manuel olarak belirlemeniz gerekebilir.*

### 3. Robotu 5 Noktaya Gönderme (Python Scripti)
Navigasyon hazır olduktan sonra Python scriptini çalıştırın:
```bash
rosrun odev_3_navigation 5_nokta.py
```
