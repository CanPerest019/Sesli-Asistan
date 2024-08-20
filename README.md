<h1 align = 'Center'>CAN'S Voice Assistant</h1>

----------------------------------------------------------------------------------------

**Uyarı**
Kod Daha Geliştirme Aşamasındadır Kodda Herhangi Bir Hata OLabilir Aldığınız Hataları Bana Discord yoluyla Bildiriniz.(MyAccount:canxd22)

----------------------------------------------------------------------------------------

## Kodun Amacı 
Bu Python kodu, kullanıcıdan sesli komutlar alarak belirli yanıtlar verebilen bir sesli asistan uygulaması geliştirmek için kullanılmaktadır. Uygulama, aşağıdaki temel işlevleri yerine getirmektedir:

**Gerekli Kütüphanelerin Kullanımı**
Kodda, sesli asistanın işlevselliğini sağlamak için çeşitli kütüphaneler kullanılmaktadır:

* Tkinter: Kullanıcı arayüzünü oluşturmak için grafik kullanıcı arayüzü (GUI) sağlar.
* FastAPI: Asenkron web uygulaması geliştirmek için kullanılır; API uç noktaları tanımlamak için idealdir.
* Pydantic: Gelen verileri doğrulamak ve yapılandırmak için kullanılır
* Sklearn: Makine öğrenimi modelleri oluşturmak için kullanılır; burada metin verilerini işlemek için Naive Bayes sınıflandırıcısı ve CountVectorizer kullanılır.
* gTTS (Google Text-to-Speech): Metni sesli olarak okumak için kullanılır.
* Pandas: Veri analizi ve işleme için kullanılır; CSV dosyaları ile çalışmak için idealdir.
* Requests: Veri setlerini indirmek için HTTP istekleri yapmak için kullanılır
* pygame: Ses dosyalarını çalmak için kullanılır.
* Threading: Paralel işlemler yapmak için kullanılır, böylece FastAPI ve Tkinter arayüzü aynı anda çalışabilir.

**Uygulamanın Başlatılması**
Uygulama, FastAPI ile başlatılır ve başlangıçta model ve vektörleştirici için global değişkenler tanımlanır.

**Komut Modelinin Tanımlanması**
CommandRequest adında bir Pydantic modeli tanımlanır. Bu model, kullanıcının sesli komutunu içerir ve gelen verilerin doğruluğunu sağlamak için kullanılır.

**Sesli Konuşma Fonksiyonu**
konus(metin) fonksiyonu, verilen metni sesli olarak okumak için kullanılır. Bu işlem, gTTS ile metin ses dosyasına dönüştürülüp pygame ile çalınarak gerçekleştirilir.

**Model Eğitimi**
model_egitimi(komutlar, yanitlar) fonksiyonu, kullanıcıdan alınan komutlar ve yanıtlar ile Naive Bayes modelini eğitir. Bu fonksiyon, metin verilerini vektörleştirir ve sınıflandırma modelini oluşturur.

**Veri Setini İndirme ve Yükleme**
veri_seti_ve_model_yukle() fonksiyonu, belirtilen bir URL'den veri setini indirir, CSV dosyasını okur ve modelin eğitilmesini sağlar. Veri setinin uygun olup olmadığını kontrol eder ve kullanıcıya sesli yanıt verir.

**Komutları İşleme**
komut_isle(komut) fonksiyonu, kullanıcıdan gelen komutu alır, vektörleştirir ve eğitilmiş modeli kullanarak tahminde bulunur. Tahmin edilen yanıt sesli olarak okunur.

**FastAPI Uç Noktaları**
* /upload-dataset/: Kullanıcıdan bir CSV dosyası yüklemesine olanak tanır ve içeriğini okur. Veri setini doğrular ve modeli yeniden eğitir.
* /process-command/: Kullanıcıdan bir komut alır, bu komutu işler ve sonucu JSON formatında döner.

**Tkinter Arayüzü**
SesliAsistanArayuz sınıfı, kullanıcı arayüzünü oluşturur. Arayüzde bir metin alanı, kullanıcıdan komut almayı sağlayan butonlar ve asistanın cevaplarını görüntülemek için alanlar bulunmaktadır. Kullanıcı, "Konuş" butonuna tıkladığında belirli bir komut ile asistanın yanıtı alınır.

**Paralel Çalışma**
Uygulama, FastAPI ve Tkinter'in aynı anda çalışmasını sağlamak için threading kütüphanesini kullanarak iki işlemi paralel olarak yürütür. Bu, kullanıcı arayüzünün yanıt vermesini sağlar.

---------------------------------------------------------------------------------------------------------------------

## Sonuç
Bu kod, temel bir sesli asistan uygulaması oluşturmak için tasarlanmış bir yapıdır. Kullanıcıdan alınan sesli komutlara göre yanıtlar vererek, kullanıcı etkileşimini artırır. Makine öğrenimi modeli, belirli komut ve yanıt çiftleri ile eğitildiği için, uygulama zamanla daha da geliştirilebilir ve kullanıcı deneyimi iyileştirilebilir.

























