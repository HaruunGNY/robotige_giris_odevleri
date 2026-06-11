# 🤖 Final Projesi: Servis Robotu / Çoklu Görev QR Doğrulama

Bu paket, Gazebo simülasyon ortamında TurtleBot3 Waffle robotu ile gerçekleştirilen otonom navigasyon ve kamerayla QR kod doğrulama projesidir.

## 🎬 Proje Tanıtım & Simülasyon Videosu

> [!NOTE]
> Videonun ilk 20-30 saniyesi haritalama (SLAM / Gmapping) sürecini, geri kalan kısmı ise otonom navigasyon ve QR kod doğrulama uygulamasını içermektedir. (Kayıt esnasındaki sıkıştırmadan ötürü video kalitesinde ufak bir düşüş mevcuttur).
GitHub üzerinde doğrudan video oynatılamadığı için, videonun kapak görseline tıklayarak YouTube üzerinden simülasyonu izleyebilirsiniz:

<p align="center">
  <a href="https://youtu.be/FBQJ61vKPPw" target="_blank">
    <img src="https://img.youtube.com/vi/FBQJ61vKPPw/0.jpg" alt="Proje Simülasyon Videosu" width="700" />
  </a>
</p>

---

## 💡 Proje Senaryosu
Robotumuz bir kitapçı/kütüphane ortamında (`AWS Bookstore World`) görev almaktadır. Robotun hedefleri:
1. Ortamın haritasını çıkarmak,
2. Çıkarılan harita üzerinde kendini konumlandırmak (AMCL),
3. Belirlenen görev noktalarına sırasıyla gitmek,
4. Gittiği her noktada bulunan QR kodu kamerasıyla okuyarak doğru yere ulaştığını doğrulamak,
5. Görev durumunu (`SUCCESS`, `SKIPPED`, `FAIL`) raporlamak.

---

## 📂 Paket Yapısı
```text
final_odev/
├── config/
│   └── mission.yaml         # Hedef koordinatları ve beklenen QR verileri
├── launch/
│   ├── gazebo.launch        # Simülasyon dünyasını ve QR modellerini başlatır
│   ├── slam.launch          # SLAM gmapping ve RViz başlatır
│   ├── navigation.launch    # AMCL + move_base başlatır
│   └── task_manager.launch  # QR okuyucu ve Görev Yöneticisini başlatır
├── maps/
│   ├── map.pgm              # Çıkarılan harita dosyası
│   └── map.yaml             # Harita yapılandırma dosyası
├── models/
│   └── qr_.../              # Gazebo için 3D QR kod modelleri (Otomatik üretilir)
├── src/
│   ├── generate_qr_models.py # QR kod modellerini üreten yardımcı kod
│   ├── qr_reader.py         # OpenCV tabanlı QR okuyucu servis düğümü
│   └── task_manager.py      # Ana Durum Makinesi / Görev Yöneticisi düğümü
├── CMakeLists.txt
└── package.xml
```

---

## ⚡ Kurulum ve Çalıştırma Adımları

### 1. Çalışma Alanının (Workspace) Oluşturulması ve Klonlama
Bu paketi ve diğer ödevleri çalıştırmak için öncelikle bir catkin çalışma alanı oluşturup projeyi `src` klasörüne klonlamanız gerekmektedir:

```bash
# Bir catkin çalışma alanı oluşturun ve src klasörüne gidin
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src

# Depoyu klonlayın
git clone https://github.com/HaruunGNY/robotige_giris_odevleri.git
```

### 2. Bağımlılıkların Kurulması
Görüntü işleme ve QR kod çözme işlemleri için OpenCV gereklidir (varsayılan olarak ROS kurulumuyla birlikte gelir).

### 3. Derleme
Çalışma alanının ana dizinine giderek projeyi derleyin ve ortam değişkenlerini yükleyin:

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

---

## 🗺️ Adım 1: Harita Çıkarma (SLAM Gmapping)
Eğer sıfırdan kendi haritanızı çıkarmak istiyorsanız aşağıdaki adımları sırasıyla farklı terminallerde çalıştırın:

**1. Gazebo Simülasyonunu Başlatın:**
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch final_odev gazebo.launch
```

**2. SLAM (Gmapping) Düğümünü Başlatın:**
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch final_odev slam.launch
```

**3. Robotu Teleop ile Gezdirin:**
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
```
*Robotu klavyeden yön tuşlarıyla yavaşça gezdirerek tüm haritayı çıkartın.*

**4. Haritayı Kaydedin:**
Harita netleştiğinde kaydedin (Dosyalar `final_odev/maps` klasörüne kaydedilecektir):
```bash
rosrun map_server map_saver -f $(rospack find final_odev)/maps/map
```

---

## 🚀 Adım 2: Navigasyon ve Çoklu Görev Testi (Otonom Çalıştırma)
Haritanız hazır olduğunda otonom görevi çalıştırmak için aşağıdaki adımları uygulayın:

**1. Simülasyonu Başlatın:**
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch final_odev gazebo.launch
```

**2. Navigasyon (AMCL + move_base) Sistemini Başlatın:**
```bash
export TURTLEBOT3_MODEL=waffle
roslaunch final_odev navigation.launch
```
*RViz ekranında "2D Pose Estimate" butonuna basarak robotun başlangıç konumunu ve yönünü haritada doğru olacak şekilde işaretleyin (lokalize edin).*

**3. Görev Yöneticisini Başlatın:**
```bash
roslaunch final_odev task_manager.launch
```
*Robot sırasıyla hedeflere gidecek, ulaştığında kameradan QR kodları okuyacak ve terminalde canlı durum güncellemeleri yayınlayacaktır.*

---

## 🛠️ ROS Arayüzü Bilgileri

### 📢 Kullanılan Konular (Topics)
*   `/camera/rgb/image_raw` (`sensor_msgs/Image`): Robot kamerasından gelen anlık renkli görüntüyü dinler.
*   `/cmd_vel` (`geometry_msgs/Twist`): Robotun hareket hızlarını yayınlar.

### ⚙️ Sunulan Servisler (Services)
*   `/read_qr` (`std_srvs/Trigger`): Çağrıldığında kameranın son karesini yakalar, OpenCV ile QR kodunu çözer ve `message` alanı içinde veriyi döndürür.

### 🎬 Kullanılan Aksiyonlar (Actions)
*   `move_base` (`move_base_msgs/MoveBaseAction`): Çoklu waypoint hedeflerini otonom olarak göndermek ve robotun ulaşıp ulaşmadığını takip etmek için kullanılır.

---

## 🧠 Durum Akışı ve Hata Yönetimi

### 1. Durum Akışı (State Machine)
*   **INIT:** move_base ve `/read_qr` servislerinin hazır olmasını bekler. `mission.yaml` parametrelerini yükler.
*   **GO_TO_LOCATION:** Sıradaki hedefin x, y, yaw koordinatlarını move_base aksiyonuna gönderir.
*   **QR_VERIFY:** Robot hedefe ulaştığında `/read_qr` servisini çağırır. Okunan değer ile beklenen değer (`qr_expected`) eşleşirse görev başarılı sayılır.
*   **REPORT / NEXT_LOCATION:** Sonuç kaydedilir ve sıradaki hedefe geçilir.
*   **FINISH:** Tüm noktalar bittiğinde başarım tablosunu terminale yazdırır.

### 2. Hata Yönetimi (Error Management)
*   **Move_base Başarısızlığı:** Robot hedefe 90 saniyede ulaşamazsa veya engeller nedeniyle takılırsa, **1 kez daha** hedefe gitmeyi dener. Başarısız olursa o hedef **FAIL** olarak işaretlenir.
*   **QR Okuma Başarısızlığı:** Robot hedefe ulaştığında QR kodunu okuyamazsa veya kameraya tam girmemişse, **2 kez daha** okuma servisini tetikler. Başarısız olunursa hedef **SKIPPED** (Atlandı) olarak işaretlenir.
