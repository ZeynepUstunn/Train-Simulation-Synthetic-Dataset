# 🤖 Otonom Sentetik Veri Seti Üretimi (BlenderProc)

Manual render ve etiketleme (labeling) süreçlerini otonomlaştırmak, veri çeşitliliğini artırmak ve model eğitimini hızlandırmak amacıyla **BlenderProc** kütüphanesi yapılandırmasına geçilmiştir.

---

### 🎯 Amaç ve Hedefler
* **Otonom Veri Üretimi:** Manuel sahne düzenleme ve render bekleme süreçleri yerine Python betikleri (scripts) üzerinden binlerce farklı konfigürasyonda görsel üretmek.
* **Görsel Çeşitlilik (Data Augmentation):** Kameranın konumunu, ışık açılarını, şiddetini ve materyal özelliklerini her karede rastgele (randomized) değiştirerek modelin ezber yapmasını (*overfitting*) engellemek.
* **Otomatik Etiketleme (Auto-Annotation):** Render esnasında sahnede bulunan anomali objelerinin 2D ve 3D sınır kutusu (Bounding Box) koordinatlarını doğrudan YOLO / COCO formatında (`.txt` / `.json`) otomatik üretmek.

---

### ⚙️ Çalışma Mantığı ve Pipeline
BlenderProc mimarisi 5 temel aşamadan oluşmaktadır:

1. **İlklendirme (`Init`):** BlenderProc çalışma ortamının başlatılması.
2. **Sahne / Obje Yükleme (`Load`):** Hazırlanan `.blend` sahnelerinin veya anomali modellerinin ortama dinamik dahil edilmesi.
3. **Parametre Rastgeleleştirme (`Randomize / Pose`):**
   * Kamera yörüngelerinin ve bakış açılarının rastgele ayarlanması.
   * Güneş ışığı açısı, ortam aydınlatması ve gölge sertliklerinin değiştirilmesi.
   * Anomali nesnelerinin ray üzerindeki konumlarının varyasyonlandırılması.
4. **Otonom Render (`Render`):** Arka planda Cycles / Eevee motorları kullanılarak görüntülerin işlenmesi.
5. **Dışa Aktarım (`Export`):** Sentetik görsellerin ve bunlara ait otomatik etiket dosyalarının diske yazılması.

---

### 🚀 Başlangıç ve Kurulum

Kütüphaneyi yerel ortama kurmak için:

```bash
pip install blenderproc
