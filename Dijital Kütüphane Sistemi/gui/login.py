# gui/login.py dosyasını şununla değiştir:

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QStackedWidget, QWidget, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from gui.styles import Theme, Styles
import hashlib
from datetime import date


class LoginDialog(QDialog):
    def __init__(self, check_login_func, db=None):
        super().__init__()
        self.check_login = check_login_func
        self.db = db
        self.styles = Styles()
        self.setWindowTitle("LibraryOS - Giriş")
        self.setFixedSize(420, 550)
        self.setStyleSheet(f"background:{Theme.DARK['bg']};")
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stack widget (giriş ve kayıt sayfaları arası geçiş)
        self.stack = QStackedWidget()
        self.stack.addWidget(self._login_page())
        self.stack.addWidget(self._register_page())
        main_layout.addWidget(self.stack)
    
    def _login_page(self):
        """Giriş sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 50, 40, 40)
        layout.setSpacing(15)
        
        logo = QLabel("📚")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size:50px;")
        layout.addWidget(logo)
        
        title = QLabel("LibraryOS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color:{Theme.DARK['text']};font-size:28px;font-weight:900;")
        layout.addWidget(title)
        
        sub = QLabel("Dijital Kütüphane Yönetim Sistemi")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color:{Theme.DARK['text_sub']};font-size:12px;")
        layout.addWidget(sub)
        layout.addSpacing(20)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("👤 Kullanıcı Adı")
        self.username.setStyleSheet(self.styles.input_field())
        layout.addWidget(self.username)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("🔒 Şifre")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(self.styles.input_field())
        self.password.returnPressed.connect(self._login)
        layout.addWidget(self.password)
        
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color:#EF4444;font-size:11px;min-height:20px;")
        layout.addWidget(self.error_label)
        
        login_btn = QPushButton("🔑 GİRİŞ YAP")
        login_btn.setStyleSheet(self.styles.button_primary(full_width=True))
        login_btn.clicked.connect(self._login)
        login_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(login_btn)
        
        # Kayıt ol linki
        register_btn = QPushButton("📝 Hesabınız yok mu? Kayıt Olun")
        register_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {Theme.DARK['accent']};
                border: none;
                font-size: 12px;
                text-decoration: underline;
            }}
            QPushButton:hover {{
                color: {Theme.DARK['accent_hover']};
            }}
        """)
        register_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        register_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(register_btn)
        
        exit_btn = QPushButton("❌ Çıkış")
        exit_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {Theme.DARK['text_sub']};
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {Theme.DARK['danger']};
            }}
        """)
        exit_btn.clicked.connect(self.reject)
        exit_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(exit_btn)
        
        version = QLabel("v3.0 Pro • SQLite • PyQt5")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet(f"color:{Theme.DARK['text_sub']};font-size:10px;")
        layout.addWidget(version)
        
        return page
    
    def _register_page(self):
        """Kayıt sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(12)
        
        logo = QLabel("📝")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size:40px;")
        layout.addWidget(logo)
        
        title = QLabel("Yeni Hesap Oluştur")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color:{Theme.DARK['text']};font-size:22px;font-weight:800;")
        layout.addWidget(title)
        
        sub = QLabel("Kütüphane sistemine kayıt olun")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color:{Theme.DARK['text_sub']};font-size:11px;")
        layout.addWidget(sub)
        layout.addSpacing(10)
        
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("👤 Kullanıcı Adı")
        self.reg_username.setStyleSheet(self.styles.input_field())
        layout.addWidget(self.reg_username)
        
        self.reg_name = QLineEdit()
        self.reg_name.setPlaceholderText("📛 Ad Soyad")
        self.reg_name.setStyleSheet(self.styles.input_field())
        layout.addWidget(self.reg_name)
        
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("📧 E-Mail")
        self.reg_email.setStyleSheet(self.styles.input_field())
        layout.addWidget(self.reg_email)
        
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("🔒 Şifre (min 6 karakter)")
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_password.setStyleSheet(self.styles.input_field())
        layout.addWidget(self.reg_password)
        
        self.reg_password2 = QLineEdit()
        self.reg_password2.setPlaceholderText("🔒 Şifre Tekrar")
        self.reg_password2.setEchoMode(QLineEdit.Password)
        self.reg_password2.setStyleSheet(self.styles.input_field())
        layout.addWidget(self.reg_password2)
        
        self.reg_error = QLabel("")
        self.reg_error.setAlignment(Qt.AlignCenter)
        self.reg_error.setStyleSheet("color:#EF4444;font-size:11px;min-height:20px;")
        layout.addWidget(self.reg_error)
        
        register_btn = QPushButton("✅ KAYIT OL")
        register_btn.setStyleSheet(self.styles.button_success(full_width=True))
        register_btn.clicked.connect(self._register)
        register_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(register_btn)
        
        back_btn = QPushButton("⬅️ Giriş Sayfasına Dön")
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {Theme.DARK['accent']};
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {Theme.DARK['accent_hover']};
            }}
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        back_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(back_btn)
        
        return page
    
    def _login(self):
        u = self.username.text().strip()
        p = self.password.text()
        if not u or not p:
            self.error_label.setText("⚠️ Kullanıcı adı ve şifre gerekli!")
            return
        success, msg, role = self.check_login(u, p)
        if success:
            self.accept()
        else:
            self.error_label.setText(f"❌ {msg}")
            QTimer.singleShot(3000, lambda: self.error_label.setText(""))
    
    def _register(self):
        """Yeni kullanıcı kaydı"""
        username = self.reg_username.text().strip()
        name = self.reg_name.text().strip()
        email = self.reg_email.text().strip()
        p1 = self.reg_password.text()
        p2 = self.reg_password2.text()
        
        # Validasyon
        if not username or len(username) < 3:
            self.reg_error.setText("⚠️ Kullanıcı adı en az 3 karakter olmalı!")
            return
        
        if not name:
            self.reg_error.setText("⚠️ Ad Soyad gerekli!")
            return
        
        if not email or '@' not in email:
            self.reg_error.setText("⚠️ Geçerli bir email girin!")
            return
        
        if len(p1) < 6:
            self.reg_error.setText("⚠️ Şifre en az 6 karakter olmalı!")
            return
        
        if p1 != p2:
            self.reg_error.setText("⚠️ Şifreler eşleşmiyor!")
            return
        
        # Veritabanına kaydet
        try:
            import hashlib
            sifre_hash = hashlib.sha256(p1.encode()).hexdigest()
            
            # Kullanıcı adı kontrolü
            mevcut = self.db.execute_query(
                "SELECT id FROM adminler WHERE kullanici_adi = ?", (username,)
            )
            if mevcut:
                self.reg_error.setText("⚠️ Bu kullanıcı adı zaten alınmış!")
                return
            
            # Ekle
            self.db.execute_update(
                """INSERT INTO adminler (kullanici_adi, sifre_hash, ad, email, rol)
                   VALUES (?, ?, ?, ?, 'kutuphaneci')""",
                (username, sifre_hash, name, email)
            )
            
            self.db.add_log("Kayıt", f"'{name}' kullanıcısı kayıt oldu")
            
            QMessageBox.information(self, "✅ Başarılı", 
                f"Hesabınız oluşturuldu!\n\n"
                f"Kullanıcı adı: {username}\n"
                f"Rol: Kütüphaneci\n\n"
                f"Giriş sayfasına yönlendiriliyorsunuz...")
            
            # Giriş sayfasına dön
            self.stack.setCurrentIndex(0)
            self.username.setText(username)
            
            # Formu temizle
            self.reg_username.clear()
            self.reg_name.clear()
            self.reg_email.clear()
            self.reg_password.clear()
            self.reg_password2.clear()
            
        except Exception as e:
            self.reg_error.setText(f"❌ Kayıt hatası: {str(e)}")