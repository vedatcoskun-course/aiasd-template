# AIASD · 6. Hafta — Kendi Özelliğiniz (feature), Uçtan Uca (end to end)

*Atlas Üniversitesi · 2026–27 Güz · Prof. Dr. Vedat Coşkun*
*Bu sayfadan sunulur. Her seferinde bir bölüm kaydırın; her `---` bir slayttır.*

<!-- Instructor: zoom the browser to 150 % and collapse the GitHub header. Total ≈ 2 h 45 min:
20 min explanation + a short demonstration (wire the course login into a fresh server in three minutes,
/docs, the Actions tab) · the login wired and the first requirement chosen until about 10:00 · its
routes and tests until about 11:00 · commits and pushes in the middle of each piece · its page until about 11:25 · the attacker round 11:25–11:45 ·
the last push at 11:45 · the mark reads the last commit pushed by the end of the lecture. -->

---

## Bugün

1. Projeniz şimdiye kadar ve her gereksiniminizin (requirement) dönüştüğü zincir (chain)
2. Giriş (login) kullanıma hazır geliyor: bağlayın — **10:00**'a kadar
3. İlk kendi gereksiniminiz: route'ları ve testleri, GitHub'da yeşil — **11:00**'e kadar
4. Sayfası (page): prototipin ekranı (screen), artık gerçek, girişin arkasında
5. Saldırgan turu (attacker round): bir grup arkadaşınız (groupmate) özelliğinizi kırmaya çalışır — **11:45**'e kadar
6. Cumartesi'ye kadar: her işlevsel (functional) `must`, gerçek e-posta, S2, düşman gözden geçiren (hostile reviewer)
7. Hafta nasıl notlandırılır

---

## Projeniz şimdiye kadar ve nereye gidiyor

- **1. hafta:** araçlarınız ve yapay zeka asistanlarıyla ilk gerçek konuşmalarınız
- **2. hafta:** gerçek bir problem, onu yaşayan gerçek insanlar, ilk gereksinimler
- **3. hafta:** pitch ve pazar (market); projeniz kesinleşti
- **4. hafta:** ekranlar ve onlara tıklayan bir sınıf arkadaşı
- **5. hafta:** tasarım (design), sözleşme, 501 dönen bir sunucu (server), hala kırmızı olan testler
- **Bu hafta ürününüz kendi işini ilk kez yapıyor:** sunucunuzda, GitHub'daki testlerinizde, giriş yapmış bir kullanıcının kullanabildiği bir sayfada
- **Sonra:** aynı özellik bir telefonda (7) · sohbet botu (chatbot) ve üç istemcide özellik, ilk build (8) · gerçek testçiler (9), gerçek kullanıcılar (10) ve Aralık'ta bir mağazadan (store) kurulan uygulamanız

<!-- Instructor: ask two students which requirement their product exists for. That is the one they build first today. -->

---

## Bir gereksinim, baştan sona

| Halka | Nerede durur | Hafta |
|---|---|---|
| 1–2. Gereksinim ve senaryosu | `requirements.json` · `SRS.md` | 2 |
| 3. Ekranı, `serves:` ile | `prototype/` | 4 |
| 4. Test case'leri, `"run"` ile | `test_cases.json` | 4 |
| 5. API sözleşmesindeki satırları | `api.md` | 5 · bugün |
| 6. **Route'ları, çalışır: 501 yok** | `server/` | **bugün** |
| 7. **Testleri, GitHub Actions'ta yeşil** | `server/tests/` | **bugün** |
| 8. **Sayfası, `fetch` ile** | `web/` | **bugün** |

**Kaynak (source) `requirements.json` dosyasıdır; diğer her halka onu izler.**

---

## StudyRoom'da zincir

| Halka | StudyRoom |
|---|---|
| Gereksinim, senaryo | REQ-002 — boş bir odayı 30–120 dakika ayırmak · UC2 |
| Ekran | `book.html`, `serves: REQ-002` |
| Test case'ler | TC-002-01 (`web`) · TC-002-02 dolu saat reddedilir (`server`) |
| API satırları | `POST /bookings` → 201 · 409 · 422 · 401 |
| Route | `create_booking`, `current_user` ile |
| Test | `test_TC_002_02_…` **Actions**'ta yeşil |
| Sayfa | `web/book.html`, `fetch("/bookings", …)` |

Yanlış çıkan bir halka **önce** değiştirilir, `PROPOSAL.md` içindeki satırıyla.

---

## Giriş kullanıma hazır geliyor

- Bir e-posta adresi → **4 haneli bir kod**: **10 dakika** geçerli, **bir kez** çalışır
- **Bir dakika içinde** yeni kod → **429** · e-posta adresi değil → **422**
- Yanlış ya da süresi dolmuş kod → **401** · **üst üste 3 yanlış kod** (yeni kod sayımı sıfırlamaz) → **15 dakika 429**
- Doğru kod → bir **token**; `Authorization: Bearer <token>` ile "me" → **200**, yoksa **401**

Hepsini **`server/course_login.py`** yapar. Herkes için aynı, on ders testiyle kontrol edilir.

**Neden:** her uygulamanın girişi aynıdır ve girişte küçük hatalar yapmak kolaydır. Haftanızı yalnızca **sizin** projenizin yaptığı şeye ayırırsınız.

---

## Bağlamak — on beş, yirmi dakika

```json
{ "request_code": "POST /auth/code", "login": "POST /auth/login", "me": "GET /auth/me",
  "email_field": "email", "code_field": "code", "token_field": "token",
  "test_email_domain": "example.com", "email_must_end_with": "", "app_name": "StudyRoom" }
```

1. `server/login_contract.json`, `api.md` dosyanızdan **elle**: metot, bir boşluk, yol.
2. `server/main.py` içinde:

```python
from server import course_login

app.include_router(course_login.router)
```

3. **Kendi üç giriş taslağınızı silin** (501 dönenler): kalırlarsa önce onlar cevap verir.
4. `python -m pytest course_tests -q` → **10 passed**.

---

## Ders testleri (course tests) ve `/docs` üzerinde denemek

```bash
python -m pytest course_tests -q
AIASD_CODE_FILE=login_code.txt uvicorn server.main:app --reload          # macOS, Linux
$env:AIASD_CODE_FILE="login_code.txt"; uvicorn server.main:app --reload  # PowerShell
```

- `/docs` üzerinde: kod isteyin, `login_code.txt` içinde okuyun, giriş yapın, token'la **Authorize**, "me"yi çağırın. `login_code.txt` `.gitignore`'a girer.
- "Fill in server/login_contract.json": bir değer hala [köşeli parantez] içinde.
- "answered 422": test adresi `email_must_end_with` kuralını geçmiyor. `test_email_domain`'i düzeltin.
- Bir `.py` dosyasını kaydetmek sunucuyu yeniden başlatır ve sunucu token'ları unutur. `login_contract.json` dosyasını değiştirdikten sonra sunucuyu durdurun (Ctrl+C) ve yeniden başlatın.
- LOGIN_01–06: ders sonu. LOGIN_07–10: Cumartesi.

<!-- Demonstration: wire the login into a fresh server live, in three minutes. -->

---

## Bu hafta asistan nerede yardım eder

| Parça | Asistan |
|---|---|
| Bir route'un kodu; gereksinimi, kabul ölçütü (acceptance criterion) ve `api.md` satırı istemde (prompt) (bir route, bir commit) | **Yardım eder** |
| Test case'lerinizden birinden bir test (satır satır kontrol sizde) | **Yardım eder**, onay sizde |
| Bir sayfanın `fetch` kullanan JavaScript'i | **Yardım eder** |
| Kırmızı bir testi ya da bir GitHub Actions kaydını okumak | **Yardım eder** |

---

## … ve nerede hiç yardım etmez

| Parça | Asistan |
|---|---|
| Gereksinim susuyorsa route'un ne yapacağı | **Yardım etmez**: önce gereksinim değişir |
| `server/login_contract.json` | **Yardım etmez**: `api.md`'den elle |
| `group_06.json`: denenen, olan, kararınız | **Yardım etmez** |
| Testleri çalıştırmak, GitHub'ın dediğini okumak | **Yardım etmez**: siz çalıştırır, siz bakarsınız |
| Change log satırları ve değişiklik talepleri (change request) | **Yardım etmez** |
| `ai_log_06.md`, Evidence bloğu dışında | **Yardım etmez** |

<!-- Instructor: read the "No help" rows aloud. The new one is the first. -->

---

<h1 align="center">GİRİŞ SÖZLEŞMESİNİ<br>VE SALDIRGANIN KAYDINI<br>ELLE YAZARSINIZ.</h1>

<p align="center"><b>login_contract.json: api.md dosyanızdan, sizin tarafınızdan kopyalanır.<br>group_06.json: saldırı olurken sizin tarafınızdan yazılır.</b></p>

<p align="center">Hiçbir asistan onları yazmaz, düzeltmez ya da tamamlamaz. Dil için bile.</p>

---

<h1 align="center">AI LOG'U<br>İNSAN YAZAR.</h1>

<p align="center"><b>Evidence bloğu ve kalın alıntıları dışında: asistan yok.<br>Yazmak için değil. Düzeltmek için değil. Dil için bile değil.</b></p>

<h1 align="center">Asistana yazdırılmış bir günlük 0 alır.</h1>

---

## Ders notunuz (lecture mark) dizüstü bilgisayarınızdan değil, GitHub'dan gelir

Her push'ta **GitHub Actions** denetleyiciyi (checker) çalıştırır. Denetleyici de ders testlerini ve **kendi testlerinizi** çalıştırır.

- Ders notu için **dersin sonuna dek push ettiğiniz son commit'in GitHub çalıştırmasını** okurum.
- **11:45**'e kadar push edin, **Actions** sekmesini açın ve çalıştırmanın bittiğini görün.
- Yalnızca sizin bilgisayarınızda geçen bir test sayılmaz.

**Asla `git push --force` yapmayın.** Commit siler; çalışmanızı geçmişinize bakarak notlandırırım. Bir yazım hatası yüzünden CI kırmızı mı? **Yeni** bir commit'le düzeltin. Küçük bir düzeltme commit puanını asla düşürmez.

---

## Şimdi — 10:00'a kadar

1. Giriş bağlanmış: sözleşme **elle**, `course_login.router`, taslaklarınız silinmiş.
2. `python -m pytest course_tests -q`: **10 passed**. TC-001 testleriniz: `AIASD_CODE_FILE` ile (ödev §1).
3. İlk kendi gereksiniminiz: halkalarını yan yana koyun. Aynı şeyi mi söylüyorlar?
4. Eksik ya da yanlış bir halka mı var (henüz `api.md` satırı yok mu)? Şimdi, elle, `PROPOSAL.md` içindeki satırıyla düzeltin.
5. `ruff check . --fix`, `ruff format .`, denetleyici, commit, **push: ortasında ve bitince**.

<!-- Start the clock. Walk round: no assistant window open while login_contract.json is typed. -->

---

## Route'ları, gerçekten

```python
from server.course_login import current_user

bookings: list[dict] = []  # şimdilik bellekte; 8. haftadan itibaren dosyada ya da veritabanında


@router.post("/bookings", status_code=201)
def create_booking(body: NewBooking, user: str = Depends(current_user)) -> dict:
    """REQ-002: a student books a free room for 30 to 120 minutes; a busy slot is refused."""
    if not 30 <= body.minutes <= 120:
        raise HTTPException(status_code=422, detail="A booking lasts 30 to 120 minutes.")
    if any(b["room"] == body.room and b["start"] == body.start for b in bookings):
        raise HTTPException(status_code=409, detail="This slot is already booked.")
    bookings.append({"id": len(bookings) + 1, **body.model_dump(), "by": user})
    return {"booking_id": len(bookings)}
```

`api.md` satırındaki her hata, durum koduyla (status code) ve **test case'inizin beklediği mesajla**.

---

## Kim yapabilir — karar sunucunun

| Kod | Ne zaman | Örnek |
|---|---|---|
| **401** | giriş yapılmamış | token yok ya da tanınmayan bir token |
| **403** | giriş var, izin yok | başkasının ayırması · eğitmenin işlemi |
| **404** | böyle bir şey yok | `/bookings/999` |
| **409** | var olan bir veriyle çakışıyor | o saat zaten ayrılmış |
| **422** | eksik, boş, yanlış biçim | 500 dakika · yalnızca boşluklar |

`current_user` **kimin** sorduğunu söyler. Bir düğmeyi gizlemek güvenlik değildir: **route** 403 ile cevap verir. Sayfanın `api.md`'de olmayan bir listeye mi ihtiyacı var? **Önce satırı ekleyin.**

---

## Asistanın "yardım" edeceği şeyler

| Önerdiği | Neden yanlış | Onu ne yakalar |
|---|---|---|
| Kimsenin istemediği bir alan (`is_admin`, `price`) | hiçbir gereksinim istemiyor | cevabı sizin gözden geçirmeniz |
| "Basit olsun diye" atlanmış sahiplik kontrolü | herkes herkesin verisini değiştirir | saldırgan turu · bir 403 testi |
| Mesajla birlikte 200'e dönüştürülmüş bir hata | istemci işin olduğunu sanır | test case'inizin durum kodu |
| Kuralın kendi yorumu ("4 saate kadar") | gereksinim 120 dakika diyor | test case'inizin değerleri |

**Bir seferde bir route.** Gereksinim, kabul ölçütü ve `api.md` satırı istemde. Cevabın tamamını okuyun.

---

## Testleri — test case'leriyle adlandırılmış

```python
from server.course_login import auth_header_for_tests


def someone(name: str) -> dict[str, str]:
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

`"run": "server"` olan her test case için bir test · her testte **yeni bir adres** · test case kimin neyi yapabileceğiyle ilgiliyse **iki kullanıcı**.

---

## Şimdi — 11:00'e kadar

1. İlk gereksiniminizin route'ları: artık 501 değil, kullanıcı gereken yerde `current_user`.
2. Önce test case'lerine `"run"`; sonra `"run": "server"` olan her biri için, kimliğiyle adlandırılmış bir test.
3. `python -m pytest server/tests -q` bilgisayarınızda yeşil.
4. Ruff, denetleyici, commit, **push: ortasında ve bitince**.
5. **Actions** sekmesi: `AIASD-TEST … TC-002-02 passed` görünüyor mu?

---

## Sayfası — prototipin ekranı, artık gerçek

Ekranını `week04/prototype/` içinden `web/` klasörüne kopyalayın: onu kökte, `server/` yanında siz oluşturursunuz. Görünüşünü ve `<!-- serves: REQ-… -->` satırını koruyun.

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
```

Prototipin sabit verileri → sunucunun cevabı. Sunucunun retleri → test case'lerinizin sözleri. Sunucunun metni → `textContent`, asla `innerHTML` değil.

---

## Girişin arkasında, sunucunuzun sunduğu

- `web/login.html` = prototipin `index.html` + `code.html` ekranı; `serves: REQ-001, REQ-006`; `style.css`.
- Giriş yolları için `api()` değil, doğrudan `fetch`. 401'de "Wrong code" gösterin.
- Token yok → her sayfa girişe gider.

```python
from pathlib import Path

from fastapi.staticfiles import StaticFiles

WEB = Path(__file__).resolve().parent.parent / "web"
if WEB.is_dir():
    app.mount("/web", StaticFiles(directory=WEB, html=True), name="web")
```

**390 px**'te açın: http://127.0.0.1:8000/web/login.html, giriş yapın, özelliğinizi kullanın. Klasör `api.md` satırı istemez.

---

## Prototipin yalnızca taklit ettiği şey artık gerçek

| Prototipte | Gerçek sayfada |
|---|---|
| Bir "Student / Instructor" düğmesi | rol **girişten** gelir |
| Sabit bir kod, sabit bir liste | onları sunucu üretir |
| Her tıklama "çalışır" | sunucu **hayır** diyebilir: 403, 409, 422 |

Adımları hala yalnızca prototipte olanı anan ("görünüm şeridinde Instructor'a dokun", "3 numaralı oda her zaman boş") bir test case, hepsi için **tek bir change request'le** değiştirilir.

---

## Saldırgan turu — yaklaşık 11:25 ile 11:45 arası

3. haftadaki grubunuz tek bir işle yeniden bir araya geliyor: **birbirinizin özelliğini kırmak**.

Sahibin sunucusu, sahibin bilgisayarında çalışır. Saldırgan orada **kendi adresiyle** giriş yapar ve dener:

- kendi token'ıyla **başkasının verisi**: adresteki kimliği değiştirin
- **kendisine ait olmayan bir işlem**: eğitmenin, sahibin
- **boş bir metin, yalnızca boşluklar, çok uzun bir metin**, aralık dışında bir sayı
- **aynı şey iki kez**; ve giriş: yanlış kodlar, token olmadan

Grubunuzdan kimse yok mu? Herhangi bir sınıf arkadaşınızla çalışın. Sonra rolleri değiştirin.

---

## `week06/group_06.json` — sahibi elle yazar

```json
{
  "student_id": "123456789",
  "role": "attacker",
  "tried": "Logged in as mia, they sent DELETE /bookings/1, Deniz's booking, with curl.",
  "happened": "200: Deniz's booking was gone."
}
```

Her saldırgan için bir kayıt (record). `accepted` ve `why` Cumartesi'yi bekler: önce bulgunun (finding) gerçek olup olmadığına bakın.

**Saldırgan bilgisayarınızı yalnızca saldırmak için kullanır.** Kimse bir sınıf arkadaşının bilgisayarında commit etmez.

---

## Şimdi — 11:45'e kadar

1. İlk gereksiniminizin sayfası `web/` içinde, girişin arkasında, 390 px'te.
2. Saldırgan turu, iki yönde.
3. `group_06.json`: her saldırgan için, sizin yazdığınız bir kayıt.
4. Ruff, denetleyici, commit, **push: ortasında ve bitince**; **Actions** sekmesi: çalıştırmanızın bitişini izleyin.

11:45'e dek push edin. Ders notu, dersin sonuna dek push ettiğiniz son commit'i ve onun Actions çalışmasını okur.

---

## Commit disiplini

**Derste:** her işi **ortasında** commit edin, çalıştığında yeniden; her commit'i hemen push edin. Tek commit'te bitmiş olarak gelen bir iş sayılmaz.

**Ders dışında:** yeni iş içeren en az iki commit, **aralarında en az bir saat olacak şekilde push edilmiş**. Commit'in üzerindeki tarih değil, GitHub'ın push saati sayılır. Bir kodlama ajanının (coding agent) yaptığı commit hiçbir zaman sayılmaz.

Küçük bir düzeltme commit'i (bir yazım hatası, bir ruff hatası) puanı asla düşürmez. Sonda tek bir commit hiçbir şey kazandırmaz. **Asla force push yapmayın** ve bir asistanın yapmasına da izin vermeyin.

---

## Cumartesi 23:59'a kadar

- **Her işlevsel `must` gereksinim, uçtan uca:** her `api.md` satırı cevap verir (501 yok) · `"run": "server"` olan her `must` test case'in testi GitHub'da yeşil · `web/` içinde `serves:` ve `fetch` içeren bir sayfa (REQ-001 için de: `login.html`)
- **Değişen her halka**, `PROPOSAL.md` içindeki satırıyla
- **Gerçek e-postayla kod**; `.env` commit edilmemiş; `.env.example`; `week06/email_code.png`
- **On ders testinin hepsi** GitHub'da yeşil
- `week04/store.json` içinde **S2** · her test case'te **`"run"`**
- Her saldırgan bulgusu için **kararınız** · **`ai_log_06.md`**: düşman gözden geçiren

`should` ve `could` hala 501 dönebilir. Yalnızca telefonun yapabildiği bir parça 7. haftada gelir.

---

## Zincirin bir halkası değişmesi gerektiğinde

Gereksinimleriniz ve test case'leriniz geçen Cumartesi **baseline'ınız** oldu.

| Ne değişiyor | Nasıl |
|---|---|
| `requirements.json`, `test_cases.json` | bir **change request**: `CR-` ve sıradaki boş numara, kimlikler, etkilediği her dosya |
| `api.md`, bir kullanım senaryosu, bir ekran | tarihli sıradan bir Change log satırı |
| Bir test case'e `"run"` | dersin istediği: change request **değil** |

*"2026-10-28 — CR-01: TC-002-01 to TC-003-02: the steps no longer use the prototype's view switch and its fixed list of rooms; the role comes from the login and the rooms from the server; affects week04/test_cases.json."*

---

## Gerçek e-postayla kod — `.env`

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=the 16-letter app password
SMTP_FROM=you@gmail.com
```

- `AIASD_CODE_FILE` yoksa giriş e-postayı gönderir. PowerShell: pencereyi kapatın ya da `Remove-Item Env:AIASD_CODE_FILE`.
- **`.env` asla commit edilmez** (`.gitignore` onu listeler). Yanlışlıkla mı commit ettiniz? Uygulama şifresini (app password) hemen değiştirin.
- `.env.example`: beş ad, **şifresiz**. Gmail: iki adımlı doğrulama, sonra bir **uygulama şifresi**.
- Kodu içeren e-postanın ekran görüntüsü: **`week06/email_code.png`**.

---

## S2 ve her test case'in nasıl çalıştırıldığı

`week04/store.json` içinde, S1'in yanında **S2**: uygulamanızın mağaza konsolundaki kaydı.

```json
"S2": { "date": "2026-10-31", "app_name": "StudyRoom", "package": "com.example.studyroom", "evidence": "store_s2.png" }
```

Paket adı (package name) ya da bundle id **asla** değiştirilemez. Google Play paket adını henüz sormaz: onu ilk yükleme (S3, 8. hafta) sabitler. Yine de onu şimdi seçin, S2'ye yazın ve 7. haftada `applicationId` olarak kullanın. Henüz kabul edilmediniz mi? AI log'da söyleyin.

Her test case'te **`"run"`**: `"server"` (`server/tests/` içinde bir test), `"web"` (sayfanızda), `"manual"` (bir insan: telefon, mağaza, kullanıcı).

---

## Kendi testleriniz

- `auth_header_for_tests` bir test kullanıcısını gerçek girişten geçirerek giriş yaptırır (testte e-posta yok).
- **Her testte yeni bir adres**; test case kimin neyi yapabileceğiyle ilgiliyse **iki kullanıcı**.
- freezegun mu? Yalnızca bir test saati ilerletiyorsa; o zaman ödevdeki `freezegun.configure` satırı.

**`api.md` satırlarınızdaki her hata için onu kontrol eden bir test yazın.** Route hatayı unuttuğunda yeşil kalan bir test onu test etmiyordur.

---

## AI log — özelliğinize karşı düşman gözden geçiren

Grup arkadaşınız özelliğinize saldırdı. Şimdi bir asistan saldırsın (`AI_Doc5` §3).

1. Ona özelliğinizin route'larını ve gereksinimlerini verin: "numaralı olarak en güçlü üç saldırı."
2. **Her birini kendiniz deneyin**: sunucunuza karşı ya da bir testte.
3. Sunucunuzun her birine karşı ne yaptığı, durum koduyla.
4. **Düzelttiğiniz** ve onu artık yakalayan test.
5. **Yanlış olan** ve kanıtı.
6. Asistan ve grup arkadaşınız: kim diğerinin kaçırdığını buldu?

Sizin sözleriniz düz, asistanın sözleri kalın. Evidence bloğu: `ME:`, `AI:`, `TERMINAL:`, dokunulmadan. **Asistana yazdırılmış bir günlük 0 alır.**

---

## 6. Hafta nasıl notlandırılır — 10 puan

| | Puan | Ne |
|---|---|---|
| Ders sonu (GitHub) | 5 | giriş (LOGIN_01–06), kendi çalışan bir route'unuz, bir testi yeşil, sayfası, saldırganın kaydı |
| Cumartesi denetleyicisi | 2 | uçtan uca her işlevsel `must`, gerçek e-posta, bütün testler yeşil, S2, `"run"`, kararlar, AI log |
| İnsan katkısı | 2 | sizin yazdığınız AI log; elle `login_contract.json` ve `group_06.json` |
| Commit disiplini | 1 | her iş en az iki push edilmiş commit'te, ilki ortasında; bir saat arayla iki ders dışı commit; ajan commit'i yok |

Bonus: her saldırgan ve her saldırı için %10; S2 mağaza bonusuna (store bonus) sayılır. **Bir öğrenci, bir bilgisayar, bir GitHub hesabı.**

---

## Gelecek hafta: aynı özellik, bir telefonda

**7. hafta:** mobil istemci (mobile client). Giriş ve kendi özelliğinizin ekranları, şimdi bir telefonda. Aynı endpoint'ler, değişmeden, telefondan çağrılır. Test case'leri bir telefonda çalıştırılır ve kayda geçer.

**8. hafta:** sunucunuz ve seçtiğiniz barındırılan bir LLM API'si (hosted LLM API) üzerinden sohbet botu; özelliğiniz sunucuda, web'de ve telefonda tamamlanır; ilk build mağazanın test kanalında (test track).

**7. haftadan önce:** seçtiğiniz mobil çatı (framework) kurulu (Flutter, React Native–Expo, Kotlin ya da Swift) ve ilk uygulamasını çalıştıran bir telefon ya da emülatör.

<!-- Instructor: the slides from "By Saturday" on are for the last minutes, after the 11:45 push. The mark reads the last commit pushed by the end of the lecture. -->
