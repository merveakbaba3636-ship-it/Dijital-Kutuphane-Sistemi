"""
SQLite veritabanı yönetimi - Connection pooling ve thread-safe operasyonlar
"""
import sqlite3
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import date
from contextlib import contextmanager
from threading import Lock


# Loglama yapılandırması
def setup_logging():
    """Loglama sistemini kur"""
    # Logs klasörünü oluştur
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        filename='logs/library.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )


class DatabaseManager:
    """Thread-safe database manager with connection pooling"""
    
    def __init__(self, db_path: str = "data/library.db"):
        self.db_path = db_path
        self._lock = Lock()
        self._ensure_directories()
        self._init_database()
        logging.info("Veritabanı başarıyla başlatıldı")
    
    def _ensure_directories(self):
        """Gerekli tüm dizinleri oluştur"""
        directories = [
            "data",           # Veritabanı için
            "logs",           # Log dosyaları için
            "exports",        # Dışa aktarılan dosyalar için
            "backups",        # Yedekleme için
            "exports/csv",    # CSV exportları
            "exports/pdf",    # PDF exportları
            "exports/excel",  # Excel exportları
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Klasör oluşturuldu: {directory}/")
    
    @contextmanager
    def get_connection(self):
        """Context manager ile güvenli bağlantı"""
        # Data klasörünü kontrol et
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode=WAL")  # Performans için
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logging.error(f"Veritabanı hatası: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Tabloları oluştur"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Kitaplar tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kitaplar (
                    id INTEGER PRIMARY KEY,
                    ad TEXT NOT NULL,
                    yazar TEXT NOT NULL DEFAULT 'Bilinmiyor',
                    kategori TEXT NOT NULL DEFAULT 'Genel',
                    isbn TEXT DEFAULT '',
                    yayin_yili INTEGER DEFAULT 0,
                    toplam_adet INTEGER NOT NULL DEFAULT 1,
                    odunc_adet INTEGER NOT NULL DEFAULT 0,
                    eklenme_tarihi TEXT NOT NULL
                )
            ''')
            
            # Üyeler tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS uyeler (
                    id INTEGER PRIMARY KEY,
                    ad TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    telefon TEXT DEFAULT '',
                    aktif_odunc INTEGER NOT NULL DEFAULT 0,
                    toplam_odunc INTEGER NOT NULL DEFAULT 0,
                    ceza_bakiyesi REAL NOT NULL DEFAULT 0.0,
                    kayit_tarihi TEXT NOT NULL
                )
            ''')
            
            # Ödünç işlemleri
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS oduncler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kitap_id INTEGER NOT NULL,
                    uye_id INTEGER NOT NULL,
                    odunc_tarihi TEXT NOT NULL,
                    beklenen_iade TEXT NOT NULL,
                    iade_tarihi TEXT,
                    ceza_tutari REAL DEFAULT 0.0,
                    odendi INTEGER DEFAULT 0,
                    FOREIGN KEY (kitap_id) REFERENCES kitaplar(id) ON DELETE RESTRICT,
                    FOREIGN KEY (uye_id) REFERENCES uyeler(id) ON DELETE RESTRICT
                )
            ''')
            
            # Admin hesapları
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS adminler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kullanici_adi TEXT UNIQUE NOT NULL,
                    sifre_hash TEXT NOT NULL,
                    ad TEXT NOT NULL,
                    email TEXT NOT NULL,
                    rol TEXT NOT NULL DEFAULT 'kutuphaneci',
                    son_giris TEXT
                )
            ''')
            
            # Sistem logları
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sistem_loglari (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    islem_tipi TEXT NOT NULL,
                    aciklama TEXT NOT NULL,
                    kullanici TEXT,
                    tarih TEXT NOT NULL
                )
            ''')
            
            # İndeksler
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_kitaplar_ad ON kitaplar(ad)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_kitaplar_yazar ON kitaplar(yazar)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_kitaplar_kategori ON kitaplar(kategori)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_oduncler_tarih ON oduncler(odunc_tarihi)')
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Güvenli sorgu çalıştırma"""
        with self._lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """Güncelleme sorgusu - etkilenen satır sayısını döndür"""
        with self._lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.rowcount
    
    def add_log(self, islem_tipi: str, aciklama: str, kullanici: str = "Sistem"):
        """Sistem logu ekle"""
        # Logs klasörünü kontrol et
        os.makedirs("logs", exist_ok=True)
        
        self.execute_update(
            "INSERT INTO sistem_loglari (islem_tipi, aciklama, kullanici, tarih) VALUES (?, ?, ?, ?)",
            (islem_tipi, aciklama, kullanici, date.today().strftime('%Y-%m-%d'))
        )
        logging.info(f"{islem_tipi}: {aciklama}")
    
    def get_stats(self) -> Dict[str, Any]:
        """İstatistikleri getir"""
        stats = {}
        
        stats['toplam_kitap'] = self.execute_query(
            "SELECT SUM(toplam_adet) as toplam FROM kitaplar")[0]['toplam'] or 0
        
        stats['odunc_kitap'] = self.execute_query(
            "SELECT SUM(odunc_adet) as odunc FROM kitaplar")[0]['odunc'] or 0
        
        stats['toplam_uye'] = self.execute_query(
            "SELECT COUNT(*) as count FROM uyeler")[0]['count']
        
        stats['aktif_odunc'] = self.execute_query(
            "SELECT COUNT(*) as count FROM oduncler WHERE iade_tarihi IS NULL")[0]['count']
        
        stats['toplam_ceza'] = self.execute_query(
            "SELECT SUM(ceza_tutari) as toplam FROM oduncler WHERE odendi = 0")[0]['toplam'] or 0.0
        
        stats['gecikmis_islem'] = self.execute_query("""
            SELECT COUNT(*) as count FROM oduncler 
            WHERE iade_tarihi IS NULL AND date(beklenen_iade) < date('now')
        """)[0]['count']
        
        stats['bugun_odunc'] = self.execute_query("""
            SELECT COUNT(*) as count FROM oduncler 
            WHERE date(odunc_tarihi) = date('now')
        """)[0]['count']
        
        stats['bugun_iade'] = self.execute_query("""
            SELECT COUNT(*) as count FROM oduncler 
            WHERE date(iade_tarihi) = date('now')
        """)[0]['count']
        
        return stats
    
    def backup_database(self, backup_path: Optional[str] = None) -> str:
        """Veritabanı yedeği al"""
        import shutil
        from datetime import datetime
        
        # Backups klasörünü oluştur
        os.makedirs("backups", exist_ok=True)
        
        if not backup_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"backups/library_backup_{timestamp}.db"
        
        shutil.copy2(self.db_path, backup_path)
        logging.info(f"Yedek oluşturuldu: {backup_path}")
        return backup_path
    
    def export_to_csv(self, table_name: str, filename: Optional[str] = None) -> str:
        """Tabloyu CSV'ye aktar"""
        import csv
        from datetime import datetime
        
        # Exports/csv klasörünü oluştur
        os.makedirs("exports/csv", exist_ok=True)
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"exports/csv/{table_name}_{timestamp}.csv"
        
        data = self.execute_query(f"SELECT * FROM {table_name}")
        
        if data:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        
        logging.info(f"CSV export: {filename}")
        return filename
    
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Sistem loglarını getir"""
        return self.execute_query(
            "SELECT * FROM sistem_loglari ORDER BY id DESC LIMIT ?",
            (limit,)
        )
    
    def clear_old_logs(self, days: int = 30):
        """Eski logları temizle"""
        from datetime import timedelta
        
        cutoff_date = (date.today() - timedelta(days=days)).strftime('%Y-%m-%d')
        deleted = self.execute_update(
            "DELETE FROM sistem_loglari WHERE date(tarih) < ?",
            (cutoff_date,)
        )
        logging.info(f"{deleted} eski log temizlendi")
        return deleted