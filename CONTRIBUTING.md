# Katkı rehberi

Bu depo bir öğrenme alanı, katkı kuralları da bilerek basit tutuldu.

## Kurulum

```bash
git clone https://github.com/Asif052004/github-ogrenme.git
cd github-ogrenme
python -m unittest discover -v   # bağımlılık yok, Python 3.10+
```

## Akış

1. Issue aç ya da var olanı seç (`good first issue` iyi başlangıç).
2. `main`'den dal aç: `git switch -c tur/kisa-aciklama`
   (ör. `docs/kurulum-netlestir`, `feat/etiket-filtresi`)
3. Küçük, tek konulu commit'ler at. Mesaj öneki: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
4. Testleri çalıştır: `python -m unittest discover -v`
5. Push et ve PR aç. Açıklamada **ne** ve **neden** yaz, ilgili issue'ya `Closes #N` ile bağla.
6. CI yeşil olmadan birleştirme yok.

## Stil

- Python: 4 boşluk, `snake_case`, docstring'ler Türkçe olabilir.
- Commit mesajları Türkçe veya İngilizce olabilir, ama tutarlı olsun.
- Yeni davranış ekliyorsan testini de ekle.

## Güvenlik

Token, parola, kişisel veri commit etme. Yanlışlıkla olduysa hemen bildir.
