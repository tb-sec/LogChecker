# log_checker
Linux için /var/log altında logları verilen parametrelere göre filtreler.

  
 * -r RANGE, --range RANGE Saat öncesinden itibaren log'ları kontrol et
 * -l LINE, --line LINE  Log'dan getirilecek satır sayısı
 * -f FILTER, --filter FILTER  Getirilen satır içinde filtrelenmek istenen kelime


Son bir saat içerisinde değişiklik yapılmış log'lardan son 10 satır getir ve yazdır.

> python3 ./log_checker.py -r 1 -l 10 

Tüm logların tüm satırlarını getir ve yazdır.

> python3 ./log_checker.py -r 0 -l 0

Son 24 saat içinde değişiklik yapılmış olan log'ların son 10 satırı içerisinde "root" kelimesi geçenleri getir ve yazdır.

> python3 ./log_checker.py -r 24 -l 10 -f root 

