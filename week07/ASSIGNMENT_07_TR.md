# 7. Hafta Ödevi: Uygulamanız Bir Telefonda

## Beş dakikada bu hafta

Öncelikle bugüne kadar yaptıklarımızı ve şu an hangi aşamada olduğumuzu hatırlayalım. 1., 2., 3. haftalarda sizin ya da çevrenizdeki kullanıcıların yaşadığı bir problemi tespit ettiniz ve kullanıcı gereksinimlerini (requirements) yazdınız. 4. haftada projenin kullanıcı ekranlarını çizdiniz ve test case'lerini yazdınız. 5. haftada tasarımı oluşturdunuz ve API sözleşmesini (API contract) yazdınız; sunucunuz ise bu aşamada 501 döndü. 6. haftada projenizin ilk versiyonu web istemcide ve sunucuda uçtan uca çalıştı.

Bu hafta aynı versiyon web yerine bir telefonda çalışacak. Sunucu tarafı normalde değişmez; değişmesi gerekirse "Web ve telefon için tek bir sunucu" kutusundaki sırayı izleyin.

```text
            web/book.html   ──┐
                              ├──►  POST /bookings   sunucunuz: iki istemci için tek
 mobile/lib/book_screen.dart ─┘     aynı token, aynı cevaplar
```

- Mobil uygulamayı Flutter, React Native–Expo, Kotlin ya da Swift kullanarak geliştirmelisiniz.
- Mobil uygulama, web sayfanızla aynı endpoint'leri çağıracaktır.
- Her ekran, ilgili olduğu gereksinimi bir yorum (comment) ile -örneğin `// serves: REQ-002` gibi- içermelidir. Bu yorum, ekran ile gereksinimi birbirine bağlayacaktır. Böylece telefon ekranı, gereksinimin zincirine (chain) dokuzuncu halka olarak eklenecektir.

Derste Yapılacaklar

| Saat | Yapacağınız iş | § |
|---|---|---|
| dersten önce | Başlamadan önce framework'ünüz kurulu olmalıdır. 6. haftada bunu yapmış olmalısınız. Kurulum için framework'ünüzün kendi sayfasını izleyin: Flutter için docs.flutter.dev/get-started/install, Expo için docs.expo.dev/get-started/set-up-your-environment, Kotlin için Android Studio (developer.android.com/studio), Swift için Mac App Store'daki Xcode. `AI_PLATFORMS_AND_STORES` belgesinin 3. bölümü, bilgisayarınız ve telefonunuzla hangi yolu seçebileceğinizi gösterir. | - |
| 09:30 | Denetleyiciyi (checker) çalıştırın. Denetleyici `week07/` klasörünü getirecektir. Sonra commit ve push edin. | §1 |
| yaklaşık 10:00 | Uygulamanızı `mobile/` içinde oluşturun. Kimliği S2'nin paket adı olmalıdır. Uygulama telefonunuzda ya da bir emülatörde çalışmalıdır. | §2 |
| yaklaşık 10:45 | Telefondaki giriş (login) ekranı sunucunuzla konuşmalıdır. Ekran görüntüsünü `week07/phone_login.png` olarak kaydedin. | §3 |
| yaklaşık 11:15 | 6. haftada ilk oluşturduğunuz gereksinimin ekranını yapın. Bu ekran, o gereksinimin `api.md` içindeki endpoint'lerine istek göndermelidir, örneğin `POST /bookings`. | §4 |
| 11:45 | Testçi turunu yapın: bir sınıf arkadaşınız test case'lerinizi sizin telefonunuzda çalıştırsın, siz de onunkileri onun telefonunda çalıştırın. Arkadaşınızın her çalıştırmasını `mobile_runs.json` dosyasına, numarasını ve bulgusunu `group_07.json` dosyasına yazın. Sonra son kez push edin. | §5–§7 |

Cumartesi 23:59'a kadar

- Her işlevsel (functional) `must` gereksinimin `mobile/` içinde karşılığı olan bir ekranı olmalıdır. Ekran, gereksinimin `api.md` içindeki endpoint'lerine istek göndermelidir (§8).
- Her işlevsel `must` gereksinimin telefonda geçmiş bir test case'i olmalıdır. Başarısız olan her test case'i yeniden çalıştırın (§9).
- Uygulamanızın kimliği S2'nin paket adı olmalıdır (§10).
- Testçinizin bulgusuyla ne yapacağınıza karar verin (§11).
- Git, uygulamanızın build klasörlerini tutmamalıdır (§12).
- Testler GitHub'da hala yeşil olmalıdır (§13).
- AI log'u, uygulamanızdaki küçük bir değişiklik üzerine yazın (§15).

Notlandırma: Ders içi bölüm 5 puan üzerinden değerlendirilecektir. Cumartesi'ye kadar teslim edilen bölüm de 5 puan üzerinden değerlendirilecektir. Ayrıntılar bu ödevin sonundaki "Bu hafta nasıl notlandırılır" bölümünde yer almaktadır.

Gelecek haftalarda ürününüz sohbet botunu (chatbot) içerecektir. Uygulamanız sunucuda, web'de ve telefonda tamamlanacak ve ilk build'iniz mağazanın (store) test kanalına (test track) çıkacaktır. 9. haftada gerçek testçiler, 10. haftada gerçek kullanıcılar devreye girecektir. Sonrasında store tarafından uygulamanız incelenecektir. Sunum öncesinde uygulamanızı yüklemiş olduğunuz mağazadan indirerek kuracaksınız.

8. haftadan önce testçilerinizin e-posta adreslerini toplayın. Yeni bir kişisel Google Play hesabı 14 gün boyunca 12 testçi ister. Kullanacağınız LLM API'sinde bir hesap da açın. Bu hesabın anahtarı (key) yalnızca `.env` dosyasına girmelidir.

## Zincire bir halka daha ekleniyor

İşlevsel gereksinimlerinizin her biri bir halka zinciridir. Bu hafta zincirin dokuzuncu halkası oluşacaktır.

| Halka | Nerede durur | Ne zamandan beri |
|---|---|---|
| 1 ve 2. Gereksinim ve Kullanım Senaryoları (use case) | `week02/requirements.json` ve `week02/SRS.md` | 2. hafta |
| 3. Ekranlar, `serves:` ile | `week04/prototype/` | 4. hafta |
| 4. Test case'ler, her biri `"run"` ile | `week04/test_cases.json` | 4. hafta |
| 5. API sözleşmesindeki satırlar | `week05/api.md` | 5. ve 6. haftalar |
| 6 ve 7. Route'lar ve GitHub'da yeşil olan testler | `server/` ve `server/tests/` | 6. hafta |
| 8. Web istemcisindeki sayfa | `web/` | 6. hafta |
| 9. Mobil istemcideki ekran; bu ekran aynı endpoint'lere istek gönderir | `mobile/`, `// serves: REQ-…` ile | Bu hafta |

Kaynak (source) hala `requirements.json` dosyasıdır. Telefon ekranı, web sayfası gibi, gereksinimin ve test case'lerinin söylediğini yapmalıdır. Telefon bir halkanın yanlış olduğunu gösterirse önce o
halkayı değiştirin. Değişiklik için `PROPOSAL.md` içine bir satır yazın. Bir gereksinim ya da bir test case
için bu satır bir değişiklik talebidir (change request), 6. hafta §9'daki gibi.

### Bu hafta bilmeniz gerekenler

| Terim | Anlamı |
|---|---|
| Mobil istemci (mobile client) | Mobil istemci, telefondaki uygulamadır. Ekranları gösterir ve sunucunuzu çağırır. Kararı yalnızca sunucunuz verir. |
| `mobile/` | `mobile/`, uygulamanızın klasörüdür. Reponuzun kökünde, `server/` ve `web/` yanında durur. Onu framework'ünüzün kendi aracıyla oluşturun (§2). |
| Emülatör, simülatör (emulator, simulator) | Emülatör ya da simülatör, dizüstü bilgisayarınızda bir program olarak çalışan bir telefondur. Android Studio'da Android emülatörü vardır. Xcode'da iOS simülatörü vardır ve Xcode yalnızca Mac'te çalışır. |
| Sunucunun adresi | Android emülatörü sunucunuza `10.0.2.2` adresinden ulaşır. iOS simülatörü ona `127.0.0.1` adresinden ulaşır. Gerçek bir telefon ona dizüstü bilgisayarınızın Wi-Fi ağındaki adresinden ulaşır (§3). |
| `--host 0.0.0.0` | Bu seçenek sunucunuzu, ağdaki başka cihazların da ulaşabileceği biçimde başlatır. Bu seçenek olmadan sunucuya yalnızca dizüstü bilgisayarınız ulaşır. |
| Endpoint, yol (path) | Endpoint, `api.md` içindeki bir satırdır, örneğin `POST /bookings`. Yolu, `/` ile başlayan kısmıdır, örneğin `/bookings`. Uygulamanız, web sayfanız gibi, isteklerini bu endpoint'lere gönderir. |
| Düz http (plain http) | Sunucunuz `https` değil, `http` konuşur. Android ve iOS, uygulama izin vermedikçe düz http'yi reddeder (§3). |
| Uygulama kimliği (app id) | Uygulama kimliği, Android'de `applicationId`, iOS'ta bundle id'dir. Bu kimlik, 6. haftada S2 için seçtiğiniz paket adıdır, örneğin `com.example.studyroom`. |
| `week07/mobile_runs.json` | Bu dosya, telefonda çalıştırılan test case'leri kaydeder. 4. haftadaki walk-through gibi çalışır. |
| Testçi (tester) | Testçi, 3. hafta grubunuzdan bir sınıf arkadaşınızdır. Testçi, derste test case'lerinizi telefonunuzda çalıştırır. |
| Küçük diff (small diff) | Küçük diff, bir asistandan istediğiniz tek bir değişikliktir. Değişikliği kabul etmeden önce satır satır okumalısınız (`AI_Doc5` §6). Diff, bir değişikliğin satır satır gösterimidir. Küçük diff'ler bu haftanın tekniğidir. |

> ## İşin ortasında commit edin, sonunda değil
>
> Yukarıdaki saatler bir tempo gösterir. Bu saatler push saatleri değildir. Her işi daha bitmeden commit
> edin. Örneğin alanlarını gösteren ama henüz sunucuyu çağırmayan bir ekranı commit edin. İş çalışınca onu
> yeniden commit edin. Her commit'i hemen push edin. Tek commit'te bitmiş olarak gelen bir iş, commit puanına
> sayılmaz.
> Bitmemiş bir işi push ettikten sonra kırmızı bir kontrol görmeniz normaldir ve size puan kaybettirmez. Ders
> notu yalnızca dersin sonundaki son push'unuzu okur.
>
> - **İlk push'unuz GitHub'a 09:30'dan önce ulaşmalıdır.** Derse denetleyiciyi çalıştırarak başlayın. Sonra
>   commit ve push edin. İlk push'unuz GitHub'a 09:30'dan sonra ulaşırsa ders işiniz için hangi bilgisayarı
>   kullandığınızı elle incelerim. Nedeni önemli değildir; geç gelmek de bir istisna değildir.
> - Çağırdığımda commit ve push edin. Ders sırasında, seçtiğim anlarda "şimdi commit ve push" derim.
>   O zaman herkes aynı anda commit ve push yapmalıdır. Her push 5 dakika içinde GitHub'a ulaşmalıdır.

> ## AI log'u tümü ile siz yazmalısınız
>
> `week07/ai_log_07.md` dosyasını kendiniz, kendi cümlelerinizle yazın. Evidence bloğu ve asistanın
> cevabından yaptığınız kalın alıntılar (§15) tek istisnadır. Günlüğün geri kalanında asistan kullanmayın.
> Asistanı günlüğü yazmak, "düzeltmek" ya da dilinizi düzeltmek için de kullanmayın. **Asistanın yazdığı bir
> günlük 0 puan alır.** İngilizceniz ya da Türkçeniz notlanmaz. Her günlüğü bir insan okur.

> ## Sizin yazacağınız iki dosya
>
> `week07/mobile_runs.json`, testçinizin telefonunuzda çalıştırdığı her test case'i kaydeder. Testçinin
> ne gördüğünü de kaydeder. `week07/group_07.json`, testçinizi ve testçinin bulduğu en yararlı şeyi
> yazar. Sonra kararınızı da tutar. İki dosyayı da testçi turu sırasında yazın. Hiçbir asistan bu dosyaları
> yazmaz, düzeltmez ya da tamamlamaz.

> ## Web ve telefon için tek bir sunucu
>
> Telefon, web sayfanızla aynı endpoint'leri çağırmalıdır. Aynı alanları ve aynı token'ı göndermelidir.
> Bazen telefon, sunucunun değişmesi gerektiğini gösterir: web sayfasının ortaya çıkarmadığı bir hata ya
> da telefonun ihtiyaç duyduğu ama sunucunun vermediği bir şey. O zaman sunucuyu iki istemci için birlikte
> şu sırayla değiştirin: önce `api.md` satırı ve Change log'da neyin, neden değiştiğini söyleyen bir satır
> (bir gereksinim ya da test case değişiyorsa bir change request), sonra route ve testi, kendi
> commit'inde. Web sayfası çalışmaya devam etmeli ve bütün testler yeşil kalmalıdır. Telefonun ortaya
> çıkardığı ve nedeniyle birlikte yazılmış bir sunucu değişikliği iyi bir işarettir: işinizi telefonda
> gerçekten test ettiğinizi gösterir. Bir endpoint'in yalnızca telefon için ikinci, farklı bir sürümünü
> asla yapmayın. Giriş, 6. haftadaki gibi dersin girişidir. Telefon üç giriş endpoint'inizi kullanmalıdır.

> ## Asla force push yapmayın
>
> `git push --force` geçmişinizden commit siler. Çalışmanızı bu geçmişe bakarak notlandırırım. CI bir ruff
> hatası ya da bir yazım hatası yüzünden kırmızı olursa hatayı düzeltin. Sonra düzeltmeyi yeni bir commit
> olarak push edin. Küçük bir düzeltme size hiçbir şeye mal olmaz.
> **Force push, neyi değiştirmiş olursa olsun, size o haftanın commit puanına mal olur.** Buna `git push -f`,
> `git push --force-with-lease`, VS Code'daki "Force Push" ve GitHub Desktop'taki "Force push origin" düğmesi de dahildir.

> Bunları hazır tutun: S2'nin paket adına ihtiyacınız var; bu ad `week04/store.json` içindedir. Üç giriş
> endpoint'inize de ihtiyacınız var; bunlar `server/login_contract.json` içindedir. Telefonunuz diğer
> platformdansa emülatörü ya da simülatörü kullanın (`AI_PLATFORMS_AND_STORES` §3). Kotlin ile bir iPhone
> bunun bir örneğidir; Swift ile bir Android telefon da başka bir örnektir.

---

## Bu haftayla ne geliyor

- `week07/` klasörü bu ödevi, `ai_log_07.md`, `group_07.json` ve `mobile_runs.json` dosyalarını içermektedir.
  `group_07.json` testçinizi içerecektir. `mobile_runs.json` telefondaki test case'lerinizi içerecektir.
- `server/course_login.py` dosyası güncellendi. Yalnızca yorumları (comments) değişti: e-posta örnekleri artık `.edu.tr` ile bitecektir. Bu dosya dersin dosyasıdır; onu değiştirmeyin. Denetleyiciyi çalıştırdığınızda, denetleyici dosyanın yeni sürümünü reponuza indirir ve eskisinin yerine yazar. Başka bir şey yapmanız gerekmez; değişen dosyayı ilk commit'inizle birlikte commit edin.

Python paketleriniz değişmez ve `week06/requirements.txt` kalır. Framework'ünüz kendi paketlerini
`mobile/` içine getirir.

---

## Bu hafta asistan nerede yardım eder, nerede etmez

| İş | Asistan |
|---|---|
| Uygulamayı `mobile/` içinde oluştururken; build'in, emülatörün ya da ağın bir hatasını okurken | Asistan yardım eder. |
| Bir ekranın kodunu yazarken | Asistan yardım eder. İstem (prompt) gereksinimi, kabul ölçütünü (acceptance criterion), `api.md` satırlarını ve web sayfasını içermelidir. Her ekran kendi commit'ini alır. |
| Elinizdeki kodda tek bir değişiklik yaparken | Asistan yardım eder. Değişikliği kabul etmeden önce satır satır okuyun (§15). Onay sizindir. |
| Gereksinim söylemediğinde ekranın ne yapacağını seçerken | Asistan yardım etmez. Gereksinim karar verir. Gereksinim bir şey söylemiyorsa önce gereksinimi değiştirin (6. hafta §9). |
| Yalnızca telefon için yeni bir endpoint ya da sunucunun farklı bir cevabını isterken | Asistan yardım etmez. Sunucu aynı kalır. Yeni bir ihtiyaç, `api.md` içinde yeni bir satırdır. |
| `week07/mobile_runs.json` ve `week07/group_07.json` dosyalarını yazarken | Asistan yardım etmez. |
| Change log satırlarını ve change request'leri yazarken | Asistan yardım etmez. |
| `ai_log_07.md` dosyasını, Evidence bloğu ve kalın alıntıları dışında yazarken | Asistan yardım etmez. |

---

## Derste: 11:45'e kadar push

Dersin beş bölümü vardır:

1. İlk push'u yapın ve "Beş dakikada bu hafta" bölümünü okuyun. Bu bölüm yaklaşık 09:30'da biter.
2. Uygulamanızı `mobile/` içinde oluşturun ve çalıştırın. Bu bölüm yaklaşık 10:00'da biter.
3. Girişi telefonda çalıştırın. Bu bölüm yaklaşık 10:45'te biter.
4. 6. haftada ilk kurduğunuz gereksinimin ekranını yapın. Bu bölüm yaklaşık 11:15'te biter.
5. Bir sınıf arkadaşınızla testçi turunu (tester round) yapın. Bu bölüm 11:45'te biter.

Her bölümde işi daha bitmeden commit ve push edin. İş çalışınca yeniden commit ve push edin.

### 1. İlk push: 09:30'dan önce

Bunu dersin başında yapın.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week07: course files"
git push
```

Denetleyici `week07/` klasörünü getirir. Bu push, ders işinizin kendi bilgisayarınızda başladığını gösterir. Bu push'tan önce `git config user.name` ve `git config user.email` komutlarını çalıştırın. Bu komutlar kendi adınızı ve GitHub hesabınızın e-posta adresini göstermelidir. Başka bir kişinin adıyla ya da e-postasıyla yapılan bir commit sizin işiniz sayılmaz.

### 2. Uygulamanız `mobile/` içinde

Bunu derste, yaklaşık 10:00'a kadar yapın.

Uygulamayı framework'ünüzün kendi aracıyla oluşturun. Onu reponuzun kökünde, `mobile` adlı bir klasörde,
`server/` ve `web/` yanında oluşturun. `AI_README_TR.md` belgesinin "Reponuz, klasör klasör" bölümü bu yeri
gösterir. Uygulamaya kimlik olarak S2'nin paket adını verin. Tablo örnek olarak `com.example.studyroom`
adını kullanır.

| Framework | Uygulama nasıl oluşturulur (reponuzun kökünde) | Kimlik nereden gelir |
|---|---|---|
| Flutter | `flutter create --org com.example --project-name studyroom mobile` komutunu çalıştırın. | Flutter kimliği `--org` ve `--project-name` değerlerinden oluşturur. |
| React Native–Expo | `npx create-expo-app@latest mobile` komutunu çalıştırın. | Kimliği `app.json` içinde `"android": {"package": …}` ve `"ios": {"bundleIdentifier": …}` alanlarına yazın. |
| Kotlin (Android Studio) | New Project → Empty Activity seçin. Save location alanına reponuzun `mobile` klasörünü yazın. | Kimliği aynı sayfadaki Package name alanına yazın. |
| Swift (Xcode, yalnızca Mac'te) | New Project → App (SwiftUI) seçin. Projeyi reponuzun `mobile` klasörüne kaydedin. | Organization Identifier alanına `com.example`, Product Name alanına `studyroom` yazın. Xcode, Bundle Identifier olarak `com.example.studyroom` gösterir. |

Yeni uygulamayı, hiçbir şeyi değiştirmeden önce, telefonunuzda ya da emülatörde çalıştırın:

- Flutter ile `flutter run` komutunu çalıştırın.
- Expo ile `npx expo start` komutunu çalıştırın. Sonra QR kodunu Expo Go ile okutun ya da Android emülatörü
  için `a` tuşuna basın.
- Kotlin ya da Swift ile Android Studio'nun ya da Xcode'un Run düğmesine basın.

Uygulama çalışınca commit ve push edin. Mac'iniz yoksa iOS build'i yapmanız gerekmez; Android emülatörü ya da bir Android telefon yeterlidir.

**Build dosyalarını asla commit etmeyin.** Framework'ünüz, yeniden üretebileceği büyük klasörler yazar:
`node_modules/`, `build/`, `.dart_tool/`, `.gradle/`, `Pods/` ve `.expo/`. Framework'ünüzün aracı genellikle
`mobile/` içine bir `.gitignore` dosyası koyar ve bu dosya bu klasörleri listeler. İlk commit'ten önce
`git status` komutunu çalıştırın ve bu klasörlerden hiçbirinin görünmediğini kontrol edin. Bunlardan biri
görünürse onu `mobile/.gitignore` dosyasına ekleyin.

### 3. Telefonda giriş

Bunu derste, yaklaşık 10:45'e kadar yapın.

Önce telefon sunucunuza ulaşmalıdır. Sunucuyu, başka cihazların ulaşabileceği biçimde başlatın:

```bash
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

| Uygulama nerede çalışıyor | Uygulamadaki sunucu adresiniz |
|---|---|
| Android emülatörü | `http://10.0.2.2:8000` |
| iOS simülatörü (Mac'te) | `http://127.0.0.1:8000` |
| Dizüstü bilgisayarınızla aynı Wi-Fi ağındaki gerçek bir telefon | Önce `http://`, sonra dizüstü bilgisayarınızın adresini, sonra `:8000` yazın. Windows'ta `ipconfig` komutu adresi IPv4 Address olarak gösterir. macOS'ta `ipconfig getifaddr en0` komutu adresi gösterir. |

- Adresi uygulamanızda tek bir yere, bir sabit (constant) olarak koyun. Böylece yeni bir ağda yalnızca
  tek bir satır değişir.
- Windows, Python'un ağı kullanıp kullanamayacağını sorar. Özel ağlar (private networks) için izin verin.
- Adresi önce telefonun tarayıcısında deneyin. Tarayıcıda `http://<adres>:8000/docs` adresini açın.
  Telefonun tarayıcısı bu sayfayı açamıyorsa uygulama da sunucuya ulaşamaz.
- Bazı Wi-Fi ağları telefonun dizüstü bilgisayara ulaşmasına izin vermez. Kampüs ağı da bunlardan biri
  olabilir. Böyle bir ağda telefonunuzun hotspot'unu açın ve dizüstü bilgisayarınızı ona bağlayın. Emülatörü
  de kullanabilirsiniz.

İkinci olarak, uygulama düz http kullanabilmelidir:

| Framework | Ne eklenir |
|---|---|
| Android'de Flutter ya da Kotlin | `AndroidManifest.xml` dosyasına `<uses-permission android:name="android.permission.INTERNET"/>` satırını ekleyin. `<application>` üzerine de `android:usesCleartextTraffic="true"` ekleyin. Flutter'da dosya `android/app/src/main/AndroidManifest.xml` yolundadır. |
| iOS'ta Flutter ya da Swift | `Info.plist` içinde `NSAppTransportSecurity` → `NSAllowsLocalNetworking` değerini YES yapın. |
| Expo Go | Bir şey eklemenize gerek yoktur. |

Sonra giriş ekranını yapın. Giriş ekranı, `web/login.html` sayfanızın yaptığını yapmalıdır. E-postayı
sormalı ve request_code endpoint'inize istek göndermelidir. Sonra kodu sormalı, login endpoint'inize istek
göndermeli ve token'ı saklamalıdır. Token'ı bellekte,
uygulamanızın bir değişkeninde tutun. Uygulama yeniden başlayınca kullanıcı yeniden giriş yapar; şimdilik bu
sorun değildir. Derste sunucuyu, 6. haftadaki gibi, `AIASD_CODE_FILE` ayarlıyken başlatın. Sunucu kodu dizüstü
bilgisayarınızdaki o dosyaya yazar. Siz de kodu telefona yazın.

Ekranın kaynak dosyası, hizmet ettiği gereksinimleri bir yorumda adlandırmalıdır: `// serves: REQ-001, REQ-006`.
Her endpoint'in yolunu `api.md` içindeki gibi, `/` işaretiyle yazın, örneğin `/auth/code`. Yolları ekranın
kodunda ya da yardımcınızda (helper) yazın.

Aşağıdaki kod, Flutter'da küçük bir yardımcıdır. Önce paketini `flutter pub add http` ile ekleyin.

```dart
// mobile/lib/api.dart
import 'dart:convert';

import 'package:http/http.dart' as http;

const server = 'http://10.0.2.2:8000'; // the Android emulator; a real phone: your laptop's address
String? token; // in memory: log in again after a restart

Future<http.Response> call(String method, String path, [Map<String, dynamic>? body]) {
  final uri = Uri.parse('$server$path');
  final headers = {
    'Content-Type': 'application/json',
    if (token != null) 'Authorization': 'Bearer $token',
  };
  return method == 'POST'
      ? http.post(uri, headers: headers, body: jsonEncode(body ?? {}))
      : http.get(uri, headers: headers);
}
```

Aşağıdaki kod, React Native–Expo'daki aynı yardımcıdır. Expo'da `fetch` zaten vardır.

```javascript
// mobile/api.js
export const SERVER = "http://192.168.1.23:8000"; // your laptop's address on the same Wi-Fi
let token = null;
export const setToken = (t) => { token = t; };

export async function api(method, path, body) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(SERVER + path, {
    method, headers, body: body === undefined ? undefined : JSON.stringify(body),
  });
  return { status: response.status, data: await response.json().catch(() => ({})) };
}
```

Kotlin ve Swift aynısını kendi araçlarıyla yapar. Kotlin `HttpURLConnection` ya da OkHttp kullanır, Swift
`URLSession` kullanır.

- Yanlış bir kod 401 alır. O zaman ekran, web sayfanızdaki gibi "Wrong code" göstermelidir.
- Girişten sonra ekran, giriş yapan kullanıcının adresini göstermelidir. Bu adresi almak için "me"
  endpoint'inize token'la istek gönderin.

Telefon giriş yapmış adresi gösterince telefonda ya da emülatörde bir ekran görüntüsü (screenshot) alın.
Onu `week07/phone_login.png` ya da `.jpg` olarak kaydedin. Sonra commit ve push edin.

### 4. İlk gereksiniminizin ekranı

Bunu derste, yaklaşık 11:15'e kadar yapın.

6. haftada ilk kurduğunuz gereksinimi alın. Onun ekranını telefonda yapın. Ekranda web sayfasındaki alanlar ve
düğmeler olmalıdır ve ekran
isteklerini aynı endpoint'lere göndermelidir.

```dart
// mobile/lib/book_screen.dart
// serves: REQ-002
final response = await call('POST', '/bookings', {'room': 3, 'start': '14:00', 'minutes': 60});
setState(() => message = response.statusCode == 201
    ? 'Booked.'
    : jsonDecode(response.body)['detail'] as String);
```

- Ekran, sunucunun retlerini (refusals) web sayfasındaki gibi, test case'lerinizin sözleriyle göstermelidir.
- Bir 401, kullanıcıyı giriş ekranına geri göndermelidir.
- Kararı sunucu verir, uygulama yalnızca gösterir. Bir kuralı yalnızca uygulama kontrol ederse o kuralı
  kimse kontrol etmez, çünkü bir kullanıcı sunucunuzu uygulama olmadan da çağırabilir.
- Ekran, tasarımınızı, yani prototipinizin ekranını, bir telefonun genişliğinde izlemelidir.

### 5. Testçi turu: `week07/mobile_runs.json`

Bunu derste, yaklaşık 11:15 ile 11:45 arasında yapın.

3. haftadaki grubunuz yeniden buluşur. Her biriniz bir grup arkadaşınızın (groupmate) testçisi olur.
Uygulama, sahibinin telefonunda ya da emülatöründe çalışır. Testçi uygulamayı bir kullanıcı gibi kullanmalıdır. Testçi, sahibinin `week04/test_cases.json` içindeki test
case'lerini çalıştırmalıdır:

- Testçi en az üç test case çalıştırmalıdır ve bunlardan en az biri girişin dışında olmalıdır.
- Sahibi izlemeli ve yardım etmemelidir.

Turdan hemen sonra sahibi her çalıştırmayı elle `week07/mobile_runs.json` dosyasına yazmalıdır:

- `tc`, test case'in kimliğidir (id). `tester`, testçinin 9 haneli numarasıdır.
- `device`, telefonu ya da emülatörü adlandırır, örneğin "Samsung A52, Android 14" ya da "Pixel 7 emulator".
- `round` 1'dir. `result`, `pass`, `fail` ya da `blocked` olur.
- `note`, testçinin ne gördüğünü tek bir tam cümleyle söylemelidir. `fail` ve `blocked` sonuçlarında not zorunludur.

Sonra rolleri değiştirin. Grubunuzdan derste kimse yoksa herhangi bir sınıf arkadaşınızla çalışın. Testçi
telefonunuzu ya da dizüstü bilgisayarınızı yalnızca test etmek için kullanır. Kimse bir sınıf arkadaşının
bilgisayarında commit etmez.

Testçiniz derste sizinle birlikte olmalıdır. Derste olmayan bir testçi, hiç testçi yazılmamış sayılır ve bonus
almaz. 1. turu derste push edin: GitHub'a ilk kez dersten sonra ulaşan bir 1. tur eksik sayılır. Kaçırdığınız
bir dersin testçi turu telafi edilemez.

### 6. Testçiniz: `week07/group_07.json`

Bunu derste, testçi turundan hemen sonra yapın.

Bir kayıt yazın. Kayıt testçinizin numarasını ve `"tester"` rolünü tutmalıdır. `what` alanına, testçinin bulduğu
ya da söylediği en yararlı şeyi tek bir tam cümleyle alıntılayın. `accepted` ve `why` Cumartesi'ye kadar
bekler (§11).

### 7. Push edin ve sonucu GitHub'da kontrol edin

Push etmeden önce `ruff check . --fix` ve `ruff format .` komutlarını çalıştırın. Ruff yalnızca Python
dosyalarını okur; bu yüzden uygulamanızın dosyaları ruff'ın sonucunu değiştirmez.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week07: tester round, mobile_runs.json"
git push
```

Actions sekmesini açın. 7. haftanın kontrolleri orada çalışır. Sunucunuzun testleri de orada çalışır. Bir
çalıştırma başlamazsa ve GitHub ödeme (billing) ya da harcama sınırı (spending limit) ile ilgili bir mesaj
gösterirse https://github.com/settings/billing sayfasını açın ve sorunu giderin. Hiç başlamayan bir
çalıştırma test sonucu vermez.

Her işi ortasında commit edin ve çalışınca yeniden commit edin. Her commit'i hemen push edin. Son commit'inizi
11:45'e kadar push edin. Ders notu (lecture mark), dersin sonuna dek push ettiğiniz son commit'i okur.

---

## Cumartesi 23:59'a kadar

### 8. Her işlevsel 'must' gereksinim tamamlanmalı

Derste bunu giriş ekranı ve ek olarak bir gereksinim için yaptınız. Şimdi bütün işlevsel `must` gereksinimlerini içerecek şekilde tamamlamalısınız. Her bir gereksinim için şunlar gerekmektedir:

- Gereksinimin `mobile/` içinde bir ekranı olmalıdır. Ekranın kaynak (source) dosyası gereksinimi `// serves: REQ-…` ile adlandırmalıdır.
- Ekran, gereksinimin `api.md` içindeki endpoint'lerine istek göndermelidir.
- Ekran, web sayfasındaki gibi, sunucunun cevaplarını ve retlerini göstermelidir.

Bir ekran birkaç gereksinime hizmet edebilir. `should` ve `could` gereksinimler sonraki hafta tamamlanabilir.

Bazı parçalar web'de çalışmaz, yalnızca telefonda çalışır; kamera, bildirimler (notifications) ve konum (location) bunlara
örnektir. İşlevsel bir `must` gereksiniminiz bunlardan birine ihtiyaç duyuyorsa o parçayı bu hafta telefonda geliştirmelisiniz. Sunucu tarafı 6. haftadan beri hazırdır.

### 9. Her gereksinim telefonda test edilmiş olmalı

`week07/mobile_runs.json` dosyasına, her işlevsel `must` gereksinimin en az bir test case'i telefonda
`pass` alana kadar yeni çalıştırmalar eklemelisiniz. Dersten sonra test case'leri kendiniz ya da testçinizle, çevrim içi ya da yüz yüze çalıştırın. Eğer kendiniz çalıştırıyorsanız, `tester` alanına kendi numaranızı yazın.

- Dersten sonraki her çalıştırmanın `round` değeri 2 olmalıdır.
- 1. turda başarısız olan her test case, düzeltmeden sonra 2. turda yeniden çalışmalıdır. Bir test case'i bir change request ile de bırakabilirsiniz (6. hafta §9).

### 10. Uygulama kimliği S2 paketinizdir

Uygulamanızın kimliği, `week04/store.json` içindeki S2'nin paket adı olmalıdır. Kimlik şuralarda kullanılmaktadır:

- Flutter'da kimlik, `android/app/build.gradle(.kts)` içindeki `applicationId` değeridir.
- Kotlin'de kimlik, `app/build.gradle(.kts)` içindeki `applicationId` değeridir.
- Expo'da kimlik, `app.json` içindeki `android.package` ve `ios.bundleIdentifier` değerleridir.
- Xcode'da kimlik, `PRODUCT_BUNDLE_IDENTIFIER` değeridir.

İlk build'iniz 8. haftada bu kimlikle store'a gider. Ondan sonra kimlik asla değişemez.

### 11. Testçinin bulguları: kararınız

`group_07.json` içine `accepted` ve `why` ekleyin. Bulgu yüzünden bir şeyi değiştirirseniz `accepted` değerini `true` yapın. Hiçbir şeyi değiştirmezseniz `false` yapın. `why` alanına tek bir tam cümle yazın. Bu cümle, neyi değiştirdiğinizi ya da bulgunun neden gerçek bir sorun olmadığını içerecektir. Bir gereksinimde ya da bir test
case'te değişiklik bir change request'tir (6. hafta §9).

### 12. Build klasörleri repoya commit edilmemelidir

`git ls-files mobile` komutu `node_modules/`, `build/`, `.dart_tool/`, `.gradle/`, `Pods/` ya da `.expo/`
listelememelidir. Bunlardan birini commit ettiyseniz onu `mobile/.gitignore` dosyasına ekleyin. Sonra
`git rm -r --cached mobile/<klasör>` komutunu çalıştırın, commit ve push edin. Dosyalar bilgisayarınızda kalır.

### 13. Sunucu ve web yeşil kalmalıdır

Mobil geliştirme yapılırken sunucu tarafı bir testi bozacak biçimde asla değiştirilmemelidir. On ders
testinin hepsi GitHub Actions'ta yeşil kalmalıdır. `"run": "server"` olan her `must` test case'inin testleri
de yeşil kalmalıdır. `web/` içindeki sayfalarınız çalışmaya devam etmelidir. `.github/workflows/check.yml` ve `.github/check_deliverables.py` dosyalarını asla değiştirmeyin: değiştirilmiş bir workflow'un çalıştırması notlarda hiç sayılmaz.

### 14. Her yeni test case nasıl çalıştırılmalıdır

Telefon için yeni bir test case bir change request ile gelmelidir. Onun `"run"` değeri `"manual"` olmalıdır, çünkü bu test case'i bir insan telefonda çalıştırır.

### 15. Küçük diff'ler: `week07/ai_log_07.md`

Bu haftanın tekniği küçük diff'lerdir (`AI_Doc5` §6). Mobil istemcinizde tek bir değişiklik seçin.
Üç örnek şunlardır. Ekran, sunucunun 409 mesajını gösterir. Uygulama, bir 401'den sonra kullanıcıyı girişe geri gönderir. Uygulama, sunucunun adresini tek bir sabitte tutar.

1. Asistandan yalnızca bu değişikliği isteyin. Ona dosyayı verin ve tam olarak neyin değişeceğini söyleyin.
2. Kabul etmeden önce diff'in tamamını okuyun, istemediğiniz satırları da aynı şekilde. `git diff` diff'i gösterir.
3. İstediğiniz kısmı tutun. Diğer her değişikliği, iyi olsa bile, reddedin.
4. Kabul ettiğiniz değişikliği, onu adlandıran bir mesajla, tek başına commit edin. Commit kimliğini günlüğe yazın. Kimliğin ilk 7 karakteri yeterlidir.
5. Ekranı telefonda çalıştırın ve değişikliğin çalıştığını gösterin.

Günlüğe istediğiniz değişikliği ve aldığınız değişikliği yazın. Neyi reddettiğinizi ve nedenini yazın.
Commit'i yazın. `ME:`, `AI:` ve `TERMINAL:` kısımlarını Evidence bloğuna yapıştırın. `TERMINAL:` kısmı
`git diff` çıktısını, dokunulmadan, tutar.

AI log'u siz yazmalısınız. Evidence bloğu ve kalın alıntılar dışında asistan kullanmayın. **Asistanın yazdığı bir günlük 0 puan alır.**

### 16. Yeniden push edin, kontroller yeşil olsun

Çalışırken birkaç commit yapın. **Her commit `mobile/` içine en fazla bir yeni ekran ve `server/` içine en fazla bir yeni route eklemelidir. İki ya da daha fazlasını ekleyen bir commit, size o haftanın commit puanına mal olur.** Bir ekran, dosyasına `// serves:` satırının ilk kez yazıldığı commit'te yeni sayılır; bu yüzden framework'ünüzün aracının oluşturduğu dosyalar o zamana kadar sayılmaz. Yalnızca taşıdığınız ya da kodunu değiştirdiğiniz bir ekran veya route yeni sayılmaz. Bir commit ya da henüz commit etmediğiniz değişiklikleriniz iki ya da daha fazlasını eklediğinde denetleyici sizi uyarır. Ders dışında yeni iş içeren en az iki commit'i, aralarında en az bir saat olacak şekilde push edin.
Bir kodlama ajanının (coding agent) yaptığı commit hiçbir zaman sayılmaz. Asla force push yapmayın ve bir asistanın yapmasına da izin
vermeyin. Sonra aşağıdaki kontrol listesine bakın.

---

## Teslim kontrol listesi

Derste, 11:45'e kadar push
- [ ] İlk push'unuz GitHub'a 09:30'dan önce ulaşmalıdır.
- [ ] `mobile/` klasöründe Flutter, React Native–Expo, Kotlin ya da Swift ile yapılmış uygulamanız olmalıdır. Git'te build dosyası olmamalıdır.
- [ ] Bir giriş ekranında `// serves: REQ-001` olmalı ve ekran üç giriş
  endpoint'inize istek göndermelidir. `week07/phone_login.png`
  giriş yapmış adresi göstermelidir.
- [ ] Kendi işlevsel `must` gereksinimlerinizden birinin ekranında `// serves:` satırı olmalı ve ekran onun endpoint'lerine istek göndermelidir.
- [ ] `week07/mobile_runs.json` dosyasında testçinizin 1. turda en az üç çalıştırması olmalı ve bunlardan biri girişin dışında olmalıdır. Dosyayı kendiniz yazmalısınız.
- [ ] `week07/group_07.json` testçinizi içermelidir. Dosyada numara, `tester` rolü ve bulgu olmalıdır.

Cumartesi 23:59'a kadar
- [ ] Her işlevsel `must` gereksinimin `mobile/` içinde `// serves:` içeren bir ekranı olmalı ve ekran onun endpoint'lerine istek göndermelidir.
- [ ] Her işlevsel `must` gereksinimin telefonda `pass` almış bir test case'i olmalıdır. 1. turdaki her başarısızlık 2. turda yeniden çalışmalıdır.
- [ ] Uygulama kimliği, `week04/store.json` içindeki S2'nin paketi olmalıdır.
- [ ] `week07/group_07.json` dosyasında `accepted` ve `why` olmalıdır.
- [ ] Git'te build dosyası olmamalıdır.
- [ ] On ders testinin hepsi ve `"run": "server"` olan her `must` testi GitHub'da yeşil olmalıdır.
- [ ] `week07/ai_log_07.md` istediğiniz değişikliği, aldığınız diff'i, neyi reddettiğinizi ve commit'i yazmalıdır. Evidence bloğunda `ME:`, `AI:` ve `TERMINAL:` olmalıdır.
- [ ] Kontroller GitHub'da yeşil olmalıdır.

---

## Bu hafta nasıl notlandırılır

Dersin içindeki görevleriniz 5 puan üzerinden değerlendirilecektir. Dersin sonuna dek push ettiğiniz son commit'i okuyarak aşağıdakileri kontrol edeceğim:

- Uygulamanız `mobile/` içinde olmalıdır
- Giriş ekranı üç giriş endpoint'inize istek göndermeli ve `phone_login.png` giriş yapmış adresi göstermelidir
- İlk gereksiniminizin ekranı onun endpoint'lerine istek göndermelidir.
- `mobile_runs.json` testçinizin çalıştırmalarını tutmalı ve `group_07.json` içinde testçinizin bilgisi yer almalıdır.

Cumartesi 23:59 öncesindeki çalışmanız 5 puan üzerinden değerlendirilecektir. GitHub'a 23:59'a kadar ulaşan son commit'i okurum. Commit'in üzerindeki saat değil, GitHub'ın push saati sayılır.

- Kontrollerin yeşil olması size 2 puan kazandıracaktır.
- İnsan katkısı (human involvement) ile oluşan başarılı dokümanlar 2 puan kazandıracaktır. Bunun için `ai_log_07.md` dosyasını usulüne uygun olarak doldurmanız gerekmektedir. `mobile_runs.json` ve `group_07.json` dosyaları da aynı şekilde elle yazılmalıdır. Bu dosyalar asistan tarafından oluşturulmuş olursa 0 verileceğini hatırlayınız.
- Commit disiplini 1 puan ile değerlendirilecektir.

Katkı bonusu (contributors' bonus). Testçiniz haftalık notunuzun %10'u kadar bonus alacaktır.

**Derste, kendi bilgisayarınızı kullanarak.** Derste yapılan tüm çalışmalar kendi bilgisayarınızda ve kendi GitHub hesabınızla yapılmalıdır; aksi durumda sınıf çalışmasından sıfır almak dışında, yaptığınız eyleme göre kopya değerlendirilmesine tabi tutulmanız söz konusu olabilir.
