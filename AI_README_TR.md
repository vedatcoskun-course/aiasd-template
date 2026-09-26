# AIASD Projesi — Öğrenci Deposu

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027**
**Prof. Dr. Vedat Coşkun**

*English: [`AI_README_EN.md`](AI_README_EN.md)*

---

## Bu depo nasıl kullanılır

Bu, 12 haftalık dersin tamamı için kişisel proje deponuz. 1. Hafta'da şablondan
oluşturur, her hafta ona commit edersiniz.

Her hafta, tam olarak ne yapıp ne teslim edeceğinizi söyleyen kendi ödeviyle, kendi
klasöründe gelir. Dönemin tamamı iki sayfada — her hafta ne öğretilir, ne zaman ne push
edersiniz — [`AI_SKELETON_TR.md`](AI_SKELETON_TR.md) dosyasında. Dönem boyunca tek bir ürün
yapılır, sizinki: bir mobil istemci, bir web istemcisi ve bir sunucu; seçtiğiniz bir public
mağazada yayınlanır; dönem sonunda mağazadan yüklenmiş uygulamadan savunulur.

Çoğu hafta ayrıca bir yapay zekâ günlüğü ister — o haftanın klasöründe `weekNN/ai_log_NN.md`.

### Şu an burada ne var, ne yok

Şu anda bu depoda dönem boyunca burada kalan dosyalar ve `week01/` var. `week02/` klasörü
yok ve olmamalı — **her haftanın klasörünü, o haftanın ödevi söylediğinde siz
oluşturursunuz.** Dosyayı doğru yere koymak işin parçasıdır; yanlış yere koyduğunuzda
denetleyici aradığı tam yolu adıyla söyler.

Kökte, dönem boyunca:

| | |
|---|---|
| `app.py` | Uygulamanız. Şimdilik boş; hafta hafta büyüyerek ürünün tamamı olur |
| `week01/ASSIGNMENT_01_EN.md`, `_TR.md` | Bu haftanın istediği, iki dilde. Haftanın klasörüyle gelir ve görevlerin yazılı olduğu tek yerdir |
| `week01/ai_log_01.md` | Bu haftanın yapay zekâ günlüğü, bu haftanın klasöründe. Her haftanın bir tane vardır ve haftayla gelir |
| `student.json` | Kim olduğunuz. 1. Hafta'da bir kez doldurun |
| `requirements.txt`, `weekNN/requirements.txt` | Bağımlılıklar, hafta hafta gelir |
| `.github/` | Her push'ta çalışan kontroller |
| `CURRENT_WEEK.txt` | Denetleyicinin yönettiği kayıt. Düzenlemeyin. Denetleyiciyi ilk çalıştırdığınızda yanında `CURRENT_WEEK_CACHE.txt` belirir — çevrimdışı önbelleği, git tarafından izlenmez, yok sayabilirsiniz |

Birkaç hafta size sıfırdan yaptırmak yerine bir iskelet verir. Bu olduğunda ödev tek bir
komutla açılır ve onu, o klasörde bir şey oluşturmadan **önce** çalıştırırsınız:

```bash
git remote add template https://github.com/vedatcoskun-course/aiasd-template.git
git fetch template
git checkout template/main -- week06
```

İlk satır yalnızca bir kez gerekir. O klasöre zaten dosya yazdıktan sonra çalıştırırsanız
üzerine yazar — o yüzden ya önce çalıştırın ya da hiç.

**Buradan başlayın:** [`AI_SETUP_CARD_TR.md`](AI_SETUP_CARD_TR.md) / [`AI_SETUP_CARD_EN.md`](AI_SETUP_CARD_EN.md)
— dönem boyunca çalıştıracağınız her komut tek sayfada, artı sık karşılaşılan hataların
anlamı. Dört kurulum adımını 1. Hafta'dan önce yapın.

**Yeni misiniz?** Haftalık rutinin tamamı — her dersten önce, ders sırasında ve sonra ne
yapılır, puanlar nasıl bölünür, takıldığınızda ne denersiniz — adım adım
[`AI_WEEKLY_WORKFLOW_STUDENT_TR.md`](AI_WEEKLY_WORKFLOW_STUDENT_TR.md) /
[`AI_WEEKLY_WORKFLOW_STUDENT_EN.md`](AI_WEEKLY_WORKFLOW_STUDENT_EN.md) dosyasında.

**1. Hafta'dan önce okuyun** — üç ön okuma ve makale kökte: `AI_Doc2` AI Technical
Background, `AI_Doc3` Development Environment and Tools, `AI_Doc4` Working with AI Tools
ve `AI_Doc1`, Transformer makalesi. Ders bunların yirmi dakikalık özetidir. Sonraki
okumalar aynı biçimde, sırayla numaralanmış olarak gelir.

İki şube de aynı dosyaları alır. Ödevler, kurulum kartı ve iş akışı iki dilde gelir, `_EN`
ve `_TR` — kendinizinkini okuyun, diğerini yok sayın. Okumalar (`AI_DocN`)
İngilizcedir. Denetleyicinin aradığı klasör ve dosya adları (`week01/`, `hello.py`,
`student.json`) herkes için aynıdır.

---

## Uygulamayı çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Bağımlılıklar hafta hafta gelir; 1. Hafta'da gigabaytlarca şey indirmezsiniz. Kökteki
`requirements.txt` asgaridir; ağır bir haftanın kendi `weekNN/requirements.txt` dosyası
olur ve o haftanın ödevi ne zaman kurulacağını söyler:

```bash
pip install -r weekNN/requirements.txt
```

---

## Kim olduğunuz — `student.json`

1. Hafta'da, depo kökünde doldurun:

```json
{
  "student_id": "20210042",
  "first_name": "Ayşe",
  "last_name": "Yılmaz",
  "nickname": "kaplumbaga",
  "section": "tr"
}
```

**section**, İngilizce şubedeyseniz `en`, Türkçe şubedeyseniz `tr`. Yanlış yazarsanız
denetleyici sizi diğer şubenin haftasına göre sınar; push etmeden önce kontrol edin.

**nickname**, her ders sonunda yansıtılan sınıf panosunda görünen addır; kendi satırınızı
bir bakışta bulmanız için. Harf, rakam, `-` ve `_`; 2–20 karakter. İstediğinizi seçin,
ama Aralık'ta hâlâ tanıyacağınız bir şey olsun.

Ders sürerken bu depoyu **private** tutun. Öğrenci numaranızı ve adınızı taşıyor.

---

## Otomatik kontroller

Her push, hocanızın çalıştırdığı kontrollerin aynısını çalıştırır. GitHub'da commit'inizin
yanında yeşil tik ya da kırmızı çarpı görürsünüz ve tam olarak hangi kontrolün başarısız
olduğunu görebilirsiniz.

**Açmanız gereken bir şey yok.** Denetleyici her çalıştığında hangi haftada olduğunu derse
sorar; gördüğünüz her zaman size karşı çalıştırılan şeydir. Depo kökündeki
`CURRENT_WEEK_CACHE.txt` o sayının önbelleğidir — kendini günceller, dokunmanız gerekmez.

Çıktı iki parça hâlinde gelir, çünkü haftanın iki teslim anı vardır:

```
In the lab:     11 of 13 done
By Saturday:     2 of  8 done
```

**In the lab**, ders sonu anlık görüntüsünün okuduğu kısımdır — haftanın on puanının beşi.
**By Saturday** gerisidir: yazılar, diyagramlar, `ai_log_NN.md`. İkinci gruptakiler hafta
açıkken çalıştırmayı başarısız kılmaz; henüz teslim vakti gelmemiştir. Birinci gruptaki
hiçbir şey evde yapmanız gereken bir şey değildir. (1. Hafta istisnadır: ilk dersin sonunda
hiçbir şey okunmaz; beş puanının tamamı Cumartesi okunur.)

Haftalar birikimli denetlenir — 3. Hafta, 1 ve 2. Haftaları da yeniden denetler. Sonraki bir
değişiklik eskiyi bozarsa bunu Aralık'ta değil CI'dan duymak istersiniz.

Tek bir haftaya bakmak için, örneğin 2. Hafta'nın hâlâ geçtiğini doğrulamak:

```bash
AIASD_WEEK=2 python .github/check_deliverables.py
```

Push etmeden önce kontrolleri yerelde çalıştırın:

```bash
python .github/check_deliverables.py
```

Kırmızı çarpı bir not değildir. Hâlâ eksik olanların listesidir ve bunu teslimden sonra
değil Salı günü görmek çok daha iyidir.

**Gizli anahtar taraması her push'ta, her hafta çalışır.** Bir API anahtarı depoya ulaşırsa
kontrol gürültüyle başarısız olur — kaldırın, anahtarı hemen yenileyin ve commit edilmiş bir
anahtarın otomatik 10 puan kesinti olduğunu unutmayın.

---

## Depo kuralları

- **Haftada en az üç commit, haftaya yayılmış** — Cumartesi gecesi tek push, commit disiplini puanına mal olur.
- O haftanın `ai_log_NN.md` dosyasını doldurun — her haftanın bir tane vardır ve onu bir insan okur.
- `.venv/`, `__pycache__/` ya da API anahtarlarını **commit etmeyin**.
- Commit'ten önce `ruff check .` çalıştırın — yapay zekânın geride bırakma eğilimindeki kullanılmayan import'ları yakalar.
- Gizli değerler için `.env` kullanın ve `.gitignore` içinde tutun.
- Uygulamanız dizüstünde olduğu kadar telefonda da çalışmalı. Tarayıcı pencerenizi ara sıra ~390px'e daraltın — bir şey kesiliyor ya da yana kayıyorsa sayfa küçükken düzeltin, 10. Hafta'da değil.
