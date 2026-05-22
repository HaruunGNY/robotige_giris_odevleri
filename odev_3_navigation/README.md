# 🗺️ Ödev 3: Turtlebot3 5 Noktaya Otonom Navigasyon

Bu paket, bir mobil robotun önceden çıkarılmış bir harita üzerinde engellerden kaçarak otonom olarak belirlenen hedeflere gitmesini sağlayan **Action Client (Eylem İstemcisi)** yapısını öğrenmek amacıyla geliştirilmiştir.

---

## 💡 Başlangıç Seviyesi Teorik Anlatım

### 1. ROS Action (Eylem) Nedir ve Servisten Farkı Nedir?
ROS Servisleri (Ödev 2) hızlı matematik işlemleri için çok iyidir. Ancak robotun bir noktadan diğerine gitmesi gibi **uzun süren işlerde** servis kullanmak iyi bir fikir değildir. Çünkü servis çağrıldığında robot gidene kadar sistem kilitlenir ve geri bildirim alınamaz.

Bunun yerine **Action (Eylem)** mimarisi kullanılır:
*   **Uzun Süren Görevler:** Robotun otonom hareket etmesi gibi dakikalar sürebilecek görevler için tasarlanmıştır.
*   **Geri Bildirim (Feedback):** Robot hedefe giderken anlık konum veya kalan mesafe gibi bilgileri sürekli bildirir.
*   **İptal Edilebilirlik (Preempt):** Robot hedefe giderken yolda acil bir durum olursa görev yarıda kesilip yeni bir hedef gönderilebilir.

### 2. `move_base` ve Navigasyon Yığını (Navigation Stack)
`move_base` düğümü, ROS'ta otonom sürüşün kalbidir. Robotun sensör verilerini ve haritasını alarak:
1.  **Global Planlama:** Haritada hedefe giden en kısa ve güvenli yolu çizer.
2.  **Lokal Planlama:** Robot yolda giderken önüne anlık çıkan engelleri (örn: yürüyen bir insan) sensörüyle fark edip etrafından dolaşacak anlık manevralar üretir.

---

## 🔍 Bu Ödevde Ne Yapılıyor?

1.  **Harita Yükleme:** `map.yaml` dosyası ile Gazebo dünyasının 2D ızgara haritası yüklenir.
2.  **Hedef Düğümü (`5_nokta.py`):** 
    - Kod içerisinde 5 farklı X, Y ve dönüş açısı (W) koordinatı tanımlanmıştır.
    - Python scriptimiz `move_base` action sunucusuna ilk hedefi gönderir ve robotun oraya varmasını bekler.
    - Robot 1. hedefe ulaştığında 1 saniye bekler ve sırasıyla 2., 3., 4. ve 5. hedeflere otonom olarak yönlenir.

---

## 🚀 Kurulum ve Çalıştırma

Projeyi çalıştırmak için sırasıyla aşağıdaki adımları izleyin. Her bir komutu **yeni bir terminal sekmesinde** çalıştırmanız gerekmektedir.

### 1. Gazebo Simülasyonunu Başlatın
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

### 2. Navigasyon ve Harita Sistemini Başlatın
Simülasyon açıldıktan sonra, navigasyon düğümlerini ve daha önceden çıkardığınız haritayı (`map.yaml`) sisteme yüklemek için:
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$(rospack find odev_3_navigation)/maps/map.yaml
```

> [!NOTE]
> *RViz ekranı açıldığında robotun konumu yanlış görünüyorsa, üst menüdeki **"2D Pose Estimate"** aracına tıklayıp haritada robotun bulunduğu yeri ve baktığı yönü sürükleyerek manuel olarak eşleştirin.*

### 3. Otonom Navigasyon Python Scriptini Çalıştırın
Navigasyon hazır olduktan sonra robotu 5 hedefe sırayla gönderecek betiği başlatın:
```bash
rosrun odev_3_navigation 5_nokta.py
```
