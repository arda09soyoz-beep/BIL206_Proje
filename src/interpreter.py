import re

# ==========================================
# 1. AŞAMA: SÖZCÜKSEL ANALİZ (LEXER)
# ==========================================
def lexer(kod):
    token_kurallari = [
        ('NUMBER',     r'\d+'),
        ('STRING',     r'"[^"]*"'),
        ('KEYWORD',    r'\b(eger|madem|goster|her|icinde)\b'),
        ('IDENTIFIER', r'[a-zA-Z_]\w*'),
        ('PUNC_OPEN',  r'<<'),           
        ('PUNC_CLOSE', r'>>'),           
        ('OPERATOR',   r'[+\-*/=><!]+'), 
        ('LPAREN',     r'\('),
        ('RPAREN',     r'\)'),
        ('TILDE',      r'~'),
        ('SKIP',       r'[ \t\n]+'),
        ('MISMATCH',   r'.')
    ]

    regex_ifadesi = '|'.join(f'(?P<{isim}>{kural})' for isim, kural in token_kurallari)
    tokenlar = []
    
    for eslesme in re.finditer(regex_ifadesi, kod):
        tur = eslesme.lastgroup
        deger = eslesme.group()
        
        if tur == 'SKIP':
            continue
        elif tur == 'MISMATCH':
            raise RuntimeError(f"NovaScript Hatası: Beklenmeyen karakter bulundu -> '{deger}'")
            
        tokenlar.append((tur, deger))
        
    return tokenlar

# ==========================================
# 2. AŞAMA: SÖZDİZİMSEL ANALİZ (PARSER)
# ==========================================
class Ayristirici:
    def __init__(self, tokenlar):
        self.tokenlar = tokenlar
        self.konum = 0

    def suanki_token(self):
        if self.konum < len(self.tokenlar):
            return self.tokenlar[self.konum]
        return None

    def tuket(self, beklenen_tur, beklenen_deger=None):
        token = self.suanki_token()
        if token and token[0] == beklenen_tur:
            if beklenen_deger is None or token[1] == beklenen_deger:
                self.konum += 1
                return token
                
        bulunan = token[1] if token else 'Dosya Sonu'
        raise SyntaxError(f"NovaScript Hatası: Beklenen '{beklenen_deger or beklenen_tur}', ancak '{bulunan}' bulundu.")

    def agaci_olustur(self):
        ifadeler = []
        while self.suanki_token() is not None:
            ifadeler.append(self.satir_ayristir())
        return ifadeler

    def satir_ayristir(self):
        token = self.suanki_token()
        
        # 1. Değişken Ataması
        if token[0] == 'IDENTIFIER':
            degisken_adi = self.tuket('IDENTIFIER')[1]
            self.tuket('OPERATOR', '=')
            deger = self.ifade_ayristir()
            self.tuket('TILDE', '~')
            return ('ATAMA', degisken_adi, deger)
            
        # 2. Ekrana Yazdırma (goster)
        elif token[0] == 'KEYWORD' and token[1] == 'goster':
            self.tuket('KEYWORD', 'goster')
            self.tuket('LPAREN', '(')
            deger = self.ifade_ayristir()
            self.tuket('RPAREN', ')')
            self.tuket('TILDE', '~')
            return ('GOSTER', deger)
            
        # 3. Eger ve Madem Blokları
        elif token[0] == 'KEYWORD' and token[1] in ('eger', 'madem'):
            anahtar_kelime = self.tuket('KEYWORD')[1]
            self.tuket('LPAREN', '(')
            kosul = self.kosul_ayristir()
            self.tuket('RPAREN', ')')
            
            self.tuket('PUNC_OPEN', '<<')
            blok_ici_ifadeler = []
            while self.suanki_token() and self.suanki_token()[0] != 'PUNC_CLOSE':
                blok_ici_ifadeler.append(self.satir_ayristir())
            self.tuket('PUNC_CLOSE', '>>')
            
            blok_turu = 'EGER_BLOK' if anahtar_kelime == 'eger' else 'MADEM_BLOK'
            return (blok_turu, kosul, blok_ici_ifadeler)

        raise SyntaxError(f"NovaScript Hatası: Tanımsız ifade -> {token}")

    def kosul_ayristir(self):
        sol_taraf = self.deger_ayristir()
        operator = self.tuket('OPERATOR')[1]
        sag_taraf = self.deger_ayristir()
        return ('KOSUL', operator, sol_taraf, sag_taraf)

    def ifade_ayristir(self):
        sol = self.deger_ayristir()
        token = self.suanki_token()
        
        if token and token[0] == 'OPERATOR' and token[1] in ('+', '-', '*', '/'):
            operator = self.tuket('OPERATOR')[1]
            sag = self.deger_ayristir()
            return ('ISLEM', operator, sol, sag)
            
        return sol

    def deger_ayristir(self):
        token = self.suanki_token()
        if token[0] == 'NUMBER':
            self.tuket('NUMBER')
            return ('SAYI', int(token[1]))
        elif token[0] == 'STRING':
            self.tuket('STRING')
            return ('METIN', token[1].strip('"'))
        elif token[0] == 'IDENTIFIER':
            self.tuket('IDENTIFIER')
            return ('DEGISKEN', token[1])
            
        raise SyntaxError("NovaScript Hatası: Geçersiz değer biçimi")

# ==========================================
# 3. AŞAMA: ÇALIŞTIRICI (EVALUATOR)
# ==========================================
class Calistirici:
    def __init__(self, soyut_agac):
        self.agac = soyut_agac
        self.bellek = {}

    def calistir(self):
        for satir in self.agac:
            self.satir_isle(satir)

    def satir_isle(self, dugum):
        tur = dugum[0]

        if tur == 'ATAMA':
            self.bellek[dugum[1]] = self.deger_hesapla(dugum[2])

        elif tur == 'GOSTER':
            print(self.deger_hesapla(dugum[1]))

        elif tur == 'EGER_BLOK':
            if self.kosul_hesapla(dugum[1]) is True:
                for ic_satir in dugum[2]:
                    self.satir_isle(ic_satir)

        elif tur == 'MADEM_BLOK':
            while self.kosul_hesapla(dugum[1]) is True:
                for ic_satir in dugum[2]:
                    self.satir_isle(ic_satir)

    def kosul_hesapla(self, kosul_dugumu):
        operator = kosul_dugumu[1]
        sol = self.deger_hesapla(kosul_dugumu[2])
        sag = self.deger_hesapla(kosul_dugumu[3])

        if operator == '>': return sol > sag
        elif operator == '<': return sol < sag
        elif operator == '==': return sol == sag
        elif operator == '!=': return sol != sag
        elif operator == '>=': return sol >= sag
        elif operator == '<=': return sol <= sag
        return False

    def deger_hesapla(self, deger_dugumu):
        if deger_dugumu[0] in ('SAYI', 'METIN'):
            return deger_dugumu[1]
            
        elif deger_dugumu[0] == 'DEGISKEN':
            degisken_adi = deger_dugumu[1]
            if degisken_adi in self.bellek:
                return self.bellek[degisken_adi]
            else:
                raise NameError(f"NovaScript Hatası: '{degisken_adi}' adında bir değişken bulunamadı!")
                
        elif deger_dugumu[0] == 'ISLEM':
            operator = deger_dugumu[1]
            sol = self.deger_hesapla(deger_dugumu[2])
            sag = self.deger_hesapla(deger_dugumu[3])
            
            if operator == '+': return sol + sag
            elif operator == '-': return sol - sag
            elif operator == '*': return sol * sag
            elif operator == '/': return sol / sag

# ==========================================
# TEST BLOĞU
# ==========================================
if __name__ == "__main__":
    kaynak_kod = """
    sayi = 10 ~
    metin = "Sistem basariyla calisiyor!" ~

    eger (sayi > 5) <<
        goster(metin) ~
    >>

    madem (sayi > 7) <<
        sayi = sayi - 1 ~
        goster(sayi) ~
    >>
    """
    
    try:
        print("Sistem Baslatiliyor...\n" + "="*30)
        tokenlar = lexer(kaynak_kod)
        ayristirici = Ayristirici(tokenlar)
        ast_agaci = ayristirici.agaci_olustur()
        
        print("Yazilim Ciktisi:")
        print("-" * 30)
        calistirici = Calistirici(ast_agaci)
        calistirici.calistir()
        print("=" * 30)
    except Exception as hata:
        print(hata)
