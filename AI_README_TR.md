# AIASD Projesi — Öğrenci Reposu

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027**
**Prof. Dr. Vedat Coşkun**

*English: [`AI_README_EN.md`](AI_README_EN.md)*

---

## Bu repo nasıl kullanılır

Bu, 12 haftalık dersin tamamı için kişisel proje reponuzdur (repo, projenizin git
tarafından izlenen klasörüdür; hem bilgisayarınızda hem GitHub'da durur). Onu 1. haftada
ders şablonundan (GitHub'ın sizin için kopyaladığı hazır bir repo) oluşturursunuz ve her
hafta ona commit edersiniz (commit, dosyalarınızın git tarafından kaydedilen bir anlık
görüntüsüdür).

Her hafta kendi ödeviyle, kendi klasöründe gelir ve ödev, tam olarak ne yapacağınızı ve
ne teslim edeceğinizi söyler. [`AI_SKELETON_TR.md`](AI_SKELETON_TR.md) dönemin tamamını
iki sayfada anlatır: her haftanın ne öğrettiğini, neyi push edeceğinizi (push etmek,
commit'lerinizi bilgisayarınızdan GitHub'a göndermektir) ve ne zaman edeceğinizi söyler.
Dönem boyunca tek bir ürün yaparsınız ve o ürün sizindir: bir mobil istemci, bir web
istemcisi ve bir sunucu. Onu seçtiğiniz bir public mağazada yayınlarsınız ve dönem
sonunda, o mağazadan yüklediğiniz uygulama üzerinden savunursunuz.

[`AI_OVERVIEW_TR.md`](AI_OVERVIEW_TR.md) projenizin parçalarını (gereksinimler, kullanım senaryoları,
ekranlar, test case'ler, tasarım, API sözleşmesi, sunucu, istemciler), nasıl uyuşmaları gerektiğini ve
birini değiştirdiğinizde birlikte neyin değişmesi gerektiğini listeler.

Her hafta bir yapay zeka günlüğü ister (o hafta bir yapay zeka asistanını nasıl
kullandığınızın yazılı kaydı). Günlük, o haftanın klasörünün içindeki
`weekNN/ai_log_NN.md` dosyasıdır.

### Her haftanın dosyaları nasıl gelir

Hafta klasörlerini siz oluşturmazsınız. Onları denetleyici getirir. (Denetleyici, her
haftanın gerektirdiği dosyaları arayan otomatik script'tir; aşağıdaki "Otomatik
kontroller" bölümüne bakın.) `python .github/check_deliverables.py` komutunu her
çalıştırdığınızda denetleyici:

- yeni bir hafta yayımlanınca o haftanın klasörünü (`week02/`, `week03/` …), ödeviyle ve
  başlangıç dosyalarıyla birlikte getirir;
- kökte değişen her ders belgesini (`AI_*`) getirir;
- 6. haftadan itibaren `course_tests/` klasörünü ve `server/course_login.py` dosyasını da
  getirir; `server/login_contract.json` sizde yoksa onu da;
- `PROPOSAL.md` iskeletini köke (2. hafta) ve `server/` başlangıç dosyalarını (5. hafta),
  yalnızca sizde henüz yoksa getirir;
- bir hafta klasöründe zaten var olan bir dosyanızı hiçbir zaman değiştirmez.

`course_tests/` ya da `course_login.py` dosyalarını değiştirmeyin: denetleyici dersin
kopyasını geri koyar ve GitHub her zaman onu kullanır.

Yeni dosyalar siz `git add .` çalıştırana kadar izlenmez; denetleyici onları listeler.
Çalışmanızı gelen dosyaların içine yazın. Onları yeniden adlandırmayın ya da taşımayın:
denetleyici her dosyayı tam yolunda arar ve bir dosya eksikse o yolu söyler.

Aşağıdaki dosya ve klasörler dönem boyunca reponuzda kalır:

| | |
|---|---|
| `server/`, `web/` | Ürününüz: sunucu (5. haftadan itibaren) ve web istemcisi (6. haftadan itibaren). Mobil istemci 7. haftada onlara katılır |
| `week01/ASSIGNMENT_01_EN.md`, `_TR.md` | Bu dosyalar bu haftanın ne istediğini iki dilde söyler. Haftanın klasörüyle birlikte gelirler ve görevlerin yazılı olduğu tek yerdirler |
| `week01/ai_log_01.md` | Bu dosya bu haftanın yapay zeka günlüğüdür ve bu haftanın klasöründe durur. Her haftanın bir tane vardır ve haftayla birlikte gelir |
| `student.json` | Bu dosya kim olduğunuzu söyler. 1. haftada bir kez doldurun |
| `requirements.txt`, `weekNN/requirements.txt` | Bu dosyalar bağımlılıkları (uygulamanızın ihtiyaç duyduğu Python paketlerini) listeler. Hafta hafta gelirler |
| `.github/` | Bu klasör her push'ta çalışan kontrolleri tutar |
| `CURRENT_WEEK.txt` | Bu dosyayı ders yazar; düzenlemeyin. Denetleyiciyi ilk çalıştırdığınızda yanında `CURRENT_WEEK_CACHE.txt` adlı bir dosya belirir. O dosya denetleyicinin çevrimdışı önbelleğidir (hafta numarasının kaydedilmiş bir kopyası). Şablonun `.gitignore` dosyası onu zaten git'in dışında tutar |

**İnternet yok mu?** Denetleyici GitHub'a ulaşamazsa bir haftanın dosyalarını elle
getirebilirsiniz. Bunu o dosyalara bir şey yazmadan önce yapın:

```bash
git remote add template https://github.com/vedatcoskun-course/aiasd-template.git
git fetch template
git checkout template/main -- week06 course_tests server/course_login.py
```

İlk satır bütün dönemde yalnızca bir kez gerekir. Son satır adını verdiği dosya ve
klasörlerin üzerine yazar. O yüzden ya önce çalıştırın ya da hiç çalıştırmayın.
`server/login_contract.json` dosyanız henüz yoksa onu son satırın sonuna ekleyin.

**Buradan başlayın:** [`AI_SETUP_CARD_TR.md`](AI_SETUP_CARD_TR.md) / [`AI_SETUP_CARD_EN.md`](AI_SETUP_CARD_EN.md)
dönem boyunca çalıştıracağınız her komutu, sık karşılaşılan hataların ne anlama
geldiğinin açıklamasıyla birlikte tek sayfada tutar. Dört kurulum adımını 1. haftadan
önce yapın.

**Yeni misiniz?** Haftalık rutinin tamamı
[`AI_WEEKLY_WORKFLOW_STUDENT_TR.md`](AI_WEEKLY_WORKFLOW_STUDENT_TR.md) /
[`AI_WEEKLY_WORKFLOW_STUDENT_EN.md`](AI_WEEKLY_WORKFLOW_STUDENT_EN.md) dosyasında adım
adım yazılıdır. Her dersten önce, ders sırasında ve sonra ne yapacağınızı, puanların nasıl
bölündüğünü ve takıldığınızda ne deneyeceğinizi söyler.

**1. haftadan önce okuyun.** Üç ön okuma ve makale köktedir. Ön okumalar `AI_Doc2` AI
Technical Background, `AI_Doc3` Development Environment and Tools ve `AI_Doc4` Working
with AI Tools'dur. Makale ise `AI_Doc1`, Transformer makalesidir (bugünkü yapay zeka
asistanlarının arkasındaki araştırma makalesi). Ders, bu dört belgenin yirmi dakikalık
özetidir. Sonraki okumalar aynı biçimde, sırayla numaralanmış olarak gelir. `AI_Doc5`
Yazılım Geliştirmede Yapay Zekayı Doğru Kullanmak, 3. hafta ile gelir. Haftalık yapay
zeka günlüğünüzün istediği sekiz tekniği anlatır ve her haftanın günlüğü kullandığı
tekniği adlandırır. 4. haftadan itibaren her hafta bir teknik zorunludur ve bu belge
final sınavında çıkar.

İki şube de aynı dosyaları alır. Ödevler, kurulum kartı ve iş akışı `_EN` ve `_TR` ile
işaretlenmiş olarak iki dilde gelir. Kendi dilinizdekini okuyun, diğerini yok sayın.
Okumalar (`AI_DocN`) İngilizcedir; yalnızca `AI_Doc5` İngilizce ve Türkçedir.
Denetleyicinin aradığı klasör ve dosya adları
(`week01/`, `hello.py`, `student.json`) herkes için aynıdır.

---

## Sunucuyu çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate                         # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -r weekNN/requirements.txt  # bir tane olan en yeni hafta
uvicorn server.main:app --reload
```

Sunucu 5. haftada gelir. Sonra tarayıcınızda http://127.0.0.1:8000/health adresini açın:
`{"status": "ok"}` cevabını verir. http://127.0.0.1:8000/docs bütün endpoint'leri listeler.

Bağımlılıklar hafta hafta gelir; böylece 1. haftada gigabaytlarca paket indirmezsiniz.
Kökteki `requirements.txt` asgaridir. Ağır bir haftanın kendi `weekNN/requirements.txt`
dosyası olur ve o haftanın ödevi ne zaman kurulacağını söyler:

```bash
python -m pip install -r weekNN/requirements.txt
```

---

## Kim olduğunuz — `student.json`

Bu dosyayı 1. haftada, repo kökünde doldurun:

```json
{
  "student_id": "230500000",
  "first_name": "Ayşe",
  "last_name": "Yılmaz",
  "nickname": "kaplumbaga",
  "section": "tr"
}
```

**section** alanınız, İngilizce şubedeyseniz `en`, Türkçe şubedeyseniz `tr` olur. Bunu
yanlış yazarsanız denetleyici sizi diğer şubenin haftasına göre sınar; o yüzden push
etmeden önce kontrol edin.

**nickname** alanınız, her ders sonunda yansıtılan sınıf panosunda görünen addır; böylece
kendi satırınızı bir bakışta bulursunuz. Harf, rakam, `-` ve `_` içerebilir ve 2–20
karakter uzunluğunda olmalıdır. İstediğinizi seçin, ama Aralık'ta hala tanıyacağınız bir
şey seçin.

Ders sürerken bu repoyu **private** tutun, çünkü öğrenci numaranızı ve adınızı taşır.

---

## Otomatik kontroller

Her push, hocanızın çalıştırdığı kontrollerin aynısını çalıştırır. GitHub'da commit'inizin
yanında yeşil tik ya da kırmızı çarpı görürsünüz ve tam olarak hangi kontrolün başarısız
olduğunu görebilirsiniz.

**Açmanız gereken bir şey yok.** Denetleyici her çalıştığında derse hangi haftada
olduğunu sorar; bu yüzden gördüğünüz her zaman size karşı çalıştırılan şeydir. Repo
kökündeki `CURRENT_WEEK_CACHE.txt` dosyası yalnızca o hafta numarasının önbelleğidir.
Kendini günceller ve ona hiçbir zaman dokunmanız gerekmez.

Çıktı iki parça halinde gelir, çünkü haftanın iki teslim anı vardır:

```
In the lab:     11 of 13 done
By Saturday:     2 of  8 done
```

**In the lab**, ders sonu anlık görüntüsünün okuduğu kısımdır (anlık görüntü, reponuzun
o andaki halinin birebir kopyasıdır). 11:45'e dek push edin. Ders notu, dersin sonuna dek
push ettiğiniz son commit'i okur (6. haftadan itibaren onun Actions çalışmasını da).
Haftanın on puanının beşi bu kısımdandır. **By
Saturday** gerisidir, yani yazılar, diyagramlar ve `ai_log_NN.md`. İkinci gruptakiler
hafta açıkken çalıştırmayı başarısız kılmaz, çünkü henüz teslim vakti gelmemiştir.
Birinci gruptaki hiçbir şey evde yapmanız gereken bir şey değildir. (1. hafta
istisnadır: ilk dersin sonunda hiçbir şey okunmaz ve beş puanının tamamı Cumartesi
okunur.)

**BEKLİYOR** satırı (İngilizce çıktıda **NOT YET**), adını verdiği bir şeyi bekler. Ne
geçti ne kaldı sayılır ve "x / y" içinde sayılmaz.

**6. haftadan itibaren ders notu GitHub Actions'ı okur.** 6. haftadan itibaren ders
notunuzdaki test sonuçları, dersin sonundan önce push ettiğiniz son commit'in GitHub
Actions çalıştırmasından gelir. Yalnızca kendi bilgisayarınızda geçen bir test sayılmaz.
Her push'tan sonra **Actions** sekmesine bakın.

Denetleyici tek bir haftayı gösterir: içinde bulunulan haftayı. Listenin altındaki bir satır,
önceki haftalarda kaç maddenin hala başarısız olduğunu söyler; böylece sonraki bir değişiklik
eskiyi bozarsa bunu Aralık'ta değil hemen öğrenirsiniz. (GitHub'ın her push'ta çalıştırdığı
otomatik kontroller, yani CI, aynı denetleyiciyi çalıştırır ve o da içinde bulunulan haftaya bakar.)

Başka bir haftaya bakmak için, örneğin 2. haftanın hala geçtiğini doğrulamak için, hafta
numarasını ekleyin:

```bash
python .github/check_deliverables.py 2 tr
```

Push etmeden önce kontrolleri yerelde (kendi bilgisayarınızda) çalıştırın:

```bash
python .github/check_deliverables.py tr
```

Sondaki `tr`, çıktıyı Türkçe yazar; kontroller ve puan aynıdır. Türkçe çıktıda **In the
lab** satırı **Derste**, **By Saturday** satırı **Cumartesiye dek** olarak görünür.

Kırmızı çarpı bir not değildir. Hala eksik olanların listesidir ve o listeyi teslimden
sonra değil dersin olduğu gün görmek çok daha iyidir.

**Gizli anahtar taraması her push'ta, her hafta çalışır.** Gizli anahtar taraması
dosyalarınızda API anahtarlarını ve token'ları arar (şifreleri değil). Bir API anahtarı (bir programın sizin adınıza bir
hizmeti kullanmasını sağlayan gizli bir dize) repoya ulaşırsa kontrol başarısız
olur. Anahtarı kaldırın, hemen yenileyin (yani eski anahtarı iptal edip yenisini
oluşturun) ve commit edilmiş bir anahtarın otomatik 10 puan kesinti olduğunu unutmayın.

---

## Repo kuralları

- **Commit ve push:**
  - **Derste:** her işi ortasında commit edin, çalıştığında yeniden commit edin ve her commit'i hemen push edin. Tek commit'te bitmiş olarak gelen bir iş sayılmaz.
  - **Ders dışında:** yeni iş içeren en az iki commit, aralarında en az bir saat olacak şekilde push edilmiş olsun.
  - Commit'in üzerindeki tarih değil, GitHub'ın push saati sayılır. Bir kodlama ajanının yaptığı commit hiçbir zaman sayılmaz.
  - **Asla force push yapmayın** ve bir asistanın yapmasına da izin vermeyin. Git push'unuzu reddederse önce `git pull`, sonra `git push` yapın.
  - Bir commit'in bitmiş bir parça olması gerekmez. Cumartesi gecesi tek bir push yapıp başka bir şey yapmazsanız, bu size commit disiplini puanına mal olur.
- O haftanın `ai_log_NN.md` dosyasını doldurun. Her haftanın bir tane vardır ve onu bir insan okur.
- `.venv/`, `.env`, `__pycache__/`, `CURRENT_WEEK_CACHE.txt` ya da API anahtarlarını **commit etmeyin**. Şablonun `.gitignore` dosyası (git'in asla commit etmemesi gereken dosyaların listesi) ilk dördünü zaten listeler: onları orada tutun.
- Commit'ten önce `ruff check .` ve `ruff format .` çalıştırın (`ruff`, Python kodundaki yaygın hataları bildiren ve kodu biçimlendiren bir araçtır). Yapay zekanın geride bırakma eğilimindeki kullanılmayan import'ları yakalar. GitHub'daki "Lint and format" işi her push'ta `ruff check .` ve ayrıca `ruff format --check .` çalıştırır. Kökteki `requirements.txt` aynı sürümü kurar (`ruff==0.15.11`).
- Gizli değerler için `.env` (gizli değerleri tutan küçük bir dosya) kullanın.
- Uygulamanız dizüstünde olduğu kadar telefonda da çalışmalı. Tarayıcı pencerenizi ara sıra ~390px'e daraltın. Bir şey kesiliyor ya da yana kayıyorsa sayfa küçükken düzeltin, 10. haftada değil.
