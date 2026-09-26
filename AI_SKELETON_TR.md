# AIASD — Dönem Bir Bakışta

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027 · Prof. Dr. Vedat Coşkun**

*English: [`AI_SKELETON_EN.md`](AI_SKELETON_EN.md)*

Bu, dönemin tamamı iki sayfada: her hafta ne öğretilir, sınıfta ne yaparsınız, Cumartesi'ye
kadar neyi bitirirsiniz ve deponuza ne gelir. İlk derste gösterilir ve deponuzda yaşar. Dönem
içinde değişebilir; her değişiklik, kendi teklifinizdeki değişiklikleri kaydettiğiniz gibi bu
dosyanın sonunda kaydedilir.

## Her hafta geçerli olanlar

- **Tek bir projeyi, yalnız, dönem boyunca** yaparsınız: bir mobil istemci, bir web istemcisi
  ve bir sunucu; e-posta kodu ve/veya OTP ile giriş; dönem sonunda **bir public mağazada
  yayınlanmış** — hangi mağaza, native mi hybrid mi, sizin seçiminiz (`docs/Week02_Doc5`).
  12. Hafta'daki savunma mağazadan yüklenmiş uygulamadan yapılır.
- **Projeniz kendisi hakkında bir sohbet botu içerir**; 6–7. Haftalarda, kendi çalıştırdığınız
  açık ağırlıklı modellerle — gömme için BGE-M3, yanıt için Ollama üzerinden Qwen — kendi
  belgeleriniz ve verileriniz üzerinde, iki istemciden de erişilebilir. Bu özellik için bulut
  model API'si yok.
- **Haftada 10 puan**: 5'i dersin sonunda, 5'i Cumartesi 23:59'da deponuzdan okunur. 1. Hafta
  5 puan, tamamı Cumartesi. Final projesi: 30.
- **Her hafta iki kişi size yardım eder**, 2. Hafta'dan itibaren, o haftanın adlandırdığı rolde;
  onları `weekNN/contributors_NN.json` içine kaydedersiniz. Sizin notunuzdan bonus kazanırlar;
  siz onlarınkinden. Dönüşümlü: her hafta en az bir yeni isim.
- **İnsan işini kanıtlarsınız**: sizinkini `weekNN/ai_log_NN.md` içinde, onlarınkini adlarının
  yanında. Cumartesi puanlarının ikisi bu kanıta bağlıdır.
- **`PROPOSAL.md` kökte yaşar** ve herhangi bir haftada değişebilir — değişiklik günlüğüne
  tarihli bir satırla. Sessiz değişiklik puana mal olur; kaydedilmiş değişiklik mühendisliktir.
- **Yayınlama adım adım notlandırılır** (plandaki S0–S6), her adım kendi haftasında. Mağazayla
  ilgili hiçbir şey son haftada yapılamaz.
- **Her diyagram Mermaid'dir**, markdown dosyasının içinde. GitHub çizer; denetleyici okur.

Puanların nasıl hesaplandığı, denetleyicinin neye baktığı ve bonusun ayrıntıları
`AI_WEEKLY_WORKFLOW_STUDENT_TR.md` / `_EN.md` içindedir.

## Haftalık plan

### Her hafta ne olur

| Hafta | İçerik | Sınıfta | Ders sonrası | Notlar |
|---|---|---|---|---|
| 1 | Derse giriş; araçlar; Git; LLM'lerle ilk temas | • Ödev adım adım anlatılır<br>• henüz bir şey yapılmaz | Araçları kur, şablondan private depoyu oluştur, Collaborator ekle, student.json'ı doldur, hello.py yaz, iki LLM'i keşfet | • 5 puan, tamamı Cumartesi (3 otomatik · 1 commit · 1 AI günlüğü)<br>• Bu hafta katkıcı yok |
| 2 | Teklif Bölüm A + Gereksinimler (SRS) | • Problemi ve çözümü yaz<br>• iki paydaşla görüş<br>• gereksinim listesine başla | • Teklif Bölüm A'yı bitir<br>• SRS'yi diyagramlarıyla yaz | • Teklif kökte yaşar, her hafta değişiklik günlüğü satırıyla revize edilebilir<br>• Rol: stakeholder |
| 3 | Tasarım + Teklif Bölüm B | • Mimari<br>• pazar ve rakipler<br>• tasarım iki kişi tarafından gözden geçirilir | • Diyagramları ve veri modeliyle tasarım belgesi<br>• ticari potansiyel<br>• mağaza seçimi dahil teknik riskler | • S0: teklif §12 mağazayı, ücreti, süreyi adlandırır<br>• Rol: design-reviewer |
| 4 | Tıklanabilir prototip | • Ana akışı kur<br>• iki testçi dolaşır | • Ekran akışını tamamla<br>• geliştirici hesabını aç | • S1: bugün kaydol, doğrulama günler sürer<br>• Rol: prototype-tester |
| 5 | Prototip revizyonu; geliştirme başlar | • Geri bildirimle prototipi revize et<br>• sunucu iskeleti yerelde çalışır | E-posta kodu / OTP ile giriş uçtan uca çalışır | Rol: prototype-tester (revizyon) |
| 6 | Sohbet botu I — motor | • Ollama + Qwen çalışıyor<br>• projenin kendi belgeleri üzerinde BGE-M3 gömmeleri<br>• sunucudaki bir chat endpoint'i proje hakkında bir soruyu yanıtlar | • Getirme ayarlanmış (chunking, top-k)<br>• model notları: denenen modeller, yanlış yaptıkları<br>• mağazada uygulama kaydını oluştur | • S2: uygulama kaydı / bundle id<br>• Rol: code-reviewer |
| 7 | Sohbet botu II — istemcilerde | Web istemcisinde sunucuyla konuşan sohbet ekranı | • Mobil istemcide sohbet ekranı<br>• testler<br>• CI | • İlk özellik üç katmanda da canlı<br>• Rol: chat-tester |
| 8 | Geliştirme — projenin kendi özelliği | Projenin çekirdek özelliği üç istemcide | • Özellik tamam<br>• ilk build'i test kanalına yükle | • S3 mağazanın zorunlu test süresini başlatır<br>• Rol: test-user |
| 9 | Beta testi | • Kanala testçi kaydet<br>• hata listesini aç | • Hataları düzelt<br>• test raporunu yaz | • Beta testçileri mağazanın testçileriyle eşleşmeli<br>• Rol: beta-tester |
| 10 | UAT + gönderim | Katılımcılarla UAT oturumunu yürüt | • UAT raporu<br>• dağıtım diyagramı<br>• incelemeye gönder | • S5, ret ve yeniden gönderim için bir hafta bırakır<br>• Rol: uat-participant |
| 11 | Yayın + sağlamlaştırma | • İnceleme düzeltmelerini uygula<br>• release-tester mağazadan yükler | • Canlıya çık<br>• son README | • S6: canlı<br>• Rol: release-tester |
| 12 | Kapanış | • Poster taslağı gözden geçirilir<br>• savunma provası | Son poster | • Savunma (final 30) mağaza kurulumundan yapılır<br>• Rol: poster-reviewer |

### Dosya akışı — öğrencinin aldığı ve push ettiği

Ödevler `_EN` ve `_TR` olarak gelir; aşağıda ek atlanmıştır. `docs/` altındaki okumalar İngilizcedir. Ders sunumu depoda bir dosya değildir.

| Hafta | Verilen (`weekNN/` ya da köke gelir) | Ders sonuna kadar push (5) | Cumartesi'ye kadar push (5) |
|---|---|---|---|
| 1 | • `docs/` Doc 1–4 ön okuma<br>• `week01/ASSIGNMENT_01`<br>• iskeletler `llm_notes.md`, `ai_log_01.md`<br>• kök: `student.json`, `README`, `AI_SETUP_CARD`, `AI_WEEKLY_WORKFLOW_STUDENT` | — | • `student.json`<br>• `week01/setup_proof.md`<br>• `hello.py`<br>• `llm_notes.md`<br>• `ai_log_01.md` (5 puanın tamamı) |
| 2 | • `week02/ASSIGNMENT_02`<br>• kök `PROPOSAL.md` iskeleti<br>• `week02/SRS.md` iskeleti<br>• `requirements.json` iskeleti<br>• `contributors_02.json`<br>• `ai_log_02.md`<br>• `docs/` Ref1/Ref2 SDLC referansları, Doc 5 Platforms and Stores | • `PROPOSAL.md` §1–§4<br>• `week02/requirements.json` ilk liste<br>• `contributors_02.json` | • `PROPOSAL.md` §5–§7<br>• `week02/SRS.md` + diyagramlar<br>• `requirements.json` son hâli<br>• `ai_log_02.md` |
| 3 | • `week03/ASSIGNMENT_03`<br>• `DESIGN.md` iskeleti<br>• `contributors_03.json`<br>• `ai_log_03.md` | • `week03/DESIGN.md` mimari + diyagram<br>• `PROPOSAL.md` §8–§10<br>• `contributors_03.json` | • `week03/DESIGN.md` diyagramlar + veri modeli<br>• `PROPOSAL.md` §11–§12 + değişiklik günlüğü<br>• `ai_log_03.md` |
| 4 | • `week04/ASSIGNMENT_04`<br>• `store/store.json` iskeleti<br>• `contributors_04.json`<br>• `ai_log_04.md` | • prototip bağlantısı/dosyası<br>• `contributors_04.json` | • tam ekran akışı<br>• testçi geri bildirim günlüğü<br>• `week04/store/store.json` S1<br>• `ai_log_04.md` |
| 5 | • `week05/ASSIGNMENT_05`<br>• `contributors_05.json`<br>• `ai_log_05.md` | • revize prototip<br>• sunucu iskeleti<br>• `contributors_05.json` | • giriş çalışıyor<br>• revizyon günlüğü<br>• `ai_log_05.md` |
| 6 | • `week06/ASSIGNMENT_06`<br>• `week06/requirements.txt` (Ollama istemcisi, sentence-transformers)<br>• `embedder.py`/`chat` iskeletleri<br>• `model_notes.md` iskeleti<br>• `contributors_06.json`<br>• `ai_log_06.md` | • `embedder.py`<br>• bir soruyu yanıtlayan `chat` endpoint'i<br>• `contributors_06.json` | • tüm proje belgeleri üzerinde getirme<br>• `week06/model_notes.md`<br>• `store.json` S2<br>• `ai_log_06.md` |
| 7 | • `week07/ASSIGNMENT_07`<br>• test + CI iskeleti<br>• `contributors_07.json`<br>• `ai_log_07.md` | • web istemcisinde sohbet ekranı<br>• `contributors_07.json` | • mobil istemcide sohbet ekranı<br>• testler + CI yeşil<br>• `ai_log_07.md` |
| 8 | • `week08/ASSIGNMENT_08`<br>• `contributors_08.json`<br>• `ai_log_08.md` | • çekirdek özellik üç istemcide<br>• `contributors_08.json` | • özellik tamam<br>• `store.json` S3 (ilk build, kanal)<br>• `ai_log_08.md` |
| 9 | • `week09/ASSIGNMENT_09`<br>• test raporu iskeleti<br>• `contributors_09.json`<br>• `ai_log_09.md` | • testçiler kayıtlı (= `contributors_09.json`)<br>• hata listesi | • düzeltmeler<br>• test raporu<br>• `store.json` S4<br>• `ai_log_09.md` |
| 10 | • `week10/ASSIGNMENT_10`<br>• UAT raporu iskeleti<br>• `contributors_10.json`<br>• `ai_log_10.md` | • UAT bulguları<br>• `contributors_10.json` | • UAT raporu<br>• dağıtım diyagramı<br>• `store.json` S5<br>• `ai_log_10.md` |
| 11 | • `week11/ASSIGNMENT_11`<br>• son README iskeleti<br>• `contributors_11.json`<br>• `ai_log_11.md` | • inceleme düzeltmeleri<br>• `contributors_11.json` | • `store.json` S6 (mağaza URL'si + web URL'si)<br>• son README<br>• `ai_log_11.md` |
| 12 | • `week12/ASSIGNMENT_12`<br>• poster şartnamesi<br>• `contributors_12.json`<br>• `ai_log_12.md` | • poster taslağı<br>• `contributors_12.json` | • son poster<br>• `ai_log_12.md`<br>• mağaza kurulumundan savunma |

## Değişiklik günlüğü

- 21 Eyl 2026 — v2, gösterilen ilk sürüm.
- 26 Eyl 2026 — mağaza seçimi öğrencinin (dört mağazadan biri; native ya da hybrid), 2. Hafta'ya Doc 5 eklendi; 1. Hafta okumaları `docs/` altında; `GRADING.md` atfı yerine öğrenci iş akışı.
