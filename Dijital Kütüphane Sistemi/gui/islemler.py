"""
Kitap, Üye ve Ödünç İşlemleri Sayfası
LibraryOS v3.0
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QLineEdit, QSpinBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QAbstractItemView, QFormLayout, QMessageBox,
                             QComboBox, QDateEdit, QTabWidget, QGroupBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
from datetime import date, timedelta
from gui.styles import Theme, Styles


class IslemPage(QWidget):
    
    def __init__(self, sistem):
        super().__init__()
        self.sistem = sistem
        self.styles = Styles()
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(self.styles.tab_widget)
        self.tab_widget.addTab(self._kitap_tab(), "📚 Kitap İşlemleri")
        self.tab_widget.addTab(self._uye_tab(), "👥 Üye İşlemleri")
        self.tab_widget.addTab(self._odunc_tab(), "🔄 Ödünç İşlemleri")
        layout.addWidget(self.tab_widget)
    
    # ============================================================
    # KİTAP SEKMESİ
    # ============================================================
    
    def _kitap_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)
        
        # SOL FORM
        sol = QFrame()
        sol.setObjectName("card")
        sol.setStyleSheet(self.styles.card)
        sol.setFixedWidth(450)
        
        sl = QVBoxLayout(sol)
        sl.setContentsMargins(25, 25, 25, 25)
        sl.setSpacing(15)
        
        sl.addWidget(QLabel("📚 Kitap Ekle / Güncelle"))
        
        f = QFormLayout()
        f.setSpacing(10)
        
        id_lay = QHBoxLayout()
        self.k_id = QSpinBox()
        self.k_id.setRange(1, 99999)
        self.k_id.setStyleSheet(self.styles.input_field())
        self.k_id.setEnabled(False)
        
        oto_btn = QPushButton("🔄 Otomatik")
        oto_btn.setStyleSheet(self.styles.button_secondary())
        oto_btn.clicked.connect(self._oto_kitap_id)
        
        id_lay.addWidget(self.k_id)
        id_lay.addWidget(oto_btn)
        f.addRow("Kitap ID:", id_lay)
        
        self.k_ad = QLineEdit()
        self.k_ad.setPlaceholderText("Kitap adı...")
        self.k_ad.setStyleSheet(self.styles.input_field())
        f.addRow("Kitap Adı:", self.k_ad)
        
        self.k_yazar = QLineEdit()
        self.k_yazar.setPlaceholderText("Yazar adı...")
        self.k_yazar.setStyleSheet(self.styles.input_field())
        f.addRow("Yazar:", self.k_yazar)
        
        self.k_kat = QComboBox()
        self.k_kat.addItems(["Roman","Hikaye","Şiir","Bilim Kurgu","Fantastik",
                             "Polisiye","Biyografi","Tarih","Felsefe","Bilim",
                             "Teknoloji","Eğitim","Çocuk","Gençlik","Diğer"])
        self.k_kat.setEditable(True)
        self.k_kat.setStyleSheet(self.styles.combo_box())
        f.addRow("Kategori:", self.k_kat)
        
        self.k_isbn = QLineEdit()
        self.k_isbn.setPlaceholderText("ISBN (opsiyonel)")
        self.k_isbn.setStyleSheet(self.styles.input_field())
        f.addRow("ISBN:", self.k_isbn)
        
        self.k_yil = QSpinBox()
        self.k_yil.setRange(1000, 2100)
        self.k_yil.setValue(2024)
        self.k_yil.setStyleSheet(self.styles.input_field())
        f.addRow("Yayın Yılı:", self.k_yil)
        
        self.k_adet = QSpinBox()
        self.k_adet.setRange(1, 100)
        self.k_adet.setValue(1)
        self.k_adet.setStyleSheet(self.styles.input_field())
        f.addRow("Stok:", self.k_adet)
        
        sl.addLayout(f)
        
        # Butonlar
        bl = QHBoxLayout()
        bl.setSpacing(8)
        
        ekle = QPushButton("✅ Ekle")
        ekle.setStyleSheet(self.styles.button_success())
        ekle.clicked.connect(self._kitap_ekle)
        
        guncelle = QPushButton("📝 Güncelle")
        guncelle.setStyleSheet(self.styles.button_primary())
        guncelle.clicked.connect(self._kitap_guncelle)
        
        sil = QPushButton("🗑️ Sil")
        sil.setStyleSheet(self.styles.button_danger())
        sil.clicked.connect(self._kitap_sil)
        
        temizle = QPushButton("🧹 Temizle")
        temizle.setStyleSheet(self.styles.button_warning())
        temizle.clicked.connect(self._kitap_form_temizle)
        
        bl.addWidget(ekle)
        bl.addWidget(guncelle)
        bl.addWidget(sil)
        bl.addWidget(temizle)
        sl.addLayout(bl)
        sl.addStretch()
        
        layout.addWidget(sol)
        
        # SAĞ TABLO
        sag = QFrame()
        sag.setObjectName("card")
        sag.setStyleSheet(self.styles.card)
        
        sgl = QVBoxLayout(sag)
        sgl.setContentsMargins(20, 20, 20, 20)
        sgl.setSpacing(15)
        
        self.k_arama = QLineEdit()
        self.k_arama.setPlaceholderText("🔍 Ara...")
        self.k_arama.setStyleSheet(self.styles.search_bar("100%"))
        self.k_arama.textChanged.connect(self._kitap_ara)
        sgl.addWidget(self.k_arama)
        
        self.k_tablo = QTableWidget()
        self.k_tablo.setColumnCount(7)
        self.k_tablo.setHorizontalHeaderLabels(["ID","KİTAP ADI","YAZAR","KATEGORİ","ISBN","STOK","DURUM"])
        self.k_tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.k_tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.k_tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.k_tablo.setAlternatingRowColors(True)
        self.k_tablo.verticalHeader().setVisible(False)
        self.k_tablo.setShowGrid(False)
        self.k_tablo.setStyleSheet(self.styles.table)
        self.k_tablo.setSortingEnabled(True)
        self.k_tablo.clicked.connect(self._kitap_sec)
        sgl.addWidget(self.k_tablo)
        
        layout.addWidget(sag)
        return widget
    
    # ============================================================
    # ÜYE SEKMESİ
    # ============================================================
    
    def _uye_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)
        
        sol = QFrame()
        sol.setObjectName("card")
        sol.setStyleSheet(self.styles.card)
        sol.setFixedWidth(450)
        
        sl = QVBoxLayout(sol)
        sl.setContentsMargins(25, 25, 25, 25)
        sl.setSpacing(15)
        
        sl.addWidget(QLabel("👥 Üye Ekle / Güncelle"))
        
        f = QFormLayout()
        f.setSpacing(10)
        
        id_lay = QHBoxLayout()
        self.u_id = QSpinBox()
        self.u_id.setRange(1, 99999)
        self.u_id.setStyleSheet(self.styles.input_field())
        self.u_id.setEnabled(False)
        
        oto_btn = QPushButton("🔄 Otomatik")
        oto_btn.setStyleSheet(self.styles.button_secondary())
        oto_btn.clicked.connect(self._oto_uye_id)
        
        id_lay.addWidget(self.u_id)
        id_lay.addWidget(oto_btn)
        f.addRow("Üye ID:", id_lay)
        
        self.u_ad = QLineEdit()
        self.u_ad.setPlaceholderText("Ad Soyad...")
        self.u_ad.setStyleSheet(self.styles.input_field())
        f.addRow("Ad Soyad:", self.u_ad)
        
        self.u_email = QLineEdit()
        self.u_email.setPlaceholderText("ornek@mail.com")
        self.u_email.setStyleSheet(self.styles.input_field())
        f.addRow("E-Mail:", self.u_email)
        
        self.u_tel = QLineEdit()
        self.u_tel.setPlaceholderText("05XX XXX XX XX")
        self.u_tel.setStyleSheet(self.styles.input_field())
        f.addRow("Telefon:", self.u_tel)
        
        sl.addLayout(f)
        
        bl = QHBoxLayout()
        bl.setSpacing(8)
        
        ekle = QPushButton("✅ Kaydet")
        ekle.setStyleSheet(self.styles.button_success())
        ekle.clicked.connect(self._uye_ekle)
        
        guncelle = QPushButton("📝 Güncelle")
        guncelle.setStyleSheet(self.styles.button_primary())
        guncelle.clicked.connect(self._uye_guncelle)
        
        sil = QPushButton("🗑️ Sil")
        sil.setStyleSheet(self.styles.button_danger())
        sil.clicked.connect(self._uye_sil)
        
        temizle = QPushButton("🧹 Temizle")
        temizle.setStyleSheet(self.styles.button_warning())
        temizle.clicked.connect(self._uye_form_temizle)
        
        bl.addWidget(ekle)
        bl.addWidget(guncelle)
        bl.addWidget(sil)
        bl.addWidget(temizle)
        sl.addLayout(bl)
        sl.addStretch()
        
        layout.addWidget(sol)
        
        sag = QFrame()
        sag.setObjectName("card")
        sag.setStyleSheet(self.styles.card)
        
        sgl = QVBoxLayout(sag)
        sgl.setContentsMargins(20, 20, 20, 20)
        sgl.setSpacing(15)
        
        self.u_arama = QLineEdit()
        self.u_arama.setPlaceholderText("🔍 Ara...")
        self.u_arama.setStyleSheet(self.styles.search_bar("100%"))
        self.u_arama.textChanged.connect(self._uye_ara)
        sgl.addWidget(self.u_arama)
        
        self.u_tablo = QTableWidget()
        self.u_tablo.setColumnCount(6)
        self.u_tablo.setHorizontalHeaderLabels(["ID","AD SOYAD","E-MAİL","TELEFON","AKTİF ÖDÜNÇ","CEZA"])
        self.u_tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.u_tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.u_tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.u_tablo.setAlternatingRowColors(True)
        self.u_tablo.verticalHeader().setVisible(False)
        self.u_tablo.setShowGrid(False)
        self.u_tablo.setStyleSheet(self.styles.table)
        self.u_tablo.setSortingEnabled(True)
        self.u_tablo.clicked.connect(self._uye_sec)
        sgl.addWidget(self.u_tablo)
        
        layout.addWidget(sag)
        return widget
    
    # ============================================================
    # ÖDÜNÇ SEKMESİ
    # ============================================================
    
    def _odunc_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Üst panel
        ust = QFrame()
        ust.setObjectName("card")
        ust.setStyleSheet(self.styles.card)
        
        ul = QHBoxLayout(ust)
        ul.setContentsMargins(25, 25, 25, 25)
        ul.setSpacing(30)
        
        # Ödünç Ver
        ov_frame = QGroupBox("📤 ÖDÜNÇ VER")
        ov_frame.setStyleSheet(self.styles.group_box)
        ovl = QFormLayout(ov_frame)
        ovl.setSpacing(10)
        
        self.o_kid = QSpinBox()
        self.o_kid.setRange(1, 99999)
        self.o_kid.setStyleSheet(self.styles.input_field())
        ovl.addRow("Kitap ID:", self.o_kid)
        
        self.o_uid = QSpinBox()
        self.o_uid.setRange(1, 99999)
        self.o_uid.setStyleSheet(self.styles.input_field())
        ovl.addRow("Üye ID:", self.o_uid)
        
        self.o_tarih = QDateEdit()
        self.o_tarih.setDate(QDate.currentDate())
        self.o_tarih.setCalendarPopup(True)
        self.o_tarih.setStyleSheet(self.styles.input_field())
        ovl.addRow("Tarih:", self.o_tarih)
        
        ov_btn = QPushButton("📤 Ödünç Ver")
        ov_btn.setStyleSheet(self.styles.button_primary(full_width=True, size="large"))
        ov_btn.clicked.connect(self._odunc_ver)
        ovl.addRow(ov_btn)
        
        ul.addWidget(ov_frame)
        
        # İade Al
        ia_frame = QGroupBox("📥 İADE AL")
        ia_frame.setStyleSheet(self.styles.group_box)
        ial = QFormLayout(ia_frame)
        ial.setSpacing(10)
        
        self.i_kid = QSpinBox()
        self.i_kid.setRange(1, 99999)
        self.i_kid.setStyleSheet(self.styles.input_field())
        ial.addRow("Kitap ID:", self.i_kid)
        
        self.i_tarih = QDateEdit()
        self.i_tarih.setDate(QDate.currentDate())
        self.i_tarih.setCalendarPopup(True)
        self.i_tarih.setStyleSheet(self.styles.input_field())
        ial.addRow("İade Tarihi:", self.i_tarih)
        
        ia_btn = QPushButton("📥 İade Al")
        ia_btn.setStyleSheet(self.styles.button_success(full_width=True))
        ia_btn.clicked.connect(self._iade_al)
        ial.addRow(ia_btn)
        
        ul.addWidget(ia_frame)
        layout.addWidget(ust)
        
        # Alt tablo
        alt = QFrame()
        alt.setObjectName("card")
        alt.setStyleSheet(self.styles.card)
        
        al = QVBoxLayout(alt)
        al.setContentsMargins(20, 20, 20, 20)
        al.setSpacing(15)
        
        al.addWidget(QLabel("📋 Aktif Ödünçler"))
        
        self.o_tablo = QTableWidget()
        self.o_tablo.setColumnCount(7)
        self.o_tablo.setHorizontalHeaderLabels(["İŞLEM ID","KİTAP","ÜYE","VERİLİŞ","BEKLENEN","KALAN GÜN","DURUM"])
        self.o_tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.o_tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.o_tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.o_tablo.setAlternatingRowColors(True)
        self.o_tablo.verticalHeader().setVisible(False)
        self.o_tablo.setShowGrid(False)
        self.o_tablo.setStyleSheet(self.styles.table)
        al.addWidget(self.o_tablo)
        
        layout.addWidget(alt)
        return widget
    
    # ============================================================
    # KİTAP FONKSİYONLARI
    # ============================================================
    
    def _oto_kitap_id(self):
        sonuc = self.sistem.db.execute_query("SELECT MAX(id) as max_id FROM kitaplar")
        self.k_id.setValue((sonuc[0]['max_id'] or 0) + 1)
    
    def _kitap_ekle(self):
        kid = self.k_id.value()
        ad = self.k_ad.text().strip()
        yazar = self.k_yazar.text().strip()
        
        if not ad:
            self._msg("Kitap adı boş olamaz!", "error")
            return
        
        if not yazar:
            self._msg("Yazar adı boş olamaz!", "error")
            return
        
        mevcut = self.sistem.db.execute_query("SELECT id FROM kitaplar WHERE id=?", (kid,))
        if mevcut:
            self._msg("Bu ID zaten var!", "error")
            return
        
        self.sistem.db.execute_update(
            """INSERT INTO kitaplar (id, ad, yazar, kategori, isbn, yayin_yili, toplam_adet, odunc_adet, eklenme_tarihi)
               VALUES (?,?,?,?,?,?,?,0,?)""",
            (kid, ad, yazar, self.k_kat.currentText(), self.k_isbn.text(),
             self.k_yil.value(), self.k_adet.value(), date.today().strftime('%Y-%m-%d'))
        )
        
        self.sistem.db.add_log("Kitap Ekleme", f"'{ad}' eklendi")
        self._msg(f"✅ '{ad}' eklendi!", "success")
        self._load_data()
        self._kitap_form_temizle()
    
    def _kitap_guncelle(self):
        kid = self.k_id.value()
        mevcut = self.sistem.db.execute_query("SELECT * FROM kitaplar WHERE id=?", (kid,))
        if not mevcut:
            self._msg("Kitap bulunamadı!", "error")
            return
        
        self.sistem.db.execute_update(
            "UPDATE kitaplar SET ad=?, yazar=?, kategori=?, isbn=?, yayin_yili=?, toplam_adet=? WHERE id=?",
            (self.k_ad.text().strip(), self.k_yazar.text().strip(), self.k_kat.currentText(),
             self.k_isbn.text(), self.k_yil.value(), self.k_adet.value(), kid)
        )
        self.sistem.db.add_log("Kitap Güncelleme", f"ID:{kid} güncellendi")
        self._msg("✅ Kitap güncellendi!", "success")
        self._load_data()
    
    def _kitap_sil(self):
        kid = self.k_id.value()
        mevcut = self.sistem.db.execute_query("SELECT * FROM kitaplar WHERE id=?", (kid,))
        if not mevcut:
            self._msg("Kitap bulunamadı!", "error")
            return
        
        if mevcut[0]['odunc_adet'] > 0:
            self._msg("Bu kitap ödünçte! Önce iade alın.", "warning")
            return
        
        reply = QMessageBox.question(self, "Onay", f"'{mevcut[0]['ad']}' silinsin mi?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sistem.db.execute_update("DELETE FROM kitaplar WHERE id=?", (kid,))
            self.sistem.db.add_log("Kitap Silme", f"'{mevcut[0]['ad']}' silindi")
            self._msg("✅ Kitap silindi!", "success")
            self._load_data()
            self._kitap_form_temizle()
    
    def _kitap_ara(self):
        arama = self.k_arama.text().lower()
        for r in range(self.k_tablo.rowCount()):
            goster = False
            if not arama:
                goster = True
            else:
                for c in [1, 2, 3, 4]:
                    item = self.k_tablo.item(r, c)
                    if item and arama in item.text().lower():
                        goster = True
                        break
            self.k_tablo.setRowHidden(r, not goster)
    
    def _kitap_sec(self):
        r = self.k_tablo.currentRow()
        if r >= 0:
            self.k_id.setValue(int(self.k_tablo.item(r, 0).text()))
            self.k_ad.setText(self.k_tablo.item(r, 1).text())
            self.k_yazar.setText(self.k_tablo.item(r, 2).text())
            self.k_kat.setCurrentText(self.k_tablo.item(r, 3).text())
            self.k_isbn.setText(self.k_tablo.item(r, 4).text())
            self.k_adet.setValue(int(self.k_tablo.item(r, 5).text()))
    
    def _kitap_form_temizle(self):
        self.k_ad.clear()
        self.k_yazar.clear()
        self.k_isbn.clear()
        self.k_adet.setValue(1)
        self._oto_kitap_id()
    
    # ============================================================
    # ÜYE FONKSİYONLARI
    # ============================================================
    
    def _oto_uye_id(self):
        sonuc = self.sistem.db.execute_query("SELECT MAX(id) as max_id FROM uyeler")
        self.u_id.setValue((sonuc[0]['max_id'] or 0) + 1)
    
    def _uye_ekle(self):
        uid = self.u_id.value()
        ad = self.u_ad.text().strip()
        email = self.u_email.text().strip()
        
        if not ad:
            self._msg("Üye adı boş olamaz!", "error")
            return
        
        if not email or '@' not in email:
            self._msg("Geçerli email girin!", "error")
            return
        
        mevcut = self.sistem.db.execute_query("SELECT id FROM uyeler WHERE id=? OR email=?", (uid, email))
        if mevcut:
            self._msg("Bu ID veya email zaten kayıtlı!", "error")
            return
        
        self.sistem.db.execute_update(
            "INSERT INTO uyeler (id, ad, email, telefon, aktif_odunc, toplam_odunc, ceza_bakiyesi, kayit_tarihi) VALUES (?,?,?,?,0,0,0.0,?)",
            (uid, ad, email, self.u_tel.text(), date.today().strftime('%Y-%m-%d'))
        )
        self.sistem.db.add_log("Üye Ekleme", f"'{ad}' eklendi")
        self._msg(f"✅ '{ad}' kaydedildi!", "success")
        self._load_data()
        self._uye_form_temizle()
    
    def _uye_guncelle(self):
        uid = self.u_id.value()
        mevcut = self.sistem.db.execute_query("SELECT * FROM uyeler WHERE id=?", (uid,))
        if not mevcut:
            self._msg("Üye bulunamadı!", "error")
            return
        
        self.sistem.db.execute_update(
            "UPDATE uyeler SET ad=?, email=?, telefon=? WHERE id=?",
            (self.u_ad.text().strip(), self.u_email.text().strip(), self.u_tel.text(), uid)
        )
        self._msg("✅ Üye güncellendi!", "success")
        self._load_data()
    
    def _uye_sil(self):
        uid = self.u_id.value()
        mevcut = self.sistem.db.execute_query("SELECT * FROM uyeler WHERE id=?", (uid,))
        if not mevcut:
            self._msg("Üye bulunamadı!", "error")
            return
        
        if mevcut[0]['aktif_odunc'] > 0:
            self._msg("Üyenin aktif ödüncü var! Önce iade alın.", "warning")
            return
        
        reply = QMessageBox.question(self, "Onay", f"'{mevcut[0]['ad']}' silinsin mi?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sistem.db.execute_update("DELETE FROM uyeler WHERE id=?", (uid,))
            self._msg("✅ Üye silindi!", "success")
            self._load_data()
            self._uye_form_temizle()
    
    def _uye_ara(self):
        arama = self.u_arama.text().lower()
        for r in range(self.u_tablo.rowCount()):
            goster = False
            if not arama:
                goster = True
            else:
                for c in [1, 2, 3]:
                    item = self.u_tablo.item(r, c)
                    if item and arama in item.text().lower():
                        goster = True
                        break
            self.u_tablo.setRowHidden(r, not goster)
    
    def _uye_sec(self):
        r = self.u_tablo.currentRow()
        if r >= 0:
            self.u_id.setValue(int(self.u_tablo.item(r, 0).text()))
            self.u_ad.setText(self.u_tablo.item(r, 1).text())
            self.u_email.setText(self.u_tablo.item(r, 2).text())
            tel = self.u_tablo.item(r, 3).text()
            self.u_tel.setText(tel if tel != "-" else "")
    
    def _uye_form_temizle(self):
        self.u_ad.clear()
        self.u_email.clear()
        self.u_tel.clear()
        self._oto_uye_id()
    
    # ============================================================
    # ÖDÜNÇ FONKSİYONLARI
    # ============================================================
    
    def _odunc_ver(self):
        kid = self.o_kid.value()
        uid = self.o_uid.value()
        tarih = self.o_tarih.date().toPyDate()
        
        kitap = self.sistem.db.execute_query("SELECT * FROM kitaplar WHERE id=?", (kid,))
        if not kitap:
            self._msg("Kitap bulunamadı!", "error")
            return
        kitap = kitap[0]
        
        if kitap['odunc_adet'] >= kitap['toplam_adet']:
            self._msg("Tüm kopyalar ödünçte!", "error")
            return
        
        uye = self.sistem.db.execute_query("SELECT * FROM uyeler WHERE id=?", (uid,))
        if not uye:
            self._msg("Üye bulunamadı!", "error")
            return
        uye = uye[0]
        
        if uye['aktif_odunc'] >= 3:
            self._msg("Üyenin 3 aktif ödüncü var!", "warning")
            return
        
        beklenen = tarih + timedelta(days=15)
        
        self.sistem.db.execute_update("UPDATE kitaplar SET odunc_adet=odunc_adet+1 WHERE id=?", (kid,))
        self.sistem.db.execute_update("UPDATE uyeler SET aktif_odunc=aktif_odunc+1, toplam_odunc=toplam_odunc+1 WHERE id=?", (uid,))
        self.sistem.db.execute_update(
            "INSERT INTO oduncler (kitap_id, uye_id, odunc_tarihi, beklenen_iade) VALUES (?,?,?,?)",
            (kid, uid, tarih.strftime('%Y-%m-%d'), beklenen.strftime('%Y-%m-%d'))
        )
        
        self.sistem.db.add_log("Ödünç", f"'{kitap['ad']}' -> '{uye['ad']}'")
        self._msg(f"✅ Ödünç verildi!\n\nKitap: {kitap['ad']}\nÜye: {uye['ad']}\nSon: {beklenen.strftime('%d.%m.%Y')}", "success")
        self._load_data()
    
    def _iade_al(self):
        kid = self.i_kid.value()
        iade_tarih = self.i_tarih.date().toPyDate()
        
        odunc = self.sistem.db.execute_query(
            """SELECT o.*, k.ad as kitap_ad, u.ad as uye_ad 
               FROM oduncler o JOIN kitaplar k ON o.kitap_id=k.id 
               JOIN uyeler u ON o.uye_id=u.id
               WHERE o.kitap_id=? AND o.iade_tarihi IS NULL
               ORDER BY o.id DESC LIMIT 1""", (kid,))
        
        if not odunc:
            self._msg("Aktif ödünç kaydı bulunamadı!", "error")
            return
        
        odunc = odunc[0]
        beklenen = date.fromisoformat(odunc['beklenen_iade'])
        gecikme = max(0, (iade_tarih - beklenen).days)
        ceza = gecikme * 5.0
        
        self.sistem.db.execute_update("UPDATE kitaplar SET odunc_adet=odunc_adet-1 WHERE id=?", (kid,))
        self.sistem.db.execute_update("UPDATE uyeler SET aktif_odunc=aktif_odunc-1 WHERE id=?", (odunc['uye_id'],))
        if ceza > 0:
            self.sistem.db.execute_update("UPDATE uyeler SET ceza_bakiyesi=ceza_bakiyesi+? WHERE id=?", (ceza, odunc['uye_id']))
        
        self.sistem.db.execute_update(
            "UPDATE oduncler SET iade_tarihi=?, ceza_tutari=? WHERE id=?",
            (iade_tarih.strftime('%Y-%m-%d'), ceza, odunc['id']))
        
        mesaj = f"✅ İade alındı!\n\nKitap: {odunc['kitap_ad']}\nÜye: {odunc['uye_ad']}"
        if ceza > 0:
            mesaj += f"\n\n⚠️ Gecikme: {gecikme} gün\n💰 Ceza: {ceza} TL"
        
        self.sistem.db.add_log("İade", f"'{odunc['kitap_ad']}' iade")
        self._msg(mesaj, "warning" if ceza > 0 else "success")
        self._load_data()
    
    # ============================================================
    # VERİ YÜKLEME
    # ============================================================
    
    def _load_data(self):
        self._load_kitaplar()
        self._load_uyeler()
        self._load_oduncler()
    
    def _load_kitaplar(self):
        kitaplar = self.sistem.db.execute_query("SELECT * FROM kitaplar ORDER BY ad")
        self.k_tablo.setRowCount(len(kitaplar))
        
        for r, k in enumerate(kitaplar):
            mevcut = k['toplam_adet'] - k['odunc_adet']
            durum = "✅ Tümü Mevcut" if mevcut == k['toplam_adet'] else "❌ Tümü Ödünçte" if mevcut == 0 else f"⚠️ {mevcut}/{k['toplam_adet']}"
            
            items = [QTableWidgetItem(str(k['id'])), QTableWidgetItem(k['ad']),
                     QTableWidgetItem(k['yazar']), QTableWidgetItem(k['kategori']),
                     QTableWidgetItem(k['isbn'] or "-"), QTableWidgetItem(str(k['toplam_adet'])),
                     QTableWidgetItem(durum)]
            
            if "Mevcut" in durum: items[6].setForeground(QColor(Theme.DARK['success']))
            elif "Ödünçte" in durum: items[6].setForeground(QColor(Theme.DARK['danger']))
            else: items[6].setForeground(QColor(Theme.DARK['warning']))
            
            for c, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.k_tablo.setItem(r, c, item)
    
    def _load_uyeler(self):
        uyeler = self.sistem.db.execute_query("SELECT * FROM uyeler ORDER BY ad")
        self.u_tablo.setRowCount(len(uyeler))
        
        for r, u in enumerate(uyeler):
            items = [QTableWidgetItem(str(u['id'])), QTableWidgetItem(u['ad']),
                     QTableWidgetItem(u['email']), QTableWidgetItem(u['telefon'] or "-"),
                     QTableWidgetItem(str(u['aktif_odunc'])),
                     QTableWidgetItem(f"{u['ceza_bakiyesi']:.2f} TL")]
            
            if u['aktif_odunc'] > 0: items[4].setForeground(QColor(Theme.DARK['warning']))
            if u['ceza_bakiyesi'] > 0: items[5].setForeground(QColor(Theme.DARK['danger']))
            else: items[5].setForeground(QColor(Theme.DARK['success']))
            
            for c, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.u_tablo.setItem(r, c, item)
    
    def _load_oduncler(self):
        oduncler = self.sistem.db.execute_query("""
            SELECT o.*, k.ad as kitap_ad, u.ad as uye_ad 
            FROM oduncler o JOIN kitaplar k ON o.kitap_id=k.id 
            JOIN uyeler u ON o.uye_id=u.id
            WHERE o.iade_tarihi IS NULL ORDER BY o.beklenen_iade ASC""")
        
        self.o_tablo.setRowCount(len(oduncler))
        bugun = date.today()
        
        for r, o in enumerate(oduncler):
            beklenen = date.fromisoformat(o['beklenen_iade'])
            kalan = (beklenen - bugun).days
            
            if kalan < 0:
                durum = f"⚠️ {abs(kalan)}g gecikti!"
                renk = Theme.DARK['danger']
            elif kalan <= 3:
                durum = f"⏰ {kalan}g kaldı"
                renk = Theme.DARK['warning']
            else:
                durum = f"✅ {kalan}g var"
                renk = Theme.DARK['success']
            
            items = [QTableWidgetItem(str(o['id'])), QTableWidgetItem(o['kitap_ad']),
                     QTableWidgetItem(o['uye_ad']), QTableWidgetItem(o['odunc_tarihi']),
                     QTableWidgetItem(o['beklenen_iade']),
                     QTableWidgetItem(str(abs(kalan)) if kalan < 0 else str(kalan)),
                     QTableWidgetItem(durum)]
            
            items[6].setForeground(QColor(renk))
            if kalan < 0: items[5].setForeground(QColor(Theme.DARK['danger']))
            
            for c, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.o_tablo.setItem(r, c, item)
    
    def _msg(self, mesaj, tip="info"):
        msg = QMessageBox(self)
        msg.setWindowTitle({"success":"✅ Başarılı","error":"❌ Hata","warning":"⚠️ Uyarı","info":"ℹ️ Bilgi"}.get(tip, "Bilgi"))
        msg.setText(mesaj)
        if tip == "success": msg.setStyleSheet(self.styles.notification_success)
        elif tip == "error": msg.setStyleSheet(self.styles.notification_error)
        elif tip == "warning": msg.setStyleSheet(self.styles.notification_warning)
        else: msg.setStyleSheet(self.styles.notification_info)
        msg.exec_()