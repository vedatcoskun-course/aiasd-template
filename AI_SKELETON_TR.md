# AIASD — Dönem Bir Bakışta

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027 · Prof. Dr. Vedat Coşkun**

*English: [`AI_SKELETON_EN.md`](AI_SKELETON_EN.md)*

Bu belge, dönemin tamamını iki sayfada anlatır: her hafta ne öğretildiğini, sınıfta ne
yaptığınızı, Cumartesi'ye kadar neyi bitirdiğinizi ve reponuza ne geldiğini söyler. İlk
derste gösterilir ve reponuzda yaşar. Dönem içinde değişebilir ve her değişiklik, kendi
teklifinizdeki değişiklikleri kaydettiğiniz gibi, bu dosyanın sonunda kaydedilir.

## Her hafta geçerli olanlar

- **Tek bir projeyi, yalnız, dönem boyunca** yaparsınız. Proje bir mobil istemci, bir web
  istemcisi ve bir sunucudur; giriş e-postayla gönderilen 4 haneli bir kodla yapılır (6.
  haftadan itibaren dersin giriş modülü, her projede aynı) ve dönem sonunda **bir public
  mağazada yayınlanmış** olur. Hangi mağazayı kullandığınız ve uygulamanın native mi hybrid
  mi olduğu sizin seçiminizdir (`AI_PLATFORMS_AND_STORES_EN/TR.md`). 13. haftadaki (EN şubesinde 13–14. haftalardaki)
  savunma mağazadan yüklenmiş uygulamadan yapılır.
- **Haftada 10 puan** kazanırsınız: 5'i dersin sonunda, 5'i Cumartesi 23:59'da reponuzdan
  okunur. 1. hafta 5 puandır ve tamamı Cumartesi okunur. Dönem notu şunlardan oluşur:
  haftalık projeler 60 · mağaza bonusu 15 · sunum (savunma, 13. hafta; EN şubesinde 13–14. hafta) 15 · final
  sınavı 40.
- **3. hafta dersinde dört kişilik bir grup kurarsınız** (sınıf dörde bölünmüyorsa beş
  kişilik). 3. haftadaki grubunuz grubunuz olarak kalır; hangi haftalarda ve ne için
  toplandığını ödev söyler. 3. haftada diğer üyeler `week03/contributors_03.json` içindeki
  değerlendirenlerinizdir. `weekNN/group_NN.json`, o haftanın ödevinin adını verdiği
  kişileri o haftanın rolüyle (tam İngilizce kelimeyle; aşağıdaki Notlar sütununda; 5.
  haftada kimse: tek başınıza çalışırsınız) tutar. Adını verdiğiniz kişiler sizin
  notunuzdan bonus kazanır, siz onlarınkinden kazanırsınız. 2. haftada katkıcı zorunlu
  değildir.
- **İnsan işini kanıtlarsınız**: sizinkini `weekNN/ai_log_NN.md` içinde kanıtlarsınız,
  yardımcılarınız kendilerininkini adlarının yanında kanıtlar. Cumartesi puanlarının ikisi bu
  kanıta bağlıdır.
- **`PROPOSAL.md` kökte yaşar** ve herhangi bir haftada değişebilir; yeter ki Change
  log'una tarihli bir satır ekleyin. Sessiz değişiklik puana mal olur; kaydedilmiş
  değişiklik mühendisliktir. **Projenin kendisi 3. hafta dersinin sonunda (11:45) kesinleşir**: o andan sonra ayrıntıları değişebilir, problemi ve ürünü değişemez.
- **Change request'ler:** 5. haftadan sonraki Pazar gününden (baseline)
  itibaren `requirements.json` ya da `test_cases.json` dosyasındaki her değişiklik,
  düşürülen bir gereksinim de dahil, `PROPOSAL.md` Change log'unda `CR-` ve sıradaki
  numarayla başlayan, değişikliği ve id'leri söyleyen ve etkilediği her dosyayı sayan tek
  bir satırdır.
- **Yayınlama adım adım notlandırılır** (plandaki S0–S6 adımları), her adımın teslim
  haftasında. Mağazayla ilgili hiçbir şey son haftada yapılamaz.
- **Her diyagram Mermaid'dir** (metin tabanlı bir diyagram gösterimi) ve markdown dosyasının
  içinde yazılır. GitHub onu çizer, denetleyici onu okur.

Puanların nasıl hesaplandığı, denetleyicinin neye baktığı ve bonusun ayrıntıları
`AI_WEEKLY_WORKFLOW_STUDENT_TR.md` / `_EN.md` içindedir.

## Haftalık plan

### Her hafta ne olur

| Hafta | İçerik | Sınıfta | Ders sonrası | Notlar |
|---|---|---|---|---|
| 1 | Derse giriş; araçlar; Git; LLM'lerle (büyük dil modelleri) ilk temas | • Ödev adım adım anlatılır<br>• henüz bir şey yapılmaz | Araçları kurun, şablondan private repoyu oluşturun, Collaborator ekleyin, student.json'ı doldurun, hello.py yazın ve iki LLM'i keşfedin | • Hafta 5 puandır, tamamı Cumartesi okunur (3 otomatik · 1 commit · 1 yapay zeka günlüğü)<br>• Bu hafta katkıcı yok |
| 2 | Teklif Bölüm A + gereksinimler (`requirements.json`, gereksinimlerin tek yeri) + SRS (use case'ler ve use case diyagramı) | • Problemi ve çözümü yazın<br>• en çok iki paydaşla görüşün (isteğe bağlı)<br>• gereksinim listesine başlayın | • Teklif Bölüm A'yı bitirin<br>• SRS + use case diyagramını yazın (§4 ve §5, `requirements.json` dosyasını gösterir) | • Teklif kökte yaşar ve onu herhangi bir haftada bir Change log satırıyla revize edebilirsiniz<br>• Rol: stakeholder |
| 3 | Pitch, inceleme, Teklif Bölüm B | • Dört kişilik grubunuzu kurun<br>• pitch'inizi grupta sunun; diğer üçü cevaplarını yazar<br>• Bölüm A'yı gözden geçirin ve Change log'u başlatın<br>• ana akışın ekranlarını yazın; proje dersin sonunda (11:45) kesinleşir | • Bölüm B'yi yazın: pazar, rakipler, karşılaştırma, ticari potansiyel, mağaza seçimiyle birlikte teknik riskler<br>• yapay zeka günlüğü: asistan düşman gözden geçiren olarak<br>• her kabul ölçütünü 4. hafta için test edilebilir hale getirin | • S0: teklifin §12'si mağazayı, ücreti ve inceleme süresini adlandırır<br>• Cumartesiden itibaren bir gereksinim id'sinin anlamı değişmez; liste 5. hafta sonundaki taban çizgisine kadar açık kalır<br>• Rol: reviewer; grup dönem boyunca kalır |
| 4 | Tıklanabilir prototip ve test case'ler | • Ana akışı düz HTML ekranlarla kurun<br>• her must gereksinim için bir test case yazın<br>• collaborator'ınız (seçtiğiniz bir sınıf arkadaşı) bunları prototip üzerinde yürütür (walk-through); söylediklerini siz elle yazarsınız | • Başarısız olanları düzeltin; collaborator'ınızla çevrim içi ikinci tur<br>• gereksinimleri ve test case'leri güncelleyin<br>• ekran akışını tamamlayın<br>• geliştirici hesabını açın | • S1: dersin olduğu gün başvurun, çünkü kimlik kontrolü günler sürer<br>• Rol: collaborator |
| 5 | Tasarım ve API sözleşmesi; geliştirme başlar | • Tasarımı yazın (bileşenler ve hizmet ettikleri REQ id'leri)<br>• API sözleşmesinin giriş satırlarını yazın<br>• sunucu iskeleti yerelde çalışır | • API sözleşmesini yazın (sunucunun her endpoint'i)<br>• giriş testlerini test case'lerinizden, TC id'leriyle adlandırarak, koddan önce yazın: giriş 6. haftada var olana kadar başarısız olurlar | • Cumartesi gereksinimler ve test case'ler taban çizginiz (baseline) olur; ondan sonra bir değişiklik bir change request ile (`PROPOSAL.md` Change log'unda bir `CR-` satırı) yapılır<br>• Bu hafta grup çalışması yok: yalnız çalışırsınız ve katkı bonusu yoktur |
| 6 | Kendi özelliğiniz, uçtan uca | • Dersin girişi bağlanır: `server/login_contract.json` elle, LOGIN_01–06 ders testleri GitHub'da geçer<br>• kendi işlevsel `must` gereksinimlerinizden biri sunucuda çalışır (artık 501 yok), test case'leriyle adlandırılmış testleri GitHub'da geçer ve prototip ekranı, girişin arkasında duran bir web istemcisi sayfası olur<br>• bir grup arkadaşı özelliğinize ve girişe saldırır | • Her işlevsel `must` gereksinim uçtan uca: `api.md` satırları cevap verir, `run: server` olan test case'lerinin GitHub'da geçen testleri vardır ve `web/` içinde bir sayfa ona hizmet eder<br>• LOGIN_07–10 ders testleri GitHub'da geçer<br>• kod gerçek e-postayla gelir (`.env` repoya girmez)<br>• saldırganların her bulgusu için kararınız (`accepted`, `why`)<br>• mağazada uygulama kaydını oluşturun<br>• her test case nasıl çalıştırıldığını söyler<br>• yapay zeka günlüğü: özelliğinizin düşman gözden geçireni olarak asistan | • Her gereksinimin zinciri: gereksinim → kullanım senaryosu → ekran → test case → `api.md` satırı → route → GitHub Actions'ta yeşil test → web sayfası; kaynak `requirements.json` dosyasıdır<br>• giriş dersindir (`server/course_login.py`), herkes için aynı<br>• S2: uygulama kaydı / bundle id (mağazanın uygulamanızı tanıdığı benzersiz ad)<br>• ders notu GitHub Actions çalıştırmasını okur<br>• Rol: attacker |
| 7 | Mobil istemci | Giriş ve kendi özelliğinizin bir ekranı bir telefonda ya da emülatörde çalışır ve sunucuyla konuşur | • Her işlevsel `must` gereksinim telefonda da<br>• mobil test case'leri telefonda koşun ve kayda geçirin (`run`: manual)<br>• sunucu ve web testleri GitHub Actions'ta yeşil kalır | • Giriş ve özelliğiniz üç katmanda da canlı<br>• Rol: tester |
| 8 | Geliştirme — sohbet botu ve tamamlanan özelliğiniz | • Sohbet botu uçtan uca çalışır: sunucudaki `POST /chat` seçtiğiniz barındırılan bir LLM API'sini çağırır, mobil istemcide sohbet ekranı vardır<br>• sohbet botu gereksinimlere bir change request ile (sıradaki CR numaranızla) girer | • Kendi özelliğinizi üç istemcide tamamlayın<br>• ilk build'i test kanalına yükleyin ve testçileri oraya kaydedin (S3): yeni bir kişisel Google Play hesabı için 12 ya da daha fazla; böylece 14 gün 10. haftadaki gönderimden önce biter | • API anahtarı yalnızca sunucunun `.env` dosyasındadır: asla uygulamada, asla repoda değil<br>• ücretli bir API'nin maliyeti size aittir; ücretsiz katmanlar vardır<br>• S3 mağazanın zorunlu test süresini başlatır<br>• 8. haftadan itibaren sunucu verilerini yeniden başlatmadan sonra da korur: bir dosyada ya da seçtiğiniz bir veritabanında (SQLite Python ile birlikte gelir)<br>• Rol: test-user |
| 9 | Beta testi | • Beta testini 8. haftada kaydedilen testçilerle yürütün<br>• hata listesini açın | • Hataları düzeltin<br>• test raporunu yazın<br>• sohbet botunun testleri, gerçek API yerine sahte bir modelle<br>• sohbet botunun cevaplarında Report düğmesi | • S4: beta testi, S3'te kaydedilen testçilerle mağazanın test kanalında yapılır (9. hafta)<br>• Beta testçileri mağazanın testçileriyle aynı kişiler olmalıdır<br>• Rol: beta-tester |
| 10 | UAT (Kullanıcı Kabul Testi, gerçek kullanıcıların ürünü denediği bir oturum) + gönderim | UAT oturumunu katılımcılarla yürütün | • UAT raporunu yazın<br>• dağıtım diyagramını çizin<br>• uygulamayı incelemeye gönderin | • S5, ret ve yeniden gönderim için bir hafta bırakır<br>• Rol: uat-participant |
| 11 | Yayın + sağlamlaştırma | • İnceleme düzeltmelerini uygulayın<br>• release-tester uygulamayı mağazadan yükler | • Canlıya çıkın<br>• son README'yi yazın | • S6: uygulama canlı<br>• Rol: release-tester |
| 12 | Kapanış | • Poster taslağı gözden geçirilir<br>• savunma provası | Son posteri bitirin | • Savunmanın kendisi 13. haftadadır (EN şubesinde 13–14. haftalarda) ve mağaza kurulumundan yapılır<br>• Rol: poster-reviewer |

### Dosya akışı — öğrencinin aldığı ve push ettiği

Ödevler `_EN` ve `_TR` olarak gelir ve aşağıda bu ek atlanmıştır. Okumalar (`AI_DocN`) İngilizcedir; yalnızca `AI_Doc5` İngilizce ve Türkçedir. Ders sunumu repoda bir dosya değildir.

| Hafta | Verilen (`weekNN/` ya da köke gelir) | Ders sonuna kadar push (5) | Cumartesi'ye kadar push (5) |
|---|---|---|---|
| 1 | • `AI_Doc1`–`AI_Doc4` ön okuma (kök)<br>• `week01/ASSIGNMENT_01`<br>• iskeletler (başlıkları hazır, içeriği boş gelen dosyalar) `llm_notes.md`, `ai_log_01.md`<br>• kök: `student.json`, `README`, `AI_SETUP_CARD`, `AI_WEEKLY_WORKFLOW_STUDENT` | — | • `student.json`<br>• `week01/setup_proof.md`<br>• `hello.py`<br>• `llm_notes.md`<br>• `ai_log_01.md` (5 puanın tamamı) |
| 2 | • `week02/ASSIGNMENT_02`<br>• kök `PROPOSAL.md` iskeleti<br>• `week02/SRS.md` iskeleti<br>• `requirements.json` iskeleti<br>• `contributors_02.json`<br>• `ai_log_02.md`<br>| • `PROPOSAL.md` §1–§4<br>• `week02/requirements.json` ilk liste<br>• `contributors_02.json` | • `PROPOSAL.md` §5–§7<br>• `week02/SRS.md` + use case diyagramı<br>• `requirements.json` son hali<br>• `ai_log_02.md` |
| 3 | • `week03/ASSIGNMENT_03`<br>• `PITCH_03.md`<br>• `group_03.json`<br>• `contributors_03.json`<br>• `screens_03.md`<br>• `ai_log_03.md`<br>• kökte `AI_Doc5` | • `PITCH_03.md` (dersten önce)<br>• `group_03.json` (her üye için aynı liste)<br>• `contributors_03.json` (üç gözden geçiren)<br>• gözden geçirilmiş `PROPOSAL.md` Bölüm A + Change log<br>• `screens_03.md` (ana akış) | • `PROPOSAL.md` §8–§12<br>• güncel `requirements.json`<br>• `ai_log_03.md` |
| 4 | • `week04/ASSIGNMENT_04`<br>• üç başlangıç ekranıyla `prototype/`<br>• `test_cases.json`, `walkthrough_04.json` ve `store.json` iskeletleri<br>• `group_04.json` (collaborator'ınız)<br>• `ai_log_04.md` | • `week04/prototype/` (en az beş ekran)<br>• `test_cases.json` (her must)<br>• `walkthrough_04.json` (birinci tur)<br>• `group_04.json` | • tam ekran akışı (en az yedi ekran)<br>• ikinci tur; güncellenmiş `requirements.json` ve `test_cases.json`<br>• `week04/store.json` S1<br>• `ai_log_04.md` |
| 5 | • `week05/ASSIGNMENT_05`<br>• `DESIGN.md` ve `api.md` iskeletleri<br>• sunucu başlangıcı<br>• `ai_log_05.md` | • `week05/DESIGN.md`, ilk sürüm<br>• `api.md`'nin giriş satırları<br>• sunucu iskeleti | • `week05/api.md`<br>• TC id'siyle adlandırılmış giriş testleri<br>• `ai_log_05.md` |
| 6 | • `week06/ASSIGNMENT_06`<br>• `server/course_login.py`, `course_tests/` ve `server/login_contract.json`<br>• `group_06.json`<br>• `ai_log_06.md` | • `server/login_contract.json`; giriş bağlanmış<br>• kendi işlevsel `must` gereksinimlerinizden biri: route'ları, testleri, `web/` içindeki sayfası<br>• `group_06.json` | • uçtan uca her işlevsel `must` gereksinim: route'lar, testler, sayfalar<br>• LOGIN_07–10 ders testleri GitHub'da yeşil<br>• gerçek e-postayla kod, `.env.example`, `email_code.png`<br>• `group_06.json`: her bulgu için `accepted` ve `why`<br>• `store.json` S2<br>• `test_cases.json` içinde `"run"`<br>• `ai_log_06.md` |
| 7 | • `week07/ASSIGNMENT_07`<br>• `group_07.json`<br>• `ai_log_07.md` | • mobil istemcide giriş ve kendi özelliğinizin bir ekranı<br>• `group_07.json` | • mobil istemcide her işlevsel `must` gereksinim<br>• mobil test koşuları kayıtlı<br>• testler GitHub Actions'ta yeşil<br>• `ai_log_07.md` |
| 8 | • `week08/ASSIGNMENT_08`<br>• `ai_log_08.md` | • sohbet botu: `POST /chat` ve mobil istemcinin sohbet ekranı<br>• change request satırı | • kendi özelliğiniz üç istemcide tamamlanmış<br>• `store.json` S3 (ilk build, kanal, kayıtlı testçiler)<br>• `ai_log_08.md` |
| 9 | • `week09/ASSIGNMENT_09`<br>• test raporu iskeleti<br>• `group_09.json`<br>• `ai_log_09.md` | • 8. haftada kaydedilen testçilerle beta testi<br>• hata listesi | • düzeltmeler<br>• test raporu<br>• sohbet botunun testleri ve Report düğmesi<br>• `store.json` S4<br>• `ai_log_09.md` |
| 10 | • `week10/ASSIGNMENT_10`<br>• UAT raporu iskeleti<br>• `group_10.json`<br>• `ai_log_10.md` | • UAT bulguları<br>• `group_10.json` | • UAT raporu<br>• dağıtım diyagramı<br>• `store.json` S5<br>• `ai_log_10.md` |
| 11 | • `week11/ASSIGNMENT_11`<br>• son README iskeleti<br>• `group_11.json`<br>• `ai_log_11.md` | • inceleme düzeltmeleri<br>• `group_11.json` | • `store.json` S6 (mağaza URL'si + web URL'si)<br>• son README<br>• `ai_log_11.md` |
| 12 | • `week12/ASSIGNMENT_12`<br>• poster şartnamesi<br>• `group_12.json`<br>• `ai_log_12.md` | • poster taslağı<br>• `group_12.json` | • son poster<br>• `ai_log_12.md`<br>• mağaza kurulumundan savunma |

## Değişiklik günlüğü

- 21 Eyl 2026 — v2, gösterilen ilk sürüm.
- 26 Eyl 2026 — dönem notu syllabus'a göre (60 · 15 · 15 · 40, final sınavı); savunma 13–14. haftaya taşındı.
- 26 Eyl 2026 — mağaza seçimi öğrencinin (dört mağazadan biri; native ya da hybrid), kökte Platforms and Stores el kitabı (`AI_PLATFORMS_AND_STORES_EN/TR.md`); 1. hafta okumaları kökte `AI_Doc1–4`; `GRADING.md` atfı yerine öğrenci iş akışı.
- 4 Eki 2026 — 3. hafta satırı ve katkıcı kuralı güncellendi (pitch, dörtlü gruplar, gereksinim id'leri kalıcı, taban çizgisi 5. hafta sonunda).
- 4 Eki 2026 — 4. ve 5. haftalar yeniden yazıldı: 4. hafta, kabul ölçütlerinden yazılan ve grubun yürüttüğü test case'lerle tıklanabilir prototiptir; 5. hafta tasarım, API sözleşmesi, sunucu iskeleti ve giriştir, sonunda gereksinimler ve test case'ler taban çizgisi olur. `store.json` dosyası `week04/` içinde durur.
- 5 Eki 2026 — 3. hafta: proje dersin sonunda (11:45) kesinleşir (ayrıntılar Change log'a bir satırla değişmeye devam edebilir); ana akışın ekranları derste `week03/screens_03.md` dosyasına yazılır; geliştirici hesabı (S1) 3. haftada da açılabilir; her üye aynı grup listesini `week03/group_03.json` dosyasına yazar.
- 6 Eki 2026 — 4. haftadan itibaren grup ve katkıları tek dosyadadır: `weekNN/group_NN.json` (diğer her üye için bir kayıt); `contributors_NN.json` yalnızca 2–3. haftalarda kalır. 9. hafta testçileri test raporunda listelenir.
- 18 Eki 2026 — Sohbet botu dersten çıkarıldı. 5. hafta ikiye bölündü: 5. hafta tasarım, API sözleşmesi, sunucu iskeleti ve giriş testleridir; 6. hafta sunucuda ve web istemcisinde e-posta koduyla giriştir (S2); 7. hafta giriş, testler ve CI ile mobil istemcidir. 5. haftada grup çalışması ve katkı bonusu yoktur.
- 20 Eki 2026 — Sohbet botu API üzerinden geri geldi: 8. haftada mobil istemci öğrencinin kendi sunucusuyla konuşur, öğrencinin seçtiği barındırılan LLM API'sini yalnızca sunucu çağırır (anahtar yalnızca sunucunun `.env` dosyasında). Gereksinimlere bir change request ile girer; projenin çekirdek özelliği Cumartesi'ye kadar tamamlanır.
- 22 Eki 2026 — 6. hafta yazıldı: giriş her projede aynı biçimde çalışır (10 dakika ve bir kez geçerli 4 haneli kod, bir dakika içinde yeni koda 429, yanlış koda 401, üç yanlış koddan sonra 15 dakikalık kilit) ve `server/login_contract.json` üzerinden on ders testiyle kontrol edilir; ders notu GitHub Actions çalıştırmasını okur; web giriş sayfası prototipinkidir ve sunucu tarafından sunulur; bir grup arkadaşı girişe saldırır (rol: attacker); Cumartesi'ye kadar kod gerçek e-postayla gelir ve her test case nasıl çalıştırıldığını söyler; S2.
- 22 Eki 2026 (akşam) — 6. hafta öğrencinin kendi özelliği etrafında yeniden yazıldı: giriş, dersin modülü `server/course_login.py` olarak hazır gelir (aynı kurallar; elle yazılan `server/login_contract.json` ile bağlanır, on ders testiyle kontrol edilir) ve hafta, öğrencinin kendi işlevsel `must` gereksinimlerinin her biri tek bir zincir olarak uçtan uca kurulmasıdır (gereksinim → kullanım senaryosu → ekran → test case → `api.md` satırı → çalışan route → GitHub Actions'ta yeşil test → web sayfası; kaynak `requirements.json` dosyasıdır); saldırgan turu öğrencinin özelliğine yönelir. 7. hafta giriş ve özelliği telefona taşır; 8. hafta özelliği sohbet botunun yanında üç istemcide tamamlar.
- 24 Eki 2026 — Plan düzeltmesi: testçiler S3'te, 8. haftada test kanalına kaydedilir (yeni bir kişisel Google Play hesabı için 12 ya da daha fazla; böylece 14 gün 10. haftadaki gönderimden önce biter); 9. hafta beta testini onlarla yürütür. Ayrıca: giriş, e-postayla gönderilen 4 haneli koddur (OTP seçeneği yok); gereksinimler yalnızca `requirements.json` içindedir, SRS use case'leri ve use case diyagramını tutar; change request'ler, 5. haftadan sonraki Pazar gününden itibaren `CR-` satırlarıdır; `group_NN.json`, haftanın ödevinin adını verdiği kişileri haftanın rolüyle tutar (grup, ödevin adını verdiği haftalarda toplanır); 6. hafta Cumartesi'ye kadar LOGIN_07–10'u ve saldırganların bulguları üzerine kararları da ister; `AI_Doc5` İngilizce ve Türkçedir. Aynı gün daha sonra (VC): hata denetimi yok; 8. haftadan itibaren sunucu verilerini yeniden başlatmadan sonra da korur (bir dosyada ya da öğrencinin seçtiği bir veritabanında); 2. haftada paydaşlar isteğe bağlıdır (0–2).
- 13 Kas 2026 — 9–15 Kasım'da ders yok: 8–13. haftalar bir hafta sonraya kaydı (8. hafta 17/18 Kasım), savunma 13. haftada (22–23 Aralık); ders 23 Aralık'ta biter.
- 14 Kas 2026 — EN şubesinde savunma 13. ve 14. haftalara yayıldı (22 ve 29 Aralık). Uygulaması 22 Aralık'ta ders başlamadan önce mağazada yayında ve indirilebilir olan EN öğrencileri o gün sunar. Sunumun kendisi 12 üzerinden notlanır; uygulaması mağazada yayında olan ve 13. haftada sunan öğrenci kalan 3 puanı da alır (en yüksek not 15), 14. haftada sunan öğrenci en fazla 12 alabilir.
- 14 Kas 2026 — Sunumun kalan 3 puanı için uygulamanın 5 Aralık Cumartesi 23:59'a kadar mağazanın incelemesine gönderilmiş olması da gerekiyor (S5). Mağazanın inceleme süresi öğrencinin sorumluluğunda.
- 14 Kas 2026 — 8. hafta hafifledi: sohbet botunun sahte modelle testleri ve cevaplarındaki Report düğmesi 9. haftaya kaydı; 8. haftada grup dosyası yok. Gizlilik metni herkese açık bir sayfada da yayınlanır, çünkü Google Play bir web adresi istiyor.
