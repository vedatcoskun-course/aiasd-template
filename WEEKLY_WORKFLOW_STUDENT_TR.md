# Haftalık İş Akışı — Her Hafta Ne Yaparsınız

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027**

**Sürüm 1 · 20 Eylül 2026** — bu belge dönem içinde yenilenir. Her haftanın dosyalarını
çektiğinizde onlarla birlikte gelir; dolayısıyla pull yapmayı sürdürdüğünüz sürece
deponuzdaki kopya günceldir.

> [!IMPORTANT]
> **Bu sürümde ne değişti**
>
> Henüz hiçbir şey — bu ilk sürüm. Belgeyi yenilediğimde bu kutu neyin değiştiğini
> listeler ve değişen başlıkların yanında **`↻ changed in v2`** işareti olur. İkisi de
> bir sonraki sürümde kaybolur; dolayısıyla işaretli olan her şey sizin için yenidir.

Bu belge değişmeyen rutini anlatır. Her haftanın *içeriği* farklıdır — ödev o haftanın
klasöründe gelir — ama *ritim* hep aynıdır.
Takıldığınızda buraya dönün.

---

## Bir bakışta

| Ne zaman | Ne yaparsınız | Puan |
|------|-------------|--------|
| Dersten önce | `weekNN/ASSIGNMENT_NN_TR.md` dosyasını okuyun | — |
| Ders sırasında (3 saat) | Çalışın ve sık push edin | — |
| Ders sonunda | Son bir push — durumu donduruyorum | 5 |
| Dersten sonra | Kalanı bitirin, `ai_log_NN.md` yazın | — |
| Cumartesi 23:59'a kadar | **Yeniden push edin.** Durumu ikinci kez donduruyorum | 5 |

Haftada on puan, iki ana eşit bölünmüş: **beşi dersin sonunda, beşi Cumartesi teslim
saatinde ölçülür.** İkisi de GitHub'dan okunur, dolayısıyla ikisi de push ister.
**1. Hafta tek istisnadır:** beş puan değerindedir, ilk dersin sonunda hiçbir şey
okunmaz ve beşinin tamamı Cumartesi 23:59'da deponuzdan okunur. Bitmiş ama push
edilmemiş iş, hiç yapılmamış işle tamamen aynı puanı alır.

Haftanın notunun yarısının derse bağlı olması bilinçli. İşin yeri burası — sınıfta,
hâlâ soru sorabilirken. Diğer yarısı bitirmeye ve bir denetleyicinin göremeyeceği iki
şeye dayanır.

**Teslim saati her hafta aynıdır: Cumartesi 23:59.** Hesaplanacak bir şey yok —
Cumartesi gece yarısı deponuzda ne varsa onu notlandırıyorum. İşin çoğu, soru
sorabileceğiniz laboratuvarda yapılmalı; sonraki günler başlamak için değil, açıkları
kapatmak içindir.

---

## Bir kez, bir daha asla

İlk ders başlamadan üç şey doğru olmalı ve hiçbiri dersin kendisi değil: (a) bir GitHub
hesabı, (b) deponuz ve (c) ona push etmesine izin verilen bir bilgisayar. Gerekli
komutlar [**Kurulum Kartı**](SETUP_CARD_TR.md)'nda — dört adım, ve sonuncusu diğer
üçünün çalışıp çalışmadığını söyler.

Kart ayrıca en çok karşılaşacağınız hataların ve her birinin gerçekte ne anlama
geldiğinin tablosunu taşır. Açık tutun; mekanik için muhtemelen ihtiyacınız olan tek
sayfa odur.

---

## 1. O haftanın dersinden önce

`weekNN/ASSIGNMENT_NN_TR.md` dosyasını okuyun — haftanın klasörüyle birlikte gelir ve o
haftanın tam olarak hangi dosyaları istediğini listeler.

Ön okuma varsa gelmeden önce okuyun.

---

## 2. Ders sırasında

### Hangi yarıda çalıştığınızı bilin

Deponuzun kökünden çalıştırın:

```bash
python .github/check_deliverables.py
```

İki parça hâlinde yanıt verir:

```
In the lab:     11 of 14 done
By Saturday:     0 of  3 done
```

İki sayı haftadan haftaya değişir; önemli olan hangi satırı okuduğunuzdur.

**In the lab**, dersin sonunda okuduğum kısımdır — haftanın notunun yarısı. Bunlar,
benimle ve aynı yerde takılmış yirmi dokuz kişiyle aynı odadayken yapmaya değer
şeylerdir.

**By Saturday** gerisidir: yazılar, diyagramlar, `ai_log_NN.md`. Gerçekten yalnız
yapılan iş. Hafta içinde çalıştırmayı başarısız kılmaz, çünkü henüz teslim vakti
gelmemiştir — ama o da notun yarısıdır ve Cumartesi anlık görüntüsü onu okur.

Kendinizi laboratuvarda `ai_log_NN.md` yazarken bulursanız haftayı tersten
yaşıyorsunuz demektir.

### Çalışın ve sık push edin

Sonda tek devasa yığın yerine iş ilerledikçe commit edin. Mesaj ne yaptığınızı
söylemeli:

```bash
git add .
git commit -m "week01: hello.py reads a name and prints the list"
git push
```

"update", "fix" ya da "asdf" gibi mesajlar commit disiplini puanına mal olur.

### Kontrolleri kendiniz çalıştırın

Aynı komut, istediğiniz kadar:

```bash
python .github/check_deliverables.py
```

Bunlar tam olarak benim çalıştıracağım kontrollerdir. Çıktı, eksik olanları satır satır
listeler. Bir not değil, yapılacaklar listesidir ve çalıştırmanın maliyeti yoktur.

### Ders bitmeden bir kez daha push edin

Dersin sonunda her depoyu olduğu gibi dondurup kontrolleri çalıştırıyorum. Push
etmediğiniz iş görünmezdir — bilgisayarınızda durur ve sayılmaz.

Sonuç anonimleştirilmiş bir tablo olarak yansıtılır; satırınızı `student.json`
içindeki takma adınızla bulun. O tablo **5 puan — haftanın yarısı** değerindedir.

### Devam, ve burada olmazsanız ne olur

**Her hafta dizüstü bilgisayarınızı getirin**, şarj aletiyle ve gereken kablosuyla.
Bu, üç saatlik uygulamalı bir çalışma fırsatıdır.

**Devam zorunludur.** Üniversite dönem boyunca birkaç hafta devamsızlık hakkı tanır ve
bu hak her şeyi zaten kapsar — hastalık, iş, aile, ne olursa olsun. Bunun üstünde ikinci
bir kategori yoktur ve telafi prosedürü yoktur.

**Kaçırdığınız ders, notlandıramadığım derstir.** Nedeni ne olursa olsun o 5 puan
gider. Nedenleri birbiriyle tartmıyorum ve bu bilinçli: yüzden fazla öğrenciyle,
mazeretleri yargılama süreci kendini en iyi anlatanı yargılama sürecine dönüşür.

Açık kalan, diğer yarıdır. Dersin işini kendi zamanınızda yapın, Cumartesi gece
yarısından önce push edin ve o beş puanı herkes gibi alın. Bir dersi kaçırmak size o
derse mal olur, haftaya değil.

---

## 3. Dersten sonra — Cumartesi 23:59'a kadar

Haftanın kalan işini Cumartesi gece yarısına kadar bitirin. O saatte ikinci bir anlık
görüntü alıyorum; teslim anındaki durumunuz diğer 5 puanı belirler.

### `ai_log_NN.md` — atlamayın

Haftada bir dosya, o haftanın klasöründe — `week01/ai_log_01.md` vb. Hafta klasöründeki
diğer belgelerle birlikte gelir. Doldurun: hangi asistanı kullandınız, neyi doğru
yaptı, neyi düzeltmek zorunda kaldınız, ne öğrendiniz.

**Evidence bloğu zorunludur.** İddianızın altına gerçek yazışmayı — gönderdiğiniz
istemi ve aldığınız yanlış yanıtı — kod bloğunun içine yapıştırın. Konuşmanın tamamı
değil: hatayı gösteren on–on beş satır. Evidence bloğu boş bir iddia hiçbir şey
kazandırmaz.

Neden: herkes "yapay zekâ hata yaptı, ben düzelttim" yazabilir. Gerçek bir model
çıktısını inandırıcı biçimde uydurmak zordur — uydurma transkriptler fazla temiz okunur
ve hataları uygun biçimde kolay fark edilir. Ve uzun bir konuşmanın hangi kısmının
kanıt sayılacağını seçmek, değerlendirilen becerinin ta kendisidir.

Konuşmanın tamamını saklamak isterseniz `weekNN/transcript.md` olarak kaydedin.
Varsayılan olarak okumam, ama bir günlük girdisi tutarsızsa okurum.

Bu dosya 2 puan değerindedir.

### Kontroller yeşil olana kadar devam edin

```bash
python .github/check_deliverables.py
git add .
git commit -m "week01: llm_notes written up"
git push
```

GitHub'da deponuzun **Actions** sekmesi her push'un sonucunu gösterir. Cumartesi
durumunuzdaki yeşil tik **2 puan** değerindedir.

### Otomatik olmayan 3 puan

**Tutarlılık ve commit disiplini — 1 puan.** Bu haftanın işi, önceki haftalarda
yazdığınız gereksinimlerden ve tasarımdan gerçekten türüyor mu; commit geçmişiniz son
dakikada tek bir yığın yerine haftaya yayılmış çalışma gösteriyor mu? Plan değişikliği
`PROPOSAL.md` değişiklik günlüğüne tarihli bir satır olarak girdi mi? Fikir değiştirmek
normal ve sağlıklıdır — ama değişiklik görünür olmalı. Sessizce terk edilen bir
gereksinim puana mal olur; `ai_log_NN.md` içinde tek satırlık gerekçeyle bırakılan bir
gereksinim hiçbir şeye mal olmaz. Mühendislik böyle görünür.

**İnsan katkısı — 2 puan.** Bu haftanın işini yalnızca modellerin değil, insanların da
yaptığının kanıtı. Kendi payınız `weekNN/ai_log_NN.md` içinde görünür: somut bir yapay
zekâ hatası, yapıştırılmış kanıt ve elle değiştirdiğiniz şey. 2. Hafta'dan itibaren her
hafta iki sınıf arkadaşınız, ödevin adlandırdığı rolde — paydaş, tasarım gözden
geçireni, testçi — size yardım eder ve onları `weekNN/contributors_NN.json` içine, her
biri için ne yaptığını söyleyen bir cümle ve kanıtla (notları, hata listesi,
günlüğünüzde tarihli bir paragraf) kaydedersiniz. Arkasında hiçbir şey olmayan iki isim
liste demektir, kanıt değil. İspat yükü sizindir; onsuz ne bu iki puan ne de
katkıcılarınızın bonusu ödenir.

**Katkıcılar bonus kazanır.** Size yardım eden bir sınıf arkadaşı o haftaki notunuzun
%10'unu kazanır; haftada en fazla iki katkı. Siz onlara yardım ettiğinizde de aynısı.
İsimler döner: her hafta en az bir yeni kişi. 1. Hafta'da katkıcı yoktur.

Bir LLM bir ödevin istediği her dosyayı üretebilir. Yapamadığı, o dosyaları çevresindeki
on haftayla tutarlı kılmak ya da kendi hatalarını sizin yerinize fark etmektir.
Asıl değerlendirilen budur.

---

## 4. Her hafta geçerli kurallar

**API anahtarını asla koda koymayın.** `.env` içinde yaşar ve `.env` `.gitignore`
içindedir. Bir anahtar depoya ulaşırsa otomatik tarama yakalar ve **10 puan**
kaybedersiniz. Anahtar bir kez push edildiyse silmek yetmez — git geçmişinde kalır.
O anahtarı iptal edip yenisini almanız gerekir.

**Kodu temiz tutun.** Push etmeden önce:

```bash
ruff check .          # sorunları listele
ruff check . --fix    # otomatik düzeltilebilenleri düzelt
ruff format .         # biçimlendir
```

Yapay zekâ üretimi kod sık sık kullanılmayan import bırakır; `ruff` anında yakalar.

**Uygulamanız telefonda çalışmalı.** Tarayıcınızı ara sıra yaklaşık 390 piksele
daraltın. Bir şey kesiliyor ya da yana kayıyorsa pencere küçükken düzeltin — 10.
Hafta'da değil.

**Önceki haftaları bozmayın.** Kontroller birikimlidir: 5. Hafta'da 1–4. Haftalar
yeniden denetlenir. Bir değişiklik eskiyi bozarsa CI söyler.

---

## Takıldığınızda

**CI kırmızı ve nedenini anlamıyorum.** GitHub'da **Actions** sekmesini açıp başarısız
çalıştırmaya tıklayın. Hangi kontrolün neden başarısız olduğunu satır satır söyler.
Aynı çıktı yerelde `python .github/check_deliverables.py` ile gelir.

**Kontroller yerelde geçiyor, GitHub'da geçmiyor.** Genellikle push etmediğiniz bir
dosya. `git status` çalıştırın.

**`ruff` yerelde temiz, CI'da değil.** Sürüm uyuşmazlığı. Elinizdeki herhangi bir sürümü
değil, `week09/requirements.txt` içinde sabitlenmiş sürümü kurun.

**Ollama çalışmıyor / model inmiyor.** Daha küçük bir modele geçin. Hiçbiri çalışmıyorsa
bulut arka ucunu kullanın ve nedenini `model_notes.md` içine yazın — bu kabul edilebilir
bir sonuçtur. Haftayı buna kaptırmayın.

**Bir şeyi bozdum ve geri alamıyorum.** Panik yapmayın; git her şeyi hatırlar:

```bash
git log --oneline           # commit geçmişi
git diff                    # şu an ne değişti
git checkout -- file.py     # bir dosyayı son commit'e döndür
```

**Hâlâ takıldınız mı?** Derste sorun ya da bir yapay zekâya sorun — ama söylediğini
doğrulayın ve yazışmayı `ai_log_NN.md` içine kaydedin. Bu ders tam olarak bununla
ilgili.

---

## Komut özeti

```bash
# çalışırken
python .github/check_deliverables.py     # neyin eksik olduğunu göster
AIASD_WEEK=2 python .github/check_deliverables.py   # istersen yalnızca bir hafta
ruff check . --fix                       # kodu temizle
git add . && git commit -m "weekNN: ..." && git push

# ortam
source .venv/bin/activate                # Windows: .venv\Scripts\activate
streamlit run app.py
```
