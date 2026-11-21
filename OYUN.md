# OYUN: Git Macerası (10 level)

`oyun.py`, Git ve GitHub'ı oyun gibi öğretir. Görevleri sen yaparsın, doğrulamayı
oyun yapar: içindeki gerçek git deposunu okur, XP verir, rütbe atlatır.

```bash
python oyun.py            # durum + sıradaki görev
python oyun.py kontrol    # görevleri doğrula, XP ver
python oyun.py harita     # level haritası
python oyun.py ipucu      # sıkışınca
python oyun.py sifirla    # ilerlemeyi sıfırla
```

İlk çalıştırmada `oyun-alani/` klasörü ve içinde `oyun.cmd` kısayolu oluşur.
Oyun alanına girince sadece `oyun` yazman yeterlidir.

## Level haritası

| # | Level | Ne öğretir | XP | Doğrulama ölçütü |
|---|-------|-----------|----|------------------|
| 1 | İlk Kan | `git init`, ilk commit | 50 | ≥1 commit |
| 2 | Üç Adım | commit geçmişi, mesaj öneki | 80 | ≥3 commit |
| 3 | Sahne Ustası | `git add` disiplini | 100 | tek dosya ekleyen commit |
| 4 | Dal Aç | `git switch -c` | 120 | ≥2 dal |
| 5 | Köprü | `merge --no-ff` | 150 | ≥1 merge commit |
| 6 | Çatışma Ustası | conflict çözme | 200 | `catisma.txt` içinde `cozuldu` |
| 7 | Mühür | anotasyonlu `tag` | 120 | ≥1 anotasyonlu tag |
| 8 | Sürüm Kapısı | sürüm dosyası + `v1.0.0` | 150 | `SURUM.txt` + tag |
| 9 | Zamanı Geri Sar | `git revert` | 180 | `Revert ...` commit'i |
| 10 | Uzak Diyar (BOSS) | remote, push, temiz ağaç | 400 | origin + upstream + temiz |

Toplam **1550 XP**.

## Rütbeler

| XP | Rütbe |
|----|-------|
| 0 | Çaylak |
| 100 | Öğrenci |
| 250 | Çırak |
| 450 | Kalfa |
| 700 | Usta |
| 1000 | Efsane |
| 1550 | Git Ustası |

## Kurallar

- Leveller sırayla açılır. Bir sonrakine geçmek için mevcut levelın ölçütünü
  sağlaman gerekir.
- Oyun sadece **okur**; senin yerine komut çalıştırmaz. Komutu yazmak zorundasın,
  öğrenme orada oluyor.
- İlerleme `oyun-durum.json` dosyasında tutulur (git'e girmez).
- Oyun alanını sıfırdan denemek istersen: `oyun-alani/` klasörünü sil,
  `python oyun.py sifirla`.

## Neden bu şekilde?

Her level gerçek bir iş akışının küçük bir parçası: depo kurma, commit, dal,
merge, çatışma, sürüm, geri alma, uzak depo. Oyun bittiğinde bunların hepsini
en az bir kez elle yapmış oluyorsun.

Boss seviyesinde `oyun-alani` deposunu GitHub'a push edeceksin; yani oyunun
sonunda kendi hesabında ikinci bir gerçek repo olacak.
