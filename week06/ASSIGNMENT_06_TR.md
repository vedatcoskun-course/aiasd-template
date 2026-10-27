# 6. Hafta Ödevi — Kendi Özelliğiniz (feature), Uçtan Uca (end to end)

**Teslim:** ders içi bölüm 11:45'e kadar push · kalanı Cumartesi 23:59 · Proje reponuza commit edin

## Projenizde şimdiye kadar ne yaptık, bundan sonra ne yapacağız

Beş hafta önce projeniz yalnızca bir fikirdi. Şimdi ona bakın:

- **1. hafta:** araçlarınız ve iki yapay zeka asistanıyla (AI assistant) ilk gerçek konuşmalarınız.
- **2. hafta:** gerçek bir problem, onu yaşayan gerçek insanlar ve ürününüzün yapması gerekenlerin ilk listesi.
- **3. hafta:** projenizi grubunuza sundunuz ve pazara (market) baktınız. Proje kesinleşti.
- **4. hafta:** proje ekranlara (screens) dönüştü ve bir sınıf arkadaşınız test case'lerinizle onlara tıkladı.
- **5. hafta:** proje yazılıma dönüştü: parçaları, API sözleşmesi (API contract), her endpoint'e cevap veren (çoğuna 501
  ile) bir sunucu (server) ve bu haftayı bekleyen kırmızı testler (red tests).

Bu hafta ürününüz kendi işini ilk kez yapıyor. Bu hafta giriş (login) ile ilgili değil. Giriş her
projede aynıdır; bu yüzden ders onu size kullanıma hazır verir. Onu yaklaşık yirmi dakikada sunucunuza
bağlarsınız. Hafta, **yalnızca sizin projenizin yaptığı** şey içindir: kendi işlevsel (functional) `must`
gereksinimleriniz (requirements). Onları 2. haftada yazdınız ve 4. haftada çizdiniz. 5. haftada API sözleşmeniz giriş
satırlarını aldı. Eksikse bu hafta onların satırlarını da alır (§2). Cumartesi'ye kadar her biri:

- sunucunuzda çalışır;
- GitHub'da geçen testlere sahiptir;
- web istemcinizde (web client), giriş yapmış bir kullanıcının onu yapabildiği bir sayfaya sahiptir.

7. haftada aynı özellik bir telefonda çalışacak. 8. haftada ürününüz sohbet botunu (chatbot) alacak ve üç
istemcide (client) de çalışacak. İlk build'i mağazanın (store) test kanalına (test track) çıkacak. Sonra gerçek testçiler (testers, 9. hafta),
gerçek kullanıcılar (users, 10. hafta) ve mağazanın incelemesi (review) gelecek. Aralık'ta kendi uygulamanızı bir
mağazadan kuracaksınız.

## Bir gereksinim, baştan sona

Her işlevsel `must` gereksiniminizin, bir zincir (chain) gibi sekiz halkası (links) vardır. İlk dördü zaten elinizde.
5. halka (`api.md` satırları) giriş için elinizde. Kendi özelliğiniz için eksikse onu şimdi yazarsınız
(§2). Sonra son üç halkayı eklersiniz ve zincir tamamlanır.

| Halka | Nerede durur | Ne zamandan beri |
|---|---|---|
| 1. Gereksinim, kabul ölçütüyle (acceptance criterion) | `week02/requirements.json` | 2. hafta |
| 2. Kullanım senaryosu (use case) | `week02/SRS.md` | 2. hafta |
| 3. Ekranı | `week04/prototype/`, `<!-- serves: REQ-… -->` ile | 4. hafta |
| 4. Test case'leri, her biri `"run"` ile | `week04/test_cases.json` | 4. hafta |
| 5. API sözleşmesindeki satırları | `week05/api.md` | 5. hafta (giriş) · şimdi (özelliğiniz) |
| 6. Route'ları, çalışır halde: artık 501 değil | `server/` | **bu hafta** |
| 7. Test case kimliğiyle (id) adlandırılmış testleri, **GitHub Actions'ta yeşil** | `server/tests/` | **bu hafta** |
| 8. Web istemcisindeki sayfası (page), sunucuyu `fetch` ile çağırır | `web/`, `<!-- serves: REQ-… -->` ile | **bu hafta** |

**Kaynak (source) `requirements.json` dosyasıdır. Diğer her halka onu izler.**

Gereksinimlerin tek yeri de odur. Onları `SRS.md` içine kopyalamayın. SRS §4 ve §5'te tek satır yeterlidir:
"The requirements are in `week02/requirements.json`." SRS, use case'lerinizi (§3) tutar.

- Route, gereksinimin ve kabul ölçütünün söylediğini yapar. Yapması en kolay olanı ya da bir asistanın
  önerdiğini yapmaz.
- Test, test case'in beklediğini kontrol eder.
- Sayfa, prototipin ekranıdır; artık gerçektir.

Bazen kurarken bir halkanın yanlış olduğunu görürsünüz. Örneğin bir test case, gereksinimin söylemediği
bir şeyi bekler ya da sayfa `api.md` içinde olmayan bir listeye ihtiyaç duyar. O zaman önce o halkayı,
`PROPOSAL.md` içindeki satırıyla (§9) değiştirin. Sonra kodu değiştirin. Gereksinimi yalnızca koda
uysun diye asla değiştirmeyin.

Dersin örnek projesi StudyRoom'dan küçük bir örnek:

| Halka | StudyRoom |
|---|---|
| Gereksinim | REQ-002 — Bir öğrenci boş bir çalışma odasını 30 ile 120 dakika arası ayırır; dolu bir saat reddedilir. |
| Kullanım senaryosu | UC2 — Oda ayır: oda, başlangıç saati ve süre seçilir; uygulama onaylar ya da saatin dolu olduğunu söyler. |
| Ekran | `book.html` — `<!-- serves: REQ-002 -->` |
| Test case'ler | TC-002-01 (boş bir saat ayrılır, `run: web`), TC-002-02 (dolu bir saat reddedilir, `run: server`) |
| API satırları | `POST /bookings` → 201 · 409 saat dolu · 422 süre 30–120 dışında · 401 giriş yapılmamış |
| Route | `server/bookings.py`: `create_booking`, `current_user` ile |
| Test | `test_TC_002_02_a_busy_slot_is_refused`, Actions sekmesinde yeşil |
| Sayfa | `web/book.html` — `<!-- serves: REQ-002 -->`, `fetch("/bookings", …)` |

### Bu hafta bilmeniz gerekenler

| | Nedir |
|---|---|
| **`server/course_login.py`** | Dersin girişi (course login). Herkes için aynı olan tek bir dosyadır. Üç giriş yolunuzda cevap verir. Onu okursunuz ama asla değiştirmezsiniz. |
| **`server/login_contract.json`** | Sizin yazdığınız birkaç satır. Dersin girişine ve ders testlerine üç giriş yolunuzu ve alanlarınızın adlarını söyler. |
| **Token, Bearer başlığı (header)** | Doğru koddan sonra sunucu bir **token**, yani uzun, rastgele bir dizgi (string) verir. İstemci onu her istekte `Authorization: Bearer <token>` başlığıyla gönderir. |
| **`current_user`** | `course_login`'den gelir. Bir route'a `user: str = Depends(current_user)` yazın. O zaman route yalnızca giriş yapmış bir kullanıcı için çalışır ve `user` onun e-posta adresidir. Token yoksa cevap 401'dir. |
| **401, 403, 404, 409, 422** | 401: giriş yapılmamış. 403: giriş yapılmış ama izin yok (başkasının verisi, eğitmene ait bir işlem). 404: böyle bir şey yok. 409: zaten var olan bir veriyle çakışıyor. 422: bir alan eksik, boş ya da yanlış biçimde. |
| **`AIASD_CODE_FILE`** | Bir ortam değişkeni (environment variable). Ayarlıysa giriş, kodu e-postayla göndermez, o dosyaya yazar. Derste ve testlerde kullanırsınız. |
| **`TestClient`** | 5. haftadaki gibi, testte ağ olmadan uygulamanızla konuşur. |
| **`fetch`** | Bir web sayfasının sunucuya istek göndermek ve cevabı okumak için kullandığı JavaScript fonksiyonu. |
| **`StaticFiles`** | FastAPI'nin `web/` sayfalarını sunan parçası. Böylece sayfalarla sunucu aynı adreste olur. |
| **`sessionStorage`** | Bir web sayfasının, sekme açıkken token'ı sakladığı yer. |
| **`.env`, `.gitignore`, SMTP** | `.env` e-posta ayarlarınızı ve şifrenizi tutar. Yalnızca sizin bilgisayarınızda durur. `.gitignore` onu git'in dışında tutar. SMTP, bir programın e-posta gönderme yoludur. |
| **CI, GitHub Actions** | Her push'tan sonra GitHub'da çalışan kontroller (checks). Bu haftadan itibaren testleri de çalıştırırlar. Ders notunuz (lecture mark) onların sonucunu kullanır. |
| **Ders testleri (course tests)** | `course_tests/`: girişin herkes için aynı olan on testi. Girişi doğru bağlayıp bağlamadığınızı kontrol ederler. |

## Ne, ne zaman teslim edilir

| Ne zaman | Ne yaparsınız | Nerede |
|---|---|---|
| **Dersten önce** | Denetleyiciyi (checker) bir kez çalıştırın; `pip install -r week06/requirements.txt`; `python -m pytest course_tests -q` (on testin hepsi bir hatayla durur: "Fill in server/login_contract.json"). İşlevsel `must` gereksinimlerinizin listesini çıkarın ve ilk kuracağınızı seçin | aşağıdaki kutu |
| **Derste, yaklaşık 10:00'a kadar** | Giriş bağlanmış: `login_contract.json` elle, `main.py` içinde `course_login.router`, kendi giriş taslaklarınız silinmiş. İlk gereksiniminiz seçilmiş ve `api.md` satırları kontrol edilmiş (ya da yazılmış, §2) | §1–§2 |
| **Derste, yaklaşık 11:00'e kadar** | Route'ları çalışıyor, kullanıcı gereken yerde `current_user` ile; test case'leriyle adlandırılmış testleri **GitHub'da yeşil** | §3–§4 |
| **Derste, 11:45'e kadar** | Prototip ekranı, bu route'ları çağıran, girişin arkasında duran bir `web/` sayfası olmuş · saldırgan turu (attacker round), `group_06.json` dosyasına yazılmış | §5–§7 |
| **Cumartesi 23:59'a kadar** | **Her** işlevsel `must` gereksinim uçtan uca · gerçek e-postayla kod · bütün testler GitHub'da yeşil · S2 · her test case'te `"run"` · her bulgu (finding) için kararınız · `ai_log_06.md` | §8–§16 |

> ## İşin ortasında commit edin, sonunda değil
>
> Yukarıdaki saatler bir tempo, push saati değil. Her işi daha bitmeden commit edin; örneğin yanıt
> veren ama henüz kullanıcıyı kontrol etmeyen bir route, yazılmış ama hala kırmızı olan bir test ya
> da ekranı gösteren ama henüz sunucuyu çağırmayan bir sayfa. Çalıştığında yeniden commit edin ve
> her commit'i hemen push edin. Geçmişiniz (history) her dosyanın nasıl büyüdüğünü gösterir; tek
> commit'te bitmiş olarak gelen bir iş commit puanına sayılmaz.

> ## AI log'u (yapay zeka günlüğü) insan yazar. İstisna yok.
>
> `week06/ai_log_06.md` dosyasını **siz**, kendi cümlelerinizle yazarsınız. Evidence bloğu ve
> asistanın cevabından yaptığınız kalın alıntılar (§15) dışında asistan kullanmazsınız: ne yazmak
> için, ne "düzeltmek" için, dil için bile. **Asistana yazdırılmış bir günlük 0 puan alır.**
> İngilizceniz ya da Türkçeniz notlanmaz. Her günlüğü bir insan okur.

> ## Elle yazdığınız iki dosya
>
> **`server/login_contract.json`**: üç giriş endpoint'iniz ve alan adlarınız. Onları `api.md`
> dosyanızdan kendiniz kopyalarsınız. **`week06/group_06.json`**: grup arkadaşınızın (groupmate) ne denediği ve
> sunucunuzun ne yaptığı. Bunu olay sırasında siz yazarsınız. Sonra kararlarınızı eklersiniz. İki
> dosyayı da hiçbir asistan yazmaz, düzeltmez ya da tamamlamaz.

> ## Giriş kullanıma hazır gelir ve her projede aynı biçimde çalışır
>
> - Kullanıcı bir e-posta adresi verir ve **10 dakika** geçerli, **yalnızca bir kez** kullanılabilen
>   **4 haneli bir kod** alır.
> - Aynı adres **bir dakika içinde** yeni kod isterse **429** alır.
> - Yanlış ya da süresi dolmuş bir kod **401** alır. E-posta adresi olmayan bir şey **422** alır.
> - **Üst üste 3 yanlış koddan** sonra (yeni kod sayımı sıfırlamaz) o adrese yapılan her giriş, doğru
>   kodla bile, **15 dakika boyunca 429** alır.
> - Doğru kod bir **token** verir. "me" endpoint'iniz, `Authorization: Bearer <token>` ile **200** ve
>   adresle cevap verir; token olmadan ya da yanlış bir token'la **401**.
>
> Bunların hepsini `server/course_login.py` yapar. Bu hafta giriş yazmazsınız. Dersin girişini
> bağlarsınız (§1) ve on ders testi bunu yaptığınızı kontrol eder. REQ-001'iniz ya da test
> case'leriniz başka bir şey söylüyorsa (örneğin 6 haneli bir kod), onları bir değişiklik talebiyle
> (change request) değiştirin (§9).

> ## Ders notunuz dizüstü bilgisayarınızdan değil, GitHub'dan gelir
>
> Push ettiğinizde GitHub Actions denetleyiciyi çalıştırır. Denetleyici de ders testlerini ve kendi
> testlerinizi çalıştırır. Ders notunuz için, dersin sonuna dek push ettiğiniz son commit'in bu
> çalıştırmadaki sonucunu alırım. 11:45'e kadar push edin. Sonra **Actions** sekmesini açın ve
> çalıştırmanın bitmesini izleyin. Yalnızca sizin bilgisayarınızda geçen bir test sayılmaz.

> ## Asla force push yapmayın. Küçük bir düzeltme size hiçbir şeye mal olmaz.
>
> `git push --force` geçmişinizden commit siler. Çalışmanızı bu geçmişe bakarak notlandırırım. CI bir
> ruff hatası ya da bir yazım hatası yüzünden kırmızı olursa, hatayı düzeltin ve düzeltmeyi **yeni** bir
> commit olarak push edin. Küçük bir düzeltme commit'i commit puanını asla düşürmez.

> **Grubunuz tek bir iş için yeniden bir araya geliyor:** §6'daki saldırgan turu. Haftanın geri
> kalanında tek başınıza, kendi projeniz üzerinde, kendi bilgisayarınızda çalışırsınız.

> **Dersten önce:** `python .github/check_deliverables.py` komutunu bir kez çalıştırın. Komut
> `week06/` klasörünü, `course_tests/` klasörünü, `server/course_login.py` dosyasını ve henüz yoksa
> `server/login_contract.json` dosyasını getirir. Sonra sanal ortamınız (virtual environment) etkinken:
>
> ```bash
> pip install -r week06/requirements.txt
> python -m pytest course_tests -q
> ```
>
> On testin hepsi bir hatayla durur ("Fill in server/login_contract.json"). Başlangıç noktası budur.
> Sonra `week02/requirements.json` dosyasını açın. `"functional": true` ve `"priority": "must"` olan her
> gereksinimi, REQ-001 (giriş) dışında, bir kenara yazın. Bu liste, bu haftaki işinizdir. İlk
> kuracağınızı seçin: ürününüzün var olma nedeni olan gereksinimi. `week05/api.md` dosyasında bu
> gereksinimin satırları henüz yoksa §2'ye bakın.

---

## Bu haftayla ne geliyor

- `week06/`: bu ödev, ders sunumu, `group_06.json` (saldırganın kaydı), `ai_log_06.md` ve `requirements.txt`
  (geçen haftanın paketleri, artı `freezegun`, `python-dotenv` ve `ruff`).
- `server/course_login.py`: dersin girişi. `course_tests/` gibi derse aittir. Onu değiştirirseniz
  denetleyici aslını geri koyar. GitHub'da dersin kendi kopyası çalışır. Okuyun: ilk satırları onun nasıl
  bağlanacağını anlatır.
- Reponun kökünde `course_tests/`: dersin on giriş testi. Onlar da derse aittir.
- Henüz yoksa `server/login_contract.json`: doldurmanız için [köşeli parantez] içinde değerler.

---

## Bu hafta asistan nerede yardım eder, nerede etmez

| Parça | Asistan |
|---|---|
| Bir route'un kodu, gereksinimi, kabul ölçütü ve `api.md` satırı isteme (prompt) yapıştırılmış olarak (bir route, bir commit) | **Yardım eder** |
| Test case'lerinizden birinden yazılan bir test (test case'le satır satır karşılaştırmak sizin işiniz) | **Yardım eder**, onay sizde |
| Bir sayfanın `fetch` kullanan JavaScript'i | **Yardım eder** |
| Kırmızı bir testi ya da bir GitHub Actions kaydını okumak | **Yardım eder** |
| Gereksinim bir şey söylemiyorsa route'un ne yapacağına karar vermek | **Yardım etmez**: gereksinim karar verir. Gereksinim bir şey söylemiyorsa önce gereksinimi değiştirin (§9) |
| `server/login_contract.json` | **Yardım etmez**: `api.md` dosyanızdan elle kopyalarsınız |
| `week06/group_06.json`: saldırganın ne denediği, ne olduğu ve kararınız | **Yardım etmez** |
| Testleri çalıştırmak ve GitHub'ın ne dediğini okumak | **Yardım etmez**: siz çalıştırır, siz bakarsınız |
| Change log satırları ve change request'ler | **Yardım etmez** |
| `ai_log_06.md`, Evidence bloğu ve kalın alıntıları dışında | **Yardım etmez** |

---

## Derste — 11:45'e kadar push

Ders dört bölümden oluşur:

1. yaklaşık yirmi dakika anlatım;
2. giriş ve ilk gereksiniminiz (yaklaşık **10:00**'a kadar);
3. onun route'ları ve testleri (yaklaşık **11:00**'e kadar);
4. sayfası ve saldırgan turu (**11:45**'e kadar).

Her bölümde işi daha bitmeden commit edip push edin, çalıştığında yeniden.

### 1. Girişi bağlamak — on beş, yirmi dakika

**Ne zaman:** derste, yaklaşık 10:00'a kadar.

**Giriş neden kullanıma hazır geliyor.** Her proje aynı biçimde giriş yapar. Girişte küçük hatalar
yapmak da kolaydır (süresi hiç dolmayan bir kod, herkese cevap veren bir "me"). Onu yazmak bütün
haftanızı alırdı ve kendi özelliğinizin öğretmediği pek az şey öğrenirdiniz. Bu yüzden ders size on testle
kontrol edilen bir giriş verir. Haftanızı yalnızca sizin kurabileceğiniz kısma ayırırsınız.

**Derse ait dosyalar.** 6. haftadan itibaren denetleyici `course_tests/` klasörünü ve
`server/course_login.py` dosyasını da getirir; `server/login_contract.json` sizde yoksa onu da.
`course_tests/` ya da `course_login.py` dosyalarını değiştirmeyin: denetleyici dersin kopyasını geri koyar
ve GitHub her zaman onu kullanır.

**Adım 1 — `server/login_contract.json`, elle.** `week05/api.md` dosyanızı açın. Üç giriş endpoint'inizi tablodakiyle birebir aynı kopyalayın: metot (method),
bir boşluk ve yol (path). Sonra alanlarınızın (fields) adlarını yazın:

```json
{
  "request_code": "POST /auth/code",
  "login": "POST /auth/login",
  "me": "GET /auth/me",
  "email_field": "email",
  "code_field": "code",
  "token_field": "token",
  "test_email_domain": "example.com",
  "email_must_end_with": "",
  "app_name": "StudyRoom"
}
```

- Giriş, `token_field` adınızın altında `{"token": "..."}` ile; "me" de `email_field` adınızın altında
  `{"email": "..."}` ile cevap verir. `api.md` başka bir şey söylüyorsa satırı değiştirin ve Change log satırını
  yazın.
- `api.md` dosyanızda "me" endpoint'i (giriş yapmış kullanıcıyla cevap veren) yoksa satırını şimdi ekleyin.
- `email_must_end_with`: bunu yalnızca REQ-001'iniz bazı adresleri kabul ediyorsa doldurun. Örneğin
  `".edu.tr"` ya da birkaç sonu olan bir liste. O zaman `test_email_domain` de kabul edilen bir alan adı (domain)
  olmalı, örneğin `"student.example.edu.tr"`.
- `app_name`, kodu getiren e-postada görünen addır.

**Adım 2 — `server/main.py`.** İki satır:

```python
from server import course_login

app.include_router(course_login.router)
```

**Adım 3 — kendi giriş taslaklarınızı silin.** 5. haftadan kalan ve bu yollarda 501 dönen üç route'u
silin. Kalırlarsa dersin girişinden önce onlar cevap verir.

**Adım 4 — çalıştırın.**

```bash
python -m pytest course_tests -q                                          # on test geçer
AIASD_CODE_FILE=login_code.txt uvicorn server.main:app --reload          # macOS, Linux
$env:AIASD_CODE_FILE="login_code.txt"; uvicorn server.main:app --reload  # Windows PowerShell
```

`/docs` sayfasında:

1. `{"email": "you@example.com"}` gövdesiyle (body) bir kod isteyin (`login_contract.json` dosyanızdaki alan
   adlarını kullanın);
2. kodu `login_code.txt` içinde okuyun;
3. `{"email": "you@example.com", "code": "1234"}` ile giriş yapın (dosyadaki 4 hane) ve token'ı
   kopyalayın;
4. **Authorize** düğmesine basın ve token'ı yapıştırın;
5. "me"yi çağırın.

`login_code.txt` dosyasını `.gitignore`'a ekleyin. `login_contract.json` dosyasını değiştirdikten sonra
sunucuyu yeniden başlatın: sunucu bu dosyayı yalnızca başlarken okur.

> **5. hafta giriş testleriniz.** Dersin girişiyle bir test gerçek bir e-posta göndermemelidir.
> `AIASD_CODE_FILE` yoksa giriş, `.env` içindeki ayarlarla bir e-posta gönderir; ayar yoksa 503 döner
> (GitHub'da her zaman). Bu yüzden her testi şöyle değiştirin:
>
> ```python
> from fastapi.testclient import TestClient
>
> from server.course_login import reset_for_tests
> from server.main import app
>
> client = TestClient(app)
>
>
> def test_TC_001_01_a_code_is_sent(monkeypatch, tmp_path):
>     reset_for_tests()
>     monkeypatch.setenv("AIASD_CODE_FILE", str(tmp_path / "code.txt"))
>     response = client.post("/auth/code", json={"email": "deniz@example.com"})
>     assert response.status_code == 200
>     assert (tmp_path / "code.txt").read_text().isdigit()
> ```
>
> - Kendi yollarınızı ve `login_contract.json` dosyanızdaki alan adlarını kullanın.
> - `email_must_end_with` kuralını geçen bir adres kullanın.
> - Giriş yapmak için kodu dosyadan okuyun.
> - Her testte yeni bir adres kullanın ya da önce `reset_for_tests()` çağırın.
> - Cevaplar dersin cevaplarıdır: `{"sent": true}`, 401, 429. Bir test yalnızca durum kodunu
>   (200, 401, 429) kontrol eder, mesajın metnini değil.
> - Dersin girişinde olmayan bir kuralı kontrol eden bir test: önce test case'ini değiştirin (§9).
>   Sonra testi değiştirin.
> - Ders testleri girişi zaten kapsar. Bu yüzden bir server testi tutmuyorsanız bir TC-001 test case'i
>   `"run": "manual"` da olabilir. Ama `"run": "server"` olan her `must` test case'inin Cumartesi günü
>   geçen bir testi olmalıdır.

### 2. İlk gereksiniminiz — seçin ve zincirini kontrol edin

**Ne zaman:** derste, yaklaşık 10:00'a kadar.

Dersten önce seçtiğiniz gereksinimi alın. Kod yazmadan önce halkalarını yan yana koyun: gereksinim ve
kabul ölçütü, kullanım senaryosu, ekranı, test case'leri ve `api.md` satırları. Kontrol edin:

- Aynı şeyi mi söylüyorlar?
- Her test case'in ihtiyaç duyduğu `api.md` satırları var mı?
- Ekran, kabul ölçütünün söz verdiğini gösteriyor mu?

`api.md` dosyasında bu gereksinimin henüz satırı yoksa (5. hafta yalnızca giriş satırlarını istedi),
satırları şimdi, elle, hiçbir route kodundan önce, tarihli bir Change log satırıyla yazın.

Bir halka eksik ya da yanlışsa onu şimdi, `PROPOSAL.md` içindeki satırıyla (§9) düzeltin.

### 3. Route'ları, gerçekten

**Ne zaman:** derste, yaklaşık 11:00'e kadar.

Her route'unda 501'i gerçek işle değiştirin. Bu hafta verilerinizi bellekte (in memory) tutun: `server/` içindeki
bir modülde bir sözlük (dictionary) ya da liste yeter. 8. haftadan itibaren, testçiler uygulamanızı kullanırken,
verileriniz sunucu yeniden başlayınca kaybolmamalıdır: onları bir dosyada ya da seçtiğiniz bir
veritabanında (database) tutun (SQLite Python ile birlikte gelir). Kullanıcı gereken bir route, onu
`current_user` ile ister:

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from server.course_login import current_user

router = APIRouter()
bookings: list[dict] = []  # şimdilik bellekte; 8. haftadan itibaren dosyada ya da veritabanında


class NewBooking(BaseModel):
    room: int
    start: str
    minutes: int


@router.post("/bookings", status_code=201)
def create_booking(body: NewBooking, user: str = Depends(current_user)) -> dict:
    """REQ-002: a student books a free room for 30 to 120 minutes; a busy slot is refused."""
    if not 30 <= body.minutes <= 120:
        raise HTTPException(status_code=422, detail="A booking lasts 30 to 120 minutes.")
    if any(b["room"] == body.room and b["start"] == body.start for b in bookings):
        raise HTTPException(status_code=409, detail="This slot is already booked.")
    booking = {
        "id": len(bookings) + 1,
        "room": body.room,
        "start": body.start,
        "minutes": body.minutes,
        "by": user,
    }
    bookings.append(booking)
    return {"booking_id": booking["id"]}
```

Bu örnek `server/bookings.py` dosyasıdır. Route'ları ancak `server/main.py` onun router'ını eklediğinde
cevap verir. Oraya iki satır ekleyin (import satırı dosyanın başına, diğer import'ların yanına):

```python
from server import bookings

app.include_router(bookings.router)
```

Sonra `ruff check . --fix`, `server`'dan gelen iki import'unuzu tek satırda birleştirir:
`from server import bookings, course_login`.

- **`api.md` satırındaki her hata, durum koduyla (status code)** ve kullanıcının anlayacağı bir mesajla. Route, test
  case'inizin beklediği mesajı gönderir ("This slot is already booked.").
- **Kim yapabilir.** `current_user` kimin sorduğunu söyler. Bir kullanıcı başka bir kullanıcının
  verisini okuyamaz ya da değiştiremez. Bir öğrenci, yalnızca eğitmenin ya da sahibin (owner) yapabileceği şeyi
  yapamaz. İki durumda da cevap **403**'tür. Buna sunucu karar verir; sayfada bir düğmeyi gizlemek
  yetmez.
- **Boş ya da yalnızca boşluklardan oluşan bir metin** boştur: kontrol etmeden önce `.strip()` uygulayın.
- Belki sayfa, `api.md` dosyanızda satırı olmayan bir şeye ihtiyaç duyar (örneğin gösterilecek bir
  liste). O zaman önce satırı, Change log satırıyla ekleyin. Sonra route'u ekleyin.

Asistanınızdan bir seferde bir route isteyin. Gereksinimi, kabul ölçütünü ve `api.md` satırını isteme
koyun. Sonra cevabın tamamını okuyun. Asistanlar "yardım etmeyi" sever: kimsenin istemediği bir alan
eklerler, "basit olsun diye" bir kontrolü atlarlar ya da bir hatayı 200'e çevirirler. Bunların her biri
test case'lerinizden birini bozar.

### 4. Test case'leriyle adlandırılmış testleri — GitHub'da yeşil

**Ne zaman:** derste, yaklaşık 11:00'e kadar.

Önce bu gereksinimin test case'lerine `"run"` ekleyin (§14). Sonra `"run": "server"` olan her biri için
`server/tests/` içine bir test yazın. Testi test case kimliğiyle adlandırın:
`test_TC_002_02_a_busy_slot_is_refused`. Her `assert`, test case'in beklenen sonuçlarından biridir. Dersin giriş yardımcısı, bir test kullanıcısını gerçek girişinizden
geçirerek giriş yaptırır (aşağıda "Kendi testleriniz"e bakın). `python -m pytest server/tests -q`
çalıştırın, push edin ve **Actions** sekmesinde çalıştırmayı izleyin. Ders notu için okuduğum satır
`AIASD-TEST … TC-002-02 passed` satırıdır.

### 5. Sayfası — prototipin ekranı, gerçek oldu

**Ne zaman:** derste, 11:45'e kadar.

Gereksinimin ekranını `week04/prototype/` içinden `web/` klasörüne kopyalayın. Görünüşünü koruyun: o
sizin tasarımınız. `<!-- serves: REQ-… -->` satırını da koruyun. Sonra onu gerçek yapın:

- prototipin sabit verilerini sunucunun cevaplarıyla değiştirin;
- kullanıcının yaptığını token'la birlikte `fetch` ile sunucuya gönderin.

```javascript
async function api(method, path, body) {
  const options = { method, headers: { Authorization: `Bearer ${sessionStorage.getItem("token")}` } };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const response = await fetch(path, options);
  if (response.status === 401) location.href = "login.html";   // girişin arkasında
  return { status: response.status, data: await response.json().catch(() => ({})) };
}

document.querySelector("#book").addEventListener("click", async () => {
  const { status, data } = await api("POST", "/bookings", { room: 3, start: "14:00", minutes: 60 });
  document.querySelector("#message").textContent = status === 201 ? "Booked." : data.detail;
});
```

- **`await` yalnızca bir `async` fonksiyonun içinde:** `api()` fonksiyonunu yukarıdaki gibi `async` bir
  tıklama işleyicisinde (click handler) çağırın (ya da script'i `type="module"` yapın).
- **Girişin arkasında:** sayfanın bir token'a ihtiyacı vardır. Prototipin `index.html` ve `code.html`
  ekranları `web/login.html` olur (iki adım tek sayfada ya da `login.html` ile başlayan iki sayfa).
  Sayfa `<!-- serves: REQ-001, REQ-006 -->` satırını korur. request_code ve login yollarınızı `api()` ile
  değil, doğrudan `fetch` ile çağırır: `api()` bir 401'i `login.html`'e geri gönderir, yani yanlış bir
  kod sayfayı yalnızca yeniden yükler. Bunun yerine 401 mesajını ("Wrong code") gösterin. Sonra token'ı
  `sessionStorage` içinde saklayın ve ilk sayfanızı açın. Token yoksa her sayfa girişe gider.
- `style.css` dosyasını da `week04/prototype/` içinden `web/` klasörüne kopyalayın.
- **Sunucunun retlerini** test case'lerinizin sözleriyle gösterin ("This slot is already booked.").
- **Prototipin yalnızca taklit ettiği şey artık gerçek:** rol sayfadaki bir düğmeden değil, girişten
  gelir. Bir kod ya da kimlik HTML'den değil, sunucudan gelir. Bir test case'in adımları hala yalnızca
  prototipte olan bir şeyi anıyorsa o test case'i değiştirin (§9).
- Sunucunun metnini sayfaya `innerHTML` ile değil, her zaman `textContent` ile koyun.

Sunucunuz sayfaları kendisi sunar. Böylece sayfalarla sunucu aynı adreste olur:

```python
from pathlib import Path

from fastapi.staticfiles import StaticFiles

WEB = Path(__file__).resolve().parent.parent / "web"
if WEB.is_dir():
    app.mount("/web", StaticFiles(directory=WEB, html=True), name="web")
```

http://127.0.0.1:8000/web/login.html adresini açın. Pencereyi 390 piksel genişliğe getirin, giriş yapın
ve özelliğinizi kullanın. Bağlanmış (mount) bir klasör bir endpoint değildir, bu yüzden `api.md` içinde
satıra ihtiyacı yoktur. `@app.get("/")` gibi bir route'un ise satıra ihtiyacı vardır. `--reload` ile her
`.py` kaydı sunucuyu yeniden başlatır ve sunucu token'ları unutur: yeniden giriş yapın.

### 6. Saldırgan turu — `week06/group_06.json`

**Ne zaman:** derste, yaklaşık 11:25 ile 11:45 arası.

3. haftadaki grubunuz tek bir iş için yeniden bir araya geliyor: **birbirinizin özelliğini kırmak**.
İkişerli çalışın. Sahibin sunucusu, sahibin dizüstü bilgisayarında çalışır. Saldırgan orada kendi
adresiyle giriş yapar ve sahibin hesaba katmadığı şeyleri dener:

- kendi token'ıyla başkasının verisi (adresteki kimliği değiştirerek);
- yalnızca eğitmenin ya da sahibin yapabileceği bir işlem, sıradan bir kullanıcı olarak;
- boş ya da yalnızca boşluklardan oluşan bir metin;
- çok uzun bir metin ya da aralık dışında bir sayı;
- aynı şey iki kez;
- giriş de (yanlış kodlar, token olmadan).

Sahip izler ve her saldırgan için `week06/group_06.json` dosyasına **elle** bir kayıt (record) yazar:

- `student_id`: saldırganın 9 haneli numarası; `role`: `"attacker"`;
- `tried`: ne denediği, değerleriyle, bir iki cümlede;
- `happened`: sunucunuzun ya da sayfanızın ne yaptığı: durum kodu, mesaj, işe yarayıp yaramadığı.

Sonra rolleri değiştirin. Grubunuzdan kimse derste değilse herhangi bir sınıf arkadaşınızla çalışın.
Bu dosyadaki her şeyi siz, kendi cümlelerinizle yazarsınız: asistan yok, dil bilgisi için bile.
`accepted` ve `why` Cumartesi'yi bekler (§13).

### 7. Push edin ve GitHub'da görün

Push etmeden önce `ruff check . --fix` ve `ruff format .` çalıştırın (sanal ortamın dışında onu
`pip install ruff==0.15.11` ile kurun). **Lint and format** işi her push'tan sonra GitHub'da ruff'ı çalıştırır.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week06: REQ-002 bookings, route and test"
git push
```

Sonra reponuzu GitHub'da açın. **Actions** sekmesini, en yeni çalıştırmayı ve **Weekly deliverables**
işini açın. Orada kırmızıysa, bilgisayarınız yeşil gösterse bile ders notu için kırmızıdır.

Her işi ortasında commit edin, çalıştığında yeniden commit edin ve her commit'i hemen push edin.
Commit'in üzerindeki saat değil, GitHub'ın push saati sayılır. Çalıştırmanın bitmeye vakti olsun
diye son commit'inizi 11:45'e dek push edin. Ders notu, dersin sonuna dek push ettiğiniz son commit'i ve onun
Actions çalışmasını okur.

---

## Cumartesi 23:59'a kadar

Bu kısım yaklaşık 4–5 saat çalışma ister. İşi dersten sonraki günlere yayın.

### 8. Her işlevsel must gereksinim, uçtan uca

Derste bunu bir gereksinim için yaptınız. Şimdi bütün işlevsel `must` gereksinimleriniz için yapın.
REQ-001 de bunlardan biridir: sunucu tarafı dersin girişidir, sayfası `web/login.html`'dir (§5). Bu sayfa
`<!-- serves: REQ-001, REQ-006 -->` satırını korur ve sunucuyu `fetch` ile çağırır. Hepsi için:

- bunlardan birine hizmet eden her `api.md` satırı gerçekten cevap verir, artık 501 ile değil;
- `"run": "server"` olan, `must` bir gereksinimin her test case'inin, kimliğiyle adlandırılmış ve GitHub'da
  geçen bir testi vardır;
- bu gereksinimlerin her birinin `web/` içinde, onu `<!-- serves: … -->` satırında adlandıran ve sunucuyu
  `fetch` ile çağıran bir sayfası vardır.

Prototipteki bir ekran gibi, bir sayfa birkaç gereksinime hizmet edebilir. `should` ya da `could`
gereksinimler hala 501 dönebilir.

Bazı parçaları yalnızca bir telefon yapabilir; örneğin bir push bildirimi ya da kamera. Bunlar 7. haftada
gelir. Sunucu tarafını şimdi kurun. Telefonun ne ekleyeceğini sayfada bir HTML yorumuyla yazın.

### 9. Zincirin bir halkası değişmesi gerektiğinde

Önceki halkaların doğru olup olmadığını kurarken anlarsınız. Gereksinimleriniz ve test case'leriniz geçen
Cumartesi **baseline'ınız** oldu. Bu yüzden:

- `requirements.json` ya da `test_cases.json` içindeki bir değişiklik bir **change request**'tir. Bu,
  `PROPOSAL.md` içinde bir Change log satırıdır. `CR-` ve sıradaki boş numarayla başlar, değişikliği ve
  kimlikleri söyler, değişikliğin etkilediği her dosyayı sayar.
- Prototip için yazılan test case'ler çoğu zaman yalnızca prototipte olan şeyleri anar: "görünüm
  şeridinde Instructor'a dokun", "3 numaralı oda her zaman boş". Sayfa artık gerçek; bu yüzden
  adımlarını değiştirin. Hepsi için tek bir change request yeter: *"2026-10-28 — CR-01: TC-002-01 to TC-003-02: the steps no
  longer use the prototype's view switch and its fixed list of rooms; the role comes from the login and the
  rooms from the server; affects week04/test_cases.json."*
- `api.md`, kullanım senaryoları ya da ekranlardaki bir değişiklik, tarihli sıradan bir Change log satırı
  alır.
- Her test case'e `"run"` eklemeyi (§14) ders istiyor. Bunu eklemek bir change request
  **değildir**.

### 10. Gerçek e-postayla kod

`AIASD_CODE_FILE` olmadan dersin girişi kodu e-postayla gönderir. `.env` dosyasındaki ayarları
kullanır. Bu dosya reponuzun kökündedir ve yalnızca sizin bilgisayarınızda durur:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=the 16-letter app password
SMTP_FROM=you@gmail.com
```

- Gmail için şifre bir **uygulama şifresidir** (app password) (Google hesabı → Güvenlik → iki adımlı doğrulama açık →
  Uygulama şifreleri); asla gerçek şifreniz değil.
- `.gitignore`, `.env` dosyasını listeler. **`.env` asla commit edilmez.** Bir gün commit ederseniz uygulama
  şifresini hemen değiştirin. Dosyayı silmek yetmez, çünkü dosya geçmişte kalır.
- `.env.example` aynı beş adı listeler, **`SMTP_PASSWORD=` satırından sonra hiçbir şey olmadan**.
- Windows PowerShell: `$env:AIASD_CODE_FILE` o pencerede ayarlı kalır. Gerçek e-postayı denemeden önce
  pencereyi kapatın ya da `Remove-Item Env:AIASD_CODE_FILE` çalıştırın.
- Web sayfanızda kendi adresinizle giriş yapın. E-posta geldiğinde, e-posta kutunuzdaki halinin ekran
  görüntüsünü (screenshot) alın. Gönderen ve kod görünmeli. Onu **`week06/email_code.png`** (ya da `.jpg`) olarak
  kaydedin.

Bazı ağlar 587 numaralı portu engeller. E-posta kampüsten gitmiyorsa evden deneyin.

### 11. GitHub'da her test yeşil

Şu testler yeşil olmalı:

- on ders testinin hepsi (LOGIN_07, yani bir kodun yalnızca bir kez çalışması, ve zamanla ilgili kurallar
  olan LOGIN_08–LOGIN_10 Cumartesi okunur);
- 5. hafta giriş testleriniz, §1'deki gibi değiştirilmiş (onları tutuyorsanız);
- `"run": "server"` olan her `must` test case'inin testleri.

### 12. S2 — uygulamanızın mağazadaki kaydı, `week04/store.json`

Mağazanızın geliştirici konsolunda (developer console) uygulamanızın kaydını oluşturun. Kaydın bir adı ve bir **paket adı** (package name)
(Google Play, Huawei, Samsung) ya da **bundle id**'si (Apple) vardır. Bu, uygulamanızın mağazadaki benzersiz
adıdır; örneğin `com.example.studyroom`. Dikkatle seçin: onu asla değiştiremezsiniz. Google Play paket
adını henüz sormaz: onu ilk yükleme (S3, 8. hafta) sabitler. Yine de onu şimdi seçin, S2'ye yazın ve
7. haftada `applicationId` olarak kullanın. `week04/store.json` dosyasına S1'in yanına S2'yi ekleyin:

```json
"S2": { "date": "2026-10-31", "app_name": "StudyRoom", "package": "com.example.studyroom", "evidence": "store_s2.png" }
```

`evidence`, konsolunuzdaki kaydın `week04/` içine kaydedilmiş ekran görüntüsünün adıdır. Adresinizi,
kimlik numaranızı ve kart bilgilerinizi kapatın. Belki mağaza geliştirici hesabınızı henüz kabul etmedi. O
zaman AI log'unuza başvurduğunuz tarihi ve mağazanın ne dediğini yazın. Kayıt oluşana kadar S2 kontrolü
kırmızı kalır.

### 13. Saldırganın bulguları: kararınız

`group_06.json` dosyasının her kaydına şunları ekleyin:

- `accepted`: onun yüzünden bir şeyi değiştiriyorsanız `true`, değiştirmiyorsanız `false`;
- `why`: tam bir cümle: neyi değiştirdiğiniz ya da neden gerçek bir sorun olmadığı.

Bir bulguyu düzelttiğinizde, onu yakalayabilecek bir test ekleyin. Testi, ait olduğu test case'in
kimliğiyle adlandırın. Hiçbir test case onu kapsamıyorsa bir change request gerekir (§9).

### 14. Her test case'in nasıl çalıştırıldığı — `week04/test_cases.json`

Her test case'e `"run"` ekleyin:

- `server/tests/` içindeki bir test onu çalıştırıyorsa `"server"`;
- tarayıcıda, sayfanızda çalıştırılıyorsa `"web"`;
- bir insan çalıştırıyorsa (telefonda, mağazada, bir kullanıcıyla) `"manual"`.

### 15. Düşman gözden geçiren (hostile reviewer) — `week06/ai_log_06.md`

Grup arkadaşınız derste özelliğinize saldırdı. Şimdi aynısını bir asistana yaptırın (`AI_Doc5` §3). Ona kendi
özelliğinizin route'larını ve hizmet ettikleri gereksinimleri verin. Numaralı olarak **en güçlü üç
saldırıyı** isteyin. Her saldırıyı kendiniz, çalışan sunucunuza karşı ya da bir testte deneyin. Sonra
günlüğe şunları yazın:

- üç saldırı (asistanın sözleri kalın);
- sunucunuzun her birine karşı ne yaptığı;
- **düzelttiğiniz** saldırı ve nasıl düzelttiğiniz;
- **yanlış olan** saldırı ve kanıtı (bir durum kodu, bir test sonucu).

`ME:`, `AI:` ve `TERMINAL:` kısımlarını (komutlar ve çıktıları, dokunulmadan) Evidence bloğuna yapıştırın.

Sonra asistanın saldırılarını grup arkadaşınızınkilerle karşılaştırın. Nerede aynı şeyi buluyorlar?
Hangisi, diğerinin kaçırdığı bir şeyi buldu?

**AI log'u bir insan yazar: siz.** Evidence bloğu ve kalın alıntılar dışında asistan kullanılmaz.
**Asistana yazdırılmış bir günlük 0 puan alır.**

### 16. Yeniden push, kontroller yeşil

Çalışırken birkaç commit yapın. Her birinde yeni bir iş ve neyin değiştiğini söyleyen bir mesaj olsun.
**Ders dışında:** yeni iş içeren en az iki commit, aralarında en az bir saat olacak şekilde push edilmiş
olsun. Commit'in üzerindeki tarih değil, GitHub'ın push saati sayılır. Bir kodlama ajanının (coding agent) yaptığı commit
hiçbir zaman sayılmaz. **Asla force push yapmayın** ve bir asistanın yapmasına da izin vermeyin. Sonra
aşağıdaki kontrol listesine bakın.

---

## Kendi testleriniz

```python
import uuid

from fastapi.testclient import TestClient

from server.course_login import auth_header_for_tests
from server.main import app

client = TestClient(app)


def someone(name: str) -> dict[str, str]:
    """A new user, logged in through the real login: the header with their token."""
    return auth_header_for_tests(client, f"{name}-{uuid.uuid4().hex[:8]}@example.com")


def test_TC_002_02_a_busy_slot_is_refused():
    deniz, mia = someone("deniz"), someone("mia")
    client.post("/bookings", json={"room": 3, "start": "14:00", "minutes": 60}, headers=deniz)

    response = client.post(
        "/bookings", json={"room": 3, "start": "14:00", "minutes": 60}, headers=mia
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "This slot is already booked."
```

- **`auth_header_for_tests`**, `AIASD_CODE_FILE` ayarlıyken bir kod ister; böylece testte e-posta
  gönderilmez. Adresle giriş yapar ve size token'lı başlığı verir. `test_email_domain` değerinizdeki alan
  adını kullanın.
- **Her testte yeni bir adres**, yukarıdaki gibi: bir adres yeni kodu dakikada yalnızca bir kez isteyebilir.
- Test case kimin neyi yapabileceğiyle ilgiliyse **iki kullanıcı**: verinin sahibi olan ve olmayan.
- **Yalnızca bir testiniz saati freezegun ile ilerletiyorsa:** bu satırları `TestClient(app)`'ten önce
  koyun. TestClient her endpoint'i ayrı bir thread'de çalıştırır. Bu satırlar olmadan freezegun o
  thread'deki saati değiştirmez:

  ```python
  import freezegun

  freezegun.configure(
      default_ignore_list=[
          m for m in freezegun.config.DEFAULT_IGNORE_LIST if m not in ("threading", "queue")
      ]
  )
  ```

---

## Teslim kontrol listesi

**Derste, 11:45'e kadar push**
- [ ] `server/login_contract.json` — elle; üç endpoint'i `api.md` satırı; `main.py` içinde `course_login.router`; ders testleri LOGIN_01–06 **GitHub'da** yeşil
- [ ] Kendi işlevsel `must` gereksinimlerinizden biri: bir route'u çalışıyor, artık 501 değil
- [ ] Test case'lerinden biriyle adlandırılmış bir test, **GitHub'da** yeşil
- [ ] Prototip ekranından yapılmış, route'larını `fetch` ile çağıran, girişin arkasında duran bir `web/` sayfası; sunucunuz sunuyor
- [ ] `week06/group_06.json` — her saldırgan için bir kayıt: numara, `attacker` rolü, ne denediği, ne olduğu; sizin yazdığınız

**Cumartesi 23:59'a kadar**
- [ ] İşlevsel `must` bir gereksinimin her `api.md` satırı gerçekten cevap veriyor (501 yok)
- [ ] `"run": "server"` olan her `must` test case'inin kimliğiyle adlandırılmış testi GitHub'da yeşil; on ders testinin hepsi yeşil
- [ ] Her işlevsel `must` gereksinimin `web/` içinde `<!-- serves: … -->` ve `fetch` içeren bir sayfası var (REQ-001: `login.html`)
- [ ] Değişen her halkanın `PROPOSAL.md` içinde satırı var (gereksinimler ve test case'ler için change request)
- [ ] Gerçek e-postayla kod; `.env` commit edilmemiş ve `.gitignore` içinde; `.env.example` beş SMTP adıyla ve şifresiz; `week06/email_code.png`
- [ ] `week04/store.json` — tarih, uygulama adı, paket adı ya da bundle id ile S2 ve `week04/` içinde ekran görüntüsü
- [ ] `week04/test_cases.json` — her test case'te `"run"`
- [ ] `week06/group_06.json` — her bulgu için `accepted` ve `why`
- [ ] `week06/ai_log_06.md` — özelliğinize üç saldırı, ne olduğu, düzelttiğiniz, yanlış olan; Evidence bloğuna yapıştırılmış `ME:`, `AI:` ve `TERMINAL:` (komutlar ve çıktıları, dokunulmadan); sizin yazdığınız (asistanın yazdığı günlük 0 alır)
- [ ] GitHub'da kontroller yeşil; 1–5. haftalar hala geçiyor

---

## Bu hafta yok

Mobil istemci yok (7. hafta). Henüz veritabanı yok: verileriniz ve girişin kodları ile token'ları bellekte
durur. Sunucu yeniden başlayınca kaybolurlar. Şimdilik bu sorun değil; 8. haftadan itibaren kendi
verileriniz yeniden başlatmadan sonra da durmalıdır (girişin kodları ve token'ları için gerekmez:
kullanıcılar yeniden giriş yapar). Şifre yok, hiçbir zaman. Sohbet
botu yok (8. hafta). S3 yok: henüz bir build yüklemiyorsunuz. `should` ve `could` gereksinimler
bekleyebilir.

---

## Bu hafta nasıl notlandırılır

**Dersin sonu — 5 puan.** Dersin sonuna dek push ettiğiniz son commit'i ve onun GitHub Actions
çalıştırmasını okurum:

- bağlanmış giriş (sözleşme, `api.md` içindeki satırları, `course_login.router`, LOGIN_01–06);
- kendi `must` gereksiniminizin çalışan bir route'u;
- test case'lerinden birinin GitHub'da geçen testi;
- sunucunuzun sunduğu `web/` sayfası;
- saldırganın kaydı.

**Cumartesi 23:59 — 5 puan.**

- Son halinizde yeşil kontroller: **2**.
- İnsan katkısı (human involvement): **2**. Yani sizin yazdığınız `ai_log_06.md` (asistanın yazdığı bir günlük **0** alır)
  ve elle yazdığınız iki dosya: `login_contract.json` ve kararlarınızla birlikte saldırganın kaydı.
- Commit disiplini: **1**. Derste: her iş (giriş, route'ları, testleri, sayfası) en az iki push edilmiş
  commit'te gelir; ilki iş daha bitmeden. Ders dışında: yeni iş içeren en az iki commit, aralarında en az bir saat
  olacak şekilde push edilmiş. Commit'in üzerindeki tarih değil, GitHub'ın push saati sayılır. Bir kodlama
  ajanının yaptığı commit hiçbir zaman sayılmaz.

**Katkı bonusu (contributors' bonus).** Adını yazdığınız her saldırgan katkı bonusunu (haftalık notunuzun %10'u) kazanır; siz de
saldırılarınız için aynısını kazanırsınız.

**S2**, mağaza bonusunun (store bonus) notlanan adımlarından biridir.

**Bir öğrenci, bir bilgisayar, bir GitHub hesabı.** Kendi bilgisayarınızdan, kendi hesabınızla commit edin.
Bir sınıf arkadaşınızın bilgisayarında ya da onun hesabıyla yapılan iş, ders için hiçbir şey kazandırmaz.
Saldırgan turunda saldırgan bilgisayarınızı yalnızca saldırmak için kullanır. Kimse bir sınıf arkadaşının
bilgisayarında commit etmez. Bir gün gerçekten başka bir bilgisayardan commit etmeniz gerekirse, bunu o
haftanın AI log'una günüyle ve nedeniyle yazın.
