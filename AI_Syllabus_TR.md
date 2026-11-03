# Ders İzlencesi

**Yazılım Mühendisliği Bölümü · Atlas Üniversitesi** · sürüm 2 · 2026-10-24

*English: [`AI_Syllabus_EN.md`](AI_Syllabus_EN.md)*

| | |
|---|---|
| **Ders Kodu** | 1413002043 |
| **Ders Adı** | AI – Assisted Software Development (Yapay Zeka Destekli Yazılım Geliştirme) |
| **Yıl ve Dönem** | 2026 – 2027 Güz |
| **Öğretim Üyesi** | Prof. Dr. Vedat COŞKUN |

## Dersin Tanımı

Öğrenciler yapay zekayı yazılım geliştirme yaşam döngüsü boyunca disiplinli bir mühendislik aracı olarak kullanır. Her öğrenci dönem boyunca tek başına tek bir ürün geliştirir. Ürün bir mobil istemci, bir web istemcisi ve bir sunucudan oluşur; kullanıcılar e-postayla gönderilen 4 haneli bir kodla giriş yapar (dersin giriş modülü, her projede aynı). Öğrenci ürünü public bir uygulama mağazasında yayınlar: Google Play, Huawei AppGallery, Samsung Galaxy Store ya da Apple App Store. Uygulama native (platformun kendi dilinde yazılmış) ya da hybrid (bir kez yazılıp iki platform için derlenen) olabilir; bu seçim öğrencinindir.

Ders, üretimi değil değerlendirmeyi notlandırır: asistanın ne ürettiğini değil, öğrencinin onu ne kadar iyi tanımladığını, denetlediğini, düzelttiğini ve hesabını verdiğini notlar. Her haftanın işi, öğrencinin ders şablonundan (GitHub'ın öğrenci için kopyaladığı hazır bir repo) oluşturduğu kendi GitHub reposuna push edilir ve her push'ta otomatik olarak denetlenir.

## Dersin Hedefleri

Dersi tamamlayan öğrenci:

1. **Proje teklifi hazırlar.** Öğrenci kendi yaşadığı gerçek bir problemden yola çıkar ve Bölüm A'yı yazar: problem ve çözüm, paydaşlar ve kullanım senaryoları. Bölüm B pazarı ve rakipleri inceler, ticari potansiyeli değerlendirir ve teknik riskleri sıralar. Öğrenci teklifi beş dakikada pitch eder (2–3. hafta).
2. **Gereksinim mühendisliği yapar.** Öğrenci fonksiyonel ve fonksiyonel olmayan gereksinimleri tek bir yerde, `week02/requirements.json` dosyasında tutar ve use case'leri ve use case diyagramını içeren bir SRS (Software Requirements Specification) yazar. Her gereksinim REQ-NNN biçiminde bir kimlik taşır, izlenebilirdir ve verildikten sonra anlamını korur. Gereksinimler ve test case'ler 5. haftanın sonunda taban çizgisine (baseline) girer; ondan sonra her değişiklik bir change request'tir (`PROPOSAL.md` Change log'unda bir `CR-` satırı). Kabul ölçütlerinden test case'ler yazılır ve prototip üzerinde yürütülür (2–5. hafta).
3. **Tasarlar ve prototipler.** Öğrenci repoda Mermaid ile (GitHub'ın markdown dosyasının içinde çizdiği, metin tabanlı bir diyagram gösterimi) dört diyagram çizer: sistem bağlam diyagramı ve use case diyagramı (2. hafta), mimari (5. hafta) ve dağıtım diyagramı (10. hafta). Öğrenci ayrıca tıklanabilir bir prototip kurar ve onu akran incelemesinden sonra revize eder (4. hafta).
4. **Full-stack uygulama geliştirir.** Öğrenci e-postayla gönderilen 4 haneli bir kodla giriş yapılan (6. haftadan itibaren dersin giriş modülü) bir sunucu, bir web istemcisi ve bir mobil istemci geliştirir; aynı özellik üç katmanda birden çalışır. Ürüne bir sohbet botu da eklenir: mobil istemci öğrencinin kendi sunucusuyla konuşur, barındırılan bir LLM API'sini (web hizmeti olarak sunulan bir büyük dil modeli) yalnızca sunucu çağırır ve anahtar sunucuda kalır (5–8. hafta).
5. **Mobil uygulama geliştirir.** Öğrenci mobil istemciyi Flutter, React Native–Expo, Kotlin ya da Swift ile geliştirir; istemci telefonda çalışır ve mağazaya hazırdır (7–8. hafta).
6. **Yapay zeka asistanlarını mühendislik aracı olarak kullanır.** Öğrenci asistana istem yazar, çıktısını doğrular ve düzeltir, hatalarını kanıtla haftalık yapay zeka günlüğünde belgeler ve asistanı kendi işinin düşman gözden geçireni olarak kullanır. Ders üretileni değil değerlendirmeyi notlar (her hafta).
7. **Sürüm kontrolü ve sürekli entegrasyon uygular.** Öğrenci küçük adımlarla commit ve push yapar, GitHub'da otomatik kontrollerin çalışmasını sağlar, kod kalitesini ruff ile (Python kodundaki stil ve hata sorunlarını bildiren bir araç) korur ve parola gibi gizli anahtarları repo dışında tutar (her hafta: CI, yani sürekli entegrasyon, 1. haftadan itibaren her push'ta çalışır; testler 6. haftadan itibaren CI'da çalışır).
8. **Formal test süreçleri yürütür.** Öğrenci birim ve entegrasyon testleri yazar, kayıtlı testçilerle beta test yapar, hata listesi tutar, test raporu yazar ve gerçek kullanıcılarla Kullanıcı Kabul Testi (gerçek kullanıcıların ürünü deneyip ihtiyaçlarını karşılayıp karşılamadığını söylediği bir oturum) yürütür (5–7. ve 9–10. hafta).
9. **Uygulamayı mağazada yayınlar.** Öğrenci S0–S6 izini izler (3–11. hafta): mağazayı seçer (S0), geliştirici hesabı açar (S1), uygulama kaydını oluşturur (S2), bir build yükler ve testçileri kaydeder (S3), beta testini test kanalında yürütür (S4), uygulamayı incelemeye gönderir (S5), inceleme düzeltmelerini uygular ve uygulamayı yayınlar (S6).
10. **İnceler ve iş birliği yapar.** Öğrenci sabit dörtlü grupta, ödevin adını verdiği haftalarda incelemelere katılır, geri bildirimi alıntı olarak, kabul/ret kararı ve gerekçesiyle kaydeder ve sınıf arkadaşlarının işine paydaş, gözden geçiren ya da testçi olarak katkı verir (3. haftadan).
11. **Ürünü savunur.** Öğrenci uygulamayı sınav görevlisinin önünde mağazadan kurar, koddaki ve belgelerdeki kararları gerekçelendirir ve poster ile sunum hazırlar (12–14. hafta).

## Ders Materyali

Ders şablonu ve haftalık ödevler github.com/vedatcoskun-course/aiasd-template adresindedir. Her haftanın `ASSIGNMENT_NN` dosyası orada İngilizce ve Türkçe olarak bulunur; `AI_SETUP_CARD`, `AI_WEEKLY_WORKFLOW_STUDENT` ve `AI_SKELETON` köktedir.

1. haftanın ön okuması Vaswani vd., "Attention Is All You Need" (2017) makalesi ve İngilizce üç ders belgesidir: AI Technical Background; Development Environment and Tools; ve Working with AI Tools. Dördüncü ders belgesi Yazılım Geliştirmede Yapay Zekayı Doğru Kullanmak (`AI_Doc5`), 3. hafta ile İngilizce ve Türkçe olarak gelir. Haftalık yapay zeka günlüğünün istediği sekiz tekniği anlatır (4. haftadan itibaren her hafta bir teknik zorunludur) ve sınav kapsamındadır. 2. hafta için öğrenciler iki tam SDLC belge seti (bir sınav salonu tahsis sistemi; simülatörlü bir asansör denetleyicisi) ile Platforms and Stores el kitabını okur.

Araçlar: Python 3.12, Git/GitHub, VS Code, sunucu için FastAPI, web istemcisi için HTML/CSS/JavaScript, öğrencinin seçtiği iki sohbet asistanı (ücretsiz katman), ürünün sohbet botu için öğrencinin seçtiği bir LLM API'si ve bir mobil çatı (Flutter / React Native–Expo / Kotlin / Swift). Öğrenciler her hafta kendi dizüstü bilgisayarlarını getirir.

## Notlandırma

| Kalem | Puan | Açıklama |
|---|---|---|
| Haftalık Projeler | 45 | 12 hafta × 10 puan, 45'e ölçeklenir (1. hafta 5 puandır ve tamamı Cumartesi okunur). Her hafta:<br>• **Ders, 5 puan:** otomatik kontroller dersin sonunda repoyu okur (6. haftadan itibaren test sonuçları GitHub Actions çalıştırmasından gelir).<br>• **Cumartesi 23:59, 5 puan:** otomatik kontroller 2 · insan katkısı 2 (çoğunlukla yapay zeka günlüğü, haftanın elle yazılmasını istediği dosyalarla birlikte; öğretim üyesi notlar) · commit disiplini 1 (öğretim üyesi notlar).<br>• **Commit disiplini:** derste her iş ortasında ve çalıştığında commit edilir, her commit hemen push edilir (6. haftadan itibaren; 5. haftaya kadar 10:00, 11:00 ve 11:45 civarında push'lar), 7. haftadan itibaren dersteki ilk push 09:30'dan önce yapılır (daha sonra gelen bir ilk push, geç gelmek dahil, elle incelenir) ve öğretim üyesi istediğinde 5 dakika içinde commit ve push yapılır; ders dışında yeni iş içeren, aralarında en az bir saat olacak şekilde push edilmiş en az iki commit. GitHub'ın push saati sayılır. Bir kodlama ajanının yaptığı commit hiçbir zaman sayılmaz. Öğrenci asla force push yapmaz. Şüpheli bir durumda önceki haftalara da bakılır.<br>• Haftanın adını verdiği her sınıf arkadaşı (katkıcı), öğrencinin o haftaki notunun %10'unu katkı bonusu olarak kazanır.<br>• Kaçırılan ders için telafi yoktur. |
| Mağaza Bonusu | en fazla 15 | Yayın bonusu. Mağaza izi S0–S6, her adımın teslim haftasında adım adım notlandırılır: öğrenci mağazayı seçer (S0), geliştirici hesabı açar (S1), uygulama kaydını oluşturur (S2), bir build yükler ve testçileri kaydeder (S3), beta testini test kanalında yürütür (S4), uygulamayı gönderir (S5) ve uygulama canlıya çıkar (S6). |
| Sunum | 15 | 13–14. haftalarda proje savunması. Öğrenci uygulamayı sınav görevlisinin önünde mağazadan yükler ve koddaki ve belgelerdeki kararlar hakkındaki soruları yanıtlar. Uygulama geliştirme makinesinden değil, mağaza build'inden çalıştırılır. |
| Final Sınavı | 40 | Üniversitenin sınav döneminde yazılı final sınavı. SDLC belgelerini, yapay zeka günlüğü pratiğini ve on iki haftanın teknik içeriğini kapsar. |

**Dönem notu:** Haftalık Projeler (45) + Sunum (15) + Final Sınavı (40) = 100. Mağaza bonusu en fazla 15 puan ekler. Dönem notu en fazla 100'dür.

## Sınıf İçi Kurallar

- En az %70 devam zorunludur. Devamsızlığın her türlü nedeni kalan %30'luk hakkın içine sığmak zorundadır. Bu yüzden lütfen başından itibaren tüm derslere katılmaya çalışın; böylece acil durumlar için kendinize esneklik bırakırsınız.
- Ders sırasında konuşmaları en aza indirin. Uzun ya da dersi bozan tartışmalara izin verilmez. Bu kuralı ihlal eden öğrenciden yer değiştirmesi ya da salondan ayrılması istenir.
- Ders sırasında telefon görüşmesi, kısa mesaj, anlık mesaj, e-posta ve genel web gezintisine izin verilmez. Bilgisayarlar yalnızca dersin materyalini izlemek için kullanılabilir.
- Ders sırasında ses ya da görüntü kaydı kesinlikle yasaktır.
- Her türlü kopya ve akademik sahtekarlık, ilgili yasal kurallara göre işlem görür.
- Notunuzu kendi çalışmanızdan başka herhangi bir yolla değiştirmeye yönelik her girişim, yöntemi ne olursa olsun kopya sayılır.

## Ders Planı

| Hafta | Tarih | Konu |
|---|---|---|
| 1 | 22/09 · 23/09 | Temeller: öğrenciler araçları kurar, Git/GitHub'ı öğrenir ve LLM'ler (büyük dil modelleri) ile transformer'larla ilk kez tanışır |
| 2 | 29/09 · 30/09 | Teklif Bölüm A, gereksinimler (`requirements.json`) ve SRS (use case'ler ve use case diyagramı): öğrenciler problemi ve çözümü anlatır, paydaşları adlandırır ve kullanım senaryolarını yazar |
| 3 | 06/10 · 07/10 | Dörtlü gruplarda pitch ve inceleme; öğrencilerin pazarı ve rakipleri incelediği, ticari potansiyeli değerlendirdiği ve riskleri sıraladığı Teklif Bölüm B; mağaza seçilir (S0); bundan sonra bir gereksinim id'sinin anlamı değişmez |
| 4 | 13/10 · 14/10 | Tıklanabilir prototip ve test case'ler: öğrenciler kabul ölçütlerinden test case'ler yazar, bunları prototip üzerinde yürütür ve gereksinimleri günceller; geliştirici hesabı açılır (S1) |
| 5 | 20/10 · 21/10 | Tasarım ve API sözleşmesi; geliştirme sunucu iskeleti ve ilk otomatik testlerle başlar; gereksinimler ve test case'ler taban çizgisi (baseline) olur (ondan sonra her değişiklik bir change request'tir) |
| 6 | 27/10 · 28/10 | Projenin kendi özelliği, uçtan uca: dersin girişi (e-postayla gönderilen 4 haneli kod) bağlanır ve her işlevsel `must` gereksinim sunucuda çalışır, testlerini CI'da geçer ve web istemcisinde sayfasına kavuşur, gereksinimden web sayfasına kadar; uygulama kaydı oluşturulur (S2) |
| 7 | 03/11 · 04/11 | Mobil istemci: giriş ekranı telefonda çalışır ve sunucuyla konuşur; testler |
| 8 | 10/11 · 11/11 | Ürünün sohbet botu sunucu ve barındırılan bir LLM API'si üzerinden mobil istemcide çalışır ve gereksinimlere bir change request ile girer; projenin kendi çekirdek özelliği üç katmanda birden çalışır; ilk build test kanalına çıkar ve testçiler kanala kaydedilir (S3); bundan sonra sunucu verilerini yeniden başlatmadan sonra da korur (bir dosyada ya da öğrencinin seçtiği bir veritabanında) |
| 9 | 17/11 · 18/11 | Beta testi, 8. haftada kaydedilen testçilerle: öğrenciler hata listesi tutar ve test raporu yazar (S4) |
| 10 | 24/11 · 25/11 | UAT ve gönderim: öğrenciler UAT raporunu ve dağıtım diyagramını yazar, uygulama incelemeye gönderilir (S5) |
| 11 | 01/12 · 02/12 | Yayın ve sağlamlaştırma: öğrenciler inceleme düzeltmelerini uygular, uygulama mağazada canlıya çıkar ve son README yazılır (S6) |
| 12 | 08/12 · 09/12 | Kapanış: poster ve savunma provası |
| 13 | 15/12 · 16/12 | **Proje savunması (sunumlar)** |
| 14 | 22/12 · 23/12 | **Proje savunması (sunumlar)** |
| | | **Final Sınavı** |

*Not: haftalık plan sınıfın ilerlemesine göre değiştirilebilir.*
