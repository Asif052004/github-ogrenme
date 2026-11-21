# 2. Dallar (branch) ve birleştirme (merge)

Branch, üzerinde serbestçe deneme yapabileceğin **paralel bir kopya** gibi
düşünülebilir. Aslında kopya değil, sadece bir commit'e işaret eden etiket.
Bu yüzden branch açmak ucuzdur: saniyeler değil, milisaniyeler.

## Neden branch?

- `main` her zaman çalışır durumda kalsın.
- Yeni özelliği ayrı dalda geliştir, bitince birleştir.
- Bir fikir tutmazsa dalı sil, `main` hiç etkilenmesin.

## Temel komutlar

```bash
git branch                     # yerel dallar
git branch -a                   # uzak dallar dahil
git switch -c ozellik/arama     # yeni dal aç ve geç
git switch main                 # main'e dön
git merge ozellik/arama         # dalı bulunduğun dala birleştir
git branch -d ozellik/arama     # birleşmiş dalı sil
git log --graph --oneline --all # dallanmayı gör
```

Eski eğitimlerde `git checkout` görürsün; `git switch` (dal) ve `git restore`
(dosya) onun yerini alan daha net komutlar.

## Merge türleri

`main` üzerindeyken bir dalı birleştirdiğinde Git iki yol seçebilir:

- **Fast-forward:** `main` hiç ilerlememişse, sadece ileri sarar. Geçmişte ek
  commit oluşmaz.
- **Merge commit (three-way):** iki taraf da ilerlemişse birleştirme commit'i
  oluşur. `--no-ff` ile fast-forward olsa bile merge commit zorlanabilir;
  böylece "bu iş bir dalda yapıldı" bilgisi geçmişte kalır.

```bash
git merge --no-ff ozellik/arama -m "merge: arama ozelligi"
```

## Çakışma (conflict)

İki dal aynı satırı farklı şekilde değiştirdiyse Git otomatik birleştiremez:

```
<<<<<<< HEAD
bu satır main'de böyle
=======
bu satır dalda böyle
>>>>>>> ozellik/arama
```

Yapılacaklar:

1. Dosyayı aç, doğru halini bırak, `<<<<<<<`, `=======`, `>>>>>>>` işaretlerini sil.
2. `git add dosya`
3. `git commit` (mesaj hazır gelir)

Vazgeçmek istersen: `git merge --abort`.

## `rebase` bir cümlede

`merge` geçmişi olduğu gibi korur, `rebase` ise dalındaki commit'leri hedef
dalın ucuna taşıyıp düz bir çizgi yapar. Kural: **sadece kimsenin görmediği,
kendi dalındaki commit'leri rebase et.**

```bash
git switch ozellik/arama
git rebase main
```

## Alıştırma (bu repoda güvenle yapılır)

1. `git switch -c alistirma/benim-dalim`
2. `notlar.py` içine kısa bir yorum satırı ekle, commit at.
3. `git switch main`, aynı dosyada **başka** bir yere bir şey ekle, commit at.
4. `git switch alistirma/benim-dalim` ve `git rebase main` dene.
5. `git switch main` + `git merge alistirma/benim-dalim`.
6. `git log --graph --oneline --all` ile sonucu incele.
7. Bilerek çakışma çıkarmayı da dene: iki dalda aynı satırı değiştir.

Sonraki: [3. Remote ve pull request](03-pull-request.md)
