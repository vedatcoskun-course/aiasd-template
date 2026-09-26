# Kurulum Kartı — her şey tek sayfada

**AI-Assisted Software Development · Atlas Üniversitesi · Güz 2026–2027**

Bu sayfayı açık tutun. Dönem boyunca çalıştırmanız gereken her şey burada.

---

## Bir kez, 1. Hafta'dan önce

**1 · Deponuzu oluşturun.** Ders şablonunda **Use this template → Create a new
repository** düğmesine tıklayın. Adını `aiasd-project` koyun. **Private** yapın — form
Public seçili açılır. Sonra **Settings → Collaborators → Add people** ile `VedatCOSKUN`
ekleyin.

**2 · Bilgisayarınızın GitHub ile konuşmasını sağlayın.** Şifreler 2021'de bunun için
çalışmaz oldu. Bir kez yapın, bir daha gerekmez:

```bash
brew install gh          # Windows: winget install GitHub.cli
gh auth login
```

Yanıtlar: `GitHub.com` → `HTTPS` → `Y` → `Login with a web browser`.

*Bilgisayarınıza yazılım kuramıyor musunuz?* Bunun yerine token kullanın: **Settings →
Developer settings → Personal access tokens → Tokens (classic) → Generate new token
(classic)**, yalnızca bir kutuyu — **`repo`** — işaretleyin ve kopyalayın. git şifre
sorduğunda token'ı yapıştırın. Ona tüm hesabınızın şifresi gibi davranın: asla bir
dosyaya, sohbete ya da commit'e koymayın.

**3 · Bilgisayarınıza kopyalayın.**

```bash
git clone https://github.com/<kullanıcı-adınız>/aiasd-project.git
cd aiasd-project
```

**4 · Kim olduğunuzu söyleyin ve push edin.** `student.json` dosyasını açın, beş alanın
tamamını doldurun — `section` `en` ya da `tr` — sonra:

```bash
git add student.json
git commit -m "week01: student identity"
git push
```

**Bu push çalışıyorsa işiniz bitti.** Testin tamamı bu.

---

## Her hafta, aynı dört komut

```bash
python .github/check_deliverables.py

git add .
git commit -m "week01: what I did"
git push
```

On iki hafta boyunca başka hiçbir şey değişmez. Yalnızca commit mesajı. Denetleyiciyi
istediğiniz kadar çalıştırın — bir not değil, yapılacaklar listesidir ve çalıştırmanın
bir maliyeti yoktur.

Bir haftanın gerektirdiğinde iki komut daha:

```bash
pip install -r weekNN/requirements.txt
streamlit run app.py
```

---

## Ders dosyaları kendiliğinden gelir

`python .github/check_deliverables.py` her çalıştığında dersin dosyalarını da reponuza
getirir: yayınlandığında yeni haftanın klasörü ve kökte değişen her ders belgesi
(`AI_*`). Bir hafta klasöründe zaten olan bir dosyanıza asla dokunmaz. Gelenler siz
`git add .` yapana kadar izlenmez — denetleyici listeler. Aşağıdaki bölüm, çevrimdışı
olduğunuzda elle yapmanın yolu.

## İki remote, birbirinden çok farklı iki komut

Deponuzda `origin` var — GitHub'daki kendi kopyanız. Bazı haftalar ders şablonundan
size bir başlangıç klasörü verilir; bunun için `template` adlı ikinci bir remote
eklersiniz. Birbirinin yerine geçmezler.

| | |
|---|---|
| `git pull` | `origin`'den. Kendi deponuz; başka bir makinede ya da tarayıcıda yaptığınız bir düzenlemeden sonra. Normal, günlük, güvenli. |
| `git pull template main` | **Asla.** |

Şablon, sizinkiyle ortak geçmişi olmayan ayrı bir depodur — kopyanız ondan
oluşturuldu, klonlanmadı. İkisini birleştirmeye çalışmak her dosyayı aynı anda
uzlaştırmaya kalkar: doldurduğunuz `student.json` boş olanla, bitirdiğiniz `hello.py`
iskeletle, çalışmanız taslakla. Dersi çakışmaları çözmekle geçirirsiniz ve bir kez
başarılı olan `git pull` her seferinde aynısını yeniden dener.

Onun yerine gerçekten istediğiniz tek yolu alın:

```bash
git remote add template https://github.com/vedatcoskun-course/aiasd-template.git   # bir kez, hep
git fetch template
git checkout template/main -- week06
```

Bu, tam olarak adını verdiğiniz yolu kopyalar ve başka hiçbir şeye dokunmaz. O klasöre
bir şey yazmadan **önce** çalıştırın — sonra çalıştırırsanız çalışmanızın üzerine yazar.

---

## Bir şey ters gittiğinde

> **Hatanın İLK değil SON satırını okuyun.** Git teşhisi en alta yazar. Üstündeki
> satırlar bağlamdır.

| Gördüğünüz | Anlamı |
|---|---|
| `Authentication failed`<br>`could not read Username for 'https://github.com'` | GitHub kim olduğunuzu bilmiyor. `gh auth login` çalıştırın. Hâlâ olmuyorsa `gh auth status` — yanlış hesapla girmiş olabilirsiniz. |
| `Support for password authentication was removed` | Aynı neden. GitHub şifreniz burada kullanılamaz; kaç kez yazarsanız yazın işe yaramaz. |
| `! [rejected] main -> main (fetch first)` | GitHub'da sizde olmayan bir commit var — genellikle tarayıcıda bir dosyayı düzenlediğiniz için. `git pull --rebase`, sonra yeniden push. |
| `nothing to commit, working tree clean` | Git bir değişiklik görmüyor. Ya editör kaydetmedi ya da yanlış klasördesiniz. `pwd` çalıştırıp bakın. |
| `fatal: not a git repository` | Projenin dışındasınız. `aiasd-project` içine `cd` yapıp yeniden deneyin. |
| `index.lock ... File exists` | Bir git komutu yarıda kesildi. `rm -f .git/index.lock` ve yeniden deneyin. |
| Denetleyici *Cannot tell which week it is* diyor | İlk çalıştırma, ağ yok. Bir kez bağlanıp yeniden çalıştırın; sonrasında çevrimdışı da çalışır. |
| `command not found: python` | `python3` deneyin. macOS'ta genellikle var olan odur. |
| `refusing to merge unrelated histories` | `origin` yerine `template`'ten pull yaptınız. `--allow-unrelated-histories` vermeyin; yukarıdaki bölüme bakın. |

---

**Hâlâ takıldınız mı?** Bir yapay zekâ asistanına sorun — ama özellikle git kimlik
doğrulaması konusunda kuşkucu olun. 2021'de değişti ve internetin çoğu hâlâ eski yolu
anlatıyor. Size GitHub şifrenizi kullanmanız ya da `git config credential.helper store`
çalıştırmanız söyleniyorsa o tavsiye eskimiştir. Görmezden gelin ve bu karta dönün.

Haftalık rutinin tamamı — puanlar neye verilir, her dersin sonunda ne olur, derse
gelemezseniz ne yaparsınız — [`AI_WEEKLY_WORKFLOW_STUDENT_TR.md`](AI_WEEKLY_WORKFLOW_STUDENT_TR.md)
dosyasında.
