"""
Pomodoro Quest otomatik testleri.
Çalıştırma:  python -m unittest -v test_pomodoro_quest.py
"""

import os
import tempfile
import unittest

import pomodoro_quest as pq


def ornek_gorev(ad="Karakter çizimi", kategori="Sanat", hedef=4, oncelik=2,
                tamamlanan=0, dakika=0):
    return {"ad": ad, "kategori": kategori, "hedef": hedef, "oncelik": oncelik,
            "tamamlanan": tamamlanan, "dakika": dakika}


class GirdiDogrulamaTestleri(unittest.TestCase):
    def test_gecerli_sayi(self):
        self.assertEqual(pq.sayiya_cevir("5", 1, 12), 5)

    def test_bosluklu_sayi(self):
        self.assertEqual(pq.sayiya_cevir("  3 ", 1, 3), 3)

    def test_harf_girilirse(self):
        self.assertIsNone(pq.sayiya_cevir("abc", 1, 12))

    def test_bos_girdi(self):
        self.assertIsNone(pq.sayiya_cevir("", 1, 12))

    def test_ondalikli_sayi(self):
        self.assertIsNone(pq.sayiya_cevir("2.5", 1, 12))

    def test_aralik_disi_ust_sinir(self):
        self.assertIsNone(pq.sayiya_cevir("13", 1, 12))

    def test_aralik_disi_negatif(self):
        self.assertIsNone(pq.sayiya_cevir("-1", 1, 12))

    def test_sinir_degerleri_kabul(self):
        self.assertEqual(pq.sayiya_cevir("1", 1, 12), 1)
        self.assertEqual(pq.sayiya_cevir("12", 1, 12), 12)


class HesaplamaTestleri(unittest.TestCase):
    def test_seviye_sinirlari(self):
        self.assertEqual(pq.seviye_bul(0), "Çaylak")
        self.assertEqual(pq.seviye_bul(49), "Çaylak")
        self.assertEqual(pq.seviye_bul(50), "Çırak")
        self.assertEqual(pq.seviye_bul(200), "Kalfa")
        self.assertEqual(pq.seviye_bul(500), "Usta")
        self.assertEqual(pq.seviye_bul(1000), "Efsane")

    def test_xp_bonus_dahil(self):
        gorevler = [ornek_gorev(hedef=2, tamamlanan=2, dakika=50),  # bitti: 50 + 50
                    ornek_gorev(hedef=3, tamamlanan=1, dakika=25)]  # bitmedi: 25
        self.assertEqual(pq.toplam_xp(gorevler), 125)

    def test_ilerleme_cubugu(self):
        self.assertEqual(pq.ilerleme_cubugu(0, 4), "[----------] 0/4")
        self.assertEqual(pq.ilerleme_cubugu(2, 4), "[#####-----] 2/4")
        self.assertEqual(pq.ilerleme_cubugu(4, 4), "[##########] 4/4")

    def test_kategori_ozeti(self):
        gorevler = [ornek_gorev(kategori="Sanat", dakika=30),
                    ornek_gorev(kategori="Sanat", dakika=20),
                    ornek_gorev(kategori="Ses", dakika=25)]
        ozet = pq.kategori_ozeti(gorevler)
        self.assertEqual(ozet["Sanat"], 50)
        self.assertEqual(ozet["Ses"], 25)
        self.assertEqual(ozet["Programlama"], 0)

    def test_oneri_bos_liste(self):
        self.assertIn("İlk görevini", pq.oneri_uret([]))

    def test_oneri_oncelikli_gorev(self):
        gorevler = [ornek_gorev(ad="Ses efekti", oncelik=3),
                    ornek_gorev(ad="Vize çalış", oncelik=1)]
        self.assertIn("Vize çalış", pq.oneri_uret(gorevler))

    def test_oneri_hepsi_bitti(self):
        gorevler = [ornek_gorev(hedef=1, tamamlanan=1)]
        self.assertIn("Tüm görevler tamam", pq.oneri_uret(gorevler))


class DosyaTestleri(unittest.TestCase):
    def setUp(self):
        self.klasor = tempfile.mkdtemp()
        self.dosya = os.path.join(self.klasor, "gorevler.csv")

    def test_kaydet_ve_yukle_turkce(self):
        gorevler = [ornek_gorev(ad="Şehir haritası çiz, ışıklandır", kategori="Level Tasarımı",
                                tamamlanan=2, dakika=50)]
        pq.gorevleri_kaydet(gorevler, self.dosya)
        self.assertEqual(pq.gorevleri_yukle(self.dosya), gorevler)

    def test_dosya_yoksa_bos_liste(self):
        self.assertEqual(pq.gorevleri_yukle(os.path.join(self.klasor, "yok.csv")), [])

    def test_bozuk_satir_atlanir(self):
        with open(self.dosya, "w", encoding="utf-8-sig") as f:
            f.write("ad,kategori,hedef,oncelik,tamamlanan,dakika\n")
            f.write("Sağlam görev,Ses,2,1,0,0\n")
            f.write("Bozuk görev,Ses,iki,1,0,0\n")    # hedef sayı değil
            f.write("Sıfır hedef,Ses,0,1,0,0\n")       # hedef 0 olamaz
            f.write("Bilinmeyen,Müzik,2,1,0,0\n")      # kategori listede yok
        gorevler = pq.gorevleri_yukle(self.dosya)
        self.assertEqual(len(gorevler), 1)
        self.assertEqual(gorevler[0]["ad"], "Sağlam görev")

    def test_rapor_kaydedilir(self):
        rapor_dosyasi = os.path.join(self.klasor, "rapor.txt")
        pq.raporu_kaydet(pq.rapor_olustur([ornek_gorev(dakika=25, tamamlanan=1)]), rapor_dosyasi)
        with open(rapor_dosyasi, encoding="utf-8") as f:
            icerik = f.read()
        self.assertIn("Toplam XP      : 25", icerik)


if __name__ == "__main__":
    unittest.main()
