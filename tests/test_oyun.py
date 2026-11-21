"""oyun.py icin hafif testler: git deposuna ihtiyac duymaz."""

import unittest

import oyun


class SeviyeTestleri(unittest.TestCase):
    def test_on_level_var(self):
        self.assertEqual(len(oyun.SEVIYELER), 10)

    def test_numaralar_tekil_ve_sirali(self):
        numaralar = [s["no"] for s in oyun.SEVIYELER]
        self.assertEqual(numaralar, list(range(1, 11)))

    def test_her_levelde_gerekli_alanlar_var(self):
        for s in oyun.SEVIYELER:
            for alan in ("ad", "xp", "amac", "olcut", "gorev", "ipucu", "kontrol"):
                self.assertIn(alan, s, f"level {s.get('no')} alani eksik: {alan}")
            self.assertGreater(s["xp"], 0)
            self.assertTrue(callable(s["kontrol"]))
            self.assertTrue(s["gorev"])

    def test_toplam_xp_1550(self):
        self.assertEqual(oyun.toplam_xp(), 1550)


class RutbeTestleri(unittest.TestCase):
    def test_baslangic_caylak(self):
        self.assertEqual(oyun.rutbe(0)[0], "Caylak")

    def test_esikler(self):
        self.assertEqual(oyun.rutbe(99)[0], "Caylak")
        self.assertEqual(oyun.rutbe(100)[0], "Ogrenci")
        self.assertEqual(oyun.rutbe(450)[0], "Kalfa")
        self.assertEqual(oyun.rutbe(1550)[0], "Git Ustasi")

    def test_cubuk_her_zaman_24_parca(self):
        for xp in (0, 50, 700, 1550):
            cubuk = oyun.xp_cubugu(xp)
            self.assertEqual(cubuk.count("█") + cubuk.count("░"), 24)


if __name__ == "__main__":
    unittest.main()
