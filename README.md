# 🚀 NovaScript - Kendi Programlama Dilim ve Yorumlayıcım

**BIL206 - Programlama Dillerinin Prensipleri Dönem Ödevi** kapsamında geliştirilmiş, Türkçe sözdizimine sahip, özgün semboller kullanan, genel amaçlı ve yorumlanan (interpreted) bir programlama dilidir.

🎥 **Proje Demo ve Anlatım Videosu:** [YouTube Linki Buraya Gelecek]

## 🌟 Dilin Özellikleri
NovaScript, karmaşık İngilizce terimlerden arındırılmış, öğrenmesi ve okuması son derece kolay bir dildir. Python tabanlı bir Yorumlayıcı (Interpreter) ile çalışır. Lexer, Parser ve Evaluator aşamaları sıfırdan yazılmıştır.

* **Değişken Atamaları:** Veri tipi belirtmeden otomatik algılama (Sayı ve Metin).
* **Özgün Anahtar Kelimeler:** `if/while/print` yerine `eger`, `madem` ve `goster`.
* **Özgün Blok Sembolleri:** Süslü parantez `{ }` yerine oklar `<< >>` ve noktalı virgül `;` yerine tilde `~` kullanılmıştır.
* **Matematik ve Mantık:** Temel operatörler (`+`, `-`, `*`, `/`) ve karşılaştırmalar (`>`, `<`, `==`, `>=`, `<=`, `!=`) desteklenir.

## 📜 NovaScript Gramer Yapısı (EBNF)
Dilin sözdizimsel kuralları (Syntax) aşağıdaki EBNF tablosunda belirtilmiştir:

<program>      ::= <statement>*
<statement>    ::= <assignment> | <eger_stmt> | <madem_stmt> | <goster_stmt>
<assignment>   ::= IDENTIFIER "=" <expression> "~"
<eger_stmt>    ::= "eger" "(" <condition> ")" "<<" <program> ">>"
<madem_stmt>   ::= "madem" "(" <condition> ")" "<<" <program> ">>"
<goster_stmt>  ::= "goster" "(" <expression> ")" "~"
<expression>   ::= IDENTIFIER | NUMBER | STRING | <expression> OPERATOR <expression>
<condition>    ::= <expression> COMPARISON_OP <expression>


## 📂 Proje Dizin Yapısı
Proje, hoca tarafından belirtilen standartlara uygun olarak klasörlenmiştir:
* `/src`: Yorumlayıcının kaynak kodlarını (Lexer, Parser, Evaluator) içerir.
* `/examples`: NovaScript ile yazılmış örnek kod senaryolarını barındırır.
* `README.md`: Proje dokümantasyonu.
* `ai_prompts.md`: Yapay zeka kullanım raporu.

## 💻 Örnek Kod Kullanımı
NovaScript'te 1'den 5'e kadar olan sayıları toplayan basit bir algoritma şu şekilde yazılır:

```text
sayac = 5 ~
toplam = 0 ~

madem (sayac > 0) <<
    toplam = toplam + sayac ~
    sayac = sayac - 1 ~
>>

goster("1'den 5'e kadar olan sayilarin toplami:") ~
goster(toplam) ~
