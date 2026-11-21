# 3. Remote, push ve pull request

Şimdiye kadarki her şey bilgisayarında. GitHub'a taşımak için bir **remote**
(uzak depo) tanımlarız.

## GitHub'da repo oluşturmak

İki yol var, ikisi de aynı sonucu verir:

**Web:** github.com → sağ üstte `+` → *New repository* → isim gir.
`README`, `.gitignore`, lisans **ekleme**; çünkü sende zaten var (eklersen iki
farklı geçmiş çakışır).

**Terminal (GitHub CLI):**

```bash
winget install --id GitHub.cli     # bir kez kurulur
gh auth login                      # tarayıcı ile giriş
gh repo create github-ogrenme --public --source=. --remote=origin --push
```

## Yerel repoyu bağlamak

```bash
git remote add origin https://github.com/Asif052004/github-ogrenme.git
git remote -v                      # bağlantıyı doğrula
git push -u origin main            # ilk push, -u takip dalını kurar
```

Sonraki push'larda sadece `git push` yeter.

Kimlik doğrulama:

- **HTTPS + Credential Manager:** ilk push'ta tarayıcı açılır, bir kez izin verirsin.
- **SSH:** `ssh-keygen -t ed25519 -C "mail"` → `~/.ssh/id_ed25519.pub` içeriğini
  GitHub → Settings → SSH and GPG keys → New SSH key'e yapıştır. Test: `ssh -T git@github.com`.

## Günlük akış

```bash
git pull                 # önce uzakdaki değişiklikleri al
git switch -c ozellik/x  # dal aç
# ... çalış ...
git add -A && git commit -m "feat: x eklendi"
git push -u origin ozellik/x
```

Push'tan sonra terminalde çıkan linki açarsan GitHub sana PR açmayı önerir.

## Pull request (PR) nedir?

"Şu dalımı `main`'e katmayı öneriyorum" demenin görsel yolu. PR üç şeyi bir arada yapar:

1. **Diff:** ne değişiyor, satır satır.
2. **Tartışma:** yorum, soru, itiraz.
3. **Otomatik kontrol:** CI testleri, lint, önizleme.

### İyi bir PR

- Küçük tut: 1 PR = 1 iş. 500 satırlık PR zor review edilir.
- Başlık ne yaptığını söylesin; açıklamada **neden** yaptığını anlat.
- `Fixes #12` yazarsan PR birleşince 12 numaralı issue otomatik kapanır.
- Kendi PR'ını bile oku; yanlışlıkla eklenen dosya çoğu zaman burada yakalanır.

### Review akışı

| Durum | Anlamı |
|-------|--------|
| Comment | Sadece yorum, onay değil |
| Approve | Onaylandı, birleştirilebilir |
| Request changes | Düzeltme istendi |

Düzeltmeyi aynı dala push'la; PR kendiliğinden güncellenir. Yeni PR açma.

### Birleştirme seçenekleri

- **Merge commit:** tüm commit'ler + bir merge commit'i. Geçmiş dallanmalı ama bilgilidir.
- **Squash and merge:** dalın tüm commit'leri tek commit olur. Küçük takımlarda en temizi.
- **Rebase and merge:** commit'ler tek tek, düz bir çizgi halinde eklenir.

## Alıştırma

1. Repoyu GitHub'a push et.
2. `git switch -c docs/kendi-notun` aç, `docs/` altına kendi notunu ekle, commit + push.
3. GitHub'da PR aç, açıklamasına ne öğrendiğini yaz.
4. PR içinde bir dosyayı web editörüyle düzelt (kalem ikonu), yeni commit'in PR'a düştüğünü gör.
5. "Squash and merge" ile birleştir, sonra dalı sil.

Sonraki: [4. Issue ve projeler](04-issue-ve-projeler.md)
