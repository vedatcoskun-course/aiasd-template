# 8. Hafta Ödevi: Sohbet Botu ve Testçiler İçin İlk Build

## 1. Kurallar ve notlandırma

### 1.1 Kurallar

- **Paylaşılmayan tek bir bilgisayar ve paylaşılmayan tek bir GitHub hesabı kullan.** Derste kendi
  bilgisayarında çalışmalısın, dersten sonra da aynı bilgisayarda çalışmalısın. Yalnız `student.json` içinde
  listelediğin bilgisayarlar sayılacak. `student.json` içinde listelenmemiş bir bilgisayarda ya da başka bir
  kişinin Git kimliğiyle yaptığın ders çalışması ders için puan getirmeyecek.

- **İşin ortasında commit et ve asla 'force push' yapma.** Her parçayı daha bitmemişken commit et, çalıştığında yeniden commit et. Her commit'i hemen push et. Bitmemiş bir işteki kırmızı kontrol sana hiçbir şey kaybettirmeyecek. Bir force push, neyi değiştirmiş olursa olsun, sana o haftanın commit puanını kaybettirecek.
- **AI log'u hiçbir yapay zeka yardımı olmadan doldur. Bir asistan AI log'da sana herhangi bir şekilde
  yardım ederse AI log'un 0 alacak.** Log'u yazmak, geliştirmek, çevirmek ya da dilini düzeltmek için bir
  asistan kullanma.

**Bu hafta asistanın yardım edebileceği ve edemeyeceği yerler:**

| İş | Asistan |
|---|---|
| `POST /chat`'in ve sohbet ekranının kodunu yaz. LLM API'sinin ya da build'in bir hatasını oku. | Asistan yardım edebilir. |
| Sohbet botunun sistem prompt'unun taslağını yaz. | Asistan yardım edebilir. Son metne sen karar vermelisin. |
| Sohbet botunun kullanıcıların için ne yapacağını seç. | Asistan yardım edemez. Buna kullanıcıların ve gereksinimlerin karar vermeli. |
| Sohbet botunun değişiklik isteğini (change request), gereksinimini ve test case'ini yaz. | Asistan yardım edemez. |
| `week04/store.json` içinde S3'ü doldur. | Asistan yardım edemez. |
| `ai_log_08.md` dosyasını yaz. | Asistan hiçbir şekilde yardım edemez. Bir asistan sana yardım ederse AI log'un 0 alacak. |

### 1.2 Performansın nasıl notlandırılacak

Dersteki performansın 5 puan üzerinden notlandırılacak. Dersin sonuna kadar push ettiğin son commit'i okuyacağım ve şunları kontrol edeceğim:

- Bilgisayarlarını `student.json` içinde, dersteki diğer commit'lerinden önceki bir commit'te listelemiş olmalısın ve ilk push'un GitHub'a 09:30'dan önce ulaşmış olmalı.
- Sohbet botunun değişiklik isteğini gereksinimi, test case'i ve `api.md` satırıyla birlikte eklemiş olmalısın.
- `POST /chat` sunucunda çalışmalı ve repoda hiçbir anahtar (key) bulunmamalı.
- `mobile/` içindeki sohbet ekranının `serves:` satırı olmalı ve ekran "AI answer" etiketini göstermeli.

Cumartesi 23:59'a kadarki performansın 5 puan üzerinden notlandırılacak. 23:59'a kadar GitHub'a ulaşan son commit'i okuyacağım. Commit'in üzerindeki saat değil, GitHub'ın push saati sayılacak.

- Yeşil kontroller sana 2 puan kazandıracak.
- AI log, bütün haftadaki gerçek kullanımını anlatıyorsa, commit'lerinle uyuşuyorsa ve cevapları nasıl kontrol ettiğini gösteriyorsa sana 2 puan kazandıracak. Çok genel kalırsa ya da cevapları nasıl kontrol ettiğini göstermezse 1 puan kazandıracak. Bir asistan yazdıysa, commit'lerin onunla çelişiyorsa ya da boşsa 0 puan alacak.
- Commit disiplini sana 1 puan kazandıracak.

Bir biçim hatası için önce sana bir uyarı vereceğim. Aynı hatayı sonraki bir haftada tekrarlarsan 1 puan kaybedeceksin.

---

## 2. Bir bakışta dönem planı

<table>
<tr><th width="10%" align="center">Hafta</th><th width="15%" align="center">Tarihler</th><th width="70%" align="left">Ne yapıyoruz</th></tr>
<tr><td align="center">1</td><td align="center">22–23 Eyl</td><td>Araçları kurdun, Git ve GitHub'ı öğrendin ve LLM'lere ilk kez baktın.</td></tr>
<tr><td align="center">2</td><td align="center">29–30 Eyl</td><td>Proposal Part A'yı, gereksinimleri ve kullanım senaryolarıyla (use case) birlikte SRS'i yazdın.</td></tr>
<tr><td align="center">3</td><td align="center">6–7 Eki</td><td>Projeni grubunda tanıttın, Proposal Part B'yi yazdın ve mağazanı seçtin (S0).</td></tr>
<tr><td align="center">4</td><td align="center">13–14 Eki</td><td>Tıklanabilir prototipi yaptın ve test case'leri yazdın (S1).</td></tr>
<tr><td align="center">5</td><td align="center">20–21 Eki</td><td>Tasarımı ve API sözleşmesini yazdın ve sunucuya başladın. Gereksinimlerin baseline'ın oldu.</td></tr>
<tr><td align="center">6</td><td align="center">27–28 Eki</td><td>Özelliğin sunucuda ve web'de uçtan uca çalıştı (S2).</td></tr>
<tr><td align="center">7</td><td align="center">3–4 Kas</td><td>Uygulaman telefonda çalıştı.</td></tr>
<tr><td align="center">–</td><td align="center">10–11 Kas</td><td>Ders yok.</td></tr>
<tr><td align="center"><b>8</b></td><td align="center"><b>17–18 Kas</b></td><td><b>Bu hafta ürünün sohbet botuna kavuşacak, sunucun verisini yeniden başlatmadan sonra da koruyacak ve ilk build'in testçilerine gidecek (S3).</b> <i>Erken başla: aşağıdaki listeye bak.</i></td></tr>
<tr><td align="center">9</td><td align="center">24–25 Kas</td><td>Testçilerin uygulamanı beta testte test edecek. Sohbet botunun testlerini yazacaksın ve cevaplarına Report düğmesini ekleyeceksin (S4).</td></tr>
<tr><td align="center">10</td><td align="center">1–2 Ara</td><td>UAT'yi yapacaksın, deployment diyagramını çizeceksin ve uygulamanı mağazaya göndereceksin (S5). <i>Erken başla: aşağıdaki listeye bak.</i></td></tr>
<tr><td align="center">11</td><td align="center">8–9 Ara</td><td>İncelemenin istediği düzeltmeleri yapacaksın, uygulamanı mağazada yayınlayacaksın ve son README'yi yazacaksın (S6). <i>Erken başla: aşağıdaki listeye bak.</i></td></tr>
<tr><td align="center">12</td><td align="center">15–16 Ara</td><td>Posteri hazırlayacaksın ve savunmanın provasını yapacaksın. <i>Erken başla: aşağıdaki listeye bak.</i></td></tr>
<tr><td align="center">13</td><td align="center">22–23 Ara</td><td>TR şubesinin bütün öğrencileri 23 Aralık'ta projelerini sunacak. EN şubesinde yalnız uygulaması mağazada yayında olan öğrenciler bu hafta sunacak.</td></tr>
<tr><td align="center">14</td><td align="center">29 Ara</td><td>Yalnız EN şubesi: EN şubesinin diğer öğrencileri projelerini sunacak. TR şubesinde ders olmayacak.</td></tr>
</table>

**Erken başla.** Önümüzdeki haftaların bazı işleri saatler değil günler sürecek, bu nedenle onlara erken başlamanı rica ederim:

- **8. hafta:** En az 12 testçiye ihtiyacın olacak ve bunların en az 6'sı sınıf arkadaşın olmalı. Google Play, üretime (production) başvurabilmen için testçilerinin 14 gün boyunca kesintisiz olarak test kanalında kalmasını şart koşuyor.
- **10. hafta:** Uygulamanın mağaza sayfasına ihtiyacın olacak: ikonu, ekran görüntüleri, açıklamaları ve gizlilik metninin adresi. UAT için birkaç gerçek kullanıcıya da ihtiyacın olacak.
- **10. ve 11. haftalar:** Mağazanın uygulamanı incelemesi birkaç gün sürebilir ve bu süre senin sorumluluğunda. Uygulamanı planlandığı gibi 10. haftada gönder, böylece 11. haftada incelemenin istediği düzeltmeleri yapmaya vaktin olur. 13. haftadaki sunumun kalan 3 puanı için uygulamanı 5 Aralık Cumartesi 23:59'a kadar göndermiş olman da gerekiyor.
- **12. hafta:** Posterin için uygulamanın ekran görüntülerine ve mimari diyagramına ihtiyacın olacak.

---

## 3. Bu hafta

### 3.1 Bir bakışta bu hafta

6. haftadan beri projen uçtan uca çalışıyor: sunucuda ve web'de, geçen haftadan beri de telefonda. Bu hafta ürünün sohbet botuna kavuşacak ve ilk build'in testçilerine gidecek.

Sohbet botu kendi sunucun üzerinden çalışmalıdır. Telefon LLM API'siyle asla doğrudan konuşmamalıdır. Onunla yalnız sunucun konuşmalı ve anahtarı yalnız sunucun tutmalıdır.

```text
başla  mobile/ içindeki sohbet ekranı
  ↓    POST /chat
  ↓    sunucun
  ↓    seçtiğin LLM API'si (anahtar yalnız server/.env içinde)
  ↓    sunucun
  ↓    sohbet ekranı cevabı "AI answer" olarak gösterir
```

- Gereksinimlerin 5. haftanın sonunda baseline olarak sabitlendi ve sohbet botu bunların arasında yoktu. Bu yüzden sohbet botunu bir değişiklik isteği olarak eklemelisin: yeni bir gereksinim, onun test case'i ve `api.md` içindeki satırı (§4.2).
- Telefon ve web, 7. haftadaki gibi aynı sunucuyu çağırmaya devam etmelidir.



**Derste yapacakların**

<table>
<tr><th width="15%" align="left">Saat</th><th width="75%" align="left">İşin</th><th width="10%" align="center">§</th></tr>
<tr><td>dersten önce</td><td>Seçtiğin LLM API'sinde bir hesap aç ve anahtarını oluştur. Bunu ders gününden önce, örneğin evde yap.</td><td align="center">4.3</td></tr>
<tr><td>diğer bütün commit'lerden önce</td><td><code>student.json</code> dosyasına bilgisayarlarının listesini ekle. Her bilgisayar için adını (§4.1'deki komut gösterir), onda kullandığın Git e-postasını, bilgisayarın kimin olduğunu ve onu başka kimin kullandığını yaz. Bu değişikliği tek başına commit et (<code>week08: my computer</code>). Bunu dersten önce de yapabilirsin. Reponda "8. haftaya hazırlık" issue'su nasıl yapılacağını gösteriyor.</td><td align="center">4.1</td></tr>
<tr><td>09:30</td><td>Checker'ı çalıştır: <code>week08/</code> klasörünü getirir. Ders dosyalarını commit et ve iki commit'i de hemen push et.</td><td align="center">4.1</td></tr>
<tr><td>yaklaşık 10:00</td><td>Sohbet botunu bir değişiklik isteği olarak yaz: gereksinimini, test case'ini ve <code>api.md</code> satırını ekle.</td><td align="center">4.2</td></tr>
<tr><td>yaklaşık 10:45</td><td><code>POST /chat</code>'i sunucunda çalışır hale getir.</td><td align="center">4.3</td></tr>
<tr><td>yaklaşık 11:30</td><td><code>mobile/</code> içinde sohbet ekranını yap.</td><td align="center">4.4</td></tr>
<tr><td>11:45</td><td>Son kez push et.</td><td align="center">4.5</td></tr>
</table>

Dersteki performansın 5 puan üzerinden, Cumartesi performansın da 5 puan üzerinden notlandırılacak. Ayrıntılar §1.2'de.

**Gelecek hafta testçilerin, senin kendi dosyalarından hazırlanan bir test planıyla çalışacak**: gereksinimlerin, ekranların ve test case'lerin. Bu hafta bu dosyaları birbiriyle uyumlu tut.

### 3.2 Bu hafta neler öğreneceksin

Bu hafta şunları öğreneceksin:

- bir sunucunun bir LLM API'sini, anahtarı kodun ve uygulamanın dışında tutarak nasıl güvenle çağırdığını;
- bir sohbet botunun login, günlük sınır ve yalnız kullanıcının kendi verisiyle nasıl korunduğunu;
- ilk build'in bir mağazanın test kanalına (test track) nasıl konduğunu.

Şu yeni terimleri de kullanacaksın:

| Terim | Anlamı |
|---|---|
| LLM API | LLM API, bir metne bir metinle cevap veren internetteki bir hizmettir; örneğin Gemini, OpenAI, Anthropic ya da Groq API'si. Sunucun ona bir mesaj gönderir ve bir cevap alır. |
| API anahtarı (API key) | API anahtarı, LLM API hesabının şifresidir. Anahtarı eline geçiren, hesabındaki parayı harcayabilir. Anahtar yalnız `server/.env` içinde durmalı. |
| `.env` | `.env`, sunucunun şifreleri ve anahtarları tutan dosyasıdır. `.gitignore` içinde listelendiği için asla GitHub'a ulaşmaz (`AI_Doc3`, python-dotenv). `server/.env.example` yalnız adları tutar, örneğin `LLM_API_KEY=`. |
| Sistem prompt'u (system prompt) | Sistem prompt'u, sunucunun kullanıcının mesajından önce modele gönderdiği talimatlardır. Sohbet botunun ne için olduğunu ve neyi yapmaması gerektiğini söyler. |
| Günlük sınır | Günlük sınır, bir kullanıcının bir günde gönderebileceği mesaj sayısıdır. Sınırdan sonra sunucun 429 ile cevap vermelidir. |
| Test kanalı (test track) | Test kanalı, bir build'in herkese açılmadan önce testçilere gittiği mağaza bölümüdür. Google Play'de test kanalının adı kapalı testtir (closed testing). |
| S3 | S3, mağazanın üçüncü adımıdır. S3'te ilk build'in test kanalındadır ve testçilerin ona kayıtlıdır. |

### 3.3 Checker bu hafta neler getiriyor

Dersin başında checker'ı çalıştırdığında (§4.1), checker repona yeni `week08/` klasörünü getirecek. Klasörde üç dosya var:

- `ASSIGNMENT_08_EN.md` ve `ASSIGNMENT_08_TR.md`: bu ödevin İngilizcesi ve Türkçesi;
- `ai_log_08.md`: Cumartesi günü dolduracağın AI log'un formu (§5.5).

Checker'ın kendisi de bu hafta yeni kontroller kazanıyor. `student.json` içindeki bilgisayar listeni, sohbet botunun değişiklik isteğini, sunucundaki `POST /chat`'i ve `mobile/` içindeki sohbet ekranını kontrol edecek. Cumartesi günü `week04/store.json` içindeki S3'ü ve gizlilik metninin adresini de kontrol edecek.

---

## 4. Dersteki işin

### 4.1 Bilgisayarların, ders dosyaları ve ilk push, 09:30'dan önce

Dersin başında bu üç adımı bu sırayla yap.

**1. adım. `student.json` dosyasını güncelle.** `student.json`, reponun kök klasöründe duruyor; ilk haftada öğrenci numaranı yazdığın dosya bu. Önce proje klasöründe bir terminal aç ve şu iki komutu çalıştır. Birincisi bilgisayarının adını, ikincisi Git e-postanı gösterir.

<table>
<tr><th width="50%" align="left">Mac'te</th><th width="50%" align="left">Windows ya da Linux'ta</th></tr>
<tr>
<td>

```bash
scutil --get LocalHostName
git config user.email
```

</td>
<td>

```bash
hostname
git config user.email
```

</td>
</tr>
</table>

E-posta, kendi GitHub hesabının e-postası olmalı. Değilse önce kendi adını ve e-postanı ayarla, sonra iki komutu yeniden çalıştır:

```bash
git config --global user.name "Adın Soyadın"
git config --global user.email "GitHub hesabının e-postası"
```

Sonra bilgisayarlarının listesini `student.json` içinde `"section"` satırından sonra ekle ve o satırın sonuna bir virgül koy. İki çıktıyı listeye yaz:

```json
  "computers": [
    {
      "hostname": "the name of your computer",
      "git_email": "the output of git config user.email",
      "owner": "your student number",
      "also_used_by": "",
      "why": ""
    }
  ]
```

- `"hostname"` alanına bilgisayarının adını birinci komutun gösterdiği gibi yaz, örneğin `"Ayses-MacBook-Air"` ya da `"DESKTOP-4F7K2Q1"`.
- `"git_email"` alanına `git config user.email` komutunun çıktısını yaz, örneğin `"vedat.coskun@atlas.edu.tr"`.
- `"owner"` alanına, bilgisayar seninse öğrenci numaranı yaz, örneğin `"123456789"`. Başka bir öğrencinin bilgisayarıysa o öğrencinin numarasını yaz. Öğrenci olmayan birinin bilgisayarıysa kim olduğunu yaz, örneğin `"my father"`.
- `"also_used_by"` alanına bu bilgisayarı kullanan diğer her öğrencinin numarasını ya da onu başka kimin kullandığını yaz, örneğin `"my sister"`. Başka kimse kullanmıyorsa boş bırak. Bu dersteki bir sınıf arkadaşın onu asla kullanamaz.
- Yalnız bir bilgisayar kullanıyorsan `"why"` alanını boş bırak. Gerçekten ikinci bir bilgisayara ihtiyacın varsa, örneğin evdeki bir masaüstü bilgisayara, onun için ikinci bir kayıt ekle ve `"why"` alanına neden ihtiyacın olduğunu yaz.

Sonra bu değişikliği tek başına commit et:

```bash
git add student.json
git commit -m "week08: my computer"
```

**2. adım. `week08/` klasörünü getir.** Checker'ı çalıştır. Checker `week08/` klasörünü getirir. Sonra ders dosyalarını commit et.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week08: course files"
```

**3. adım. Hemen push et.** İki commit'i de hemen, 09:30'dan önce push et.

```bash
git push
```

Checker bilgisayarının adını ve `git config user.email` çıktını da okur ve bu bilgisayar `student.json` içinde listelenmemişse sana söyler.

### 4.2 Değişiklik isteği olarak sohbet botu

Önce sohbet botunun kullanıcıların için ne yapacağına tek bir cümleyle karar ver. Sohbet botu ürününe hizmet etmelidir. Örneğin kullanıcının rezervasyonlarıyla ilgili soruları cevaplar ya da kullanıcının kayıtlarından haftalık bir plan önerir. Yalnız her konuda sohbet eden bir sohbet botu sayılmayacak.

Gereksinimlerin 5. haftada baseline'ın oldu, bu yüzden yeni bir gereksinim bir değişiklik isteğidir (6. hafta §9). Aşağıdaki üç değişikliği yap ve üçünü de `PROPOSAL.md` içindeki Change log'un tek bir satırında an.

- **Gereksinimi ekle.** `week02/requirements.json` dosyasına, sıradaki boş id ile işlevsel (functional) bir `must` gereksinim ekle. Kabul kriteri, sohbet botunun neye cevap verdiğini, yalnız giriş yapmış bir kullanıcının onu kullanabileceğini, yalnız o kullanıcının verisini kullandığını ve bir kullanıcının bir günde kaç mesaj gönderebileceğini söylemeli.
- **Test case'i ekle.** Gereksinim için `week04/test_cases.json` dosyasına `"run": "manual"` olan en az bir test case ekle. Bu test case'i bu hafta bir kişi telefonda çalıştırmalı. LLM API'sinin yerine sahte bir modelle sunucuda çalışan testler 9. haftada gelecek.
- **`api.md` satırını ekle.** `week05/api.md` dosyasına `POST /chat` satırını ekle. İstek kullanıcının mesajını, cevap da sohbet botunun cevabını tutmalıdır. Hatalar şunlar olmalıdır: token yoksa 401, günlük sınırdan sonra 429, LLM API'si cevap vermezse 503.

Change log satırı için bir örnek: *"2026-11-18 — CR-03: sohbet botu. Yeni REQ-012 (must), yeni TC-012-01 (manual), yeni api.md satırı POST /chat; etkilenen dosyalar: week02/requirements.json, week04/test_cases.json, week05/api.md."*

### 4.3 Sunucunda `POST /chat`

- **Anahtarını dersten önce al.** Seçtiğin LLM API'sinde bir hesap aç ve bir anahtar oluştur. Kayıt biraz zaman alabilir, bu yüzden bunu ders gününden önce, örneğin evde yap.
- **Anahtarı yalnız `server/.env` içinde tut.** Anahtarı `server/.env` dosyasına `LLM_API_KEY=...` olarak koy ve `os.getenv("LLM_API_KEY")` ile oku. Anahtarı asla koduna, uygulamana ya da commit ettiğin bir dosyaya yazma. `server/.env.example` dosyasına değeri olmadan `LLM_API_KEY=` satırını ekle. Checker reponun her dosyasında anahtar arar.
- **Login iste.** Geçerli bir token olmadan route, diğer route'ların gibi 401 ile cevap vermelidir.
- **Modele yalnız kullanıcının verisini gönder.** Sohbet botu kayıtlarla ilgili soruları cevaplıyorsa modele yalnız giriş yapmış kullanıcının kayıtlarını gönder. Diğer kullanıcıların verisini, e-posta adreslerini ya da şifreleri asla gönderme.
- **Her kullanıcının mesajlarını sınırla.** Her kullanıcının günlük mesajlarını say. Gereksinimindeki sınırdan sonra sunucun, kullanıcının okuyabileceği bir mesajla 429 ile cevap vermelidir.
- **LLM API'sinin bir hatasını karşıla.** Sunucun LLM API'sini en fazla 20 saniye beklemelidir. API cevap vermezse ya da bir hatayla cevap verirse route'un bir mesajla 503 ile cevap vermelidir. Sunucu çökmemelidir.

LLM API'sini sen seçeceksin. Para ödemen gerekmiyor: Gemini API, Groq ve GitHub Models'in kredi kartı istemeyen ücretsiz kullanımları var. Ücretli bir API seçersen maliyeti sana ait olacak. Ücretsiz bir kullanım, sağlayıcının gönderdiğin veriyi kullanmasına izin verebilir, bu yüzden ona asla kişisel veri gönderme.

### 4.4 `mobile/` içinde sohbet ekranı

- Ekranın kaynak dosyası sohbet botunun gereksinimini anmalıdır: `// serves: REQ-0NN`.
- Ekran mesajı, diğer ekranların gibi token ile `POST /chat`'e göndermelidir.
- Ekran, sohbet botunun her cevabını **AI answer** etiketiyle göstermelidir; böylece kullanıcı onu bir modelin yazdığını bilir.
- Ekran 429 ve 503 mesajlarını kullanıcıya göstermelidir.

Ekranı daha bitmemişken commit et, örneğin alanı ve düğmeyi gösterdiği ama henüz sunucuyu çağırmadığı zaman. Çalıştığında yeniden commit et.

### 4.5 Push et ve sonucu GitHub'da kontrol et

`ruff check . --fix` ve `ruff format .` komutlarını çalıştır. Sonra checker'ı çalıştır, commit et ve push et. Actions sekmesini aç ve çalıştırmayı kontrol et. Ders notu için dersin sonuna kadar push ettiğin son commit'i okuyacağım.

---

## 5. Cumartesi 23:59'a kadarki işin

### 5.1 Kendi özelliğin üç istemcide de tamamlanmış olmalı

Her işlevsel `must` gereksinim sunucuda, web'de ve telefonda çalışmalıdır. Her gereksinimin yeşil bir testi olan bir route'a, `web/` içinde bir sayfaya ve `mobile/` içinde bir ekrana ihtiyacı vardır ve bunların her birinin `serves:` satırı olmalıdır. Özelliğin, testçilerin onu gelecek hafta görmeden önce tamamlanmış olmalı.

**Önce 5., 6. ve 7. haftalardan hala eksik olanları tamamla.** Checker'ı çalıştır: hala eksik olan her route'u, testi, sayfayı ve ekranı listeler. Checker her Cumartesi önceki bütün haftaların işini yeniden kontrol eder, bu yüzden eksik bir parça, sen onu tamamlayana kadar her hafta checker puanını düşürecek. Testçilerin yalnız çalışan parçaları test edebilir.

### 5.2 Verin yeniden başlatmadan sonra da kalmalı

Şimdiye kadar sunucun verisini bellekte tutabiliyordu. Bu haftadan itibaren sunucun verisini bir dosyada ya da seçtiğin bir veritabanında, örneğin SQLite'ta tutmalıdır. Bunu dene: sunucuyu başlat, bir kayıt ekle, sunucuyu durdur, yeniden başlat ve kaydın hala orada olduğunu kontrol et. `week05/DESIGN.md` dosyasına sunucunun verisini nerede tuttuğunu tek bir satırla yaz ve Change log'a tarihli bir satır ekle.

### 5.3 S3: test kanalındaki ilk build'in

Mağaza hangisi olursa olsun her öğrenci en az 12 testçi kaydetmeli ve bunların en az 6'sı sınıf arkadaşı olmalı. Bir sınıf arkadaşın, ancak telefonu uygulamanı senin mağazandan yükleyebiliyorsa testçin olabilir: Google Play, Huawei AppGallery ya da Samsung Galaxy Store için bir Android telefon, App Store için bir iPhone. Önce testçilerinin e-posta adreslerini topla. Google Play, her testçinin Google hesabının e-posta adresini ister.

Sonra ilk build'ini mağazanın test kanalına yükle ve testçilerini oraya kaydet.

- Google Play'de test kanalı kapalı bir testtir (closed testing). Google Play'in kendisi, yeni bir kişisel hesap için en az 12 testçi istiyor ve bu testçiler uygulama yayınlanabilmeden önce 14 gün boyunca kesintisiz olarak kayıtlı kalmalı. Onları bu hafta kaydedersen 14 gün, 10. haftadaki gönderimden önce dolar.
- Diğer mağazaların kendi test kanalları var (`AI_PLATFORMS_AND_STORES`). 12 testçini orada da aynı şekilde kaydet.

Sonra `week04/store.json` içinde S3'ü kendin doldur ve test kanalının, kayıtlı testçilerini gösteren bir ekran görüntüsünü ekle:

```json
  "S3": {
    "date": "2026-11-21",
    "track": "closed testing",
    "version": "1.0.0 (1)",
    "classmate_testers": ["123456789", "234567891", "345678912", "456789123", "567891234", "678912345"],
    "other_testers": ["Ayşe Yılmaz", "Mehmet Demir", "Elif Kaya", "Can Öztürk", "Zeynep Arslan", "Emre Şahin"],
    "privacy_url": "https://gist.github.com/your-name/...",
    "evidence": "store_s3.png"
  }
```

`"classmate_testers"` alanına testçin olan sınıf arkadaşlarının öğrenci numaralarını yaz. `"other_testers"` alanına diğer her testçinin adını ve soyadını yaz. İki liste birlikte en az 12 testçi tutmalı ve `"classmate_testers"` en az 6 numara tutmalı. Testçilerinin e-posta adresleri asla repona girmemeli.

### 5.4 Gizlilik metnin

Uygulamanın gizlilik metni, sohbet botunun mesajlarının LLM API'ne gittiğini söylemeli ve sağlayıcının adını vermelidir. Metni reponun kök klasöründeki `PRIVACY.md` dosyasına yaz. Google Play gizlilik metnini, herkesin giriş yapmadan açabileceği bir web adresi olarak ister, ama senin repon özel (private). Bu yüzden aynı metni herkese açık bir sayfada da yayınla, örneğin herkese açık bir GitHub Gist olarak. Bu sayfanın adresini `week04/store.json` içindeki S3'e (§5.3) ve Play Console'a yaz.

### 5.5 AI log: `week08/ai_log_08.md`

Bu haftadan itibaren AI log, bütün hafta boyunca, bütün işinde yapay zeka asistanlarını nasıl kullandığını anlatmalı. Artık tek bir alıştırmayı ya da tek bir örneği anlatmamalı. Log'u commit'lerinle karşılaştıracağım ve gerçekten anlattığı şekilde çalışıp çalışmadığını kontrol edeceğim. Log'u Cumartesi günü kendin doldur:

1. **Asistanlarım.** Kullandığın her asistanı, modelini ve ücretsiz mi ücretli mi olduğunu listele. Ücretli bir asistan için paketin adını yaz.
2. **Bu haftaki her asistan kullanımı.** Her gerçek kullanım için, haftanın sırasıyla bir satır yaz; yalnız iyi gidenleri değil. Satıra neyi sorduğunu, cevabı nasıl kontrol ettiğini, onunla ne yaptığını (olduğu gibi tuttun, değiştirdin ya da reddettin) ve sonucun girdiği commit'i yaz.
3. **Bu hafta asistanlarla nasıl çalıştım.** Birkaç cümleyle bütün haftadaki çalışma biçimini anlat: bir asistana ne zaman başvurdun, cevaplarını genellikle nasıl kontrol ettin ve genellikle neyi tuttun ya da reddettin.
4. **Asistansız yaptıklarım.** İşin hangi kısmını kendin yaptığını yaz.
5. **Gelecek hafta.** Gelecek hafta farklı yapacağın bir şeyi yaz.
6. **Bu dersten önce ve şimdi.** Bu kısım notlandırılmayacak, bu nedenle dürüstçe yazmanı rica ederim. Bu dersten önce yapay zeka asistanlarını kod için nasıl kullandığını ve şimdi neyi farklı yaptığını yaz.

Kısa ve sade cümleler yeterli. Log'da artık bir Evidence bloğu ya da kalın yazılmış alıntılar yok. Log'u bir insan okuyacak ve commit'lerinle karşılaştıracak. **AI log'u hiçbir yapay zeka yardımı olmadan yazmalısın. Bir asistan log'da sana herhangi bir şekilde yardım ederse AI log'un 0 alacak.**

### 5.6 Commit'ler ve yeşil kontroller

- Ders dışında, aralarında en az bir saat olan, yeni iş içeren en az iki commit push et.
- Her commit `mobile/` içine en fazla bir yeni ekran ve `server/` içine en fazla bir yeni route eklemeli. Checker seni commit etmeden önce uyarır.
- Bir kodlama ajanının (coding agent) yaptığı bir commit asla sayılmayacak.
- On ders testi ve `"run": "server"` olan her `must` test case'inin testleri GitHub'da yeşil kalmalı. `.github/workflows/check.yml` ya da `.github/check_deliverables.py` dosyasını asla değiştirme.
- Git, uygulamanın build klasörlerini tutmamalı (7. hafta §12).


### 5.7 Proje belgelerinin hepsini her hafta gerektiği gibi güncelle

Gereksinimler, kullanım senaryolarıyla birlikte SRS, her diyagram, `serves:` satırlı ekranlar, test case'ler, `api.md`, `DESIGN.md`, kod ve testler tek bir ürünü anlatmalı. Bunlardan biri değiştiğinde diğerlerini aynı hafta güncelle ve Change log'a bir satır yaz. §5.8'deki kontrol listesi sana yardım eder.

### 5.8 Belgelerin: bir kontrol listesi

Cumartesi günkü son push'undan önce belgelerinin ürününü şimdiki haliyle anlattığını kontrol et:

- `PROPOSAL.md` §5'teki diyagram şu an sahip olduğun parçaları gösteriyor. Bu hafta LLM API'ni de gösteriyor. Change log'da haftanın her değişikliği için bir satır var.
- `week02/requirements.json` içindeki her gereksinim `week02/SRS.md` içindeki bir kullanım senaryosuna ait ve kullanım senaryosu diyagramı, sohbet botununki de dahil, her kullanım senaryosunu gösteriyor.
- `web/` ve `mobile/` içindeki her ekran, `serves:` satırında var olan bir gereksinimi anıyor.
- `week04/test_cases.json` içindeki her test case var olan bir gereksinimi anıyor ve adımları ekranlarının şimdiki haliyle uyuşuyor.
- Sunucunun her route'unun `week05/api.md` içinde aynı yol, istek ve durum kodlarıyla bir satırı var.
- `week05/DESIGN.md` içindeki bileşenler ve mimari diyagramı kodunla uyuşuyor. Bu hafta LLM API'sini ve verinin tutulduğu yeri de gösteriyorlar.
- Bir gereksinimdeki ya da bir test case'teki her değişikliğin CR satırı var.

Checker id'ler arasındaki bağlantıların bir kısmını kontrol eder. Diyagramları ve metinleri yalnız sen kontrol edebilirsin.
