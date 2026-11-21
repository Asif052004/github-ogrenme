# 6. Fork, açık kaynak ve güvenlik

## Fork nedir?

Başkasının reposunu **kendi hesabına kopyalamak**. Klonlamaktan farkı: klon
sadece bilgisayarına indirir, fork GitHub'da senin adına bir repo oluşturur.
Yazma iznin olmayan projelere katkı böyle verilir.

```
orijinal repo (upstream)  --fork-->  senin kopyan (origin)  --clone-->  bilgisayarın
```

## Tipik açık kaynak akışı

```bash
gh repo fork sahiplik/proje --clone   # ya da web'den Fork düğmesi
cd proje
git switch -c fix/yazim-hatasi
# ... düzelt ...
git commit -am "fix: yazım hatası düzeltildi"
git push -u origin fix/yazim-hatasi
# GitHub'da "Compare & pull request" → orijinal repoya PR
```

Güncel kalmak için:

```bash
git remote add upstream https://github.com/sahiplik/proje.git
git fetch upstream
git switch main && git merge upstream/main
```

## Katkı görgü kuralları

- Önce `CONTRIBUTING.md` ve açık issue'ları oku; aynı işi ikinci kez yapma.
- Büyük değişiklikten önce issue açıp "bunu yapmayı düşünüyorum" de.
- Tek PR'da tek konu. Biçimlendirme değişikliğini özellikle ayır.
- Review yorumlarını kişisel algılama; kod hakkında konuşulur, kişi hakkında değil.

## Güvenlik: asla commit etmemek gerekenler

- `.env`, API anahtarı, token, parola
- Özel anahtarlar (`*.pem`, `*.key`, `id_rsa`)
- Müşteri verisi, kişisel bilgi (KVKK/GDPR)

Yanlışlıkla commit ettiysen **dosyayı silmek yetmez**, geçmişte kalır. O token'ı
derhal iptal et (revoke) ve gerekirse geçmişi `git filter-repo` ile temizle.

Repo ayarlarından açman gerekenler:

| Ayar | Neden |
|------|-------|
| Branch protection (`main`) | Doğrudan push'u engelle, PR + CI zorunlu olsun |
| Secret scanning | Yanlışlıkla eklenen anahtarı GitHub yakalasın |
| Dependabot | Bağımlılık güvenlik açığı için otomatik PR |
| 2FA | Hesap çalınmasına karşı |

## İyi ilk katkı: dokümantasyon

Kod yazmadan katkı yapmanın en kolay yolu:

- Yazım hatası düzelt
- Kurulum adımını netleştir
- Örnek kullanım ekle
- `good first issue` etiketli işlere bak

## Alıştırma

1. Kendi hesabınla tanınmış küçük bir repoyu fork'la, `upstream` ekle, `fetch` yap.
2. README'de bir yazım hatasını düzelt, dal aç, PR aç (istersen kapat).
3. Bu repoda branch protection aç: `main`'e doğrudan push engellensin.
4. Dependabot alerts ve secret scanning'i aç, ayarları incele.

Başa dön: [README](../README.md)
