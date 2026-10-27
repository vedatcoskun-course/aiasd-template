# Haftalık İş Akışı

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027**

**Sürüm 2 · 24 Ekim 2026** — bu belge dönem içinde yenilenir. Denetleyiciyi
(`python .github/check_deliverables.py tr`) çalıştırdığınızda en yeni kopyayı reponuza
kendisi getirir. Dolayısıyla reponuzdaki (repo, projenizin git tarafından takip edilen
klasörüdür; hem bilgisayarınızda hem GitHub'da bulunur) kopya günceldir. Gelen her dosya
gibi onu da `git add .` ile ekleyin.

> [!IMPORTANT]
> **Sürüm 2'de ne değişti (24 Ekim 2026)**
>
> - Commit'ler: derste her işi ortasında ve çalıştığında commit edin, her commit'i hemen push edin;
>   ders dışında yeni iş içeren, aralarında
>   en az bir saat olacak şekilde push edilmiş en az iki commit; GitHub'ın push saati sayılır (§2).
> - Asla force push yapmayın ve bir asistanın yapmasına da izin vermeyin (§2, §4).
> - 5. haftadan sonraki Pazar gününden itibaren `requirements.json` ya da `test_cases.json`
>   değişikliği, `PROPOSAL.md` Change log'unda bir `CR-` satırıdır (§3).
> - 6. haftadan itibaren ders notu GitHub Actions çalıştırmasını okur (§2).
> - `group_NN.json` içindeki roller, hafta hafta (§3).
> - Yapay zeka günlüğünde asistanın sözleri yalnızca **kalın** olarak, Evidence bloğundan
>   kopyalanarak yer alır. Evidence bloğunda `ME:`, `AI:` ve `TERMINAL:` parçaları vardır (§3).
> - Evidence bloğu: hatayı gösteren turları yapıştırın; tuttuğunuz her parça bütün olarak
>   yapıştırılır (§3).
> - Yeşil tik ders içi kontrolleri, gizli anahtar taramasını ve ruff'ı gösterir.
>   Denetleyicinin Cumartesi 2 puanı, 23:59'da okunan "By Saturday" kontrollerinden gelir (§3).
> - GitHub ruff 0.15.11 ile `ruff format --check .` da çalıştırır (§4).
> - Haftalık çevrim içi grup toplantısı artık yok. Grubunuzun ne zaman toplandığını ödev
>   söyler (§3).
> - Kırmızı bir çalıştırmadan sonraki küçük bir düzeltme commit'i commit puanını asla
>   düşürmez (§2, §4).
>
> Denetleyici her yeni sürümü kendisi getirir. Bu kutu, bir önceki sürümden bu yana neyin
> değiştiğini listeler.

Bu belge değişmeyen rutini anlatır. Her haftanın *içeriği* farklıdır, çünkü her haftanın
ödevi o haftanın klasöründe gelir; ama *ritim* hep aynıdır.
Takıldığınızda buraya dönün.

---

## Bir bakışta

| Ne zaman | Ne yaparsınız | Puan |
|------|-------------|--------|
| Dersten önce | `weekNN/ASSIGNMENT_NN_TR.md` dosyasını okuyun | — |
| Ders sırasında (3 saat) | Çalışın ve sık push edin (push, bilgisayarınızda kaydettiğiniz işi GitHub'a gönderir) | — |
| Ders sonunda | 11:45'e dek push edin. Ders notu, dersin sonuna dek push ettiğiniz son commit'i okur (anlık görüntü alırım: reponuzun o andaki halinin birebir kopyası) | 5 |
| Dersten sonra | Kalanı bitirin ve `ai_log_NN.md` dosyasını yazın | — |
| Cumartesi 23:59'a kadar | **Yeniden push edin.** Reponuzun ikinci bir anlık görüntüsünü alırım | 5 |

Her hafta on puan değerindedir ve bu puan iki ana eşit bölünür: **beşi dersin sonunda,
beşi Cumartesi teslim saatinde ölçülür.** İki yarı da GitHub'dan okunur, dolayısıyla
ikisi de push ister (push, bilgisayarınızdaki commit'leri GitHub'daki reponuza gönderen
`git push` komutudur). **1. hafta tek istisnadır:** beş puan değerindedir, ilk dersin
sonunda hiçbir şey okunmaz ve beşinin tamamı Cumartesi 23:59'da reponuzdan okunur.
Bitmiş ama push edilmemiş iş, hiç yapılmamış işle tamamen aynı puanı alır.

Haftanın notunun yarısının derse bağlı olması bilinçlidir. İşin yeri derstir:
sınıftasınızdır ve hala soru sorabilirsiniz. Diğer yarısı, haftanın işini bitirmeye ve
bir denetleyicinin (her haftanın istediği dosyaları arayan otomatik script; nasıl
çalıştırılacağını §2 gösterir) göremeyeceği iki şeye dayanır. O iki şeyi §3 anlatır.

**Teslim saati her hafta aynıdır: Cumartesi 23:59.** Hesaplanacak bir şey yoktur, çünkü
Cumartesi gece yarısı reponuzda ne varsa onu notlandırırım. İşin çoğu, soru
sorabileceğiniz laboratuvarda yapılmalıdır; dersten sonraki günler başlamak için değil,
açıkları kapatmak içindir.

---

## Bir kez, bir daha asla

İlk ders başlamadan önce üç şeyin doğru olması gerekir ve hiçbiri dersin içeriğinin bir
parçası değildir: (a) bir GitHub hesabınız vardır, (b) reponuz vardır ve (c) o repoya
push etmesine izin verilen bir bilgisayarınız vardır. Gerekli komutlar
[**Kurulum Kartı**](AI_SETUP_CARD_TR.md)'ndadır. Kartta dört adım vardır ve son adım,
diğer üçünün çalışıp çalışmadığını söyler.

Kart ayrıca en çok karşılaşacağınız hataların ve her birinin gerçekte ne anlama
geldiğinin tablosunu da taşır. Açık tutun; git ve GitHub mekaniği için muhtemelen
ihtiyacınız olan tek sayfa odur.

---

## 1. O haftanın dersinden önce

`weekNN/ASSIGNMENT_NN_TR.md` dosyasını okuyun. Haftanın klasörüyle birlikte gelir ve o
haftanın tam olarak hangi dosyaları istediğini listeler.

Ön okuma varsa gelmeden önce okuyun.

---

## 2. Ders sırasında

### Hangi yarıda çalıştığınızı bilin

Reponuzun kökünden (projenizin en üst klasörü, yani `.github` klasörünü içeren klasör)
çalıştırın:

```bash
python .github/check_deliverables.py
```

İki parça halinde yanıt verir:

```
In the lab:     11 of 14 done
By Saturday:     0 of  3 done
```

Yukarıdaki sayılar yalnızca örnektir; gerçek sayılar haftadan haftaya değişir. Önemli
olan, iki satırdan hangisini okuduğunuzdur.

Çıktıyı Türkçe görmek için sonuna `tr` ekleyin: `python .github/check_deliverables.py tr`
(başka bir hafta için `python .github/check_deliverables.py 2 tr`). Kontroller ve puan
aynıdır; yalnızca dil değişir. Türkçe çıktıda **In the lab** satırı **Derste**, **By
Saturday** satırı **Cumartesiye dek** olarak görünür.

**BEKLİYOR** satırı (İngilizce çıktıda **NOT YET**), adını verdiği bir şeyi bekler. Ne
geçti ne kaldı sayılır ve "x / y" içinde sayılmaz.

**In the lab**, dersin sonunda okuduğum satırdır ve haftanın notunun yarısı değerindedir.
Bu maddeler, benimle ve aynı yerde takılmış, diyelim, yirmi dokuz kişiyle aynı odadayken
yapmaya değer şeylerdir.

**By Saturday** haftanın geri kalanıdır: yazılar, diyagramlar ve `ai_log_NN.md` (yapay
zeka asistanıyla yaptığınız işin haftalık günlüğü; §3 açıklar).
Bu, gerçekten yalnız yaptığınız iştir. Hafta içinde kontrolü başarısız kılmaz, çünkü
henüz teslim vakti gelmemiştir; ama notun diğer yarısıdır ve Cumartesi anlık görüntüsü
onu okur.

Laboratuvarda `ai_log_NN.md` yazıyorsanız işleri yanlış sırayla yapıyorsunuz demektir:
günlük, laboratuvar işinden sonra gelir.

### Çalışın ve sık push edin

Her şeyi sonda tek devasa yığın halinde commit etmek yerine iş ilerledikçe commit edin
(commit, git geçmişinde `git commit` ile kaydedilen tek bir adımdır). Her commit'in
mesajı ne yaptığınızı söylemelidir:

```bash
git add .
git commit -m "week01: hello.py reads a name and prints the list"
git push
```

"update", "fix" ya da "asdf" gibi bir mesaj ne olduğu hakkında hiçbir şey söylemez ve
böyle mesajlar size commit disiplini puanına (§3'te anlatılır) mal olur.

**Commit ve push kuralı:**

- **Derste:** her işi, hangi durumda olursa olsun, ortasında commit edin; çalıştığında yeniden
  commit edin ve her commit'i hemen push edin. Tek commit'te bitmiş olarak gelen bir iş sayılmaz.
- **Ders dışında:** yeni iş içeren en az iki commit, aralarında en az bir saat olacak
  şekilde push edilmiş olsun.
- Commit'in üzerindeki tarih değil, GitHub'ın push saati sayılır.
- Bir kodlama ajanının yaptığı commit hiçbir zaman sayılmaz.
- **Asla force push yapmayın** ve bir asistanın yapmasına da izin vermeyin (§4).

10:00'da ve 11:00'de sınıf tablosuna (her öğrencinin reposunun ne durumda olduğunu
gösteren, perdeye yansıtılan tablo) bakıp herkesin nerede olduğunu görürüm. 11:45'e dek
push edin: ders notu, dersin sonuna dek push ettiğiniz son commit'i okur. Push etmek hiçbir şeye mal olmaz. Push
edilmiş yarım bir bölüm, push edilmemiş bitmiş bir bölümden daha değerlidir.

### Kontrolleri kendiniz çalıştırın

Aynı komutu, istediğiniz kadar sık çalıştırın (sondaki `tr`, çıktıyı Türkçe yazar):

```bash
python .github/check_deliverables.py tr
```

Bunlar tam olarak benim çalıştıracağım kontrollerdir. Çıktı, eksik olanları satır satır
listeler. Bir not değil, yapılacaklar listesidir ve çalıştırmanın maliyeti yoktur.

### Ders bitmeden bir kez daha push edin

11:45'e dek push edin. Ders notu, dersin sonuna dek push ettiğiniz son commit'i okur (6.
haftadan itibaren onun Actions çalışmasını da). O commit'in anlık görüntüsünü alırım (reponun
o andaki halinin birebir kopyası) ve kontrolleri o anlık görüntü üzerinde çalıştırırım. Push etmediğiniz iş görünmezdir: bilgisayarınızda durur ve
sayılmaz.

Sonuç anonimleştirilmiş bir tablo (kimsenin gerçek adının görünmediği bir tablo) olarak
yansıtılır; satırınızı `student.json` (reponuzda bilgilerinizi, seçtiğiniz takma ad
dahil, tutan dosya) içindeki takma adınızla bulun. O tablo **5 puan — haftanın yarısı**
değerindedir.

**6. haftadan itibaren ders notu GitHub Actions'ı okur.** 6. haftadan itibaren ders
notunuzdaki test sonuçları, dersin sonundan önce push ettiğiniz son commit'in GitHub
Actions çalıştırmasından gelir. Yalnızca kendi bilgisayarınızda geçen bir test sayılmaz.
Her push'tan sonra **Actions** sekmesine bakın.

Bir öğrenci bir bilgisayarda, bir GitHub hesabıyla çalışır. Bir sınıf arkadaşınızın
bilgisayarında ya da onun GitHub oturumunda yapılan iş, ders için hiçbir puan getirmez.

**Commit disiplini (haftada 1 puan) her hafta değerlendirilir.** Yukarıdaki kurala
bakarım: derste üç push, ders dışında aralarında en az bir saat olan iki push. Ayrıca üç
soru sorarım:

- İş adım adım mı büyümüş?
- Bir commit'ten diğerine gerçek bir ilerleme var mı?
- Metin üzerinde çalışılmış mı, yoksa bitmiş halde mi yapıştırılmış?

Her commit'in mesajı neyin değiştiğini söyler. Bir commit'in bitmiş bir parça olması
gerekmez. Hafta sonunda tek bir commit ya da tek parça halinde gelen metin puan getirmez.
Kırmızı bir çalıştırmadan sonraki küçük bir düzeltme commit'i puanı asla düşürmez. Bir
haftada şüpheli bir durum görürsem karar vermeden önce önceki haftalarınıza da bakarım.
Ayrıca herhangi bir derste size projeniz hakkında iki dakikalık bir soru sorabilirim.

### Devam, ve burada olmazsanız ne olur

**Her hafta dizüstü bilgisayarınızı getirin**, şarj aletiyle ve gereken kablosuyla
birlikte. Ders, üç saatlik uygulamalı bir çalışma fırsatıdır.

**Devam zorunludur.** Üniversite dönem boyunca birkaç hafta devamsızlık hakkı tanır ve
bu hak, nedeni ister hastalık, ister iş, ister aile, isterse başka herhangi bir şey
olsun, her şeyi zaten kapsar. Bunun üstünde ikinci bir kategori yoktur ve telafi
prosedürü yoktur.

**Kaçırdığınız ders, notlandıramadığım derstir.** Nedeni ne olursa olsun o 5 puan gider.
Nedenleri birbiriyle tartmam ve bu bilinçli bir karardır: yüzden fazla öğrenciyle,
mazeretleri yargılama süreci kendini en iyi anlatanı yargılama sürecine dönüşür.

Açık kalan, diğer yarıdır. Dersin işini kendi zamanınızda yapın, Cumartesi gece
yarısından önce push edin ve o beş puanı herkes gibi alın. Bir dersi kaçırmak size o
derse mal olur, haftaya değil.

---

## 3. Dersten sonra — Cumartesi 23:59'a kadar

Haftanın kalan işini Cumartesi gece yarısına kadar bitirin. O saatte ikinci bir anlık
görüntü alırım ve teslim anındaki durumunuz diğer 5 puanı belirler.

### `ai_log_NN.md` — atlamayın

Haftada bir dosya yazarsınız ve dosya o haftanın klasöründe durur; yani 1. haftanın
dosyası `week01/ai_log_01.md` olur ve böyle devam eder. Dosya, hafta klasöründeki diğer
belgelerle birlikte gelir ve siz doldurursunuz. Hangi asistanı kullandığınızı, neyi doğru
yaptığını, neyi düzeltmek zorunda kaldığınızı ve ne öğrendiğinizi yazarsınız. **Kendiniz,
kendi cümlelerinizle yazarsınız**: Evidence bloğu ve kalın alıntılar dışında asistan
kullanılmaz, dili düzeltmek için bile. İngilizceniz ya da Türkçeniz notlanmaz; asistanın yazdığı bir günlük, ne kadar
düzgün olursa olsun 4. haftadan itibaren 0 alır (1–3. haftalarda 2 puanın en çok 1'ini alıyordu).

Asistanın sözleri günlüğünüzde yalnızca **kalın** olarak yer alabilir. Her kalın ifade
Evidence bloğundan harfi harfine kopyalanır. Kalın yazıyı başka hiçbir şey için
kullanmayın. Her haftanın günlüğü ayrıca kullandığı `AI_Doc5` tekniğini adlandırır (hangisi
olduğunu o haftanın günlük dosyası söyler). 4. haftadan itibaren teknik zorunludur.

**Evidence bloğu zorunludur.** Gerçek yazışmayı kod bloğunun (üçer ters tırnaktan oluşan
iki satır arasındaki blok) içine yapıştırın: `ME:` altına gönderdiğiniz istemi, `AI:`
altına yanıtı geldiği gibi ve hafta istediğinde `TERMINAL:` altına komutları ve
çıktılarını, dokunmadan. Hatayı gösteren turları yapıştırın; hatayı göstermeyen turları
bütünüyle dışarıda bırakabilirsiniz. Tuttuğunuz her `ME:`, `AI:` ya da `TERMINAL:` parçası
bütün olarak, geldiği gibi yapıştırılır: 4. haftadan itibaren hiçbir şey çıkarılmaz, hiçbir
şey düzeltilmez, dil bilgisi bile. Evidence bloğu boş olan bir iddia hiçbir şey kazandırmaz.

Bu neden zorunlu? Herkes "yapay zeka hata yaptı, ben düzelttim" yazabilir. Gerçek bir
model çıktısını inandırıcı biçimde uydurmak zordur, çünkü uydurma transkriptler fazla
temiz okunur ve hataları fazlasıyla kolay fark edilir. Ve uzun bir konuşmanın hangi
kısmının kanıt sayılacağını seçmek, değerlendirilen becerinin ta kendisidir.

Konuşmanın tamamını saklamak isterseniz `weekNN/transcript.md` olarak kaydedin. O
dosyaları varsayılan olarak okumam, ama bir günlük girdisi tutarsız olduğunda sizinkini
okurum.

Yapay zeka günlüğü, haftanın elle yazılmasını istediği dosyalarla birlikte, 2 insan katkısı
puanının ana parçasıdır (1. hafta: 1 puan).

### Kontroller yeşil olana kadar devam edin

```bash
python .github/check_deliverables.py tr
git add .
git commit -m "week01: llm_notes written up"
git push
```

GitHub'da reponuzun **Actions** sekmesi her push'un sonucunu gösterir. GitHub her
push'tan sonra iki iş çalıştırır ve bu otomatik çalıştırmaya CI (sürekli entegrasyon)
denir: "Weekly deliverables" (denetleyici) ve "Lint and format" (ruff). Yeşil tik ders içi
kontrolleri, gizli anahtar taramasını ve ruff'ı gösterir. "By Saturday" kontrolleri onu
kırmızı yapmaz, çünkü henüz teslim vakti gelmemiştir. Denetleyicinin **Cumartesi 2
puanı**, 23:59'da okunan "By Saturday" kontrollerinden gelir. Bu yüzden denetleyiciyi
çalıştırın ve "By Saturday" satırını (Türkçe çıktıda **Cumartesiye dek**) okuyun.

### Otomatik olmayan 3 puan

**Tutarlılık ve commit disiplini — 1 puan.** Bu haftanın işi, önceki haftalarda
yazdığınız gereksinimlerden ve tasarımdan gerçekten türüyor mu; commit geçmişiniz son
dakikada gelen tek bir yığın yerine adım adım büyüyen bir çalışma gösteriyor mu? Planınızı
değiştirdiyseniz, değişiklik `PROPOSAL.md` dosyasının Change log'una tarihli bir
satır olarak girdi mi? Fikir değiştirmek normal ve sağlıklıdır, ama değişiklik görünür
olmalıdır. Projenin kendisi (problemi ve ürünü) 3. hafta dersinin sonunda (11:45) kesinleşir; ondan sonra yalnızca ayrıntıları değişir. Sessizce terk edilen bir gereksinim puana mal olur.

5. haftadan sonraki Pazar gününden (baseline) itibaren `requirements.json` ya da
`test_cases.json` dosyasındaki her değişiklik, düşürülen bir gereksinim de dahil, bir
**change request**'tir: `PROPOSAL.md` Change log'unda `CR-` ve sıradaki
numarayla başlayan, değişikliği ve id'leri söyleyen ve etkilediği her dosyayı sayan tek
bir satır. Örnek: "2026-10-28 — CR-01: REQ-002 now allows 15-minute slots; affects
requirements.json, test_cases.json (TC-002-02), week05/api.md, server/bookings.py."
Diğer değişiklikler (`api.md`, use case'ler, ekranlar) normal, tarihli bir Change log
satırı alır. Kaydedilmiş bir değişiklik hiçbir şeye mal olmaz. Mühendislik böyle görünür.

**İnsan katkısı — 2 puan.** Bu, bu haftanın işini yalnızca modellerin değil, insanların da
yaptığının kanıtıdır. Kendi payınız `weekNN/ai_log_NN.md` içinde görünür: somut bir yapay
zeka hatası, yapıştırılmış kanıt ve elle değiştirdiğiniz şey. Bu günlük, haftanın elle
yazılmasını istediği dosyalarla birlikte, bu iki puanın ana parçasıdır (1. hafta: 1 puan).
Size yardım eden sınıf arkadaşları da kaydedilir: her biri için ne yaptığını
söyleyen bir cümle ve o işin kanıtı; kanıt, onların notları, hata listeleri ya da
günlüğünüzdeki tarihli bir paragraf olabilir. 2. haftada en çok iki sınıf arkadaşınız
paydaş olarak yardım edebilir ve `week02/contributors_02.json` içine kaydedilir; zorunlu
değildir, yalnız çalışmak size hiçbir şeye mal olmaz. 3. haftada derste sizi
değerlendiren üç kişi `week03/contributors_03.json` içine kaydedilir. 4. haftadan
itibaren size yardım edenler, haftanın ödevinin adlandırdığı rolle `weekNN/group_NN.json`
içine kaydedilir (liste aşağıdadır). Listelediğiniz kişi gerçek olmalıdır; arkasında
hiçbir şey olmayan isimler bir listedir, kanıt değil, ve kanıt olmadan katkı bonusu
ödenmez.

**Grubunuz ve `weekNN/group_NN.json`.** 3. haftada dört kişilik grubunuzu kendiniz
kurarsınız (sınıf dörde bölünmüyorsa beş kişilik). 3. haftadaki grubunuz grubunuz olarak
kalır; hangi haftalarda ve ne için toplandığını ödev söyler. `weekNN/group_NN.json`, o
haftanın ödevinin adını verdiği kişileri o haftanın rolüyle (tam İngilizce kelimeyle)
tutar. 2. ve 3. haftalarda size yardım eden kişiler `contributors_NN.json` içindedir.

| Hafta | Rol |
|---|---|
| 2 | stakeholder |
| 3 | reviewer |
| 4 | collaborator |
| 5 | kimse (tek başınıza çalışırsınız) |
| 6 | attacker |
| 7 | tester |
| 8 | test-user |
| 9 | beta-tester |
| 10 | uat-participant |
| 11 | release-tester |
| 12 | poster-reviewer |

Her kişi için ne yaptığını ya da söylediğini ve sizin bunun üzerine ne yaptığınızı
yazarsınız; alanları haftanın ödevi verir. Orada olmayan biri için o kayıtları kimse
yazamaz.

**Katkıcılar bonus kazanır.** Size yardım eden bir sınıf arkadaşı o haftaki notunuzun
%10'unu kazanır; bu, haftada en fazla üç katkı için geçerlidir. Siz onlara yardım
ettiğinizde de aynısı sizin için geçerlidir. 2. haftada isimler sizin seçiminizdir;
3. haftadan itibaren haftanın ödevinin adını verdiği kişilerdir. 1. ve 5. haftalarda
katkıcı yoktur.

Bir LLM (büyük dil modeli; yapay zeka asistanlarının arkasındaki model türü) bir ödevin
istediği her dosyayı üretebilir. Yapamadığı şey, o dosyaları çevresindeki on haftayla
tutarlı kılmak ya da kendi hatalarını sizin yerinize fark etmektir. Asıl değerlendirilen
budur.

---

## 4. Her hafta geçerli kurallar

**API anahtarını asla koda koymayın.** (API anahtarı, programınızın bir dış hizmeti
kullanmasını sağlayan, parolaya benzer gizli bir dizgidir.) Anahtar `.env` içinde yaşar
(yalnızca kendi bilgisayarınızın okuduğu küçük bir ayar dosyası) ve `.env`,
`.gitignore` içinde listelenir (git'e hangi dosyaların asla commit edilmeyeceğini
söyleyen dosya). Bir anahtar repoya ulaşırsa otomatik gizli anahtar taraması onu yakalar
(tarama API anahtarlarını ve token'ları bulur, şifreleri değil) ve **10 puan**
kaybedersiniz. Anahtar bir kez push edildiyse silmek yetmez,
çünkü git geçmişinde kalır. O anahtarı iptal edip yenisini almanız gerekir.

**Kodu temiz tutun.** Push etmeden önce `ruff` çalıştırın (Python kodundaki biçem
sorunlarını bulan ve düzelten bir araç):

```bash
ruff check .          # sorunları listele
ruff check . --fix    # otomatik düzeltilebilenleri düzelt
ruff format .         # biçimlendir
```

Yapay zeka üretimi kod sık sık arkasında kullanılmayan import bırakır (import satırı,
kodun hiç kullanmadığı bir modülü yükleyen satırdır); `ruff` bunları anında yakalar.

GitHub'daki "Lint and format" işi, 1. haftadan itibaren her push'ta `ruff check .` ve
`ruff format --check .` çalıştırır. GitHub'la aynı sürümü kullanın: kökteki
`requirements.txt` içindeki `ruff==0.15.11` (`python -m pip install -r requirements.txt`).

**Uygulamanız telefonda çalışmalı.** Tarayıcı pencerenizi ara sıra yaklaşık 390 piksele
(aşağı yukarı bir telefon ekranının genişliği) daraltın. Bir şey kesiliyor ya da yana
kayıyorsa pencere küçükken düzeltin, 10. haftada değil.

**Asla force push yapmayın.** Force push (`git push --force` ya da VS Code'daki "Force Push")
reponuzun geçmişinden commit siler; bu geçmiş de çalışmanızın benim okuduğum kaydının bir
parçasıdır. Bir asistanın sizin yerinize yapmasına da izin vermeyin. Git push'unuzu reddederse
önce `git pull`, sonra yeniden `git push` yapın (VS Code'da: **Sync Changes**).
`git pull` "Need to specify how to reconcile divergent branches" diyerek durursa bir kez
`git config pull.rebase false` çalıştırın, sonra yeniden `git pull` yapın. Git bir çakışma
(conflict) bildirirse ve ne yapacağınızdan emin değilseniz, push'u zorlamak yerine derste sorun.
Notlarınız commit'lerinizin üzerindeki tarihlerden değil, GitHub'ın her push'un ne zaman
geldiğine dair kendi kaydından okunur.
Küçük bir düzeltme commit'i (bir ruff hatası, bir yazım hatası) commit puanını asla düşürmez:
eski bir commit'i değiştirmek yerine onu yeni bir commit olarak push edin.

**Önceki haftaları bozmayın.** Kontroller birikimlidir: 5. haftada 1–4. haftalar
yeniden denetlenir. Bir değişiklik eski bir şeyi bozarsa CI (kontrollerin GitHub'daki
otomatik çalıştırması; bkz. §3) size söyler.

---

## Takıldığınızda

**CI kırmızı ve nedenini anlamıyorum.** GitHub'da **Actions** sekmesini açıp başarısız
çalıştırmaya tıklayın. Hangi kontrolün neden başarısız olduğunu satır satır söyler. Aynı
çıktı, `python .github/check_deliverables.py` komutunu yerelde (kendi bilgisayarınızda)
çalıştırdığınızda da gelir.

**Kontroller yerelde geçiyor, GitHub'da geçmiyor.** Olağan neden, push etmediğiniz bir
dosyadır. `git status` çalıştırın (değişmiş ama henüz commit ya da push edilmemiş
dosyaları listeler). 6. haftadan itibaren başka bir neden de değiştirdiğiniz bir ders
dosyasıdır (`course_tests/`, `server/course_login.py`): GitHub her zaman dersin kopyasını
kullanır. Bu dosyaları değiştirmeyin.

**`ruff` yerelde temiz, CI'da değil.** Bu bir sürüm uyuşmazlığıdır: bilgisayarınız ve CI
farklı `ruff` sürümleri çalıştırıyordur. Elinizde hangisi varsa onu değil, kökteki
`requirements.txt` dosyasında (dersin ihtiyaç duyduğu paketlerin, tam sürümleriyle
birlikte listesi) sabitlenmiş sürümü kurun: `python -m pip install -r requirements.txt`,
`ruff==0.15.11` kurar. `ruff format .` da çalıştırın, çünkü GitHub biçimi de kontrol eder.

**Bir şeyi bozdum ve geri alamıyorum.** Panik yapmayın, çünkü git her şeyi hatırlar:

```bash
git log --oneline           # commit geçmişi
git diff                    # şu an ne değişti
git checkout -- file.py     # bir dosyayı son commit'e döndür
```

**Hala takıldınız mı?** Derste sorun ya da bir yapay zekaya sorun. Bir yapay zekaya
sorarsanız söylediğini doğrulayın ve yazışmayı `ai_log_NN.md` içine kaydedin. Bu ders
tam olarak bununla ilgilidir.

---

## Komut özeti

```bash
# çalışırken
python .github/check_deliverables.py tr     # neyin eksik olduğunu göster (Türkçe)
python .github/check_deliverables.py 2 tr   # isterseniz başka bir hafta
ruff check . --fix                          # kodu temizle
ruff format .                               # kodu biçimlendir
git add . && git commit -m "weekNN: ..." && git push

# ortam
source .venv/bin/activate                # Windows: .venv\Scripts\activate
uvicorn server.main:app --reload         # sunucuyu başlat (5. haftadan itibaren)
```
