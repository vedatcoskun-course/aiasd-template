# Platformlar ve Mağazalar: Ne Geliştirebilirsiniz, Nerede Yayınlayabilirsiniz

AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027

*Prof. Dr. Vedat Coşkun · English: [`AI_PLATFORMS_AND_STORES_EN.md`](AI_PLATFORMS_AND_STORES_EN.md)*

Projeniz bir **mobil uygulama, bir web istemcisi ve bir sunucu** olarak teslim edilir ve
mobil uygulama dönem sonuna kadar **public bir mağazadan yüklenmiş** olmalıdır. Bu el
kitabı, 2. Hafta'da her birinizin sorduğu soruyu yanıtlar: *elimdeki bilgisayar ve
telefonla ne geliştirebilirim, hangi mağazaya gerçekten ulaşabilirim?* Teklifinizin §6
(teknoloji yığını) ve §12 (riskler) bölümlerini yazmadan önce okuyun.

Ücretler, süreler ve mağaza politikaları değişir. Buradaki rakamlar yazıldığı tarihte
geçerli olanlardır; bir plana bağlanmadan önce mağazanın kendi sayfasına bakın.

# 1. Kurallar

- **En az bir public mağazada yayınlarsınız**; hangisi olduğu sizin seçiminiz: Google
  Play, Huawei AppGallery, Samsung Galaxy Store ya da Apple App Store. Biri yeter. Bu
  sınıftaki her bilgisayar + telefon kombinasyonu bunlardan en az birine ulaşabilir (§3).
- **Native Android, native iOS ya da hybrid — üçü de kabul edilir.** Native iOS, bir Mac ve
  Apple'ın yıllık üyeliği demektir; native Android tek platform demektir; hybrid tek kod
  tabanından ikisini de verir. Teslim edebileceğinizi seçin ve §6'da gerekçelendirin.
- **Savunma, mağazadan yüklenmiş build'den yapılır**, o platformun bir telefonunda —
  sizinki ya da salonda ödünç alınan bir telefon. Bir mağazada yayınlayıp kendi telefonunuz
  diğer platformsa uygulamayı kendi telefonunuza da getirin; sınav yapan ikisini de görsün.
- **"Teslim edildi" sayılan tek şey mağaza yayınıdır.** Kendi telefonunuzdaki geliştirici
  build'i test ve gösterim içindir, yayın değildir.

# 2. Native mi hybrid mi?

| | Native | Hybrid |
|---|---|---|
| Android | Kotlin + Jetpack Compose (Android Studio) | Flutter (Dart), React Native / Expo (TypeScript), Capacitor (web teknolojileri) |
| iOS | Swift + SwiftUI (Xcode, **yalnızca Mac**) | yukarıdakiyle aynı kod tabanı; iOS build'i için Mac ya da bulut build hizmeti gerekir |
| Kod tabanı | iki platform istiyorsanız iki | bir |
| Web istemcisi | ayrı | Flutter ve Expo web için de derler; Capacitor zaten web istemcisidir |
| iOS tarafının maliyeti | Mac + Apple Developer üyeliği | aynı — hybrid, Apple'ın ücretini kaldırmaz |
| Ne zaman uygun | dili zaten biliyorsanız ya da tek platform hedefliyorsanız | tek kod tabanından iki platform istiyorsanız ya da Windows bilgisayarınız var ve iOS da istiyorsanız |

Uygulamanızın içindeki sohbet botu (6–7. Haftalar) *sizin sunucunuzla* konuşur; hangi
mobil çatıyı seçtiğiniz onu ilgilendirmez. Denetleyiciyi de. Teslim edebileceğinizi seçin.

# 3. Bilgisayarınız + telefonunuz → yollarınız

Her satır bu sınıftaki birinin kurulumu. **X**, o yolun o mağazaya çıktığı anlamına gelir;
boş hücre, ne yaparsanız yapın çıkmadığı anlamına gelir.

| Bilgisayar + telefon | Geliştirme | Google Play | AppGallery | Galaxy Store | App Store |
|---|---|:---:|:---:|:---:|:---:|
| **Mac + Android** | native Android (Kotlin) | X | X | X | |
| | native iOS (Swift) \*\* | | | | X |
| | hybrid | X | X | X | X |
| **Mac + iPhone** | native Android (Kotlin) \*\* | X | X | X | |
| | native iOS (Swift) | | | | X |
| | hybrid | X | X | X | X |
| **Windows + Android** | native Android (Kotlin) | X | X | X | |
| | native iOS (Swift) | | | | |
| | hybrid | X | X | X | X\* |
| **Windows + iPhone** | native Android (Kotlin) \*\* | X | X | X | |
| | native iOS (Swift) | | | | |
| | hybrid | X | X | X | X\* |

\*\* Telefonunuz diğer platform: emülatör/simülatörde geliştirir ve test edersiniz.

\* Windows'tan iOS binary'si bulutta derlenir (Expo EAS, Codemagic); Apple üyeliği yine
gerekir. Windows'tan native iOS yoktur: Xcode yalnızca Mac'te çalışır. Her App Store hücresi
ayrıca ≈ 99 $/yıl üyeliği varsayar (§4).

Aynı tabloyu sütun sütun okuyun: **dört mağazanın üçü herkese açık** — her bilgisayar, her
telefon, üç geliştirme yolunun herhangi biriyle. Sahip olduklarınıza bağlı olan tek mağaza
App Store.

Tabloda saklı iki gerçek:

- **Bir Android mağazasında yayınlamak için Android telefon gerekmez.** Android
  Studio'daki emülatör geliştirmek ve test etmek için yeter; mağaza paketi her iki durumda
  da kabul eder.
- **Native iOS derlemek için Mac gerekir.** App Store isteyen Windows kullanıcıları iOS
  binary'sini bulutta derleyen Expo EAS ya da Codemagic'ten geçer — ama Apple üyeliğini
  yine siz ödersiniz.

# 4. Mağazalar

| | Google Play | Huawei AppGallery | Samsung Galaxy Store | Apple App Store |
|---|---|---|---|---|
| Geliştirici ücreti | tek seferlik (≈ 25 $) | ücretsiz | ücretsiz | yıllık (≈ 99 $) |
| Kayıt | Google hesabı, kimlik doğrulama | Huawei ID, kimlik belgesi, birkaç günlük onay | Samsung hesabı, satıcı onayı | Apple ID, kimlik doğrulama, ödeme |
| Derleme | Mac ya da Windows | Mac ya da Windows | Mac ya da Windows | Mac (ya da bulut build) |
| Yayından önce | yeni bireysel hesaplar: 14 gün boyunca 12 testçiyle kapalı test | inceleme, birkaç gün | inceleme, birkaç gün | inceleme, genellikle günler; reddedilebilir |
| Bu sınıftaki erişim | neredeyse her Android telefon | Huawei telefonlar; diğerleri AppGallery uygulamasını kurabilir | Samsung telefonlar; diğerleri Galaxy Store'u kurabilir | her iPhone |
| Dikkat | test kanalı kuralı — planlayın, 10. Hafta'da keşfetmeyin | Google servislerine (Firebase, Google Maps, Google Sign-In) bağımlı uygulamalar Huawei telefonlarda çalışmaz ve reddedilebilir | — | tek ücretli yol; Mac gerektiren tek yol |
| Toplam ödediğiniz | ≈ 25 $, bir kez | hiç | hiç | her yıl ≈ 99 $ — öğrenci indirimi yok |

İki sonuç:

- **Google Play'in test kanalı kuralı, planlarsanız bir armağandır.** On dört gün boyunca
  on iki testçi, tam olarak sınıf arkadaşlarınızın testçi olduğu beta haftasıdır (9. Hafta)
  ve o testçiler sizin `contributors_09.json` dosyanızdır. İlk kez 10. Hafta'da duyarsanız
  felakettir. Yalnızca yeni *bireysel* hesaplara uygulanır.
- **Google servislerine bağımlı olmayın.** Girişiniz *kendi* sunucunuzdan e-posta kodu ya
  da OTP ile; öyle kalsın, uygulamanız her mağazada çalışır. Harita ya da push
  gerekiyorsa tek mağazaya bağlı olmayan bir sağlayıcı seçin.
