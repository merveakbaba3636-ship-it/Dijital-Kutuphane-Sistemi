# 📚 LibraryOS v3.0 - Profesyonel Kütüphane Yönetim Sistemi

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

Modern ve kullanıcı dostu arayüzü ile kütüphane yönetimini kolaylaştıran, PyQt5 tabanlı profesyonel bir masaüstü uygulaması.

![LibraryOS Screenshot](screenshot.png)

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Sistem Gereksinimleri](#-sistem-gereksinimleri)
- [Kurulum](#-kurulum)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kullanım Kılavuzu](#-kullanım-kılavuzu)
- [Proje Yapısı](#-proje-yapısı)
- [Varsayılan Hesaplar](#-varsayılan-hesaplar)
- [Veritabanı](#-veritabanı)
- [Export İşlemleri](#-export-i̇şlemleri)
- [Sık Sorulan Sorular](#-sık-sorulan-sorular)
- [Geliştirici Notları](#-geliştirici-notları)
- [Lisans](#-lisans)

---

## ✨ Özellikler

### 📊 Dashboard
- Gerçek zamanlı KPI kartları (toplam kitap, mevcut kitap, ödünç kitap, üye sayısı)
- Gecikmiş iade ve toplam ceza takibi
- Otomatik yenilenen istatistikler (30 saniye)
- Hızlı arama ve filtreleme

### 📚 Kitap Yönetimi
- Kitap ekleme, güncelleme ve silme
- ISBN doğrulama (ISBN-10 ve ISBN-13)
- Kategori bazlı sınıflandırma
- Stok takibi (toplam/ödünç/mevcut)
- Detaylı kitap arama

### 👥 Üye Yönetimi
- Üye kayıt, güncelleme ve silme
- Email ve telefon doğrulama
- Aktif ödünç takibi (max 3 kitap limiti)
- Ceza bakiyesi yönetimi
- Ödünç geçmişi görüntüleme

### 🔄 Ödünç İşlemleri
- Kolay ödünç verme ve iade alma
- Otomatik ceza hesaplama (günlük 5 TL)
- 15 gün standart ödünç süresi
- Gecikme uyarıları ve renkli göstergeler
- Detaylı işlem logları

### 📝 Raporlama
- CSV, PDF ve Excel export desteği
- Tarih aralığı ve durum filtreleme
- Detaylı ödünç geçmişi raporları
- İstatistiksel veri analizi

### 🔐 Güvenlik
- SHA-256 şifreleme ile güvenli giriş
- Rol tabanlı yetkilendirme (Admin/Kütüphaneci)
- Kullanıcı kaydı ve yönetimi
- Sistem logları ve aktivite takibi

### 🎨 Arayüz
- Modern Dark tema
- Responsive tasarım
- Sidebar navigasyon
- Animasyonlu hover efektleri
- Gölge ve gradient destekli kartlar

---

## 💻 Sistem Gereksinimleri

| Bileşen | Minimum |
|---------|---------|
| **Python** | 3.8 veya üzeri |
| **RAM** | 512 MB |
| **Disk** | 100 MB boş alan |
| **İşletim Sistemi** | Windows 7+, Linux, macOS 10.14+ |
| **Ekran Çözünürlüğü** | 1366x768 veya üzeri |

---

## 🚀 Kurulum

### Adım 1: Depoyu Klonlayın
```bash
git clone https://github.com/kullanici/libraryos.git
cd libraryos
```

### Adım 2: Sanal Ortam Oluşturun (Önerilir)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

Gereken paketler:
- **PyQt5** (5.15.10): GUI framework
- **reportlab** (4.0.9): PDF export
- **Pillow** (10.2.0): Görüntü işleme
- **qrcode** (7.4.2): QR kod oluşturma

### Adım 4: Uygulamayı Başlatın
```bash
python main.py
```

---

## 🎯 Hızlı Başlangıç

### İlk Çalıştırma
1. Uygulamayı başlattığınızda otomatik olarak:
   - Gerekli klasörler oluşturulur (`data/`, `logs/`, `exports/`, `backups/`)
   - SQLite veritabanı başlatılır
   - Varsayılan admin hesapları oluşturulur
   - Demo kitaplar, üyeler ve ödünç kayıtları yüklenir

2. Giriş ekranında varsayılan bilgileri kullanın:
   - **Kullanıcı Adı:** `admin`
   - **Şifre:** `admin123`

3. Dashboard'a yönlendirileceksiniz. Buradan tüm özelliklere erişebilirsiniz.

### Temel İşlemler

| İşlem | Yol |
|-------|-----|
| Kitap Ekleme | Kitap Yönetimi → Kitap Ekle |
| Üye Kaydı | Üye Yönetimi → Üye Ekle |
| Ödünç Verme | Ödünç İşlemleri → Ödünç Ver |
| İade Alma | Ödünç İşlemleri → İade Al |
| Rapor Alma | İşlem Geçmişi → CSV/PDF Export |

---

## 📖 Kullanım Kılavuzu

### 1. Giriş Ekranı
![Login](docs/login.png)
- Kayıtlı kullanıcı bilgilerinizle giriş yapın
- "Hesabınız yok mu?" ile yeni kayıt oluşturabilirsiniz
- Çıkış butonu ile uygulamayı kapatabilirsiniz

### 2. Dashboard
- **KPI Kartları:** Anlık istatistikleri gösterir
- **Kitap Listesi:** Tüm kitapları tablo halinde listeler
- **Arama Çubuğu:** Kitap adı, yazar veya kategoriye göre filtreleme
- **Otomatik Yenileme:** 30 saniyede bir güncellenir

### 3. Kitap İşlemleri
```
Kitap Ekle:
├── ID: Otomatik veya manuel
├── Kitap Adı (Zorunlu)
├── Yazar (Zorunlu)
├── Kategori (Açılır liste + özel giriş)
├── ISBN (Opsiyonel, otomatik doğrulama)
├── Yayın Yılı
└── Stok Adedi
```

### 4. Üye İşlemleri
```
Üye Kaydı:
├── ID: Otomatik veya manuel
├── Ad Soyad (Zorunlu)
├── E-Mail (Zorunlu, format kontrolü)
└── Telefon (Opsiyonel)
```

### 5. Ödünç İşlemleri
- **Ödünç Verme:** Kitap ID ve Üye ID girilerek
- **İade Alma:** Kitap ID ile otomatik işlem
- **Ceza Sistemi:** Gecikme başına günlük 5 TL
- **Limit Kontrolü:** Üye başına max 3 aktif ödünç

### 6. Raporlama
- Tarih aralığı filtreleme
- Durum filtresi (Tümü/Aktif/İade/Gecikmiş)
- Metin araması
- CSV, PDF, Excel export seçenekleri

---

## 📁 Proje Yapısı

```
libraryos/
│
├── main.py                 # Ana çalıştırıcı
├── requirements.txt        # Python bağımlılıkları
├── README.md              # Proje dokümantasyonu
│
├── backend/
│   ├── database.py        # SQLite veritabanı yönetimi
│   ├── models.py          # Veri modelleri (Kitap, Üye, Ödünç)
│   └── utils.py           # Yardımcı fonksiyonlar
│
├── gui/
│   ├── styles.py          # UI tema ve stil tanımlamaları
│   ├── login.py           # Giriş ekranı
│   ├── main_window.py     # Ana pencere ve navigasyon
│   ├── dashboard.py       # Dashboard sayfası
│   ├── islemler.py        # Kitap/Üye/Ödünç işlemleri
│   └── gecmis.py          # İşlem geçmişi ve raporlama
│
├── data/                  # SQLite veritabanı
│   └── library.db
│
├── logs/                  # Sistem logları
│   └── library.log
│
├── exports/               # Dışa aktarma dosyaları
│   ├── csv/
│   ├── pdf/
│   └── excel/
│
└── backups/              # Veritabanı yedekleri
```

---

## 👤 Varsayılan Hesaplar

| Kullanıcı Adı | Şifre | Rol | Açıklama |
|--------------|-------|-----|----------|
| `admin` | `admin123` | Admin | Tam yetkili yönetici |
| `kutuphaneci` | `kutuphaneci123` | Kütüphaneci | Standart kullanıcı |

> ⚠️ **Güvenlik Uyarısı:** İlk girişten sonra varsayılan şifreleri değiştirmeniz önerilir!

---

## 🗄️ Veritabanı

### Tablo Yapısı

```sql
-- Kitaplar
kitaplar(id, ad, yazar, kategori, isbn, yayin_yili, 
         toplam_adet, odunc_adet, eklenme_tarihi)

-- Üyeler
uyeler(id, ad, email, telefon, aktif_odunc, 
       toplam_odunc, ceza_bakiyesi, kayit_tarihi)

-- Ödünç İşlemleri
oduncler(id, kitap_id, uye_id, odunc_tarihi, 
         beklenen_iade, iade_tarihi, ceza_tutari, odendi)

-- Admin Hesapları
adminler(id, kullanici_adi, sifre_hash, ad, email, rol, son_giris)

-- Sistem Logları
sistem_loglari(id, islem_tipi, aciklama, kullanici, tarih)
```

### Yedekleme
```python
# Manuel yedek alma
from backend.database import DatabaseManager
db = DatabaseManager()
db.backup_database()  # backups/library_backup_YYYYMMDD_HHMMSS.db
```

---

## 📤 Export İşlemleri

### Desteklenen Formatlar
- **CSV:** UTF-8 BOM ile Türkçe karakter desteği
- **PDF:** reportlab ile profesyonel raporlar
- **Excel:** openpyxl ile formatlı çıktı

### Export Klasörleri
```
exports/
├── csv/    # CSV dosyaları
├── pdf/    # PDF raporları
└── excel/  # Excel dosyaları
```

---

## ❓ Sık Sorulan Sorular

<details>
<summary><b>Program başlamıyor, ne yapmalıyım?</b></summary>

1. Python sürümünüzü kontrol edin: `python --version`
2. Bağımlılıkları yeniden yükleyin: `pip install -r requirements.txt --force-reinstall`
3. Log dosyasını kontrol edin: `logs/library.log`
</details>

<details>
<summary><b>Veritabanı nerede saklanıyor?</b></summary>

SQLite veritabanı `data/library.db` dosyasında saklanır. Bu dosyayı yedekleyerek tüm verilerinizi taşıyabilirsiniz.
</details>

<details>
<summary><b>Şifremi unuttum, ne yapabilirim?</b></summary>

1. `data/library.db` dosyasını silin
2. Programı yeniden başlatın (varsayılan hesaplar yeniden oluşturulur)
3. Veya veritabanı yöneticisi ile şifre hash'ini sıfırlayın
</details>

<details>
<summary><b>Ceza sistemi nasıl çalışıyor?</b></summary>

- Standart ödünç süresi: 15 gün
- Gecikme cezası: Günlük 5 TL
- Ceza iade sırasında otomatik hesaplanır
- Üyenin ceza bakiyesine eklenir
</details>

<details>
<summary><b>Kaç kitap ödünç verilebilir?</b></summary>

Her üye aynı anda maksimum 3 kitap ödünç alabilir. Bu limit `models.py` dosyasındaki `Odunc` sınıfında değiştirilebilir.
</details>

---

## 🔧 Geliştirici Notları

### Kod Standartları
- **Dil:** Python 3.8+
- **GUI:** PyQt5
- **Veritabanı:** SQLite3 (WAL mod)
- **Mimari:** MVC (Model-View-Controller)
- **Threading:** Thread-safe veritabanı işlemleri
- **Logging:** Dosya tabanlı log sistemi

### Katkıda Bulunma
1. Bu depoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

### Özelleştirme
- **Tema:** `gui/styles.py` dosyasından Dark/Light tema değiştirilebilir
- **Ceza:** `backend/models.py` içinde `GUNLUK_CEZA` değiştirilebilir
- **Süre:** `STANDART_SURE` değişkeni ile ödünç süresi ayarlanabilir
- **Limit:** Üye başına kitap limiti `odunc_al()` metodunda değiştirilebilir

### Bilinen Sorunlar
- PDF export için reportlab kütüphanesi gereklidir
- Yüksek DPI ekranlarda ölçekleme sorunları olabilir
- CSV import özelliği henüz eklenmemiştir
