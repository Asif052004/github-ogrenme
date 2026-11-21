# Değişiklik günlüğü

Bu dosya GitHub'da "release notes" mantığını yerelde görmek için var.
Sürümler `git tag` ile işaretlenir, notlar buraya yazılır.

## [0.2.0] - 2026-11-21

### Eklendi

- `oyun.py`: 10 levellik oyun modu (1550 XP, 7 rütbe, otomatik doğrulama)
- `OYUN.md`: level haritası, ölçütler, rütbe tablosu
- `tests/test_oyun.py`: 7 oyun testi (toplam 18 test)
- README'ye oyun bölümü, `.gitignore`'a `oyun-alani/` ve `oyun-durum.json`

### Notlar

- Oyun `oyun-alani/` içinde kendi git deposunu kurar; ilerleme `oyun-durum.json` dosyasında.

## [0.1.0] - 2026-11-21

### Eklendi

- `notlar.py`: ekle / listele / ara / sil komutları (sıfır bağımlılık, Python 3.10+)
- 11 birim testi (`tests/test_notlar.py`)
- GitHub Actions CI: Python 3.10, 3.12, 3.13 matrisi
- Altı bölümlük Türkçe Git/GitHub rehberi (`docs/`)
- Alıştırma listesi ve hata bildirimi şablonu

### Notlar

- İlk sürüm: yerel kullanım için hazır, veri `notlar.json` dosyasında tutulur.
