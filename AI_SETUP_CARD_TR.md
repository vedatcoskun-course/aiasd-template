# Kurulum Kartı — her şey tek sayfada

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027**

Bu sayfayı açık tutun. Dönemin tamamı boyunca çalıştırmanız gereken her şey bu
sayfadadır.

---

## Bir kez, 1. Hafta'dan önce

**1 · Reponuzu oluşturun.** Ders şablonunda (GitHub'ın sizin için kopyaladığı hazır bir
repo) **Use this template → Create a new repository** düğmesine tıklayın. Adını
`aiasd-project` koyun. **Private** yapın, çünkü form Public seçili açılır. Sonra
**Settings → Collaborators → Add people** bölümüne gidin ve `VedatCOSKUN` ekleyin.

**2 · Bilgisayarınızın GitHub ile konuşmasını sağlayın.** Şifreler 2021'de bu amaç için
çalışmaz oldu. Bu adımı bir kez yapın; bir daha yapmanız gerekmez:

```bash
brew install gh          # Windows: winget install GitHub.cli
gh auth login
```

Soruları şu sırayla yanıtlayın: `GitHub.com` → `HTTPS` → `Y` → `Login with a web browser`.

*Bilgisayarınıza yazılım kuramıyor musunuz?* O zaman bunun yerine token kullanın (token,
şifrenizin yerine geçen uzun ve rastgele bir dizedir). **Settings → Developer settings →
Personal access tokens → Tokens (classic) → Generate new token (classic)** yolunu izleyin,
yalnızca bir kutuyu, yani **`repo`** kutusunu işaretleyin ve token'ı kopyalayın. git şifre
sorduğunda token'ı yapıştırın. Ona tüm hesabınızın şifresi gibi davranın: asla bir
dosyaya, bir sohbete ya da bir commit'e koymayın.

**3 · Bilgisayarınıza kopyalayın.**

```bash
git clone https://github.com/<kullanıcı-adınız>/aiasd-project.git
cd aiasd-project
git config pull.rebase false   # bir kez: pull, GitHub'daki commit'leri sizinkilerle birleştirir
```

**4 · Kim olduğunuzu söyleyin ve push edin.** `student.json` dosyasını açın ve beş alanın
tamamını doldurun. `section` alanı `en` ya da `tr` olur. Sonra şunu çalıştırın:

```bash
git add student.json
git commit -m "week01: student identity"
git push
```

**Bu push çalışıyorsa işiniz bitti.** Bu push, testin tamamıdır.

---

## Her hafta, aynı dört komut

```bash
python .github/check_deliverables.py tr

git add .
git commit -m "week01: what I did"
git push
```

Yalnızca commit mesajı değişir. Denetleyiciyi (haftanın gerektirdiği dosyaları arayan ilk
komutu) istediğiniz kadar çalıştırın. Sondaki `tr`, çıktıyı Türkçe yazar; başka bir hafta
için `python .github/check_deliverables.py 2 tr`. Bir not değil, yapılacaklar listesidir
ve çalıştırmanın bir maliyeti yoktur.

**Push etmeden önce, 1. haftadan itibaren:** GitHub her push'ta ruff çalıştırır. Aynı
kontrolleri siz de çalıştırın:

```bash
python -m pip install -r requirements.txt  # bir kez, .venv içinde: ruff 0.15.11, GitHub'daki gibi
ruff check .                               # sorunları listele
ruff format --check .                      # biçimi kontrol et
```

Bir ruff satırı sorun bildirirse `ruff check . --fix` ve `ruff format .` çalıştırın,
sonra yeniden kontrol edin.

**Ne zaman push edersiniz:**

- **Derste:** her işi ortasında commit edin, çalıştığında yeniden commit edin ve her commit'i
  hemen push edin.
- **Ders dışında:** yeni iş içeren en az iki commit, aralarında en az bir saat olacak
  şekilde push edilmiş olsun.
- Commit'in üzerindeki tarih değil, GitHub'ın push saati sayılır. Bir kodlama ajanının
  yaptığı commit hiçbir zaman sayılmaz.
- **Asla force push yapmayın** ve bir asistanın yapmasına da izin vermeyin. Git push'unuzu
  reddederse önce `git pull`, sonra `git push` yapın.

## 5. haftadan itibaren: sunucu ve testler

```bash
python -m venv .venv                              # yalnızca bir kez
source .venv/bin/activate                         # Windows: .venv\Scripts\activate
python -m pip install -r week06/requirements.txt  # bir tane olan en yeni hafta
uvicorn server.main:app --reload                  # sunucuyu başlat
python -m pytest                                  # testleri çalıştır
```

Her yeni terminal açtığınızda sanal ortamı (`.venv`, dersin Python paketlerini tutan
klasör) etkinleştirin. Sunucu kendi terminalini meşgul eder; testleri ikinci bir
terminalde çalıştırın.

---

## Ders dosyaları kendiliğinden gelir

`python .github/check_deliverables.py` her çalıştığında dersin dosyalarını da reponuza
getirir. Bir hafta yayınlandığında o haftanın klasörünü getirir ve kökte değişen her
ders belgesini (`AI_*`) getirir. `PROPOSAL.md` iskeletini köke (2. hafta) ve `server/`
başlangıç dosyalarını (5. hafta), yalnızca sizde henüz yoksa getirir. Bir hafta
klasöründe zaten olan bir dosyanıza asla dokunmaz. Gelenler siz `git add .` çalıştırana kadar izlenmez (git dosyaları görür ama
henüz kaydetmez) ve denetleyici bu dosyaları listeler. Aşağıdaki bölüm, çevrimdışı
olduğunuzda kullanacağınız elle yapma yolunu anlatır.

6. haftadan itibaren denetleyici `course_tests/` klasörünü ve `server/course_login.py`
dosyasını da getirir; `server/login_contract.json` sizde yoksa onu da. `course_tests/` ya
da `course_login.py` dosyalarını değiştirmeyin: denetleyici dersin kopyasını geri koyar ve
GitHub her zaman onu kullanır.

## İki remote, birbirinden çok farklı iki komut

Reponuzda `origin` adlı bir remote vardır (remote, reponuzun başka bir bilgisayardaki
kopyasının adresidir) ve `origin`, GitHub'daki kendi kopyanızdır. Yalnızca çevrimdışı
olduğunuzda bir haftanın dosyalarını ders şablonundan elle getirirsiniz; bunun için
`template` adlı ikinci bir remote eklersiniz. Bu iki remote birbirinin yerine geçmez.

| | |
|---|---|
| `git pull` | Bu komut `origin`'den, yani kendi reponuzdan çeker; örneğin başka bir makinede çalıştıktan ya da tarayıcıda bir dosyayı düzenledikten sonra. Normal, günlük ve güvenlidir. |
| `git pull template main` | **Bu komutu asla çalıştırmayın.** |

Şablon, sizinkiyle ortak geçmişi olmayan ayrı bir repodur, çünkü kopyanız ondan
oluşturuldu, klonlanmadı. İkisini birleştirmek (birleştirmek, git'ten iki geçmişi tek
geçmişte toplamasını istemektir) git'in her dosyayı aynı anda uzlaştırmaya kalkmasına yol
açar: doldurduğunuz `student.json` boş olanla, bitirdiğiniz `hello.py` iskeletle ve
çalışmanız taslakla. Dersi çakışmaları çözmekle geçirirsiniz ve bir kez başarılı olan bir
`git pull` her seferinde aynısını yeniden dener.

Bunun yerine, yalnızca çevrimdışı olduğunuzda, yalnızca gerçekten istediğiniz yolları
alın:

```bash
git remote add template https://github.com/vedatcoskun-course/aiasd-template.git   # yalnızca bir kez
git fetch template
git checkout template/main -- week06 course_tests server/course_login.py
```

Bu komutlar tam olarak adını verdiğiniz yolları kopyalar ve başka hiçbir şeye dokunmaz. O
dosyalara bir şey yazmadan **önce** çalıştırın. Sonra çalıştırırsanız çalışmanızın
üzerine yazarlar. `server/login_contract.json` dosyanız henüz yoksa onu son satırın sonuna
ekleyin.

---

## Bir şey ters gittiğinde

> **Hatanın İLK değil SON satırını okuyun.** Git teşhisi en alta yazar. Üstündeki
> satırlar bağlamdır.

| Gördüğünüz | Anlamı |
|---|---|
| `Authentication failed`<br>`could not read Username for 'https://github.com'` | GitHub kim olduğunuzu bilmiyor. `gh auth login` çalıştırın. Hala olmuyorsa `gh auth status` çalıştırın, çünkü yanlış hesapla girmiş olabilirsiniz. |
| `Support for password authentication was removed` | Bunun nedeni aynıdır. GitHub şifreniz burada kullanılamaz ve yeniden yazmak işe yaramaz. |
| `! [rejected] main -> main (fetch first)` | GitHub'da sizde olmayan bir commit var; genellikle tarayıcıda bir dosyayı düzenlediğiniz için. Önce `git pull`, sonra `git push` çalıştırın. **Asla force push yapmayın.** |
| `Need to specify how to reconcile divergent branches` | Bir kez `git config pull.rebase false` çalıştırın, sonra yeniden `git pull` yapın. |
| `nothing to commit, working tree clean` | Git bir değişiklik görmüyor. Ya editör kaydetmedi ya da yanlış klasördesiniz. `pwd` çalıştırın ve yazdığı klasöre bakın. |
| `fatal: not a git repository` | Projenin dışındasınız. `aiasd-project` içine `cd` yapın ve yeniden deneyin. |
| `index.lock ... File exists` | Bir git komutu yarıda kesildi. `rm -f .git/index.lock` çalıştırın ve yeniden deneyin. |
| Denetleyici *Hangi haftada olduğumuz anlaşılamıyor* (*Cannot tell which week it is*) diyor | Bu ilk çalıştırmadır ve ağ yoktur. Bir kez bağlanıp yeniden çalıştırın; sonrasında çevrimdışı da çalışır. |
| `command not found: python` | Bunun yerine `python3` deneyin. macOS'ta genellikle var olan `python3`tür. |
| `refusing to merge unrelated histories` | `origin` yerine `template`'ten pull yaptınız. `--allow-unrelated-histories` vermeyin; yukarıdaki bölüme bakın. |

---

**Hala takıldınız mı?** Bir yapay zeka asistanına sorun, ama özellikle git kimlik
doğrulaması konusunda kuşkucu olun. Kimlik doğrulama 2021'de değişti ve internetin çoğu
hala eski yolu anlatıyor. Size GitHub şifrenizi kullanmanız ya da `git config credential.helper store` çalıştırmanız söyleniyorsa o tavsiye eskimiştir. Görmezden gelin
ve bu karta dönün.

Haftalık rutinin tamamı
[`AI_WEEKLY_WORKFLOW_STUDENT_TR.md`](AI_WEEKLY_WORKFLOW_STUDENT_TR.md) dosyasındadır.
Puanların neye verildiğini, her dersin sonunda ne olduğunu ve derse gelemezseniz ne
yapacağınızı söyler.
