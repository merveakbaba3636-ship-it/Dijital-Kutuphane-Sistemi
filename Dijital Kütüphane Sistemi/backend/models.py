"""
Kütüphane Sistemi Veri Modelleri
OOP prensipleri ile encapsulation, inheritance ve polymorphism kullanımı
"""
from datetime import datetime, timedelta, date
from typing import Optional, Dict, Any
import hashlib
import re


class Kisi:
    """Temel kişi sınıfı - Üye ve Admin için base class"""
    def __init__(self, ad: str, email: str):
        self._ad = ad.strip().title()
        self._email = self._validate_email(email)
        self._kayit_tarihi = date.today()
    
    @staticmethod
    def _validate_email(email: str) -> str:
        """Gelişmiş email validasyonu"""
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError(f"Geçersiz email formatı: {email}")
        return email
    
    def get_ad(self): return self._ad
    def get_email(self): return self._email
    def get_kayit_tarihi(self): return self._kayit_tarihi
    
    def set_ad(self, yeni_ad: str):
        if not yeni_ad.strip():
            raise ValueError("İsim boş olamaz!")
        self._ad = yeni_ad.strip().title()


class Uye(Kisi):
    """Kütüphane üyesi - ödünç alma/iade işlemleri"""
    def __init__(self, uye_id: int, ad: str, email: str, telefon: str = ""):
        super().__init__(ad, email)
        self.__uye_id = uye_id
        self.__telefon = telefon
        self.__aktif_odunc_sayisi = 0
        self.__toplam_odunc_sayisi = 0
        self.__ceza_bakiyesi = 0.0
    
    def get_id(self): return self.__uye_id
    def get_telefon(self): return self.__telefon
    def get_aktif_odunc(self): return self.__aktif_odunc_sayisi
    def get_toplam_odunc(self): return self.__toplam_odunc_sayisi
    def get_ceza(self): return self.__ceza_bakiyesi
    
    def set_telefon(self, tel: str): self.__telefon = tel
    def ceza_ekle(self, tutar: float): self.__ceza_bakiyesi += tutar
    def ceza_ode(self, tutar: float): self.__ceza_bakiyesi = max(0, self.__ceza_bakiyesi - tutar)
    
    def odunc_al(self) -> bool:
        if self.__aktif_odunc_sayisi >= 3:  # Max 3 kitap limiti
            return False
        self.__aktif_odunc_sayisi += 1
        self.__toplam_odunc_sayisi += 1
        return True
    
    def iade_et(self):
        if self.__aktif_odunc_sayisi > 0:
            self.__aktif_odunc_sayisi -= 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.__uye_id,
            'ad': self._ad,
            'email': self._email,
            'telefon': self.__telefon,
            'aktif_odunc': self.__aktif_odunc_sayisi,
            'toplam_odunc': self.__toplam_odunc_sayisi,
            'ceza': self.__ceza_bakiyesi,
            'kayit_tarihi': self._kayit_tarihi.strftime('%Y-%m-%d')
        }


class Kitap:
    """Kitap sınıfı - stok yönetimi ile"""
    def __init__(self, kitap_id: int, ad: str, yazar: str, kategori: str, 
                 isbn: str = "", yayin_yili: int = 0, toplam_adet: int = 1):
        self.__kitap_id = kitap_id
        self.__ad = ad.strip().title()
        self.__yazar = yazar.strip().title()
        self.__kategori = kategori.strip().title()
        self.__isbn = isbn
        self.__yayin_yili = yayin_yili
        self.__toplam_adet = toplam_adet
        self.__odunc_adet = 0
        self.__eklenme_tarihi = date.today()
    
    def get_id(self): return self.__kitap_id
    def get_ad(self): return self.__ad
    def get_yazar(self): return self.__yazar
    def get_kategori(self): return self.__kategori
    def get_isbn(self): return self.__isbn
    def get_yayin_yili(self): return self.__yayin_yili
    def get_toplam_adet(self): return self.__toplam_adet
    def get_odunc_adet(self): return self.__odunc_adet
    def get_mevcut_adet(self): return self.__toplam_adet - self.__odunc_adet
    def get_eklenme_tarihi(self): return self.__eklenme_tarihi
    
    def get_durum(self) -> str:
        mevcut = self.get_mevcut_adet()
        if mevcut == 0:
            return "Tümü Ödünçte"
        elif mevcut == self.__toplam_adet:
            return "Tümü Mevcut"
        else:
            return f"{mevcut}/{self.__toplam_adet} Mevcut"
    
    def set_ad(self, ad: str): self.__ad = ad.strip().title()
    def set_yazar(self, yazar: str): self.__yazar = yazar.strip().title()
    def set_kategori(self, kat: str): self.__kategori = kat.strip().title()
    def set_isbn(self, isbn: str): self.__isbn = isbn
    def set_yayin_yili(self, yil: int): self.__yayin_yili = yil
    
    def stok_ekle(self, adet: int = 1):
        if adet > 0:
            self.__toplam_adet += adet
    
    def odunc_ver(self) -> bool:
        if self.__odunc_adet < self.__toplam_adet:
            self.__odunc_adet += 1
            return True
        return False
    
    def iade_al(self) -> bool:
        if self.__odunc_adet > 0:
            self.__odunc_adet -= 1
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.__kitap_id,
            'ad': self.__ad,
            'yazar': self.__yazar,
            'kategori': self.__kategori,
            'isbn': self.__isbn,
            'yayin_yili': self.__yayin_yili,
            'toplam_adet': self.__toplam_adet,
            'odunc_adet': self.__odunc_adet,
            'durum': self.get_durum()
        }


class Odunc:
    """Ödünç işlemi - ceza sistemi entegre"""
    GUNLUK_CEZA = 5.0  # TL
    STANDART_SURE = 15  # gün
    
    def __init__(self, odunc_id: int, kitap: Kitap, uye: Uye, 
                 odunc_tarihi: Optional[date] = None):
        self.__odunc_id = odunc_id
        self.__kitap = kitap
        self.__uye = uye
        self.__odunc_tarihi = odunc_tarihi if odunc_tarihi else date.today()
        self.__beklenen_iade = self.__odunc_tarihi + timedelta(days=self.STANDART_SURE)
        self.__iade_tarihi: Optional[date] = None
        self.__ceza_tutari = 0.0
        self.__odendi = False
    
    def get_id(self): return self.__odunc_id
    def get_kitap(self): return self.__kitap
    def get_uye(self): return self.__uye
    def get_odunc_tarihi(self): return self.__odunc_tarihi
    def get_beklenen_tarih(self): return self.__beklenen_iade
    def get_iade_tarihi(self): return self.__iade_tarihi
    def get_ceza(self): return self.__ceza_tutari
    
    def iade_et(self) -> float:
        """İade işlemi - ceza varsa hesaplar"""
        self.__iade_tarihi = date.today()
        gecikme = (self.__iade_tarihi - self.__beklenen_iade).days
        
        if gecikme > 0:
            self.__ceza_tutari = gecikme * self.GUNLUK_CEZA
            self.__uye.ceza_ekle(self.__ceza_tutari)
        else:
            self.__ceza_tutari = 0.0
        
        self.__kitap.iade_al()
        self.__uye.iade_et()
        return self.__ceza_tutari
    
    def gecikme_hesapla(self, referans_tarih: Optional[date] = None) -> int:
        """Gecikme gün sayısını hesapla"""
        kontrol = referans_tarih if referans_tarih else date.today()
        if self.__iade_tarihi:
            kontrol = self.__iade_tarihi
        return max(0, (kontrol - self.__beklenen_iade).days)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.__odunc_id,
            'kitap_id': self.__kitap.get_id(),
            'kitap_ad': self.__kitap.get_ad(),
            'uye_id': self.__uye.get_id(),
            'uye_ad': self.__uye.get_ad(),
            'odunc_tarihi': self.__odunc_tarihi.strftime('%Y-%m-%d'),
            'beklenen_iade': self.__beklenen_iade.strftime('%Y-%m-%d'),
            'iade_tarihi': self.__iade_tarihi.strftime('%Y-%m-%d') if self.__iade_tarihi else None,
            'gecikme_gun': self.gecikme_hesapla(),
            'ceza_tutari': self.__ceza_tutari,
            'durum': 'İade Edildi' if self.__iade_tarihi else 'Devam Ediyor'
        }


class Admin(Kisi):
    """Yönetici hesabı"""
    def __init__(self, kullanici_adi: str, sifre: str, ad: str, email: str, rol: str = "admin"):
        super().__init__(ad, email)
        self.__kullanici_adi = kullanici_adi
        self.__sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        self.__rol = rol
        self.__son_giris: Optional[datetime] = None
    
    def get_kullanici_adi(self): return self.__kullanici_adi
    def get_rol(self): return self.__rol
    def get_son_giris(self): return self.__son_giris
    
    def sifre_dogrula(self, sifre: str) -> bool:
        return self.__sifre_hash == hashlib.sha256(sifre.encode()).hexdigest()
    
    def sifre_degistir(self, eski_sifre: str, yeni_sifre: str) -> bool:
        if self.sifre_dogrula(eski_sifre):
            self.__sifre_hash = hashlib.sha256(yeni_sifre.encode()).hexdigest()
            return True
        return False
    
    def giris_kaydet(self):
        self.__son_giris = datetime.now()