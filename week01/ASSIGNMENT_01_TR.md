# 1. Hafta Ödevi — Temeller: Ortam, Git ve LLM'lerle İlk Temas

**Teslim:** Cumartesi 23:59 · Proje deponuza commit edin

> **Dersten önce** `docs/` altındaki üç ön okuma belgesini okuyun: *AI Technical
> Background* (kavramlar), *Development Environment and Tools* (ortam ve araçlar) ve
> *Working with AI Tools* (araçların maliyeti ve iyi kullanımı).
> Ders, tam olarak bu malzemenin 20 dakikalık bir özetidir.

---

## Görevler

### 1. Şablondan proje deponuzu oluşturun
`https://github.com/vedatcoskun-course/aiasd-template` adresine gidin ve
**Use this template → Create a new repository** düğmesine tıklayın. O formda üç şey var:

**Repository name:** tam olarak `aiasd-project`. Küçük harf, tek tire, başka hiçbir şey.
Çalışmanızı bu adla buluyorum; farklı bir ad, bulamıyorum demektir.

**Visibility: Private.** ⚠️ **Form Public seçili açılır.** Create'e basmadan önce
değiştirmeniz gerekiyor. Public bırakırsanız öğrenci numaranız ve adınız açık internete
düşer — bu düzenin var olma nedeni tam da bunu önlemektir. Yine de olursa panik yapmayın:
Settings'ten hemen değiştirin ve bana söyleyin.

**Include all branches:** kapalı bırakın.

Sonra depoyu bilgisayarınıza klonlayın.

Şimdi beni Collaborator olarak ekleyin: **Settings → Collaborators → Add people**, ardından
**`VedatCOSKUN`** araması yapın — tam bu yazım, tiresiz; notunuzu veren hesap budur. Bu
olmadan deponuz benim için görünmezdir ve hafta teslim edilmemiş sayılır.

Beni eklemek, kabul etmem gereken bir davet gönderir; dolayısıyla bir şey görebilmem için
kısa bir gecikme olur. Başka bir şey yapmanız gerekmez — ama ders sonu panosunda sizin
için hiçbir şey görünmüyorsa ilk baktığımız yer burasıdır.

Depo bilerek private: öğrenci numaranızı ve adınızı taşıyor, bunların açık internette işi
yok. Ders bittikten sonra public yapmakta serbestsiniz.

### 2. `student.json` dosyasını doldurun

Dosya, az önce oluşturduğunuz deponun kökünde, tüm değerleri boş olarak zaten duruyor.
Yenisini oluşturmayın — o dosyayı açıp doldurun. Beş alan, hepsi zorunlu:

```json
{
  "student_id": "20210042",
  "first_name": "Ayşe",
  "last_name": "Yılmaz",
  "nickname": "kaplumbaga",
  "section": "tr"
}
```

**nickname**, her ders sonunda yansıtılan sınıf panosunda görünen addır; kendi satırınızı
bir bakışta bulmanız için. Yalnızca harf, rakam, `-` ve `_`; 2–20 karakter. Ötesi size
kalmış — Aralık'ta hâlâ tanıyacağınız bir şey seçin.

**`section`**, kayıtlı olduğunuz şubeye göre `en` ya da `tr`. Deponuz, hangi haftaya göre
denetleneceğini derse bununla sorar; yanlış yazarsanız size yanlış haftanın kontrolleri
gösterilir.

Numaranız ve adınız resmî not kaydı içindir ve bilgisayarımdan dışarı çıkmaz.

### 3. Python ortamınızı kurun
*Development Environment and Tools* belgesinin 1–5. bölümlerini izleyin: Python 3.12, bir
sanal ortam ve Python eklentili VS Code.

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Kanıtı `week01/setup_proof.md` dosyasına kaydedin — `python --version`, `pip --version`,
`git --version` çıktılarını ve etkin sanal ortamı gösteren terminal çıktısı ya da ekran
görüntüleri.

### 4. `week01/hello.py` dosyasını yazın
Python'ı yalnızca çalıştırabildiğinizi değil, yazabildiğinizi gösteren küçük bir betik.
`input()` ile bir ad okumalı ve **bir f-string, bir liste ve bir for döngüsü**
kullanmalı. Kısa tutun — on satır fazlasıyla yeter.

**Ve yalnızca sizin aklınıza gelecek bir şey yapsın.** "Merhaba, ad" değil — o örnek; otuz
kişi örneği teslim ederse hiçbiri hakkında bir şey öğrenmem. Sizin için anlamı olan bir
liste üzerine kurun: bu dönem aldığınız dersler, kampüse giderken geçtiğiniz beş durak,
takip ettiğiniz bir takımın kadrosu, pişirdiğiniz bir yemeğin malzemeleri. On satır yine
yeter. Amaç, dosyanızın en üstteki ad okunmadan da sizin olduğunun anlaşılmasıdır.

```
python week01/hello.py
```

### 5. Bir LLM'i web arayüzünden keşfedin
Bu hafta API çağrısı yok — anahtar yok, SDK yok. **İki farklı asistan** seçin ve
tarayıcıda açın: Claude, Gemini, ChatGPT, Copilot, Codex — erişebildiğiniz herhangi ikisi.
20 dakika ikisine de sorular sorun.

`week01/llm_notes.md` dosyasını **kendi cümlelerinizle, en az 300 kelime** yazın ve şu
soruları yanıtlayın: transformer nedir, attention mekanizması hangi sorunu çözer ve bir
LLM bir sonraki token'ı nasıl üretir?

Bu, derste bir modelin değil sizin cümlelerinizi istediğim tek dosya. Bunu okuyarak
anlayabilirmişim gibi yapmayacağım, çünkü anlayamam; anladığını iddia eden hiçbir araç da
anlayamaz — bu yüzden görev, yapıştırılmış bir yanıtın oturmayacağı biçimde kuruldu:

- **Her açıklamayı kendi oturumunuza bağlayın.** İki asistanınızdan birinin verdiği gerçek
  yanıtı alıntılayın ve nerede belirsiz, yanlış ya da beklediğinizden iyi olduğunu
  söyleyin. Konuşmanızda bulunmayan bir model bu paragrafı yazamaz.
- **Token'ları açıklarken örnek olarak kendi `hello.py` dosyanızı kullanın:** sizce kendi
  on satırınız kaç token ve bu sayı neden kelime sayısıyla aynı değil?
- **Hâlâ anlamadığınız şeyle bitirin.** Dürüst bir paragraf. Bir dil modelinin en kötü
  olduğu kısım budur, çünkü neyi kaçırdığınızı bilmez — ve en dikkatle okuduğum kısım
  da budur.

Transformer'lar hakkında akıcı, doğru, genel bir kompozisyon; sizin yirmi dakikanız
olduğu görülen daha kaba bir metinden daha az puan alır. Dönem bir proje savunmasıyla
biter. Şimdiden o güne kadar yazdığınız her şey, o konuşmaya verdiğiniz bir sözdür.

Oradayken sorularınızdan birini **iki kez** sorun: bir kez belirsiz biçimde, bir kez de
bağlamı ve kısıtları açıkça yazarak. İki yanıtı da `llm_notes.md` içine koyun ve neyin
değiştiğini bir cümleyle söyleyin. Bu hafta size prompt teknikleri öğretilmiyor —
sorunun yanıtı biçimlendirdiğini fark etmeniz isteniyor. Dönemin ilerisinde buna
doğru düzgün döneceğiz.

### 6. Modelin yanlış yaptığı bir şey bulun
İki asistana da, iyi bildiğiniz bir konuda aynı olgusal soruyu sorun. Çelişkiyi ya da
hatayı `llm_notes.md` içine kaydedin. Her model halüsinasyon görür; bu dönemki işiniz,
ne zaman gördüğünü fark etmektir.

### 7. `week01/ai_log_01.md` dosyasını yazın

Dosya `week01/` içinde, bu haftanın diğer işlerinin yanında. Hangi asistanı
kullandığınız, ne sorduğunuz, neyi doğru yaptığı ve neyi düzeltmek zorunda kaldığınız.
**Evidence** bloğu isteğe bağlı değildir: gerçek yazışmayı — sizin isteminizi ve yanlış
yanıtı — kod bloğunun içine yapıştırın. On–on beş satır, hatayı gösteren kısma kırpılmış.

Arkasında yazışma olmayan bir iddia puan getirmez. Konuşmanın tamamını saklamak
isterseniz `week01/transcript.md` olarak kaydedin; günlüğünüzde tutarsız bir şey
olmadıkça okumam.

### 8. `.gitignore` dosyanızı doğrulayın
`.venv`, `.env` ve `__pycache__` zaten içinde olmalı.
Depo kökünde `.env.example` oluşturun — yalnızca değişken adları, asla değerler.

### 9. Kontrolleri kendiniz çalıştırın

Deponuz her push'ta kendi teslimlerini denetler ve açmanız gereken bir şey yoktur: hangi
haftada olduğunu derse sorar, dolayısıyla gördüğünüz şey her zaman size karşı çalıştırılan
şeydir.

Push etmeden önce aynı kontrolleri yerelde çalıştırın:

```bash
python .github/check_deliverables.py
```

Bildirdiklerini düzeltin. GitHub'daki kırmızı çarpı bir not değil, bilgidir — hâlâ bir şey
yapabilecekken neyin eksik olduğunu söyler.

### 10. Commit ve push
```
git add .
git commit -m "week01: environment setup and first LLM exploration"
git push
```

### 11. Bu hafta LMS'e teslim edilecek bir şey yok

Form yok, yapıştırılacak bağlantı yok, bana gönderilecek kullanıcı adı yok. Beni
Collaborator olarak eklemek teslimin **kendisidir** — GitHub kimin eklediğini bana söyler,
`student.json` dosyanız da o kişinin hangi öğrenci olduğunu.

Bu, haftanın tamamını iki şeyin taşıdığı anlamına gelir ve ikisi de 1. ve 2. görevde:
Collaborator olmalıyım ve `student.json` içindeki öğrenci numaranız doğru olmalı. Birini
yanlış yaparsanız çalışmanız, ne kadar iyi olursa olsun, benim için görünmezdir.

2. Hafta'da gösterilen panoda sizin için bir şey yoksa sınıfta söyleyin. Neredeyse her
zaman bu ikisinden biridir ve ikisi de bir dakikada düzelir.

---

## Teslim listesi
- [ ] `student.json` — beş alan da dolu, `section` doğru
- [ ] Depo **private** ve ben Collaborator olarak ekliyim
- [ ] `week01/setup_proof.md` — ortam doğrulanmış
- [ ] `week01/hello.py` — çalışıyor; f-string, liste ve for döngüsü kullanıyor
- [ ] `week01/llm_notes.md` — kendi cümlelerinizle 300+ kelime, bir model hatası ve bir sorunun iki farklı ifadesi
- [ ] `week01/ai_log_01.md` — doldurulmuş, **yapıştırılmış Evidence bloğu dahil**
- [ ] `.gitignore` `.venv`, `.env`, `__pycache__` içeriyor; `.env.example` mevcut
- [ ] Kontroller GitHub'da yeşil
- [ ] En az 3 commit push edilmiş
- [ ] Depo adı tam olarak `aiasd-project`, bildirdiğiniz kullanıcı adının altında

---

## Bu hafta nasıl notlanıyor

Bu hafta olağan ritmin istisnasıdır. 2. Hafta'dan itibaren her dersin sonunda deponuzdan
beş puan, Cumartesi 23:59'da beş puan okunur. 1. Hafta'da ders sonunda hiçbir şey
alınmaz — çoğunuzun henüz çalışan bir ortamı olmayacak ve kurulum notlanan bir iş
değildir. **Bu hafta beş puan değerindedir; tamamı Cumartesi 23:59'da deponuzdan
okunur:**

- **3** — otomatik kontroller: şablondan oluşturulmuş depo, private, ben Collaborator,
  `student.json` tam, `setup_proof.md`, üç gereksinimi karşılayan `hello.py`, kendi
  cümlelerinizle `llm_notes.md`, `.gitignore` ve `.env.example`, kontroller yeşil.
- **1** — commit disiplini: haftaya yayılmış en az üç commit; Cumartesi gecesi tek push
  değil.
- **1** — `week01/ai_log_01.md` dosyanız: gerçek bir oturum, gerçek bir model hatası,
  yapıştırılmış yazışma. Bunu kendim okuyorum.

Teslim saati her hafta aynıdır, dolayısıyla hesaplanacak bir şey yok: Cumartesi gece
yarısı deponuzda ne varsa, notladığım odur.

Bir LLM bu ödevin istediği her dosyayı üretebilir. Yapamadığı şey, o dosyaları
çevresindeki on haftayla tutarlı kılmak ya da kendi hatalarını sizin yerinize fark
etmektir. Asıl değerlendirilen budur.
