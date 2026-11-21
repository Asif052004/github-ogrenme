# github-ogrenme

[![CI](https://github.com/Asif052004/github-ogrenme/actions/workflows/ci.yml/badge.svg)](https://github.com/Asif052004/github-ogrenme/actions/workflows/ci.yml)
[![Lisans: MIT](https://img.shields.io/badge/lisans-MIT-blue.svg)](LICENSE)

Git ve GitHub'ı **yaparak** öğrenmek için açılmış küçük bir alıştırma deposu.

Burada teoriğin en azı, komutların en çoğu var: her ders dosyası sonunda
yapabileceğin gerçek görevler bulunuyor. Repo'nun kendisi de ders boyunca
kullanılan canlı bir örnek (commit geçmişi, branch'ler, tag ve CI ile).

## Oyun modu (10 level)

Git'i oyun gibi öğrenmek istersen:

```bash
python oyun.py
```

`oyun.py` senin yerine komut çalıştırmaz; `oyun-alani/` içinde kurduğun gerçek
bir git deposunu okur, görevleri doğrular, XP ve rütbe verir. 10 level, 1550 XP,
son levelda depoyu GitHub'a push ediyorsun.

```bash
python oyun.py kontrol   # görevleri doğrula + XP ver
python oyun.py harita    # level haritası
python oyun.py ipucu     # sıkışınca
```

Detaylar: [OYUN.md](OYUN.md)

## İçindekiler

| # | Konu | Dosya |
|---|------|-------|
| 🎮 | 10 levellik oyun | [OYUN.md](OYUN.md) |
| 1 | Git temelleri: init, status, add, commit, log | [docs/01-git-temelleri.md](docs/01-git-temelleri.md) |
| 2 | Branch ve merge | [docs/02-dallar-ve-birlestirme.md](docs/02-dallar-ve-birlestirme.md) |
| 3 | Remote, pull request ve review | [docs/03-pull-request.md](docs/03-pull-request.md) |
| 4 | Issue, proje panosu, README | [docs/04-issue-ve-projeler.md](docs/04-issue-ve-projeler.md) |
| 5 | GitHub Actions (CI) | [docs/05-github-actions.md](docs/05-github-actions.md) |
| 6 | Fork, açık kaynak ve güvenlik | [docs/06-fork-ve-acik-kaynak.md](docs/06-fork-ve-acik-kaynak.md) |

Alıştırma listesi: [alistirmalar/ALISTIRMALAR.md](alistirmalar/ALISTIRMALAR.md)

## Demo uygulama: `notlar.py`

Repo'da öğrenirken değiştirebileceğin, sıfır bağımlılıklı bir not defteri CLI'si var.
Commit/branch mantığını bu dosya üzerinde denemek kolay.

```bash
python notlar.py ekle "Git ogrenmeye basladim" --etiket ogrenme
python notlar.py listele
python notlar.py ara ogren
python notlar.py sil 1
```

Testler:

```bash
python -m unittest discover -v
```

## Hızlı komut kartı

```bash
git status                 # neyi değiştirdim?
git add -A                 # tüm değişiklikleri sahneye al
git commit -m "mesaj"      # kaydet
git log --oneline --graph  # geçmişi gör
git switch -c yeni-dal     # yeni dal aç ve geç
git switch main            # main'e dön
git merge yeni-dal         # dalı main'e birleştir
git push -u origin main    # GitHub'a gönder
git pull                   # GitHub'dan güncellemeyi al
```

## Yol haritası

1. Ders 1-2: yerelde commit ve branch mantığı.
2. Ders 3: repoyu GitHub'a taşı, pull request aç.
3. Ders 4: issue aç, kapat, proje panosuna taşı.
4. Ders 5: CI'ın yeşile dönmesini izle.
5. Ders 6: başka bir repoyu fork'la, katkı akışını gör.

## Lisans

[MIT](LICENSE)
