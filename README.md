# log_checker
Linux için /var/log altında logları verilen parametrelere göre filtreler.

Kullanımı : 

#Son bir saat içerisinde değişiklik yapılmış log'lardan son 10 satır getir ve yazdır.
python3 ./log_checker.py -r 1 -l 10 

#Tüm logların tüm satırlarını getir ve yazdır.
#-r 0 : Saat filtrelemesi yapmadan getir
#-l 0 : Log'un tüm içeriğini getir.
python3 ./log_checker.py -r 0 -l 0

#Son 24 saat içinde değişiklik yapılmış olan log'ların son 10 satırı içerisinde "root" kelimesi geçenleri getir ve yazdır.
python3 ./log_checker.py -r 24 -l 10 -f root 

