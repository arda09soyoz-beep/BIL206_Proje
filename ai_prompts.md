# 🤖 Yapay Zeka Kullanım Raporu

Bu proje geliştirilirken beyin fırtınası yapmak, Lexer/Parser mantığını oturtmak ve hata ayıklamak (debugging) amacıyla Gemini yapay zeka modelinden destek alınmıştır. 

Aşağıda süreç boyunca kullanılan temel promptlar (istemler) ve entegrasyon açıklamaları listelenmiştir:

* **Tarih:** 24 Mayıs 2026
* **Prompt 1:** "Hocanın proje gereksinimleri PDF'ini inceleyip Lexer ve Parser mantığında genel amaçlı bir dil tasarlamama yardım eder misin? Süslü parantez yerine '<< >>', noktalı virgül yerine '~' kullanmak istiyorum."
* **Kullanım:** Yapay zekanın önerdiği RegEx (Düzenli İfadeler) tabanlı ayrıştırma mantığı projenin Lexer modülüne temel oluşturdu. İngilizce terimler (if, while) Türkçe karşılıklarıyla (eger, madem) değiştirilerek projeye entegre edildi.

* **Tarih:** 24 Mayıs 2026
* **Prompt 2:** "Kodumda şöyle bir çıktı/hata aldım: *NovaScript Hatası: Beklenen '<<', ancak '<<' bulundu.* Bu neden kaynaklanıyor?"
* **Kullanım:** Yapay zeka, bu hatanın Lexer içerisindeki RegEx öncelik sırasından kaynaklandığını tespit etti. `OPERATOR` kuralı ile `PUNC_OPEN` kuralının yeri değiştirilerek sorun çözüldü ve kod düzeltildi.

* **Tarih:** 24 Mayıs 2026
* **Prompt 3:** "Projem için yazdığımız dilin yeteneklerini gösterecek 3 farklı örnek kod (matematiksel, karar yapısı ve iç içe bloklar) oluşturucam onları kontrol eder misin?"
* **Kullanım:** Üretilen örnek kodlar test edilerek doğruluğu onaylandı ve `/examples` klasöründeki senaryolar olarak projeye eklendi.
