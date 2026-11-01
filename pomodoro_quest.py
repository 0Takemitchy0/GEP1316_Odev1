"""
Pomodoro Quest - Oyunlaştırılmış Çalışma Planlayıcı
GEP1316 Kodlama Okuryazarlığı - Ara Değerlendirme Ödevi 1

Oyun tasarımı öğrencileri ve küçük oyun ekipleri için komut satırı uygulaması.
Kullanıcı görev (quest) ekler, her görev için pomodoro (odaklı çalışma süresi)
kaydeder, çalıştıkça XP kazanır ve seviye atlar. Görevler gorevler.csv
dosyasına, rapor rapor.txt dosyasına kaydedilir.

Çalıştırma:  python pomodoro_quest.py
"""

import csv
import os
import sys
from datetime import datetime

# ---------- Sabitler ----------

# Görev kategorileri (liste): menüde numarayla seçilir
KATEGORILER = ["Ders", "Programlama", "Sanat", "Level Tasarımı", "Ses"]

TAMAMLAMA_BONUSU = 50  # bir görev bitince kazanılan ek XP
ALANLAR = ["ad", "kategori", "hedef", "oncelik", "tamamlanan", "dakika"]

# Dosyalar, programın bulunduğu klasöre kaydedilir
KLASOR = os.path.dirname(os.path.abspath(__file__))
GOREV_DOSYASI = os.path.join(KLASOR, "gorevler.csv")
RAPOR_DOSYASI = os.path.join(KLASOR, "rapor.txt")


# ---------- Girdi alma ve doğrulama ----------

def sayiya_cevir(metin, en_az, en_cok):
    """Metni tam sayıya çevirir. Sayı değilse veya aralık dışındaysa None döndürür."""
    try:
        sayi = int(metin.strip())
    except ValueError:
        return None
    if sayi < en_az or sayi > en_cok:
        return None
    return sayi


def sayi_al(mesaj, en_az, en_cok):
    """Geçerli bir tam sayı girilene kadar kullanıcıya sorar."""
    while True:
        sayi = sayiya_cevir(input(mesaj), en_az, en_cok)
        if sayi is not None:
            return sayi
        print(f"  ! Lütfen {en_az} ile {en_cok} arasında bir tam sayı girin.")


def metin_al(mesaj, en_uzun=40):
    """Boş olmayan ve en_uzun karakteri geçmeyen bir metin girilene kadar sorar."""
    while True:
        cevap = input(mesaj).strip()
        if cevap == "":
            print("  ! Bu alan boş bırakılamaz.")
        elif len(cevap) > en_uzun:
            print(f"  ! En fazla {en_uzun} karakter girebilirsiniz.")
        else:
            return cevap


# ---------- Hesaplamalar ----------

def toplam_xp(gorevler):
    """Her çalışılan dakika 1 XP, her tamamlanan görev ek bonus XP kazandırır."""
    xp = 0
    for gorev in gorevler:
        xp += gorev["dakika"]
        if gorev["tamamlanan"] >= gorev["hedef"]:
            xp += TAMAMLAMA_BONUSU
    return xp


def seviye_bul(xp):
    """XP miktarına göre oyuncunun unvanını döndürür."""
    if xp >= 1000:
        return "Efsane"
    elif xp >= 500:
        return "Usta"
    elif xp >= 200:
        return "Kalfa"
    elif xp >= 50:
        return "Çırak"
    else:
        return "Çaylak"


def ilerleme_cubugu(tamamlanan, hedef, genislik=10):
    """Örnek çıktı: [####------] 2/5"""
    dolu = min(tamamlanan, hedef) * genislik // hedef
    return "[" + "#" * dolu + "-" * (genislik - dolu) + f"] {tamamlanan}/{hedef}"


def kategori_ozeti(gorevler):
    """Her kategoride toplam kaç dakika çalışıldığını sözlük olarak döndürür."""
    ozet = {}
    for kategori in KATEGORILER:
        ozet[kategori] = 0
    for gorev in gorevler:
        ozet[gorev["kategori"]] += gorev["dakika"]
    return ozet


def oneri_uret(gorevler):
    """Sıradaki görev için bir öneri cümlesi üretir."""
    bitmemisler = [g for g in gorevler if g["tamamlanan"] < g["hedef"]]
    if len(gorevler) == 0:
        return "İlk görevini ekleyerek maceraya başla!"
    elif len(bitmemisler) == 0:
        return "Tüm görevler tamam! Yeni bir quest ekleme zamanı."
    else:
        # Önce önceliği yüksek (1), sonra kalan pomodorosu çok olan görev
        secilen = min(bitmemisler, key=lambda g: (g["oncelik"], g["tamamlanan"] - g["hedef"]))
        kalan = secilen["hedef"] - secilen["tamamlanan"]
        return (f"Sıradaki önerilen görev: {secilen['ad']} "
                f"(öncelik {secilen['oncelik']}, kalan {kalan} pomodoro)")


def rapor_olustur(gorevler):
    """Ekrana yazılan ve rapor.txt'ye kaydedilen rapor metnini hazırlar."""
    xp = toplam_xp(gorevler)
    toplam_dakika = sum(g["dakika"] for g in gorevler)
    satirlar = [
        "=" * 46,
        "        POMODORO QUEST - ÇALIŞMA RAPORU",
        "=" * 46,
        f"Tarih          : {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        f"Görev sayısı   : {len(gorevler)}",
        f"Toplam çalışma : {toplam_dakika} dk ({toplam_dakika / 60:.1f} saat)",
        f"Toplam XP      : {xp}",
        f"Unvan          : {seviye_bul(xp)}",
        "-" * 46,
        "Kategorilere göre çalışma süresi:",
    ]
    for kategori, dakika in kategori_ozeti(gorevler).items():
        satirlar.append(f"  {kategori:<16}{dakika:>5} dk")
    satirlar.append("-" * 46)
    satirlar.append("Öneri: " + oneri_uret(gorevler))
    satirlar.append("=" * 46)
    return "\n".join(satirlar)


# ---------- Dosya işlemleri ----------

def gorevleri_kaydet(gorevler, dosya=GOREV_DOSYASI):
    """Görev listesini CSV dosyasına yazar (utf-8-sig: Excel Türkçe karakterleri doğru gösterir)."""
    with open(dosya, "w", newline="", encoding="utf-8-sig") as f:
        yazici = csv.DictWriter(f, fieldnames=ALANLAR)
        yazici.writeheader()
        yazici.writerows(gorevler)


def gorevleri_yukle(dosya=GOREV_DOSYASI):
    """CSV dosyasındaki görevleri okur. Dosya yoksa boş liste, bozuk satırları atlar."""
    gorevler = []
    if not os.path.exists(dosya):
        return gorevler
    with open(dosya, newline="", encoding="utf-8-sig") as f:
        for satir in csv.DictReader(f):
            try:
                gorev = {
                    "ad": satir["ad"],
                    "kategori": satir["kategori"],
                    "hedef": int(satir["hedef"]),
                    "oncelik": int(satir["oncelik"]),
                    "tamamlanan": int(satir["tamamlanan"]),
                    "dakika": int(satir["dakika"]),
                }
            except (KeyError, TypeError, ValueError):
                print("  ! Dosyada bozuk bir satır atlandı.")
                continue
            if gorev["kategori"] not in KATEGORILER or gorev["hedef"] < 1:
                print("  ! Dosyada geçersiz bir görev atlandı.")
                continue
            gorevler.append(gorev)
    return gorevler


def raporu_kaydet(metin, dosya=RAPOR_DOSYASI):
    """Rapor metnini .txt dosyasına yazar."""
    with open(dosya, "w", encoding="utf-8") as f:
        f.write(metin + "\n")


# ---------- Menü işlemleri ----------

def gorev_ekle(gorevler):
    """Kullanıcıdan görev bilgilerini alıp listeye ekler."""
    print("\n--- Yeni Görev ---")
    ad = metin_al("Görev adı: ")
    for i, kategori in enumerate(KATEGORILER, start=1):
        print(f"  {i}) {kategori}")
    kategori = KATEGORILER[sayi_al("Kategori (1-5): ", 1, len(KATEGORILER)) - 1]
    hedef = sayi_al("Hedef pomodoro sayısı (1-12): ", 1, 12)
    oncelik = sayi_al("Öncelik (1=yüksek, 2=orta, 3=düşük): ", 1, 3)
    gorevler.append({"ad": ad, "kategori": kategori, "hedef": hedef,
                     "oncelik": oncelik, "tamamlanan": 0, "dakika": 0})
    print(f"  + '{ad}' eklendi.")


def gorevleri_listele(gorevler):
    """Görevleri biçimli bir tablo halinde ekrana yazar."""
    if len(gorevler) == 0:
        print("\n  Henüz görev yok. Menüden 1'i seçerek ekleyebilirsin.")
        return
    print(f"\n{'No':<4}{'Görev':<22}{'Kategori':<16}{'Önc.':<6}{'İlerleme':<18}{'Süre':>6}")
    print("-" * 72)
    for i, g in enumerate(gorevler, start=1):
        # Uzun adlar sütuna sığsın diye kısaltılır, kesildiği "..." ile belli olur
        ad = g["ad"] if len(g["ad"]) <= 21 else g["ad"][:18] + "..."
        print(f"{i:<4}{ad:<22}{g['kategori']:<16}{g['oncelik']:<6}"
              f"{ilerleme_cubugu(g['tamamlanan'], g['hedef']):<18}{g['dakika']:>4} dk")


def pomodoro_kaydet(gorevler):
    """Seçilen göreve bir pomodoro ve çalışılan süreyi ekler."""
    if len(gorevler) == 0:
        print("\n  Önce bir görev eklemelisin.")
        return
    gorevleri_listele(gorevler)
    gorev = gorevler[sayi_al(f"Görev no (1-{len(gorevler)}): ", 1, len(gorevler)) - 1]
    if gorev["tamamlanan"] >= gorev["hedef"]:
        print("  Bu görev zaten tamamlanmış.")
        return
    sure = sayi_al("Kaç dakika çalıştın? (5-60): ", 5, 60)
    eski_unvan = seviye_bul(toplam_xp(gorevler))
    gorev["tamamlanan"] += 1
    gorev["dakika"] += sure
    print(f"  +{sure} XP!  {ilerleme_cubugu(gorev['tamamlanan'], gorev['hedef'])}")
    if gorev["tamamlanan"] == gorev["hedef"]:
        print(f"  *** Görev tamamlandı! +{TAMAMLAMA_BONUSU} bonus XP ***")
    yeni_unvan = seviye_bul(toplam_xp(gorevler))
    if yeni_unvan != eski_unvan:
        print(f"  >>> SEVİYE ATLADIN: {eski_unvan} -> {yeni_unvan} <<<")


def kaydet(gorevler):
    """Görevleri CSV'ye, raporu TXT'ye kaydeder."""
    gorevleri_kaydet(gorevler)
    raporu_kaydet(rapor_olustur(gorevler))
    print(f"  Kaydedildi: {os.path.basename(GOREV_DOSYASI)}, {os.path.basename(RAPOR_DOSYASI)}")


def menu_goster():
    print("\n===== POMODORO QUEST =====")
    print("1) Görev ekle")
    print("2) Görevleri listele")
    print("3) Pomodoro kaydet")
    print("4) Rapor göster")
    print("5) Kaydet")
    print("6) Kaydet ve çık")


def main():
    gorevler = gorevleri_yukle()
    print(f"Hoş geldin! {len(gorevler)} görev yüklendi.")
    while True:
        menu_goster()
        secim = input("Seçimin: ").strip()
        if secim == "1":
            gorev_ekle(gorevler)
        elif secim == "2":
            gorevleri_listele(gorevler)
        elif secim == "3":
            pomodoro_kaydet(gorevler)
        elif secim == "4":
            print("\n" + rapor_olustur(gorevler))
        elif secim == "5":
            kaydet(gorevler)
        elif secim == "6":
            kaydet(gorevler)
            print("Görüşmek üzere, iyi çalışmalar!")
            break
        else:
            print("  ! Geçersiz seçim, 1-6 arasında bir sayı girin.")


if __name__ == "__main__":
    # Windows'ta girdi/çıktı dosyadan veya başka programdan yönlendirildiğinde
    # Türkçe karakterler bozulmasın diye kodlamayı UTF-8'e sabitliyoruz
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C veya girdinin aniden bitmesi durumunda program çökmeden kapanır
        print("\nProgram kapatıldı (kaydedilmemiş değişiklikler kayboldu).")
