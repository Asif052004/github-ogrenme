# 4. Issue, proje panosu ve README

## Issue nedir?

Yapılacak iş, hata bildirimi veya soru. PR'ın "kod" tarafıysa issue "konuşma"
tarafıdır. Her issue'nun numarası vardır (`#1`, `#2`...) ve bu numara commit
mesajlarında, PR'larda referans olarak kullanılır.

### İyi hata bildirimi şablonu

```markdown
**Ne oldu:** `python notlar.py sil 99` çalıştırınca çöktü
**Beklenen:** "bulunamadı" uyarısı
**Tekrar adımları:**
1. `python notlar.py ekle "a"`
2. `python notlar.py sil 99`
**Ortam:** Windows 11, Python 3.12
```

### Faydalı issue özellikleri

- **Label:** `bug`, `enhancement`, `good first issue`, `question`
- **Assignee:** kim yapacak
- **Milestone:** hangi sürümde
- **Template:** `.github/ISSUE_TEMPLATE/` altına şablon koyarsan herkes aynı
  formu doldurur.
- **Kapatma:** `Fixes #3`, `Closes #3` yazan PR birleşince issue kapanır.

## Projects (proje panosu)

Kanban mantığı: `Todo → In Progress → Done`. Issue ve PR'ları kart olarak
sürüklersin. Küçük ekiplerde "kim ne yapıyor" sorusunu tek ekranda cevaplar.

## README: projenin vitrini

Biri repona girdiğinde ilk 10 saniyede şu üç sorunun cevabını almalı:

1. Bu proje ne yapıyor?
2. Nasıl çalıştırırım?
3. Nasıl katkı veririm?

İyi bir README'de:

- Tek cümlelik tanım ve varsa ekran görüntüsü/GIF
- Kurulum ve çalıştırma komutları (kopyalanabilir)
- Kullanım örnekleri
- Lisans ve katkı bilgisi

Rozetler (badge) README'nin üstünde durum bilgisi verir:

```markdown
![CI](https://github.com/Asif052004/github-ogrenme/actions/workflows/ci.yml/badge.svg)
```

## `CONTRIBUTING.md`

"Katkı verirken şu komutları çalıştır, şu stile uy" yazan dosya. Yeni gelen
kişiye soru sormadan katkı imkânı verir.

## Alıştırma

1. GitHub'da `notlar.py` için gerçekçi bir issue aç (ör. "etiketle filtreleme yok").
2. `bug` ve `enhancement` etiketi ekle, kendine ata.
3. Bir Projects panosu oluştur, issue'yu `Todo`'ya ekle, sonra `In Progress`'e taşı.
4. README'ye bir "Yol haritası" bölümü ekleyip issue numaralarına link ver.
5. Issue'yu bir PR ile kapat (`Closes #1`).

Sonraki: [5. GitHub Actions](05-github-actions.md)
