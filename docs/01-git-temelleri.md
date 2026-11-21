# 1. Git temelleri

Git, dosyalarının **zaman içindeki halini** kaydeden bir araç. GitHub ise bu
kayıtları internete koyduğun yer. Yani GitHub'sız da Git vardır, Git'siz GitHub
yoktur.

## Üç alan mantığı

```
çalışma klasörü  --git add-->  sahne (staging)  --git commit-->  geçmiş (repo)
```

- **Çalışma klasörü:** üzerinde düzenleme yaptığın dosyalar.
- **Sahne:** bir sonraki commit'e girecek değişiklikler. Neyi kaydedeceğini sen seçersin.
- **Geçmiş:** commit'lerin kalıcı listesi. Her commit bir fotoğraf gibidir.

## İlk kurulum

```bash
git config --global user.name "Asif Babazade"
git config --global user.email "asifbabazade052004@gmail.com"
git config --global init.defaultBranch main
```

Kontrol:

```bash
git config --global --list
```

## Yeni repo başlatmak

```bash
mkdir deneme && cd deneme
git init
echo "# Deneme" > README.md
git status
```

`git init` klasörde gizli bir `.git` dizini oluşturur. Tüm geçmiş orada durur.
`.git` klasörünü silmek, geçmişi silmek demektir.

## Değişikliği kaydetmek

```bash
git add README.md      # sadece bu dosya
git add -A             # her şey
git status             # neyin sahnede olduğunu gör
git commit -m "docs: ilk README eklendi"
```

`git add` sonrası `git status` çıktısında dosyalar yeşil ("Changes to be
committed") görünür. Commit'ten sonra "working tree clean" yazar.

## Geçmişi okumak

```bash
git log                        # ayrıntılı
git log --oneline              # tek satır
git log --oneline --graph --all
git show <commit-hash>         # bir commit'te ne değişti
git diff                       # sahnede olmayan değişiklikler
git diff --staged              # sahnedeki değişiklikler
```

## İyi commit mesajı

Kısa, emir kipinde, ne yaptığını söyleyen bir başlık:

```
feat: not silme komutu eklendi
fix: boş dosyada çöken json okuma düzeltildi
docs: kurulum adımları güncellendi
chore: .gitignore'a __pycache__ eklendi
```

`feat`, `fix`, `docs`, `chore`, `test`, `refactor` öneki (Conventional Commits)
takım çalışmasında geçmişi okumayı kolaylaştırır.

## Geri almak

```bash
git restore dosya.txt              # sahne öncesi değişikliği at
git restore --staged dosya.txt     # sahneden çıkar, değişiklik kalsın
git commit --amend -m "yeni mesaj" # son commit'in mesajını düzelt
git revert <commit-hash>           # o commit'i geri alan yeni bir commit yaz
```

Altın kural: **başkasına gitmiş commit'i `--amend` veya `reset` ile değiştirme.**
Ortak geçmişi düzeltmenin güvenli yolu `revert`.

## Alıştırma

1. Bu repoda `git log --oneline` çalıştır, ilk commit'i bul.
2. `README.md` içine tek satır ekle, `git diff` ile farkı gör.
3. `git add -p` deneyerek satır satır sahnele.
4. Commit at, `git log --graph --oneline` ile yeni halkayı gör.

Sonraki: [2. Dallar ve birleştirme](02-dallar-ve-birlestirme.md)
