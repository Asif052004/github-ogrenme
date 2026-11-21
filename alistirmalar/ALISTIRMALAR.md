# Alıştırma listesi

Kolaydan zora. Her maddeyi yaptıkça `[x]` yap; istersen bu dosyayı commit'leyerek
ilerlemeni kendi geçmişinde tut.

## Yerel Git

- [ ] `git log --oneline` ile son 5 commit'i listele
- [ ] `git diff` ile commit'lenmemiş bir değişikliği incele
- [ ] `git add -p` ile tek dosyadaki değişiklikleri parça parça sahnele
- [ ] İki ayrı commit üret, `git log --graph` ile gör
- [ ] `fix:` önekli bir commit yaz, sonra `git commit --amend` ile mesajını düzelt
- [ ] Bir commit'i `git revert` ile geri al
- [ ] `.gitignore`'a bir dosya ekle, `git status`'ta görünmediğini doğrula

## Dallar

- [ ] `git switch -c alistirma/dal-1` ile dal aç
- [ ] `alistirma/dal-1` içinde `notlar.py`'ye bir yorum ekle, commit at
- [ ] `main`'de başka bir satırı değiştir, commit at
- [ ] `git merge` ile birleştir, çakışmayı elle çöz
- [ ] `git rebase main` deneyip farkı `git log --graph` ile gör
- [ ] Bir dalı sil (`git branch -d`)

## GitHub

- [ ] Repoyu GitHub'a push et
- [ ] Yeni bir issue aç, `enhancement` etiketi ver
- [ ] `main`'den dal açıp PR aç, açıklamasına `Closes #<issue-no>` yaz
- [ ] PR'da bir yorum yaz, sonra çöz (resolve)
- [ ] PR'ı `Squash and merge` ile birleştir, dalı sil
- [ ] Bir tag at: `git tag v0.1.0 && git push origin v0.1.0`
- [ ] GitHub'da Releases sekmesinden tag'den bir release oluştur
- [ ] Branch protection aç: `main`'e doğrudan push engellensin
- [ ] Actions sekmesinden CI iş akışını elle çalıştır (`workflow_dispatch`)

## İleri

- [ ] Bilerek bir testi boz, PR aç, kırmızı CI'ı gör, düzelt
- [ ] `notlar.py`'ye `guncelle` komutu ekle + testini yaz (bu gerçek bir özellik PR'ı)
- [ ] Bir başka repoyu fork'la, `upstream` ekle, bir yazım hatası düzeltip PR gönder
- [ ] README'ye CI rozeti ekle
- [ ] `.github/ISSUE_TEMPLATE/bug_report.md` oluştur

## Fikirler (kendi PR'ın için)

- Not güncelleme komutu (`guncelle`)
- Etiketlere göre sıralama
- `notlar.json` yerine `~/.notlar.json` varsayılanı
- `--json` çıktı seçeneği
- Renkli çıktı (yalnızca terminalde)
