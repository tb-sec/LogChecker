# LogChecker
Linux için /var/log altındaki logları verilen parametrelere göre filtreler.

  ## Parametreler
 * -r RANGE, --range RANGE Saat öncesinden itibaren log'ları kontrol et
 * -l LINE, --line LINE  Log'dan getirilecek satır sayısı
 * -f FILTER, --filter FILTER  Getirilen satır içinde filtrelenmek istenen kelime

## Örnek Kullanımlar

Son 2 saat içerisinde değişiklik yapılmış log dosyalarının son 10 satırını getir ve yazdır.

> python3 ./log_checker.py -r 2 -l 10 

Tüm logların tüm satırlarını getir ve yazdır.

> python3 ./log_checker.py -r 0 -l 0

Son 24 saat içinde değişiklik yapılmış olan log'ların son 10 satırı içerisinde "root" kelimesi geçenleri getir ve yazdır.

> python3 ./log_checker.py -r 24 -l 10 -f root 

