# 5. GitHub Actions (CI)

Actions, "şu olay olunca şu makinede şu komutları çalıştır" demenin yolu.
En yaygın kullanımı **CI** (sürekli entegrasyon): her push ve PR'da testleri
otomatik çalıştırmak.

## Dosya nerede?

```
.github/workflows/ci.yml
```

`workflows` klasöründeki her `.yml` bir iş akışıdır. Bu repoda hazır bir tane var.

## Yapı taşları

| Kavram | Anlamı |
|--------|--------|
| `on` | Tetikleyici: `push`, `pull_request`, `workflow_dispatch`, `schedule` |
| `jobs` | Paralel çalışan iş grupları |
| `runs-on` | Hangi makine: `ubuntu-latest`, `windows-latest`, `macos-latest` |
| `steps` | Sırayla çalışan adımlar |
| `uses` | Hazır aksiyon kullan (`actions/checkout@v4`) |
| `run` | Kabuk komutu çalıştır |

## Minimal örnek

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m unittest discover -v
```

## Nerelerde işe yarar?

- Test + lint: bozuk kod `main`'e giremez.
- Build: paket/derleme çıktısı üret.
- Yayın: tag atınca otomatik sürüm yayınla.
- Zamanlanmış iş: her gece bağımlılık kontrolü (`schedule` + cron).
- Etiketleme: yeni issue'ya otomatik `triage` etiketi.

## Bilmen gereken iki şey

1. **Sırlar (secrets):** Settings → Secrets and variables → Actions. Token,
   parola, API anahtarı **asla** YAML'a yazılmaz; `${{ secrets.ADI }}` ile çağrılır.
2. **Ücret:** public repolarda standart runner'lar ücretsiz; private repolarda
   aylık dakika kotası var.

## Yeşil kırmızı

PR sayfasının altında kontroller görünür:

- ✅ yeşil: geçti, birleştirme düğmesi açılır.
- ❌ kırmızı: kaldı. `Details` → log → hatalı adımı oku.

Kırmızıyı düzeltmenin en hızlı yolu: logdaki ilk `Error` satırını yerelde aynı
komutla tekrar üretmek.

## Alıştırma

1. Repoyu push et, **Actions** sekmesinde `CI` iş akışının yeşile döndüğünü gör.
2. Bilerek bir testi boz (`tests/test_notlar.py` içinde bir `assert`i ters çevir),
   commit + push et, kırmızıyı gör.
3. Logdan hatayı bul, düzelt, yeşile dön.
4. `workflow_dispatch` ekleyip Actions sekmesinden elle tetikle.
5. README'ye CI rozetini ekle.

Sonraki: [6. Fork ve açık kaynak](06-fork-ve-acik-kaynak.md)
