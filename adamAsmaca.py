import json
import os
 
try:
    from termcolor import cprint # BU PROJEDE PYTHON'UN TERMCOLOR KÜTÜPHANESİNİ KULLANIYORUZ
    #Bu kütüphaneyi kurmak için: pip install termcolor
except ImportError:
    def cprint(*args, **kwargs):
        print(*args)
 
kelimeler = ["qbasic", "visualbasic", "python", "php", "perl", "html", "css", "csharp", "java"]
#Adam asmaca oyunundaki random gelecek kelimeler. Buraya ekleme veya çıkarma yapılabilir. Bu kelimeleri bilmemiz istenilecek:,
#buradaki kelimeleri girerken lütfen hepsini küçük harf olarak giriniz. Program büyük küçük harfe duyarlıdır.
 
 
def oyun_hazirlik():
    """ Adam Asmaca degisken tanımlama"""
    global secilen_kelime, gorunen_kelime, hak
    import random
    secilen_kelime = random.choice(kelimeler)
    gorunen_kelime = ["-"] * len(secilen_kelime)
    hak = 7 #hak KISMIMIZI BURADAN GİRİYORUZ VARSAYILAN OLARAK 5 hak ATADIK.
    
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def kullanici_adini_guncelle():
    """Kullanıcıdan aldığı adı alıp ayarlara yazdırmaya gönderir"""
    veri = ayar_oku()
    veri["son_kullanan"] = input("Kullanıcı Adınız: ")
    while not veri["son_kullanan"] or len(veri["son_kullanan"]) > 9:
        veri["son_kullanan"] = input("lykpython ile 9 karakter uzunluğunda yazın: ")
    ayar_yaz(veri)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def kullanici_kontrol():
    """Bir önce giriş yapan kullanıcı ismini gösterip kullanıcıya bu siz misiniz diye sorar"""
    veri = ayar_oku()
    print("Son Giriş Yapan: " + veri["son_kullanan"])
    if not veri["son_kullanan"]:
        kullanici_adini_guncelle()
    elif input("Bu siz misiniz?(e/h) ").lower() == "h": # Bu siz misiniz e denilirse daha önce girilen kullanıcının adını alır.
        #h denilirse yeni bir isim girmenizi ister. 
        kullanici_adini_guncelle() #yeni bir isim girmesi için kullanıcı_adini_guncelle() fonksiyonuna yönlendirir.

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------        
 
def harf_al(): #kullanıcıdan oyun için tek tek harf alınan kısım
    """Kullanıcıdan bir harf alır, alana kadar gerekirse hata verir, birisi quit yazarsa programı kapatır"""
    devam = True
    while devam:
        harf = input("Bir harf giriniz: ")
        if harf.lower() == "quit": #quit yazarsanız oyun kapanır.
            cprint("Oyun kapatiliyor...", color="red", on_color="on_blue")
            exit()
        elif len(harf) == 1 and harf.isalpha() and harf not in gorunen_kelime: #harf olup olmadığını kontrol ediyor. Rakam veya ! ? gibi karakterleri kontrol ediyor.
            devam = False 
        else:
            cprint("Hatali bir giris yaptiniz.", color="red", on_color="on_grey") #burada harf haricinde sayı girildiğinde verdirdiği uyarı mesajı

    return harf.lower() # harfleri küçük harfe çeviriyor. büyük küçük harften dolayı sorun yaşanmamsı için....

#-------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------- 

def oyun_dongusu():
    """  ----------------------------------------------- OYUNUN ÇALIŞMA MANTIĞI

     Oyundaki mantık: kullanıcıdan harf alır. Gelen harf random gelen kelime içerisinde varsa yazar. Yoksa hakı azaltır.
     hak bitene kadar kelime ister. hak  bittiğinde oyun biter.

     """
    global gorunen_kelime, hak
    while hak > 0 and secilen_kelime != "".join(gorunen_kelime):
        cprint("Bilmeniz Gereken Kelime: " + "".join(gorunen_kelime), color="cyan", attrs=["bold"])
        cprint("Kalan Hakkınız:   : <" + " ❤ " * hak + " " * (5 - hak) + ">", color="cyan", attrs=["bold"])
 
        girilen_harf = harf_al()
        pozisyonlar = harf_kontrol(girilen_harf)
        if pozisyonlar:
            for p in pozisyonlar:
                gorunen_kelime[p] = girilen_harf
        else:
            hak -= 1 #hakkı bir düşür.
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def skor_tablosunu_goster(): #her karakter girdiğinde veya kelime bildiğinizde veya oyun sonlandığında gösterilen skor tablosu yapısı
    """Skor tablosunu gösterir"""
    veri = ayar_oku()
    cprint("|       Skor\t\tKullanıcı |", color="white", on_color="on_grey")
    cprint("|---------------------------------|", color="white", on_color="on_grey")
    for skor, kullanici in veri["skorlar"]:
        cprint("|"+str(skor) +"\t\t"+ kullanici+" "*(9-len(kullanici))+"         |", color="white", on_color="on_grey")
    cprint("|---------------------------------|", color="white", on_color="on_grey")
 
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def harf_kontrol(girilen_harf):
    """Kullanıcının girdiği harfin, kelimemizde nerede olduğunu bulur."""
    poz = []
    for index, h in enumerate(secilen_kelime): #girilen harf kelimemizde aratan döngü
        if h == girilen_harf: #eğer harf kelimede varsa
            poz.append(index)
    return poz

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def skor_tablosunu_guncelle(): #skor tablosundaki değerlerin güncellendiği alan
    """Skorları gösterdiğimiz tablodan kullanıcının adıyla ve skoruyla birlikte güncellemesini yapar.
    """
    veri = ayar_oku()
    veri["skorlar"].append((hak, veri["son_kullanan"]))
    veri["skorlar"].sort(key=lambda skor_tuplei: skor_tuplei[0], reverse=True)
    veri["skorlar"] = veri["skorlar"][:5]
    ayar_yaz(veri)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def oyun_sonucu(): # oyunumuz sonlandığında gösterilen ekran.
    """Oyun bittiğinde kazanıp kazanamadığımızı ekrana yazar."""
    if hak > 0: #hakkımız hala 0'dan büyükse ve kelimeyi bildiysek
        cprint("Kazandınız", color="yellow", on_color="on_red") #oyunu kazandığımızda gelen mesaj ve renkler
        skor_tablosunu_guncelle()
    else: #hakkımız sıfırdan küçükse doğal olarak kaybettik. hakkımız bitti.
        cprint("Kaybettiniz", color="red", on_color="on_yellow")#oyunu kaybettiğimizde gelen mesaj ve renkler
    skor_tablosunu_goster() #skor göstermesi için skor_tablosunu_goster() fonksiyonuna gidiyor.

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
 
def dosyayi_kontrol_et_yoksa_olustur(): # ayar dosyası.
    """Ayar dosyası var mı kontrol eder, varsa sağlam mı diye bakar,
    bozuk ya da olmayan durum için dosyayı öntanımlı değerlerle oluşturur"""
    yaz = False
    if os.path.exists("ayarlar.json"): #ayarlar.json adam asmacadaki skorları ve daha önce giriş yapan kullanıcıları kaydetmemize yardımcı olan dosya.
        try:                           # bu ayarlar.json dosyası python oyunun kurulu olduğu yerde çalışmaktadır.
            ayar_oku()
        except ValueError as e:
            cprint("Hata: ValueError(" + ",".join(e.args) + ")", color="red", on_color="on_blue", attrs=["bold"])
            os.remove("ayarlar.json")
            yaz = True
    else:
        yaz = True
 
    if yaz:
        ayar_yaz({"skorlar": [], "son_kullanan": ""})
 
 
def ayar_oku(): #ayarları okumamıza yarayan fonksiyon
    """Ayarlar dosyasını okur"""
    with open("ayarlar.json") as f:
        return json.load(f)
 
 
def ayar_yaz(veri): #ayar dosyasına gönderilen veriyi yazan fonksiyon
    """Ayarlar dosyasına gönderilen veriyi yazar"""
    with open("ayarlar.json", "w") as f:
        json.dump(veri, f)

  
def main(): ##### OYUNUN ANA DÖNGÜSÜ VE ÇALIŞMASINI SAĞLAYAN KISIM
    """Programın ana döngüsü, oyunun çalışmasından yükümlü"""
    tekrar_edecek_mi = True
    dosyayi_kontrol_et_yoksa_olustur()
    cprint("Merhaba, Adam Asmacaya hoşgeldiniz.", color="cyan", on_color="on_magenta", attrs=["bold"]) #adam asmaca oyununa hoşgeldin karşılama mesajı
    cprint("Yardım: Oyun sırasında quit diyerek çıkabilirsiniz", color="cyan", on_color="on_magenta", attrs=["bold"]) #oyundan çıkmak için quit komutunu kullanacağımızı bildiren mesaj
    cprint("-"*30, color="cyan", on_color="on_magenta", attrs=["bold"])
    skor_tablosunu_goster() #skor tablosunu göster
    kullanici_kontrol() #kullanıcıyı kontrol et
    while tekrar_edecek_mi:
        oyun_hazirlik()
        oyun_dongusu()
        oyun_sonucu()
        if input("Devam?(e/h) ").lower() == "h": #oyuna devam etmek istemediğinizde h tuşuna basıyorsunuz çıkış yapıyor ve skoru yazdırıyor.
            tekrar_edecek_mi = False
    cprint("Oyundan başarıyla çıkış yaptınız. ", color="red", on_color="on_blue")
  
main()