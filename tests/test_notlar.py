"""notlar.py icin birim testleri (sadece standart kutuphane)."""

import json
import tempfile
import unittest
from pathlib import Path

from notlar import Not, NotDefteri, main


class NotDefteriTestleri(unittest.TestCase):
    def setUp(self) -> None:
        self.klasor = tempfile.TemporaryDirectory()
        self.dosya = Path(self.klasor.name) / "notlar.json"
        self.defter = NotDefteri(self.dosya)

    def tearDown(self) -> None:
        self.klasor.cleanup()

    def test_baslangicta_bos(self):
        self.assertEqual(self.defter.listele(), [])

    def test_ekle_numara_dondurur(self):
        self.assertEqual(self.defter.ekle("ilk"), 1)
        self.assertEqual(self.defter.ekle("ikinci"), 2)

    def test_ekle_dosyaya_yazar_ve_geri_okur(self):
        self.defter.ekle("kalici not", ["git"])
        yeniden = NotDefteri(self.dosya)
        self.assertEqual(len(yeniden.listele()), 1)
        self.assertEqual(yeniden.listele()[0].etiketler, ["git"])

    def test_bos_not_reddedilir(self):
        with self.assertRaises(ValueError):
            self.defter.ekle("   ")

    def test_sil_kaydi_kaldirir(self):
        self.defter.ekle("a")
        self.defter.ekle("b")
        silinen = self.defter.sil(1)
        self.assertEqual(silinen.metin, "a")
        self.assertEqual([n.metin for n in self.defter.listele()], ["b"])

    def test_sil_gecersiz_numarada_hata(self):
        with self.assertRaises(IndexError):
            self.defter.sil(5)

    def test_ara_metin_ve_etiket(self):
        self.defter.ekle("Git ogrendim", ["ogrenme"])
        self.defter.ekle("Alisveris listesi")
        self.assertEqual(len(self.defter.ara("git")), 1)
        self.assertEqual(len(self.defter.ara("alisveris")), 1)
        self.assertEqual(len(self.defter.ara("ogrenme")), 1)
        self.assertEqual(len(self.defter.ara("yok")), 0)

    def test_etiketle_filtrele(self):
        self.defter.ekle("a", ["x"])
        self.defter.ekle("b", ["y"])
        sonuc = self.defter.listele("x")
        self.assertEqual([n.metin for n in sonuc], ["a"])

    def test_bozuk_json_cokertmez(self):
        self.dosya.write_text("{bozuk", encoding="utf-8")
        self.assertEqual(NotDefteri(self.dosya).listele(), [])

    def test_tarih_otomatik_atilir(self):
        not_ = Not(metin="tarihsiz")
        self.assertTrue(not_.tarih)


class KomutSatiriTestleri(unittest.TestCase):
    def test_ekle_ve_listele_akisi(self):
        with tempfile.TemporaryDirectory() as klasor:
            dosya = str(Path(klasor) / "n.json")
            self.assertEqual(main(["--dosya", dosya, "ekle", "deneme"]), 0)
            self.assertEqual(main(["--dosya", dosya, "listele"]), 0)
            veri = json.loads(Path(dosya).read_text(encoding="utf-8"))
            self.assertEqual(veri[0]["metin"], "deneme")


if __name__ == "__main__":
    unittest.main()
