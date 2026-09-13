# Haftalık Akış — Her Hafta Ne Yapacaksınız?

**AI-Assisted Software Development · Atlas Üniversitesi · 2026–2027 Güz**

Bu dosya dönem boyunca değişmeyen düzeni anlatır. Her haftanın **içeriği** farklı
olacak — ödev metni LMS'te yayınlanır — ama **akış** hep aynıdır. Tıkandığınızda
buraya dönün.

---

## Kısa özet

| Ne zaman | Ne yaparsınız | Kaç puan |
|----------|---------------|----------|
| Dersten önce | Ödev metnini okursunuz | — |
| Derste (3 saat) | `WEEK` dosyasını ayarlar, çalışır, push edersiniz | 3 |
| Ders sonunda | Son bir push — hoca o anki durumu dondurur | ↑ aynı 3 puan |
| Ders bitiminden sonraki 24 saat | Kalanları bitirir, `ai_log.md`'yi yazarsınız | 4 |
| Her hafta | `ai_log.md` kalitesi ve commit düzeni | 3 |

Haftalık toplam **10 puan**. Haftalık notlarınızın ortalaması dönem notunun
**%70'ini** oluşturur; kalan %30 final projesidir.

**Teslim süresi ders bitiminden sonraki 24 saattir** — bir sonraki hafta değil.
Bu süre bilerek kısa: işin büyük kısmı derste, soru sorabildiğiniz ortamda bitsin;
akşam kalan boşlukları kapatmak için, sıfırdan başlamak için değil.

---

## 1. Dersten önce

Ödev metnini LMS'ten okuyun. O haftanın tam olarak hangi dosyaları istediği orada
yazar. Ön okuma verilmişse (Hafta 1'de iki doküman var) derse gelmeden okuyun —
derste anlatılan 20 dakika, okuduğunuz şeyin özetidir. Okumadan gelirseniz o 20
dakika size bir şey ifade etmez.

---

## 2. Derste

### Önce `WEEK` dosyasını ayarlayın

Repo kökündeki `WEEK` dosyası, otomatik kontrolün hangi haftaya bakacağını söyler.
Haftaya başlarken güncelleyin:

```bash
echo 3 > WEEK        # 3. hafta için
```

Bunu yapmazsanız kontroller o haftanın dosyalarına hiç bakmaz ve ders sonunda
puanınız sıfır görünür.

### Çalışın ve sık sık push edin

Tek bir dev commit yerine, iş parça parça ilerledikçe commit edin. Commit mesajı
ne yaptığınızı söylesin:

```bash
git add .
git commit -m "week03: llm_client ollama backend calisiyor"
git push
```

`"update"`, `"fix"`, `"asdf"` gibi mesajlar commit düzeni puanını götürür.

### Kontrolleri kendiniz çalıştırın

Push etmeden önce, hocanın çalıştıracağı kontrollerin **aynısını** çalıştırabilirsiniz:

```bash
python .github/check_deliverables.py
```

Çıktı eksiklerinizi tek tek yazar. Bu bir not değil, yapılacaklar listesidir.

### Ders bitmeden son push'unuzu yapın

Ders sonunda hoca bütün repoları o anki hâliyle dondurur ve kontrolleri çalıştırır.
O anda push edilmemiş çalışma **görünmez** — bilgisayarınızda durur ama sayılmaz.

Sonuç, isimsiz bir tabloyla sınıfta yansıtılır; kendi satırınızı `student.json`
içindeki takma adınızdan bulursunuz. Bu tablo **3 puanlıktır**.

---

## 3. Ders bittikten sonra — 24 saat

Haftanın kalan işlerini **ders bitiminden sonraki 24 saat içinde** bitirin. Bu süre dolduğunda hoca ikinci bir anlık görüntü alır; o andaki hâliniz 4 puanlık kısmı belirler.

### `ai_log.md` — atlamayın

Repo kökündeki tek dosya, 12 haftanın hepsi için bölümleri hazır. O haftanın
bölümünü doldurun: AI'ı ne için kullandınız, ne doğru yaptı, **neyi düzeltmek
zorunda kaldınız**, ne öğrendiniz.

Bu dosya 2 puanlık ve insan tarafından okunuyor. "AI çok yardımcı oldu" yazan bir
kayıt puan getirmez. Somut bir hata ve onu nasıl fark edip düzelttiğiniz gerekir.
Dersin asıl öğrettiği şey bu.

### Kontroller yeşil yanana kadar devam edin

```bash
python .github/check_deliverables.py
git add .
git commit -m "week03: model_notes tamamlandi"
git push
```

GitHub'da reponuzun **Actions** sekmesinde her push'un sonucunu görürsünüz. Yeşil
tik, o haftanın otomatik kısmının tamam olduğu anlamına gelir — 4 puan.

---

## 4. Her hafta geçerli kurallar

**API anahtarı asla koda yazılmaz.** `.env` dosyasında durur, `.env` de
`.gitignore` içindedir. Repoya anahtar giderse otomatik tarama yakalar ve
**10 puan** kesilir. Anahtar bir kez GitHub'a gittiyse silmek yetmez — o anahtarı
iptal edip yenisini almanız gerekir.

**Kod temiz olmalı.** Push etmeden önce:

```bash
ruff check .          # sorunlari listeler
ruff check . --fix    # duzeltilebilenleri duzeltir
ruff format .         # bicimlendirir
```

AI'ın ürettiği kod sıklıkla kullanılmayan `import` bırakır; `ruff` bunu anında
yakalar.

**Geçmiş haftalar bozulmamalı.** Kontroller kümülatiftir: 5. haftadayken 1–4 arası
da yeniden denetlenir. Bir değişiklik eski bir şeyi bozarsa CI size söyler.

---

## Takıldığınızda

**CI kırmızı yandı, neden anlamıyorum.** GitHub'da **Actions** sekmesine girin,
kırmızı çalıştırmaya tıklayın. Hangi kontrolün neden düştüğü satır satır yazar.
Aynısını yerelde `python .github/check_deliverables.py` ile de görebilirsiniz.

**Kontroller yerelde geçiyor ama GitHub'da geçmiyor.** Genellikle push etmediğiniz
bir dosya vardır. `git status` ile bakın.

**`ruff` yerelde temiz, CI'da değil.** Sürüm farkıdır. `requirements/week09.txt`
içindeki sürümü kurun, kendi kurduğunuz başka bir sürümü değil.

**Ollama çalışmıyor / model inmiyor.** Makineniz yetmiyorsa daha küçük modele geçin.
Hiçbiri olmuyorsa bulut API'siyle devam edin ve nedenini `model_notes.md`'ye yazın —
bu kabul edilebilir bir sonuçtur, haftayı buna kurban etmeyin.

**Bir şeyi bozdum, geri alamıyorum.** Panik yapmayın, git her şeyi hatırlıyor:

```bash
git log --oneline           # commit gecmisi
git diff                    # su an ne degismis
git checkout -- dosya.py    # bir dosyayi son commit'e dondur
```

**Hâlâ tıkalıysanız** derste sorun, ya da AI'a sorun — ama AI'ın verdiği cevabı
doğrulayın ve bu alışverişi `ai_log.md`'ye yazın. Bu dersin konusu tam olarak budur.

---

## Komut özeti

```bash
# haftaya baslarken
echo N > WEEK

# calisirken
python .github/check_deliverables.py     # eksiklerimi goster
ruff check . --fix                       # kodu temizle
git add . && git commit -m "weekNN: ..." && git push

# ortam
source .venv/bin/activate                # Windows: .venv\Scripts\activate
streamlit run app.py
```
