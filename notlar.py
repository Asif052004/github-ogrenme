"""notlar - sifir bagimlilikli kucuk not defteri.

Bu dosya GitHub ogrenme reposunun deneme tahtasi: commit, branch, PR ve CI
mantigini burada guvenle deneyebilirsin.

Kullanim:
    python notlar.py ekle "Git ogrendim" --etiket ogrenme
    python notlar.py listele
    python notlar.py listele --etiket ogrenme
    python notlar.py ara git
    python notlar.py sil 1
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

VARSAYILAN_DOSYA = Path("notlar.json")


@dataclass
class Not:
    """Tek bir not kaydi."""

    metin: str
    etiketler: list[str] = field(default_factory=list)
    tarih: str = ""

    def __post_init__(self) -> None:
        if not self.tarih:
            self.tarih = datetime.now().isoformat(timespec="seconds")


class NotDefteri:
    """JSON dosyasinda tutulan not listesi."""

    def __init__(self, dosya: Path | str = VARSAYILAN_DOSYA) -> None:
        self.dosya = Path(dosya)
        self.notlar: list[Not] = self._oku()

    def _oku(self) -> list[Not]:
        if not self.dosya.exists():
            return []
        try:
            veri = json.loads(self.dosya.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        return [Not(**kayit) for kayit in veri]

    def kaydet(self) -> None:
        icerik = [asdict(not_) for not_ in self.notlar]
        self.dosya.write_text(
            json.dumps(icerik, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def ekle(self, metin: str, etiketler: list[str] | None = None) -> int:
        temiz = metin.strip()
        if not temiz:
            raise ValueError("Bos not eklenemez.")
        self.notlar.append(Not(metin=temiz, etiketler=list(etiketler or [])))
        self.kaydet()
        return len(self.notlar)

    def sil(self, numara: int) -> Not:
        if not 1 <= numara <= len(self.notlar):
            raise IndexError(f"Not bulunamadi: {numara}")
        silinen = self.notlar.pop(numara - 1)
        self.kaydet()
        return silinen

    def listele(self, etiket: str | None = None) -> list[Not]:
        if etiket is None:
            return list(self.notlar)
        hedef = etiket.lower()
        return [n for n in self.notlar if hedef in (e.lower() for e in n.etiketler)]

    def ara(self, kelime: str) -> list[Not]:
        hedef = kelime.lower()
        return [
            n
            for n in self.notlar
            if hedef in n.metin.lower()
            or any(hedef in e.lower() for e in n.etiketler)
        ]


def _yazdir(notlar: list[Not], baslangic: int = 1) -> None:
    if not notlar:
        print("(kayit yok)")
        return
    for sira, not_ in enumerate(notlar, start=baslangic):
        etiketler = " ".join(f"#{e}" for e in not_.etiketler)
        print(f"{sira:>3}. {not_.metin}  {etiketler}".rstrip())
        print(f"     {not_.tarih}")


def _secenek_ayristirici() -> argparse.ArgumentParser:
    ayristirici = argparse.ArgumentParser(description="Kucuk not defteri")
    ayristirici.add_argument(
        "--dosya",
        default=str(VARSAYILAN_DOSYA),
        help="not dosyasi (varsayilan: notlar.json)",
    )
    alt = ayristirici.add_subparsers(dest="komut", required=True)

    p_ekle = alt.add_parser("ekle", help="yeni not ekle")
    p_ekle.add_argument("metin")
    p_ekle.add_argument("--etiket", action="append", default=[])

    p_listele = alt.add_parser("listele", help="notlari listele")
    p_listele.add_argument("--etiket")

    p_ara = alt.add_parser("ara", help="notlarda ara")
    p_ara.add_argument("kelime")

    p_sil = alt.add_parser("sil", help="notu sil")
    p_sil.add_argument("numara", type=int)

    return ayristirici


def main(argv: list[str] | None = None) -> int:
    args = _secenek_ayristirici().parse_args(argv)
    defter = NotDefteri(args.dosya)

    if args.komut == "ekle":
        numara = defter.ekle(args.metin, args.etiket)
        print(f"Eklendi: #{numara}")
    elif args.komut == "listele":
        _yazdir(defter.listele(args.etiket))
    elif args.komut == "ara":
        _yazdir(defter.ara(args.kelime))
    elif args.komut == "sil":
        silinen = defter.sil(args.numara)
        print(f"Silindi: {silinen.metin}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
