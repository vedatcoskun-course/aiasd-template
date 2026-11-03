# Yazılım Geliştirmede Yapay Zekayı Doğru Kullanmak — kullanmak, denetlemek, kararlarınızı açıklamak

*AIASD · Atlas Üniversitesi · 2026–27 Güz · Prof. Dr. Vedat Coşkun*
*Bu belge `AI_Doc4` ile birlikte okunur. `AI_Doc4` araçların ne olduğunu ve onları nasıl iyi
kullanacağınızı anlatır. Bu belge ise araçların size verdiğiyle ne yapmanız gerektiğini
anlatır. 3. haftayla birlikte gelir ve dersin hem İngilizce hem Türkçe olan tek okumasıdır
(`AI_Doc2`–`AI_Doc4` İngilizcedir). Final sınavının bir parçasıdır: sınavda bu belgeden
soru çıkar.*

---

## 0. Dört kişi, bir asistan

Aynı istemi — *"Bana e-postayla dört haneli kod gönderen ve kontrol eden bir giriş
endpoint'i yaz"* — dört farklı kişiye verin. Asistan her birine hemen hemen aynı cevabı
verir: yaklaşık kırk satır kod. 1. haftada dört repo birbirinin aynısı görünür. 5.
haftada artık öyle görünmezler ve bu fark, bu belgenin konusudur.

Dört kişi iki açıdan birbirinden ayrılır. Birincisi, **yazılım mühendisliğinin
kavramlarına** sahip olup olmadıklarıdır: gereksinim nedir, arayüz nedir, `429` durum kodu
ne anlama gelir, bir test neyi kanıtlar, sürüm nedir ve risk nedir. İkincisi, **asistan
kullanma disiplinine** sahip olup olmadıklarıdır: çıktısını bir olgu değil bir iddia
sayarlar; onu kontrol ederler; kararı kaydederler; ve onu nerede hiç kullanmamaları
gerektiğini bilirler. Bu ders, birincisini lisans programınızın öğrettiğini varsayar ve
ikincisini öğretir. İkisini birlikte notlar.

| | Asistan disiplini olmadan | Asistan disipliniyle |
|---|---|---|
| **Mühendislik kavramları olmadan** | Bu kişi o satırları yapıştırır, kodun çalıştığını görür ve push eder. İlk gerçek kullanıcı kodu almaz ve birkaç saniye sonra ikinci bir kod ister. Endpoint düpedüz ikinci bir kod gönderir; o durumu kimse düşünmemiştir. İlk hata ortaya çıktığında bu kişi, cevabı okumadan asistana yeniden sorarak hatayı "düzeltir". Commit geçmişi Cumartesi gecesi yapılmış tek bir commit'tir. Ürün gösterimde çalışır, başka hiçbir yerde çalışmaz. | Bu kişi özenli bir istem yazar, cevaba güvenmez ve aynı soruyu ikinci bir asistana sorar. Ama *neyi* kontrol edeceğini söyleyemez. "Bir kullanıcı birincisinden sonraki bir dakika içinde ikinci bir kod ister" durumunun, kodun ele alması gereken bir durum olduğunu bilmez. HTTP durum kodu `429 Too Many Requests`'i (sunucunun "çok fazla istek: bekleyin, sonra yeniden deneyin" deme biçimi) hiç görmemiştir. Bir kabul ölçütü yazamaz, çünkü kavramı ona henüz kimse öğretmemiştir. Şüphe yerindedir, ama hiçbir şey doğrulanmaz. |
| **Mühendislik kavramlarıyla** | Bu kişi endpoint'in tam olarak ne yapması gerektiğini bilir, ama acelesi vardır. Asistanın değişikliklerini satır satır okumadan kabul eder. Gerçek bir testçinin e-posta adresini test verisi olarak isteme yapıştırır. Asistanın seçtiği e-posta kütüphanesinin en son iki yıl önce güncellendiğini fark etmez. Kavramlar vardır, ama bu kişi "derlendi" diye onları asistanın çıktısına uygulamaz. Ya da bu kişi asistanı büsbütün kullanmayı reddeder ve 6. haftada üç hafta geridedir. | Bu kişi o satırları REQ-001 gereksinimine ("60 saniye içinde istenen yeni kod 429 alır") karşı okur. Aynı adres için bir dakika içinde iki istek gönderir ve ikinci bir kodun gönderildiğini görür. Kodu reddeder, o durum için bir test ekler ve düzeltmeyi, onu adlandıran bir mesajla kendi başına commit eder. Her iki sunucu yanıtını yapıştırarak yapay zeka günlüğüne dört satır yazar. Asistan aynı asistan, istem aynı istemdir, ama mühendis başka bir mühendistir. |

Bu derste giriş, 6. haftadan itibaren dersin kendi modülüdür (`server/course_login.py`) ve
herkes için aynıdır. 60 saniye içinde istenen ikinci koda zaten `429` ile cevap verir.
Örnek, böyle bir kuralın neden gerektiğini gösterir. Aynı düşünceyi kendi özelliğinizde
kullanırsınız.

Sağ sütundaki hiçbir şey başka bir asistan ya da daha iyi bir istem gerektirmez. Üç şey
gerektirir: çıktının ne yapması gerektiğini bilirsiniz, bunu yapıp yapmadığını kontrol
edersiniz ve başkasının okuyabileceği bir kayıt bırakırsınız. Aşağıdaki sekiz teknik, bu
üç şeyi yapmanın yollarıdır. Her tekniğin altındaki örnekler iki sütunun etiketlerini
taşır: **Eğitimsiz kullanıcı** ve **Bu dersi alan**. Her çift, aynı durumun iki farklı
kişi tarafından nasıl ele alındığını gösterir.

Mühendislik kavramları olmadan başlayan bir öğrenci de sağ sütuna ulaşabilir. Aşağıdaki
her teknik, ihtiyaç duyduğu kavramı ve dersin o kavramı hangi hafta öğrettiğini söyler.
Sıra önemlidir: önce kavram gelir, asistan ikinci sırada gelir.

---

## 0.1 Tek cümle

Bu ders asistanın ne ürettiğini notlamaz. Ürettiğini sizin ne kadar iyi **tarif
ettiğinizi, kontrol ettiğinizi, düzelttiğinizi ve açıkladığınızı** notlar. Bir
asistan bir ödevin her dosyasını on dakikada yazabilir. Her hafta iki puan insan katkısı
içindir ve bunun çoğu `ai_log`'unuzdan gelir. Bu puanlar üç şey için verilir: asistanı
yanlış yaparken yakaladığınız an, yapıştırdığınız kanıt ve bu konuda ne yaptığınız.

Aşağıdaki her teknik, o anı kendiliğinden olmasını beklemek yerine bilerek yaratmanın bir
yoludur. Her haftanın ödevi beklediği tekniği adlandırır ve §10'daki tablo bütün dönemi
gösterir. Herhangi bir tekniği herhangi bir hafta kullanabilirsiniz. 4. haftadan itibaren
her hafta bunlardan biri zorunludur; 2. ve 3. haftalarda teknik önerilmişti. Her haftanın
yapay zeka günlüğü kullandığı tekniğin adını verir.

Teknikler zaten bildiğiniz haftalık rutinin içinde işler:

- her push'tan önce denetleyici;
- derste her işin ortasındaki commit'ler ve ders sonunda reponuzun okunması;
- Cumartesi 23:59 son teslim saati;
- `requirements.json` dosyanızdaki kimlikler ve `PROPOSAL.md`'nin sonundaki Change log;
- ödevin istediği haftalarda toplanan dörtlü grubunuz;
- `weekNN/group_NN.json` (2–3. haftalarda `contributors_NN.json`).

Tekniklerin hiçbiri yeni bir dosya ya da yeni bir alışkanlık istemez. Zaten push ettiğiniz
dosyalara ne konacağını söylerler.

### Asistan on iki haftanın neresinde

Aynı asistan projenizin her fazında başka bir araçtır. Aşağıdaki tablo her fazda neyi iyi
yaptığını, neyi sık sık yanlış yaptığını ve hatayı hangi tekniğin yakaladığını
gösterir.

| Faz (haftalar) | İyi yaptığı | Sık sık yanlış yaptığı | Yakalayan teknik |
|---|---|---|---|
| Teklif ve gereksinimler (2–3) | Listeleri ve yapıyı hızla üretir: bir dakikada sekiz gereksinim. | Sizin önceliklerinizi ve sizin kullanıcılarınızı bilmez. Kaynağı olmayan sayılar (pazar büyüklüğü, inceleme süresi) verir. Hiç istemediğiniz özellikler ekler, örneğin para almayan bir uygulamaya ödeme. | §4, §3, §5 |
| Prototip, test case'ler ve tasarım (4–5) | Kısa bir tariften ekran akışlarını, test case'leri, tasarımın bileşenlerini ve mimari diyagramını yazar. | Bir kısıtı her istemde tekrarlamazsanız onu unutur. Bir fazla bileşen ekler. Bir işi yanlış bileşene verir (örneğin check-in'i rezervasyonlara değil girişe verir). | §1 |
| Sunucu, giriş ve istemciler (5–7) | Sıradan kodu, endpoint'leri, testleri ve sunucuyla istemcileri birbirine bağlayan kodu yazar. | Uç durumları kaçırır: örneğin iki kullanıcı aynı odayı aynı saat için rezerve eder ve kod, ikincisini 409 ile reddetmek yerine iki rezervasyonu da kabul eder. O zamandan beri kaldırılmış ya da yeniden adlandırılmış kütüphane sürümleri kurar, dolayısıyla `pip install` başarısız olur. Tek bir değişiklik istendiğinde, söz etmediği ikinci bir değişikliği de yapar. | §2, §3, §6 |
| Üç katman ve sohbet botu (8) | Her katmanı (sunucu, web, mobil) kendi başına doğru yazar; sohbet botunun LLM API'sini çağıran sunucu kodunu da. | Üç katmanı birbiriyle uyuşturmaz: aynı alan sunucuda `room_id`, uygulamada `roomId` adını taşır; sunucu hiçbir istemcinin ele almadığı bir durum kodu döndürür. API anahtarını sunucunun `.env` dosyası yerine uygulamaya koyabilir. | §7, §9 |
| İnsanlarla test (9–10) | Test planları, hata raporu şablonları ve olası arızaların bir listesini yazar. | Testçilerinizin gerçekte ne yapacağını bilemez, çünkü onlarla hiç tanışmamıştır. | §8 |
| Mağaza ve yayın (11) | Kontrol listelerini ve mağaza ilanının metnini yazar. | Mağaza kurallarını bir yıl önceki halleriyle aktarır ve inceleme süresini yeni bir hesap için değil yerleşik bir hesap için verir. | §3, §5 |
| Kapanış ve savunma (12–14) | Özetleri ve posterin ilk taslağını yazar. | Neyi neden kararlaştırdığınızı söyleyemez; bunu yalnızca siz bilirsiniz ve size sorulacaktır. | §9 |

Tabloyu yukarıdan aşağı okuyun. Asistan, işin genel olduğu yerde en yararlıdır. İşin
*sizin* ürününüz ve *sizin* insanlarınızla ilgili olduğu yerde en az yararlıdır. Bu ders
ona aynı sırayla gitgide daha az güvenir.

---

## 1. Önce kabul ölçütü

**Ne.** Bir şey istemeden önce, cevabın doğru olduğunu nasıl anlayacağınızı yazın. Kendi
sözlerinizle, istemden *önce* yazılmış iki üç satır yeterlidir. Sonra bunları istemin içine
koyun.

**Neden.** Testi olmayan bir istek, makul görünen bir şey isteğidir: doğru görünen bir şey.
Modeller makul görünen şeyler üretmekte çok iyidir. "StudyRoom tasarımının bileşenlerini
yaz" içinde bir `Server: payments` bileşeni bulunan derli toplu bir tablo döndürür.
"StudyRoom tasarımının bileşenlerini yaz: en çok beş tane, hiçbir yerde para yok, her
birinin hizmet ettiği REQ kimlikleri ve check-in'i rezervasyon bileşeni yürütsün" ise satır
satır kontrol edebileceğiniz bir şey döndürür. Ve kontrol zaten yazılmıştır.

**Eğitimsiz kullanıcı.** *"Claude'dan tasarımımın bileşenlerini istedim. İyi
görünüyorlardı, bu yüzden kullandım."*

**Bu dersi alan.** *"Sormadan önceki ölçütlerim şunlardı: en çok beş bileşen, ödeme yok,
her birinin REQ kimlikleri ve check-in rezervasyon bileşeninde. İlk cevapta
`Server: invoices` dahil yedi bileşen vardı. Ölçütlerin yapıştırıldığı ikinci istem beş
bileşen verdi. Ama check-in'i `Server: bookings`'e değil `Server: login`'e koymuştu. Bu
yanlıştır: bir check-in tek bir rezervasyona aittir ve bir kullanıcının çok sayıda
rezervasyonu olur. Elle düzelttim; son tablo `week05/DESIGN.md` dosyasındadır."*

**Günlükte.** Önce yazdığınız ölçütleri, cevabın onlara göre ölçülmüş durumunu ve neyin
başarısız olduğunu kaydedin.

**Bu derste.** Ölçütleriniz zaten vardır: bunlar `requirements.json` kimlikleridir.
Anlamları 3. haftadan beri sabittir ve 5. hafta sonundan itibaren taban çizginizdir
(baseline). Tasarımın ya da kodun karşılaması gereken REQ satırlarını istemin içine
yapıştırın. Bir REQ'i bozan cevap haftanın hatasıdır. Elinizde olmayan bir REQ'e ihtiyaç
duyan cevap asla sessizce eklenmez. Taban çizgisine kadar `PROPOSAL.md` Change log'una
tarihli bir satır alır. 5. haftadan sonraki Pazar gününden itibaren bir **change
request**'tir (değişiklik talebi): Change log'da `CR-` ve sıradaki numarayla başlayan,
değişikliği ve kimlikleri söyleyen ve etkilediği her dosyayı sayan tek bir satır (§9).

---

## 2. Okuyarak değil, çalıştırarak doğrulayın

**Ne.** Bir şey çalışabiliyorsa, onu çalıştırarak doğrulayın: kodu çalıştırın, isteği
gönderin, sayfayı bir telefonda açın, Mermaid kaynağını önizlemeye yapıştırın. Çıktıyı
okuyup ona katılmak doğrulama değildir.

**Neden.** Üretilen kod, doğru çalıştığından çok daha sık doğru görünür. Asistan da onu
çalıştırmamıştır; yalnızca ona benzeyen çok miktarda kod görmüştür.

**Eğitimsiz kullanıcı.** *"Copilot rezervasyon endpoint'ini üretti. Kod doğru görünüyor."*

**Bu dersi alan.** *"Endpoint'i çalıştırdım. Aynı oda ve aynı başlangıç saati için ikinci
bir rezervasyon, reddedilmek yerine kabul edildi (201). REQ-002'm dolu bir zaman
diliminin reddedildiğini söylüyor ve `api.md` satırım 409 diyor. İki yanıt aşağıya
yapıştırılmıştır. Rezervasyon kaydedilmeden önce yapılan bir kontrolle düzelttim ve
TC-002-02 testi artık bunu yakalıyor."*

**Günlükte.** Çalıştırdığınız komutu ve çıktısını (Kanıt bloğunda `TERMINAL:` altında, hiç
dokunulmadan) ve düzeltmeyi kaydedin.

**Bu derste.** İlk çalıştırma her zaman `python .github/check_deliverables.py` komutudur:
derste her push'tan önce ve Cumartesi 23:59'dan önce. Kırmızı
bir kontrol kanıttır, bu yüzden yapıştırın. 6. haftadan itibaren her push'tan sonra
**Actions** sekmesine de bakın: yalnızca kendi bilgisayarınızda geçen bir test sayılmaz.
İkinci çalıştırma kendi telefonunuzdadır: uygulama her hafta telefon genişliğinde
çalışmalıdır, yalnızca 10. haftada değil.

---

## 3. Düşman gözden geçiren

**Ne.** Asistana kendi işinizi ve bir rol verin: hayır demek isteyen yatırımcı, uygulamayı
reddetmek isteyen mağaza incelemecisi ya da onu kırmak isteyen testçi veya saldırgan. En
güçlü üç itirazı numaralı olarak isteyin. Sonra belgede **birini yanıtlayın** ve kanıtla
**birinin yanlış olduğunu gösterin**.

**Neden.** Bir modele "Bu iyi mi?" diye sorun, evet der. "Bu neden başarısız olacak?" diye
sorun, bir liste verir. Kabaca her üç maddeden biri, sizin görmediğiniz gerçek bir
sorundur. Diğer ikisi size onunla gerekçeli olarak aynı fikirde olmamayı öğretir.

**Eğitimsiz kullanıcı.** *"ChatGPT'den teklifimi incelemesini istedim. Yararlı geri
bildirim verdi, ben de uyguladım."*

**Bu dersi alan.** *"İtiraz 2 şuydu: 'Kimse rezervasyonu elle girmez; doğrudan içeri
girerler.' Bu, zemin kat odaları için doğru, bu yüzden §4'e QR ile check-in ekledim. İtiraz
3 şuydu: 'Kütüphanenin zaten bir rezervasyon sistemi var.' Kontrol ettim: Atlas
kütüphanesinde yok (2026-10-07 tarihinde bankoda sordum). Projeyi korudum ve kontrolü §9'a
yazdım."*

**Günlükte.** Üç itirazı kelimesi kelimesine, hangisini nerede yanıtladığınızı ve
hangisinin yanlış olduğunu hangi kanıtla gösterdiğinizi kaydedin.

**Bu derste.** Ödevin istediği haftalarda iki düşman gözden geçireniniz vardır: insanlar
ve asistan. Yorumları farklı dosyalara gider.

- İnsanlar, ödevin adını verdiği kişilerdir: 3. haftada dörtlü grubunuz, 6. haftada bir
  saldırgan (grubunuzdan ya da herhangi bir sınıf arkadaşınız). 3. haftada cümleleri,
  alıntılanmış olarak, sizin `accepted` (true ya da false) ve `why` kararınızla birlikte
  `contributors_03.json` dosyasına gider. 6. haftada `group_06.json` dosyasına `tried` ve
  `happened` alanlarını kendiniz, kendi sözlerinizle yazarsınız; sonra `accepted` ve `why`
  kararınızı eklersiniz.
- Asistanın itirazları `ai_log_NN.md` dosyasına gider.

İkisini yan yana koyun. Asistanla insanların ayrıştığı yerde, *sizin* kullanıcılarınız
hakkında genellikle insanlar haklıdır. Pazar ya da teknoloji hakkında genellikle asistan
haklıdır. Hangisinin söz konusu olduğunu ve nedenini `why` alanında söyleyin. 3. haftada
gözden geçirenler salondaki kişilerdi (`PITCH_03.md`'nin 7. slaytı). 11. haftada rol,
mağazanın kendi inceleme kurallarını (Apple App Review Guidelines, Google Play
politikaları) kullanan mağaza incelemecisidir.

---

## 4. Çapraz sorgu: iki asistan, tek istem

**Ne.** İki farklı asistana tam olarak aynı istemi ve aynı kaynak metni verin. İki cevabı
birbiriyle ve zaten bildiklerinizle karşılaştırın.

**Neden.** İki modelin uyuştuğu yerde bir adayınız vardır, bir olgu değil. Ayrıştıkları
yerde en az biri yanlıştır. Hangisinin yanlış olduğunu bulmak, gerçek kanıtlı gerçek bir
hataya giden en hızlı yoldur. Bu 2. haftanın tekniğidir ve bütün dönem boyunca yararlı
kalır.

**Eğitimsiz kullanıcı.** *"İkisi de benzer gereksinimler verdi, bu yüzden birleştirdim."*

**Bu dersi alan.** *"Claude şöyle yazdı: 'Rezervasyon, check-in yapılmazsa 15 dakika sonra
düşer.' Gemini şöyle yazdı: '2 saat sonra.' İkisi de bana sormadı. Doğru sayı benim
§3'ümdedir: sorun, gitmiş insanlar tarafından bütün öğleden sonra tutulan odalardır,
dolayısıyla 15 dakika doğrudur. Bunu kendi kabul ölçütümle REQ-004 yaptım."*

**Günlükte.** İstemi bir kez, iki cevabı (her biri `AI:` altında bütün olarak, geldiği gibi
yapıştırılmış; bkz. §9'daki Kanıt bloğu) ve kararı kaydedin.

**Bu derste.** Bu, 2. haftanın alıştırmasıydı: aynı §3–§4 iki asistana verildi, her biri
sekiz gereksinim verdi ve siz bir yanlış gereksinim buldunuz. İki cevabın az emek istediği
ve doğrunun kendi belgelerinizde olduğu her yerde tekniği yeniden kullanın: örneğin 5.
haftadaki tasarımda ve 9. haftadaki test planında. İki asistan, 1. haftada
seçtiklerinizden (`week01/ASSIGNMENT_01` §5) ikisi olmalıdır; ücretsiz katmanlar
yeterlidir.

---

## 5. Kaynak gösterttirin ve "bilmiyorum" demesine izin verin

**Ne.** Her olgusal iddianın kaynağını isteyin: bir belge, bir sayfa ya da kendi kodunuzdan
bir satır. Asistana "bilmiyorum"un kabul edilebilir bir cevap olduğunu açıkça söyleyin.
Sonra **kaynağı açın**.

**Neden.** Modeller kaynakları da diğer her şey kadar kolayca yazar ve bu kaynakların bir
kısmı yoktur. Kontrol etmediğiniz bir olgu, bildiğiniz bir olgu değildir.

**Eğitimsiz kullanıcı.** *"Yapay zekaya göre Google Play incelemesi bir ile üç gün
sürüyor."*

**Bu dersi alan.** *"'Bir ile üç gün'ün kaynağını istedim. Bir Play Console yardım sayfası
verdi. Sayfayı açtım (2026-10-08): sayfa, incelemenin 'yeni geliştirici hesapları için 7
güne kadar ya da daha uzun sürebileceğini' söylüyor. §12 artık 7 gün diyor ve sayfayı
kaynak gösteriyor. Aynı soruyu Gemini'ye sordum; güncel bir rakamı olmadığını söyledi, ki bu
daha iyi cevaptı."*

**Günlükte.** İddiayı, asistanın verdiği kaynağı ve kaynağın gerçekte ne dediğini kaydedin.

**Bu derste.** 3. ve 10. haftada `PROPOSAL.md` §8–§12'deki ve UAT raporundaki her sayı
kaynağını taşır: geldiği sayfayı ya da kişiyi, tarihiyle birlikte. Buna mağaza ücretleri,
inceleme süreleri ve pazar büyüklükleri dahildir.

---

## 6. Küçük diff'ler: bir seferde bir değişiklik, ve onu okuyun

**Ne.** Yeniden yazım değil, tek bir değişiklik isteyin. Kabul etmeden önce diff'in
tamamını okuyun, değiştirilmesini istemediğiniz satırları da. Kabul ettiğiniz her
değişikliği kendi başına commit edin.

**Neden.** "Bu dosyayı yeniden düzenle" deyin; istemediğiniz üç şeyin değiştiği, birinin
hiç söz edilmeden değiştiği bir dosya geri alırsınız. İki dakikada okuyabildiğiniz bir
diff'in sorumluluğunu alabilirsiniz. Küçük diff'ler, haftanın commit disiplini puanı
verilirken commit geçmişinizi de okunur kılar.

**Eğitimsiz kullanıcı.** *"Copilot'tan `server/tests/test_login.py` dosyasını temizlemesini
istedim, sonucu kabul ettim ve push ettim."*

**Bu dersi alan.** *"Yalnızca kullanılmayan import'ların kaldırılmasını istedim. Diff
ayrıca TC-001-01 testinin kontrol ettiği kod uzunluğunu dört haneden altı haneye
değiştirmişti. Bunu istememiştim ve asistan bundan söz etmemişti. O parçayı (hunk'ı)
reddettim ve import değişikliklerini tuttum. `ruff` sonucu doğruluyor; `e41c…` commit'i
yalnızca import değişikliklerini içeriyor."*

**Günlükte.** İstediğiniz değişikliği, aldığınız değişikliği ve reddettiğinizi kaydedin.

**Bu derste.** Haftalık commit disiplini puanı şuna bakar:

- **Derste:** her işi ortasında commit edin, çalıştığında yeniden commit edin ve her commit'i
  hemen push edin.
- **İlk push 09:30'dan önce** (7. haftadan itibaren): derse checker'ı çalıştırarak başlayın,
  sonra commit ve push edin. İlk push'unuz 09:30'dan sonra gelirse (geç gelmek dahil), ders
  işinizin hangi bilgisayarda yapıldığını elle incelerim.
- **Çağırdığımda commit ve push** (7. haftadan itibaren): ders sırasında herkesten aynı anda
  commit ve push isteyebilirim; push'unuz 5 dakika içinde GitHub'a ulaşmalıdır.
- **Ders dışında:** yeni iş içeren en az iki commit, aralarında en az bir saat olacak
  şekilde push edilmiş olsun.
- Commit'in üzerindeki tarih değil, GitHub'ın push saati sayılır. Bir kodlama ajanının
  yaptığı commit hiçbir zaman sayılmaz.
- **Asla force push yapmayın** ve bir asistanın yapmasına da izin vermeyin.

Her commit mesajında değişikliğin adını verin (örneğin `week06: REQ-002 busy slot answers
409, test added`). Cumartesi gecesi yapılmış, bütünüyle yapıştırılmış olabilecek tek büyük
bir commit puanı kazandırmaz. Her commit'ten önce `ruff check .` ve `ruff format .`
çalıştırın. Commit'e giren bir anahtar, iş akışı belgesinde anlatıldığı gibi, on puana mal
olur ve anahtarı iptal etmeniz gerekir.

---

## 7. Üç katman arasında tutarlılık

**Ne.** Aynı özellik sunucuda, web istemcisinde ve mobil istemcide varsa, üçünü de asistana
verin ve tutarsızlıkları bulmasını isteyin. Sonra bulduğunu doğrulayın ve kaçırdığını
arayın.

**Neden.** Üretilmiş üç kod parçasının her biri kendi içinde tutarlıdır, birbiriyle değil:
bir alan sunucuda `room_id`, uygulamada `roomId` adını taşır ya da sunucu hiçbir istemcinin
ele almadığı bir durum döndürebilir. Modeller, siz istediğinizde bunları bulmakta iyidir.
İstemediğinizde hiçbir şey bulmazlar.

**Eğitimsiz kullanıcı.** *"Üçünde de her şey çalışıyor."*

**Bu dersi alan.** *"`server/bookings.py`, `web/book.html` ve `mobile/api.dart` arasındaki
uyumsuzlukları istedim. `checked_in` ile `checkedIn` farkını buldu; bu gerçekti ve
düzelttim. Sunucunun çifte rezervasyonda `409 Conflict` döndürdüğünü, mobil istemcinin ise
başarı dışındaki her cevabı 'ağ hatası' saydığını kaçırdı. Bunu test ederek buldum
(teknik 2) ve ele almayı ekledim."*

**Günlükte.** Asistanın ne bulduğunu, neyi doğruladığınızı, neyi kaçırdığını ve onu nasıl
bulduğunuzu kaydedin.

**Bu derste.** Kendi özelliğiniz 6. haftadan itibaren sunucuda ve webde, 7. haftadan
itibaren mobil istemcide çalışır. 8. haftada sohbet botu onlara katılır: sunucunuz
seçtiğiniz barındırılan bir LLM API'sini çağırır (ücretsiz katman yeter) ve mobil
istemcide sohbet ekranı olur. Sohbet botu gereksinimlerinize bir change request ile girer.
API anahtarı yalnızca sunucunun `.env` dosyasındadır: uygulamada da, repoda da asla
bulunmaz. 8. haftanın sonunda özelliğiniz üç katmanda da çalışır. Grubunuz o hafta toplanıyorsa
bulduğunuz uyumsuzluğu getirin: diğerlerinde de aynı üç katman ve çoğu zaman aynı türden
hata vardır.

---

## 8. Tahmin ile gözlem

**Ne.** İnsanlarla yapılacak bir testten önce (9. hafta beta testi ve 10. hafta UAT)
asistana neyin ters gideceğini sorun ve tahmini yazın. Testten sonra testçilerin gerçek
hata listesini onun yanına koyun.

**Neden.** Bu, bir modelin kullanıcılarınız hakkında ne bildiğini ölçmenin bu dersteki en
açık yoludur: genellikle bir şeyler, asla her şey. İki liste arasındaki fark, insanlarla
testin gerekli olduğunu gösterir. Test raporunuzu okunmaya değer kılan paragraf da budur.

**Eğitimsiz kullanıcı.** *"Testçiler bazı hatalar buldu, ben de düzelttim."*

**Bu dersi alan.** *"Tahmin (beş madde): giriş kodunun gelmemesi, yavaş bir liste ve
benzerleri. Gözlem (14 testçiden dokuz madde): tahmin edilen beş maddeden ikisi
gerçekleşti. En sık şikayet olan 'haritada hangi odanın benim olduğunu anlayamıyorum'
hiçbir tahminde yoktu. Tablo, `week09/` içindeki test raporumdadır."*

**Günlükte.** Tahmini (tarihli, testten önce), gözlenen listeyi ve ikisi arasındaki
örtüşmeyi kaydedin.

**Bu derste.** Kaç testçiye ihtiyacınız olduğunu mağaza belirler. Yeni bir kişisel Google
Play hesabı, uygulama yayınlanmadan önce kapalı bir testte 14 gün kesintisiz kalan en az
12 testçi ister. Onları S3'te, 8. haftada kaydedin; böylece 14 gün 10. haftadaki
gönderimden önce biter. Testçileriniz, sunumunuzdaki beş kişi (`PITCH_03.md`'nin 3.
slaytı) artı sınıf arkadaşları ve arkadaşlarınızdır (9. haftada beta-tester rolü).
Kullanıcı Kabul Testi (UAT) 10. haftada, sunumunuzdaki beş kişiyle yapılır.

Tahmin, 9. hafta dersinden önce `ai_log_08.md` içinde tarihlenir. Testçilerin listesi
`week09/` içinde, UAT raporu `week10/` içinde tutulur. Testçiler uygulamayı mağazanın test
kanalından (S3–S4) kurar. Beş gerçek insan ürününüzü kullanamıyorsa, bu dönemin en önemli
bulgusudur. Bu dersin bir kuralının nedeni de budur: ürününüz çevrenizdeki gerçek insanların
kullanabileceği bir üründür ve onu o insanlar test eder.

---

## 9. Karar kaydı: günlük ne içindir

`weekNN/ai_log_NN.md` dosyanız **bir sohbet dökümü değildir** ve yapay zekayı ne kadar
kullandığınızın günlüğü de değildir. Haftada bir kararın dört parçalı mühendislik kaydıdır:

| Parça | Yanıtladığı soru | Şöyle dediğinde başarısız olur |
|---|---|---|
| **Ne için kullandım** | Hangi asistan, hangi istem ve hangi dosyanız üzerinde? | "Teklif için ChatGPT kullandım." |
| **Doğru yaptığı** | Neyi tuttunuz ve neden doğruydu? | "Yardımcı oldu." |
| **Yanlış yaptığı** | Haftanın tekniğiyle üretilmiş somut bir hata | "Bazı şeyler alakasızdı." |
| **Kanıt ve düzeltme** | Yapıştırılmış çıktı ve elle yaptığınız değişiklik | Hiçbir şey yapıştırılmamış; "düzelttim." |

Her haftanın iskeleti kendi başlıklarını verir, ama bu dört soruyu sorar.

**Kanıt** (Evidence) bloğu, bir insanın ilk okuduğu kısımdır. Hatayı tarif etmek yerine
gösterir. Hatayı gösteren turları yapıştırın; hatayı göstermeyen turları bütünüyle
dışarıda bırakabilirsiniz. Parçalar şunlardır:

- isteminiz `ME:` altında;
- asistanın cevabı `AI:` altında;
- hafta istediğinde, çalıştırdığınız komutlar ve çıktıları `TERMINAL:` altında.

Tuttuğunuz her `ME:`, `AI:` ya da `TERMINAL:` parçası bütün olarak, geldiği gibi
yapıştırılır: 4. haftadan itibaren hiçbir şey çıkarılmaz, hiçbir şey düzeltilmez, dil
bilgisi bile. Kanıtı olmayan bir günlük, ne kadar uzun olursa olsun, hiçbir şey
kazandırmaz.

**Döngüdeki insanlar.** Asistan tek gözden geçireniniz değildir ve tek gözden geçireniniz
olmamalıdır. `weekNN/group_NN.json` (2–3. haftalarda `contributors_NN.json`), o haftanın
ödevinin adını verdiği kişileri o haftanın rolüyle (tam İngilizce kelimeyle) tutar:
2 stakeholder · 3 reviewer · 4 collaborator · 5 kimse (tek başınıza çalışırsınız) ·
6 attacker · 7 tester · 8 test-user · 9 beta-tester · 10 uat-participant ·
11 release-tester · 12 poster-reviewer. 3. haftadaki grubunuz grubunuz olarak kalır;
hangi haftalarda ve ne için toplandığını ödev söyler. Toplandığında o haftanın asistan
hatasını getirin. "Sizi de kandırdı mı?" sorusu var olan en hızlı çapraz kontroldür.
Dosyadaki kayıtlar o kişilerdir: onların sözleri ya da yaptıkları. Asistanın orada kaydı
yoktur. Bir öğrenci, bir bilgisayar, bir GitHub hesabı: bir sınıf arkadaşının bilgisayarında yazılmış
bir günlük sizin değildir. Bana sorular kendi reponuzda bir issue olarak gönderilir;
onları Pazar günleri okurum.

### Doğrulukla ilgisi olmayan dört risk

Bir cevap doğru olup yine de istenmesi ya da push edilmesi yanlış olan şey olabilir. Bu
projede böyle dört risk vardır, her biri belirli bir haftada.

**Güvenlik.** Üretilen kod loglamayı sever. 6. haftada, her isteği token'ıyla birlikte
"hata ayıklamak için" konsola basan bir route, sunucu logunu okuyabilen herkese her girişi
sızdırır. Verinin kime ait olduğunu hiç sormayan bir route, giriş yapmış her kullanıcının
herkesin verisini okumasına ya da değiştirmesine izin verir; onu yazan asistan o kullanıcıyı
düşünmemiştir. Repodaki bir API anahtarı, satırı kim yazmış olursa olsun, on puana mal olur
ve iptal edilmek zorundadır. 8. haftadan itibaren buna sohbet botunun API anahtarı da
dahildir: o yalnızca sunucunun `.env` dosyasında durur. Üretilen kodu yalnızca ne
döndürdüğü için değil, ne *gönderdiği* ve ne *sakladığı* için okuyun.

**Kişisel veri.** 3. slayttaki beş kişi, testçilerinizin adları ve e-posta adresleri (8–9.
haftalar) ve `contributors_NN.json` ile `group_NN.json` içindeki öğrenci numaraları kişisel
veridir. Adlar ve numaralar repo dosyalarınızda kalır; onları bulutta barındırılan bir
asistana asla yapıştırmayın. Kişiyi tarif edin ("akşamları çalışan ikinci sınıftan bir
sınıf arkadaşı"); kişiyi yapıştırmayın.

**Bayat bilgi.** Her model belirli bir tarihe kadarki verilerden öğrenmiştir ve mobil
çatılar ile mağaza kuralları o tarihten sonra da değişmeye devam eder. Bir asistan, Expo
SDK'sının ya da Flutter API'sinin eski bir sürümü için kod yazabilir ve kod derlenmez.
Değişmiş bir Play Console politikasını aktarabilir. Size verdiği her sürüm numarasını ve
her mağaza kuralını bir iddia sayın. Onu resmî sayfaya karşı doğrulayın ve kontrol
ettiğiniz tarihi not edin (§5). Aldığınız hata mesajı, asistanın olacağını söylediği şeye
uymuyorsa, bayat olan modeldir, siz değil.

**Köken** (kodun nereden geldiği). Bir asistanın ürettiği kod, başka birinin bir lisansla
yayımladığı kodun yakın bir kopyası olabilir. O zaman o lisansı bilmeden çiğnemiş
olursunuz. Bu proje için kural basittir. Sizin yazmadığınız ve satır satır
açıklayamadığınız, bir fonksiyondan uzun hiçbir blok repoya girmez. Bir kütüphane
yapıştırılarak değil, adı ve sürümüyle `requirements.txt` üzerinden girer. Savunmada
belirli bir kod bloğunun neden orada olduğu size sorulacaktır ve "asistan yazdı" bir cevap
değildir. Push sizindir, dolayısıyla kod da sizindir.

Günlük iki kural daha taşır:

- **Değişen plan yazılır.** Bıraktığınız bir gereksinim, sadeleştirdiğiniz bir katman ya da
  geçtiğiniz bir mağaza, `PROPOSAL.md` Change log'una gerekçesiyle tarihli tek bir satır
  olarak kaydedilir. 5. haftadan sonraki Pazar gününden (taban çizgisi, baseline)
  itibaren `requirements.json` ya da `test_cases.json` dosyasındaki her değişiklik,
  düşürülen bir gereksinim de dahil, bir **change request**'tir: Change log'da `CR-` ve
  sıradaki numarayla başlayan, değişikliği ve kimlikleri söyleyen ve etkilediği her
  dosyayı sayan tek bir satır. Diğer değişiklikler (`api.md`, use case'ler, ekranlar)
  normal, tarihli bir Change log satırı alır. Fikir değiştirmek
  mühendisliktir; sessizce değiştirmek değildir.
- **Bazı şeyler asistanla hiç yapılmaz.** Bunları yalnızca siz yazarsınız: pitch'iniz
  (`PITCH_03.md`), sorunun en son başınıza geldiği an, ürününüzü test edecek beş kişi,
  gözden geçirenlerinizin ya da saldırganlarınızın yazdığı cümleler ve onlar hakkında
  verdiğiniz kararlar. Bunlar sizin hayatınız ve sizin insanlarınızla ilgilidir. Bir
  asistan bunları bilemez ve ben bunları soracağım. **Yapay zeka günlüğünün kendisi de bu
  listededir.** `ai_log_NN.md` dosyasını kendiniz, kendi cümlelerinizle yazın; dili
  düzeltmek için bile asistan kullanmayın. İngilizceniz ya da Türkçeniz notlanmaz. Düz,
  kusurlu cümlelerle yazılmış bir günlük tam puan alır; asistana yazdırılmış bir günlük 4.
  haftadan itibaren 0 alır (1–3. haftalarda en çok 1). Asistanın sözleri Kanıt bloğuna,
  aynen yazdığı gibi aittir. Kanıt bloğunun dışında yalnızca **kalın** yazıyla
  görünebilirler: işaret ettiğiniz bir ifade, tek bir cümle ya da kodundan tek bir satır,
  Kanıt bloğundan harfi harfine kopyalanmış olarak. Kalın yazıyı başka hiçbir şey için
  kullanmayın.

---

## 10. Dönem, teknik teknik

| Hafta | Tekniğin hizmet ettiği teslim | Haftanın tekniği | Durum |
|---|---|---|---|
| 2 | Teklif Bölüm A, gereksinimler | §4 Çapraz sorgu | önerilen |
| 3 | Teklif Bölüm B | §3 Düşman gözden geçiren (yatırımcı) | önerilen |
| 4 | Tıklanabilir prototip, kabul ölçütlerinden test case'ler | §1 Önce kabul ölçütü | zorunlu |
| 5 | Tasarım, API sözleşmesi, sunucu iskeleti, giriş testleri | §2 Çalıştırarak doğrulama | zorunlu |
| 6 | Kendi özelliğiniz uçtan uca: sunucu, testler, web sayfası (dersin girişi bağlanmış) | §3 Düşman gözden geçiren (saldırgan) | zorunlu |
| 7 | Mobil istemci: giriş ve özelliğiniz | §6 Küçük diff'ler | zorunlu |
| 8 | Sohbet botu: sunucunuz barındırılan bir LLM API'sini çağırır, mobil istemcide sohbet ekranı olur; özelliğiniz üç katmanda | §7 Katmanlar arası tutarlılık | zorunlu |
| 9 | Beta test, hata listesi, test raporu | §8 Tahmin ile gözlem | zorunlu |
| 10 | UAT raporu, gönderim | §5 Kaynak gösterttirme, kendi iddialarınız üzerinde | zorunlu |
| 11 | Yayın, inceleme düzeltmeleri | §3 Düşman gözden geçiren (mağaza incelemecisi) | zorunlu |
| 12 | Kapanış, poster | Yeni teknik yok: §9 Dönemin günlüğüne geriye bakış (en pahalıya mal olan hata) | zorunlu |

2. ve 3. haftalarda teknik önerilmişti; 4. haftadan itibaren zorunludur. Haftanın
tekniğine ek olarak herhangi bir hafta başka herhangi bir tekniği de kullanabilirsiniz.
Her haftanın `ai_log_NN.md` iskeleti, haftanın hangi tekniği kullandığını (görev notunda)
söyler ve haftanın `ASSIGNMENT_NN` ödevi bu belgeye gönderme yapar. Her haftanın iki insan
katkısı puanı çoğunlukla yapay zeka günlüğünden, haftanın adını verdiği elle yazılmış
dosyalarla birlikte gelir. Bu puanlar tabloya karşı okunur: haftanın tekniği, uygulanmış
ve kanıtı yapıştırılmış olarak.
Kişilerin adının verildiği haftalarda `group_NN.json` onun yanında okunur.

---

## 11. 14. Hafta'da yapabildiğiniz, 1. Hafta'da yapamadığınız

Aşağıdaki her satır kendi üzerinizde sınayabileceğiniz bir iddiadır. Her biri, §0'daki
dört kişiden birinin diğerlerinden ayrıldığı bir noktayı işaretler.

1. Bir ürün fikri verildiğinde, ne yapması ve ne yapmaması gerektiğini kabul ölçütlü
   numaralı gereksinimler olarak söyleyebilir ve bunları bir asistana tek bir satır
   yazmasından *önce* verebilirsiniz (§1, 2–4. hafta).
2. Üretilmiş birkaç düzine satırı okuyup her parçanın hangi gereksinime hizmet ettiğini ve
   hangi durumu ele almadığını söyleyebilirsiniz (§1, §2, 5. hafta).
3. Çalışan bir programı makul görünen bir programdan ayırabilirsiniz, çünkü onu
   çalıştırdınız, ve farkı gösteren çıktıyı üretebilirsiniz (§2).
4. Kendi işinize yönelik üç güçlü itiraz alıp birini belgede yanıtlayabilir ve birinin
   yanlış olduğunu bir kaynak göstererek ortaya koyabilirsiniz (§3, 3., 6. ve 11. hafta).
5. İki asistana aynı görevi verip cevaplarını karşılaştırabilir ve yanlış olanı, gerekçesi
   kendi belgelerinizden alınmış olarak bulabilirsiniz (§4).
6. Kaynaklı bir olguyu uydurulmuş olandan ayırabilirsiniz, çünkü kaynağı açıp
   tarihlediniz (§5, 3. ve 10. hafta).
7. Aynı diff içinde istediğiniz değişikliği kabul edip istemediğinizi reddedebilirsiniz.
   Geçmişiniz tek büyük bir commit yerine bir hafta boyunca adlandırılmış değişiklikler
   gösterir (§6, haftalık commit disiplini puanı).
8. Üretilmiş üç katmanın birbiriyle nerede çeliştiğini bulabilir, asistanın bulduğunu
   doğrulayabilir ve kaçırdığını yakalayabilirsiniz (§7, 8. hafta).
9. Gerçek insanlar ürününüzü test etmeden önce (9. haftada beta testçiler, 10. haftada
   UAT'de sunumunuzdaki beş kişi) neyin ters gideceğini yazabilir ve sonrasında onların
   listesini sizinkinin yanına koyabilirsiniz (§8).
10. Kullanıcılarınızın ve sınıf arkadaşlarınızın adlarını, numaralarını ve e-posta
    adreslerini bulutta barındırılan bir asistandan ve bir anahtarı repodan, bir kural
    olarak değil bir alışkanlık olarak uzak tutabilirsiniz (§9).
11. Bir asistanın size verdiği hangi sürüm numarasının ve hangi mağaza kuralının eskidiğini
    ve nerede kontrol ettiğinizi söyleyebilirsiniz (§9).
12. Uygulama mağazadan kurulmuş halde bir sınav görevlisinin karşısına çıkıp uygulamanın
    herhangi bir satırı için "Bu neden burada?" sorusunu yanıtlayabilirsiniz. Bunu
    yapabilirsiniz, çünkü push sizindi ve kayıt vardır (§9, 13–14. hafta).

Asistanı olan eğitimsiz kullanıcı bunların hiçbirini yapamaz ve bunu bilmez. Disiplini
olmayan mühendis çoğunu yapabilir ve yapmaz. On iki haftanın amacı, §0'daki sağ sütunun
yaptığını bir alışkanlık olarak yapmanızdır.

---

## 12. Kısa sürüm

Testi istemden önce yazın. Çalıştırılabilen her şeyi çalıştırın. İyi mi diye değil, neden
başarısız olacak diye sorun. İki asistana aynı istemi verin ve nerede ayrıştıklarına bakın.
Asistana kaynağını gösterttirin ve kaynağı açın. Bir seferde bir şeyi değiştirin ve diff'i
okuyun. Üç katmanınızın nerede ayrıştığını sorun ve neyi kaçırdığını kontrol edin. Tahmini
sonucun yanına koyun. Kararı yazın, kanıtı yapıştırın ve kendi hayatınızı
ve insanlarınızı asistandan uzak tutun.

Push sizindir, dolayısıyla kod da sizindir: savunmada "Bu neden burada?" sorusuna "asistan
yazdı" bir cevap değildir. Hiç yanlış yaparken yakalanmamış bir asistan iyi bir asistan
değildir; kimsenin kontrol etmediği bir asistandır.
