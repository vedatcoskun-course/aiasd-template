# Ders İzlencesi

**Yazılım Mühendisliği Bölümü · Atlas Üniversitesi** · sürüm 1 · 2026-09-21

*English: [`AI_Syllabus_EN.md`](AI_Syllabus_EN.md)*

| | |
|---|---|
| **Ders Kodu** | 1413002043 |
| **Ders Adı** | AI – Assisted Software Development (Yapay Zekâ Destekli Yazılım Geliştirme) |
| **Yıl ve Dönem** | 2026 – 2027 Güz |
| **Öğretim Üyesi** | Prof. Dr. Vedat COŞKUN |

## Dersin Tanımı

Öğrenciler yapay zekâyı yazılım geliştirme yaşam döngüsü boyunca disiplinli bir mühendislik aracı olarak kullanır. Her öğrenci dönem boyunca tek başına tek bir ürün geliştirir — e-posta kodu/OTP ile giriş yapılan bir mobil istemci, bir web istemcisi ve bir sunucu, artı açık ağırlıklı modellerle çalışan ve projenin kendisi hakkında konuşan bir sohbet botu — ve bunu bir public uygulama mağazasında yayınlar (Google Play, Huawei AppGallery, Samsung Galaxy Store ya da Apple App Store; native ya da hybrid, öğrencinin seçimi).

Ders, üretimi değil değerlendirmeyi notlandırır: asistanın ne ürettiğini değil, öğrencinin onu ne kadar iyi tanımladığını, denetlediğini, düzelttiğini ve hesabını verdiğini. Her haftanın işi, ders şablonundan oluşturulan öğrencinin kendi GitHub reposuna push edilir ve her push'ta otomatik olarak denetlenir.

## Dersin Hedefleri

Dersi tamamlayan öğrenci:

- gerçek bir ürün için gereksinim, tasarım ve test belgelerini yazar ve ürün değiştikçe bunları tutarlı tutar (repoda Mermaid diyagramları);
- yapay zekâ asistanlarını (Claude, Gemini, ChatGPT, Copilot, Ollama) verimli ve eleştirel kullanır — istem yazar, doğrular, düzeltir ve hataları kanıtlı bir haftalık yapay zekâ günlüğünde belgeler;
- açık ağırlıklı modeller (Ollama/Qwen, BGE-M3) üzerinde, projenin kendi belgeleri üzerinden çalışan bir getirme destekli sohbet botu kurar ve çalıştırır;
- Git/GitHub ile her gün çalışır: küçük commit'ler, CI kontrolleri, kod kalitesi (ruff), gizli anahtarların repo dışında tutulması;
- bir uygulamayı mağaza yayın izinden geçirir — geliştirici hesabı, test kanalı, testçiler, inceleme, yayın — ve teslim edilen ürünü sözlü olarak savunur.

## Ders Materyali

Ders şablonu ve haftalık ödevler: github.com/vedatcoskun-course/aiasd-template (her haftanın `ASSIGNMENT_NN` dosyası İngilizce ve Türkçe; kökte `AI_SETUP_CARD`, `AI_WEEKLY_WORKFLOW_STUDENT` ve `AI_SKELETON`).

Ön okuma, 1. Hafta: Vaswani vd., "Attention Is All You Need" (2017); AI Technical Background; Development Environment and Tools; Working with AI Tools. 2. Hafta: iki tam SDLC belge seti (sınav salonu tahsisi; simülatörlü asansör denetleyicisi); Platforms and Stores el kitabı.

Araçlar: Python 3.12, Git/GitHub, VS Code, Streamlit, açık ağırlıklı bir modelle Ollama, öğrencinin seçtiği iki sohbet asistanı (ücretsiz katman), bir mobil çatı (Flutter / React Native–Expo / Kotlin / Swift). Öğrenciler her hafta kendi dizüstü bilgisayarlarını getirir.

## Notlandırma

| Kalem | Puan | Açıklama |
|---|---|---|
| Haftalık Projeler | 60 | 12 hafta × 10 puan, 60'a ölçeklenir. Her hafta: 5 puan dersin sonunda, 5 puan Cumartesi 23:59'da repodan okunur (1. Hafta: 5 puan, tamamı Cumartesi). Otomatik kontroller artı öğretim üyesinin yapay zekâ günlüğü ve commit disiplini puanları. Kaçırılan ders için telafi yoktur. |
| Mağaza Bonusu | 15 | Yayın bonusu: mağaza izi S0–S6 (mağaza seçimi, geliştirici hesabı, uygulama kaydı, test kanalı build'i, testçiler, gönderim, canlı) her adımın teslim haftasında adım adım notlandırılır; her hafta yardım eden sınıf arkadaşları (katkıcılar) öğrencinin notundan pay kazanır. |
| Sunum | 15 | 13–14. Haftalarda proje savunması: öğrenci, uygulamayı sınav yapanın önünde mağazadan yükler ve koddaki ve belgelerdeki kararlar hakkında soruları yanıtlar. Geliştirme makinesinden değil, mağaza build'inden çalıştırılır. |
| Final Sınavı | 40 | Üniversitenin sınav döneminde yazılı final sınavı; SDLC belgelerini, yapay zekâ günlüğü pratiğini ve on iki haftanın teknik içeriğini kapsar. |

## Sınıf İçi Kurallar

- En az %70 devam zorunludur. Tüm mazeretler kalan %30'luk hak içinde karşılanmalıdır. Acil durumlar için kendinize esneklik bırakmak üzere başından itibaren tüm derslere katılmaya çalışın.
- Ders sırasında konuşmaları en aza indirin. Uzun ya da dersi bozan tartışmalara izin verilmez. İhlal edenlerden yer değiştirmeleri ya da salondan ayrılmaları istenir.
- Ders sırasında telefon görüşmesi, kısa mesaj, anlık mesaj, e-posta ve genel web gezintisine izin verilmez. Bilgisayarlar yalnızca ders materyalini izlemek için kullanılabilir.
- Ders sırasında ses ya da görüntü kaydı kesinlikle yasaktır.
- Her türlü kopya ve akademik sahtekârlık, ilgili yasal kurallara göre işlem görür.

## Ders Planı

| Hafta | Tarih | Konu |
|---|---|---|
| 1 | 22/09 · 23/09 | Temeller — araçlar, Git/GitHub, LLM'ler ve transformer'larla ilk temas |
| 2 | 29/09 · 30/09 | Teklif Bölüm A + Gereksinimler (SRS) — problem, çözüm, paydaşlar, kullanım senaryoları |
| 3 | 06/10 · 07/10 | Tasarım + Teklif Bölüm B — mimari, veri modeli, pazar, riskler; mağaza seçildi (S0) |
| 4 | 13/10 · 14/10 | Tıklanabilir prototip; geliştirici hesabı açıldı (S1) |
| 5 | 20/10 · 21/10 | Prototip revizyonu; geliştirme başlar — sunucu iskeleti, e-posta kodu / OTP ile giriş |
| 6 | 27/10 · 28/10 | Sohbet botu I — motor: Ollama + Qwen, BGE-M3 gömmeleri, chat endpoint'i; uygulama kaydı (S2) |
| 7 | 03/11 · 04/11 | Sohbet botu II — web ve mobil istemcilerde; testler; CI |
| 8 | 10/11 · 11/11 | Projenin kendi çekirdek özelliği üç katmanda; test kanalında ilk build (S3) |
| 9 | 17/11 · 18/11 | Beta testi — testçiler kayıtlı, hata listesi, test raporu (S4) |
| 10 | 24/11 · 25/11 | UAT ve gönderim — UAT raporu, dağıtım diyagramı, incelemeye gönderildi (S5) |
| 11 | 01/12 · 02/12 | Yayın ve sağlamlaştırma — inceleme düzeltmeleri, mağazada canlı, son README (S6) |
| 12 | 08/12 · 09/12 | Kapanış — poster, savunma provası |
| 13 | 15/12 · 16/12 | **Proje savunması (sunumlar)** |
| 14 | 22/12 · 23/12 | **Proje savunması (sunumlar)** |
| | | **Final Sınavı** |

*Not: haftalık plan sınıfın ilerlemesine göre değiştirilebilir.*
