from root import Wallpaper

generator = Wallpaper()

print("1-) Veritabanına özlü söz ekle \n2-) Arkaplanı değiştir ")
select = int(input("Hangisini Yapmak İstersiniz?: ")) 
if select==1:
    howmuch = int(input("Kaç Adet eklenmesi istersiniz?: "))
    generator.addAphorism(howmuch)
    print("Ekleme İşlemi Başarı İle Sonuçlandı!")
elif select==2:
    generator.changeContent()
    print("Arkaplan başarı ile değiştirildi")

else:
    print("Geçerli bir değer giriniz!!!!")

