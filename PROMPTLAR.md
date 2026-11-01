# YZ ile Çalışma Günlüğü (PROMPTLAR.md)

**Öğrenci:** Ege Dişkaya (2202420)
**Kullanılan araç:** Claude (Anthropic), Claude Code masaüstü uygulaması
**Tarih:** 1 Kasım 2026

Aşağıdaki promptlar projede YZ'ye verdiğim gerçek komutlardır. Her birinin altında YZ'nin ne yaptığını ve benim kararımı yazdım.

---

## Prompt 1: Ödevi analiz ettirme ve planlama

**Prompt:** Ödev PDF'ini ekleyip: *"Hocamızdan bir ödev geldi ve bunu sana yaptıracağım, detayları iletiyorum, beraber planlayalım."*

**YZ'nin yanıtı:** PDF'teki 14 gereksinimi özetledi ve 6 adımlık bir plan önerdi (konu → akış şeması → kod → test → belgeler → GitHub). Sözlü doğrulama yapılacağı ve prompt günlüğünün gerçek olması gerektiği konusunda uyardı. Konu, bölüm ve kapsam için seçenekli sorular sordu.

**Kararım:** ✅ Kabul. Plan, hocanın önerdiği zaman planıyla uyumluydu.

---

## Prompt 2: Konu ve bölüm seçimi

**Prompt:** Seçeneklerden *"Çalışma planı + pomodoro"* konusunu seçtim, bölümümü *"Dijital Oyun Tasarımı"* olarak yazdım, kapsam olarak da "hepsi"ni seçtim.

**YZ'nin yanıtı:** Konuyu bölümüme göre uyarladı ve "Pomodoro Quest" adında, XP ve seviye sistemi olan, oyunlaştırılmış bir planlayıcı önerdi. Kategoriler Ders, Programlama, Sanat, Level Tasarımı ve Ses oldu. Verilerin sözlük listesinde tutulmasını önerdi.

**Kararım:** ✅ Kabul. Oyunlaştırma bölümümle doğrudan ilgili. XP eşikleri de if/elif/else için doğal bir örnek oluşturuyor.

---

## Prompt 3: Kodun yazılması

**Prompt:** *"Evet, başla"* (önerilen tasarımın onayı)

**YZ'nin yanıtı:** `pomodoro_quest.py` (18 fonksiyon) ve `test_pomodoro_quest.py` (19 test) dosyalarını yazdı ve testleri çalıştırdı, hepsi geçti. Ardından programı hatalı girdilerle uçtan uca çalıştırdı.

**Kararım:** ✏️ Düzenleyerek kabul (bkz. Prompt 3a).

### Prompt 3a: YZ'nin eksik ürettiği nokta: Türkçe karakter hatası ⚠️

**Ne oldu?** Birim testlerin hepsi geçmesine rağmen, program girdileri yönlendirilerek (pipe ile) çalıştırıldığında `gorevler.csv` dosyasına şu kaydedildi:

```
Boss savaÅŸÄ± mekaniÄŸi,Programlama,4,1,2,55      ← olması gereken: Boss savaşı mekaniği
```

**Nasıl yakalandı?** Testler yalnızca fonksiyonları doğrudan çağırıyordu. Klavye girdisinin programa nasıl ulaştığını hiç test etmiyordu. Hata, programın gerçek bir çalıştırmasının ardından **oluşan CSV dosyasının içeriğine bakınca** ortaya çıktı.

**Sebep:** Windows, yönlendirilen girdiyi UTF-8 yerine eski Türkçe kod sayfasıyla (cp1254) okuyor. YZ'nin ilk ürettiği kod bu durumu hesaba katmamıştı.

**Düzeltme:** Programın başına şu iki satır eklendi:

```python
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
```

Tekrar çalıştırınca CSV doğru kaydedildi. Program kapatılıp açıldığında görevler de doğru yüklendi.

**Ders:** "Testler geçti" demek "program doğru çalışıyor" demek değil. Çıktı dosyalarını da kontrol etmek gerekiyor.

---

## Prompt 4: Kodu anlamak için açıklama isteme

**Prompt:** *"Kodu bana açıkla"*

**YZ'nin yanıtı:** Kodu bölüm bölüm açıkladı: sabitler, doğrulama (`try/except`, `None`), sözlük listesi, hesaplamalar, dosya işlemleri, menü ve `if __name__ == "__main__"`. Özellikle şu noktaları vurguladı:
- `seviye_bul` içindeki koşulların neden büyükten küçüğe sıralandığı
- `//` (tam sayı bölmesi) ile ilerleme çubuğu hesabı
- `oneri_uret` içindeki `min(..., key=lambda ...)` satırı
- Kullanıcı "1" yazınca neden `gorevler[0]` seçildiği

Sonunda sözlü sınavda sorulabilecek 5 soru listeledi.

**Kararım:** ✅ Kabul. Açıklamanın en faydalı kısmı, kodun "neden böyle yazıldığını" anlatan yerlerdi. Örneğin if/elif sırası küçükten büyüğe olsaydı 1000 XP'li birinin "Çırak" çıkacağını öğrendim. En zor bulduğum satır `min(..., key=lambda ...)` satırıydı.

---

## Prompt 5: Kalan işleri planlama

**Prompt:** *"Şimdi ne yapmamız gerekiyor, ne kaldı?"*

**YZ'nin yanıtı:** Biten işleri ve kalan 7 adımı (promptlar, ekran görüntüleri, yansıtma, kişisel bilgiler, GitHub, son kontrol, teslim) kim yapacağı ve tahmini süreleriyle bir tablo halinde listeledi.

**Kararım:** ✅ Kabul. Teslim tarihine kadar neyin eksik olduğunu net gördüm.

---

## Prompt 6: Ekran görüntüleri ve kalan kısımlar ⚠️ YZ hatası

**Prompt:** *"Ege Dişkaya, öğrenci no: 2202420. SS almak için PowerShell'de programı çalıştır ve kalan kısımları da kendine göre yaz."*

**YZ'nin yanıtı (1. deneme, hatalı):** YZ, bir PowerShell penceresi açıp programa klavye tuşlarını "simüle ederek" (SendKeys) girdi göndermeye çalıştı. Ancak tuşlar, o anda ekranın önündeki pencereye gönderiliyordu. Yeni açılan PowerShell penceresi zamanında öne gelmediği için tuşlar benim açık olan **mesajlaşma uygulamama** gitti. Bir grup sohbetine "Boss savaşı mekaniği", "2", "4", "1" gibi mesajlar gönderildi.

**Nasıl yakalandı?** YZ'nin aldığı ilk ekran görüntüsünde program yerine mesajlaşma uygulaması görünüyordu. YZ bunu görünce işlemi durdurdu, özel sohbet içeren görüntüyü sildi, açtığı pencereyi kapattı ve bana durumu açıkça bildirdi. Gönderilen mesajları ben sildim.

**Kararım:** ❌ İlk yöntemi **reddettim**. *"Güvenli yöntemle dene"* diyerek tuşların klavye üzerinden değil, doğrudan programın kendi konsoluna yazılmasını istedim.

**YZ'nin yanıtı (2. deneme):** Tuşları `WriteConsoleInput` ile sadece o konsolun girdi tamponuna yazdı ve ekran görüntüsünü sadece o pencereden (`PrintWindow`) aldı. Ayrıca bir güvenlik kontrolü ekledi: pencere programın kendi penceresi değilse işlem iptal ediliyordu. Bu kontrol ilk denemede gerçekten devreye girip işlemi durdurdu, kontrol düzeltilince 5 ekran görüntüsü sorunsuz alındı.

**Ders:** YZ'ye bilgisayarımda işlem yaptırırken, ne yaptığını ve bunun başka uygulamaları etkileyip etkilemeyeceğini sorgulamam gerekiyor. "Ekran görüntüsü al" gibi basit görünen bir istek bile yanlış yöntemle yapılınca gerçek bir zarara yol açabiliyor.

**Bu prompttaki diğer işler:** YZ, listede uzun görev adlarının 21. karakterde habersizce kesilmesini düzeltti. Artık ad kesildiğinde sonuna `...` ekleniyor (`Vize: Kodlama Okur...`). PROMPTLAR, rapor ve yansıtma taslağını da bu prompt üzerine yazdı.

**Kararım:** ✏️ Düzenleyerek kabul. Yansıtma taslağını okuyup kendi düşüncelerime göre düzenledim.

---

## Özet tablo

| # | Prompt (kısa) | Karar | Gerekçe |
|---|---|---|---|
| 1 | Ödevi analiz et, planla | Kabul | Plan, hocanın zaman planıyla uyumlu |
| 2 | Konu: pomodoro + oyun tasarımı | Kabul | Bölümümle ilgili, if/elif için doğal örnek |
| 3 | Kodu yaz | Düzenleyerek kabul | Testler geçti ama Türkçe karakter hatası çıktı |
| 4 | Kodu bana açıkla | Kabul | Sözlü sınava hazırlık; "neden" sorularını cevapladı |
| 5 | Ne kaldı? | Kabul | Kalan işler netleşti |
| 6 | SS al, kalanları yaz | 1. yöntem **red**, 2. yöntem kabul | İlk yöntem tuşları yanlış uygulamaya gönderdi |
