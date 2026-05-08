"""
LibraryOS v3.0 - Profesyonel Kütüphane Yönetim Sistemi
Ana Çalıştırıcı

Kullanım: python main.py
Varsayılan Giriş: admin / admin123
"""

import sys
import os
import hashlib
from datetime import date, timedelta

# Proje kök dizinini Python path'ine ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QBrush

from backend.database import DatabaseManager
from backend.models import Admin
from backend.utils import FileManager
from gui.main_window import MainWindow
from gui.login import LoginDialog
from gui.styles import Theme


class KutuphaneSistemi:
    """
    Ana Sistem Kontrolcüsü
    - Veritabanı yönetimi
    - Demo veri oluşturma
    - Giriş kontrolü
    """
    
    def __init__(self):
        """Sistemi başlat"""
        print("=" * 60)
        print("  📚 LibraryOS v3.0 - Professional Edition")
        print("=" * 60)
        
        # 1. Gerekli klasörleri oluştur/kontrol et
        self._setup_directories()
        
        # 2. Veritabanını başlat
        print("\n⏳ Veritabanı başlatılıyor...")
        self.db = DatabaseManager()
        print("✅ Veritabanı hazır!")
        
        # 3. Admin hesabı oluştur (yoksa)
        self._create_default_admin()
        
        # 4. Demo verileri yükle (boşsa)
        self._load_demo_data()
        
        # 5. İstatistikleri göster
        self._show_stats()
        
        print("\n✅ Sistem kullanıma hazır!")
        print("=" * 60)
    
    def _setup_directories(self):
        """Gerekli klasörleri oluştur"""
        created = FileManager.ensure_directories()
        if created:
            print("\n📁 Yeni klasörler oluşturuldu:")
            for d in created:
                print(f"   ✓ {d}/")
    
    def _create_default_admin(self):
        """Varsayılan admin hesabını oluştur"""
        adminler = self.db.execute_query("SELECT COUNT(*) as count FROM adminler")
        
        if adminler[0]['count'] == 0:
            print("\n👤 Varsayılan admin hesabı oluşturuluyor...")
            
            sifre_hash = hashlib.sha256("admin123".encode()).hexdigest()
            
            self.db.execute_update(
                """INSERT INTO adminler (kullanici_adi, sifre_hash, ad, email, rol)
                   VALUES (?, ?, ?, ?, ?)""",
                ("admin", sifre_hash, "Sistem Yöneticisi", "admin@library.com", "admin")
            )
            
            # Ek kullanıcılar
            self.db.execute_update(
                """INSERT INTO adminler (kullanici_adi, sifre_hash, ad, email, rol)
                   VALUES (?, ?, ?, ?, ?)""",
                ("kutuphaneci", hashlib.sha256("kutuphaneci123".encode()).hexdigest(),
                 "Ahmet Kütüphaneci", "ahmet@library.com", "kutuphaneci")
            )
            
            self.db.add_log("Sistem", "Varsayılan admin hesapları oluşturuldu")
            print("✅ Admin hesapları oluşturuldu!")
            print("   🔑 admin / admin123 (Yönetici)")
            print("   🔑 kutuphaneci / kutuphaneci123 (Kütüphaneci)")
    
    def _load_demo_data(self):
        """Demo verileri yükle (veritabanı boşsa)"""
        kitap_sayisi = self.db.execute_query("SELECT COUNT(*) as count FROM kitaplar")[0]['count']
        uye_sayisi = self.db.execute_query("SELECT COUNT(*) as count FROM uyeler")[0]['count']
        
        if kitap_sayisi == 0 and uye_sayisi == 0:
            print("\n📚 Demo veriler yükleniyor...")
            self._create_demo_kitaplar()
            self._create_demo_uyeler()
            self._create_demo_oduncler()
            self.db.add_log("Sistem", "Demo veriler yüklendi")
            print("✅ Demo veriler yüklendi!")
    
    def _create_demo_kitaplar(self):
        """Demo kitapları ekle"""
        kitaplar = [
            (1, "Suç ve Ceza", "Fyodor Dostoyevski", "Roman", 
             "9789750728600", 1866, 5, 2),
            (2, "1984", "George Orwell", "Distopya", 
             "9789750718311", 1949, 3, 1),
            (3, "Küçük Prens", "Antoine de Saint-Exupéry", "Masal", 
             "9789750724947", 1943, 7, 0),
            (4, "Simyacı", "Paulo Coelho", "Roman", 
             "9789750726439", 1988, 4, 0),
            (5, "Hayvan Çiftliği", "George Orwell", "Politik Taşlama", 
             "9789750717871", 1945, 3, 1),
            (6, "Sefiller", "Victor Hugo", "Roman", 
             "9789750724948", 1862, 2, 0),
            (7, "Dönüşüm", "Franz Kafka", "Roman", 
             "9789750724949", 1915, 4, 0),
            (8, "Yabancı", "Albert Camus", "Roman", 
             "9789750724950", 1942, 3, 0),
            (9, "Fareler ve İnsanlar", "John Steinbeck", "Roman", 
             "9789750724951", 1937, 2, 0),
            (10, "Bülbülü Öldürmek", "Harper Lee", "Roman", 
             "9789750724952", 1960, 3, 1),
        ]
        
        bugun = date.today().strftime('%Y-%m-%d')
        
        for kitap in kitaplar:
            kitap_id, ad, yazar, kategori, isbn, yil, toplam, odunc = kitap
            self.db.execute_update(
                """INSERT INTO kitaplar (id, ad, yazar, kategori, isbn, yayin_yili, toplam_adet, odunc_adet, eklenme_tarihi)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (kitap_id, ad, yazar, kategori, isbn, yil, toplam, odunc, bugun)
            )
        
        print(f"   📚 {len(kitaplar)} kitap eklendi")
    
    def _create_demo_uyeler(self):
        """Demo üyeleri ekle"""
        uyeler = [
            (1, "Ahmet Yılmaz", "ahmet@email.com", "05551234567"),
            (2, "Ayşe Demir", "ayse@email.com", "05559876543"),
            (3, "Mehmet Kaya", "mehmet@email.com", "05321234567"),
            (4, "Zeynep Çelik", "zeynep@email.com", "05431234567"),
            (5, "Ali Öztürk", "ali@email.com", ""),
            (6, "Fatma Şahin", "fatma@email.com", "05561234567"),
            (7, "Mustafa Aydın", "mustafa@email.com", ""),
            (8, "Esra Koç", "esra@email.com", "05391234567"),
        ]
        
        bugun = date.today().strftime('%Y-%m-%d')
        
        for uye in uyeler:
            uye_id, ad, email, telefon = uye
            self.db.execute_update(
                """INSERT INTO uyeler (id, ad, email, telefon, aktif_odunc, toplam_odunc, ceza_bakiyesi, kayit_tarihi)
                   VALUES (?, ?, ?, ?, 0, 0, 0.0, ?)""",
                (uye_id, ad, email, telefon, bugun)
            )
        
        print(f"   👥 {len(uyeler)} üye eklendi")
    
    def _create_demo_oduncler(self):
        """Demo ödünç kayıtları ekle"""
        bugun = date.today()
        
        # Bazı ödünç kayıtları
        oduncler = [
            # (kitap_id, uye_id, gun_once, iade_edildi_mi, gecikme_var_mi)
            (1, 1, 10, False, False),   # Ahmet - Suç ve Ceza (aktif)
            (2, 2, 5, False, False),    # Ayşe - 1984 (aktif)
            (5, 3, 20, False, True),    # Mehmet - Hayvan Çiftliği (gecikmiş)
            (10, 4, 3, False, False),   # Zeynep - Bülbülü Öldürmek (aktif)
            (1, 5, 30, True, True),     # Ali - Suç ve Ceza (iade, gecikmeli)
            (3, 6, 25, True, False),    # Fatma - Küçük Prens (iade, normal)
        ]
        
        for kitap_id, uye_id, gun_once, iade_edildi, gecikmeli in oduncler:
            odunc_tarihi = bugun - timedelta(days=gun_once)
            beklenen_tarih = odunc_tarihi + timedelta(days=15)
            
            if iade_edildi:
                if gecikmeli:
                    iade_tarihi = beklenen_tarih + timedelta(days=5)
                    gecikme = 5
                else:
                    iade_tarihi = beklenen_tarih - timedelta(days=2)
                    gecikme = 0
                
                ceza = gecikme * 5.0
                
                self.db.execute_update(
                    """INSERT INTO oduncler (kitap_id, uye_id, odunc_tarihi, beklenen_iade, iade_tarihi, ceza_tutari, odendi)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (kitap_id, uye_id,
                     odunc_tarihi.strftime('%Y-%m-%d'),
                     beklenen_tarih.strftime('%Y-%m-%d'),
                     iade_tarihi.strftime('%Y-%m-%d'),
                     ceza, 1 if ceza == 0 else 0)
                )
            else:
                # Aktif ödünç
                self.db.execute_update(
                    """INSERT INTO oduncler (kitap_id, uye_id, odunc_tarihi, beklenen_iade)
                       VALUES (?, ?, ?, ?)""",
                    (kitap_id, uye_id,
                     odunc_tarihi.strftime('%Y-%m-%d'),
                     beklenen_tarih.strftime('%Y-%m-%d'))
                )
        
        # Üye istatistiklerini güncelle (aktif ödünç sayıları)
        for uye_id in range(1, 9):
            aktif = self.db.execute_query(
                "SELECT COUNT(*) as count FROM oduncler WHERE uye_id = ? AND iade_tarihi IS NULL",
                (uye_id,)
            )[0]['count']
            
            toplam = self.db.execute_query(
                "SELECT COUNT(*) as count FROM oduncler WHERE uye_id = ?",
                (uye_id,)
            )[0]['count']
            
            self.db.execute_update(
                "UPDATE uyeler SET aktif_odunc = ?, toplam_odunc = ? WHERE id = ?",
                (aktif, toplam, uye_id)
            )
        
        print(f"   🔄 {len(oduncler)} ödünç kaydı eklendi")
    
    def _show_stats(self):
        """Başlangıç istatistiklerini göster"""
        stats = self.db.get_stats()
        print(f"\n📊 Sistem İstatistikleri:")
        print(f"   📚 Toplam Kitap: {stats['toplam_kitap']}")
        print(f"   📖 Ödünçte: {stats['odunc_kitap']}")
        print(f"   👥 Kayıtlı Üye: {stats['toplam_uye']}")
        print(f"   🔄 Aktif Ödünç: {stats['aktif_odunc']}")
        print(f"   ⚠️ Gecikmiş: {stats['gecikmis_islem']}")
        print(f"   💰 Toplam Ceza: {stats['toplam_ceza']:.2f} TL")
    
    def check_login(self, username: str, password: str) -> tuple:
        """
        Kullanıcı girişi kontrol et
        
        Args:
            username: Kullanıcı adı
            password: Şifre
            
        Returns:
            (başarılı_mı, mesaj, rol)
        """
        # Boş kontrol
        if not username or not username.strip():
            return False, "❌ Kullanıcı adı boş olamaz!", None
        
        if not password:
            return False, "❌ Şifre boş olamaz!", None
        
        # Kullanıcıyı bul
        adminler = self.db.execute_query(
            "SELECT * FROM adminler WHERE kullanici_adi = ?",
            (username.strip(),)
        )
        
        if not adminler:
            return False, "❌ Kullanıcı bulunamadı!", None
        
        admin = adminler[0]
        
        # Şifre kontrolü
        sifre_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if sifre_hash != admin['sifre_hash']:
            return False, "❌ Hatalı şifre!", None
        
        # Son giriş tarihini güncelle
        from datetime import datetime
        self.db.execute_update(
            "UPDATE adminler SET son_giris = ? WHERE id = ?",
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), admin['id'])
        )
        
        # Log kaydı
        self.db.add_log(
            "Kullanıcı Girişi",
            f"{admin['ad']} ({admin['rol']}) sisteme giriş yaptı",
            admin['kullanici_adi']
        )
        
        return True, f"✅ Hoş geldiniz, {admin['ad']}!", admin['rol']


def main():
    """Ana program giriş noktası"""
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont("Segoe UI", 10))
    
    try:
        sistem = KutuphaneSistemi()
    except Exception as e:
        QMessageBox.critical(None, "Sistem Hatası",
            f"Sistem başlatılırken hata:\n\n{str(e)}")
        return 1
    
    # db parametresini de gönder
    login = LoginDialog(sistem.check_login, sistem.db)
    
    if login.exec_() == LoginDialog.Accepted:
        try:
            # DÜZELTİLDİ: username_input → username
            username = login.username.text()
            
            admin_data = sistem.db.execute_query(
                "SELECT * FROM adminler WHERE kullanici_adi = ?", (username,)
            )
            
            if not admin_data:
                QMessageBox.critical(None, "Hata", "Kullanıcı bilgileri alınamadı!")
                return 1
            
            admin_data = admin_data[0]
            
            admin = Admin(
                admin_data['kullanici_adi'],
                "",
                admin_data['ad'],
                admin_data['email'],
                admin_data['rol']
            )
            
            window = MainWindow(sistem, admin)
            window.show()
            
            exit_code = app.exec_()
            
            sistem.db.add_log("Çıkış", f"{admin.get_ad()} çıkış yaptı", admin.get_kullanici_adi())
            
            return exit_code
            
        except Exception as e:
            QMessageBox.critical(None, "Çalışma Zamanı Hatası",
                f"Program çalışırken bir hata oluştu:\n\n{str(e)}")
            return 1
    else:
        return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Program kullanıcı tarafından sonlandırıldı.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)