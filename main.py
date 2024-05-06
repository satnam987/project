import random
from faker import Faker

fake = Faker()

class Kiezer:
    def __init__(self, voornaam, achternaam, leeftijd):
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.leeftijd = leeftijd
        self.heeft_gestemd = False

    def stem(self, kandidaten, lijsten):
        if not self.heeft_gestemd:
            gekozen_lijst = random.choice(lijsten)
            gekozen_kandidaat = random.choice(gekozen_lijst.kandidaten)
            gekozen_kandidaat.ontvang_stem()
            self.heeft_gestemd = True
            print(f"{self.voornaam} {self.achternaam} heeft gestemd op {gekozen_kandidaat.voornaam} {gekozen_kandidaat.achternaam}.")
        else:
            print(f"{self.voornaam} {self.achternaam} heeft al gestemd en mag niet opnieuw stemmen.")

class Kandidaat:
    def __init__(self, voornaam, achternaam, partij):
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.partij = partij
        self.stemmen = 0

    def ontvang_stem(self):
        self.stemmen += 1

class Lijst:
    def __init__(self, naam, kandidaten):
        self.naam = naam
        self.kandidaten = kandidaten

class Stembiljet:
    def __init__(self, kiezer, keuze):
        self.kiezer = kiezer
        self.keuze = keuze

class Stembus:
    def __init__(self):
        self.stembiljetten = []

    def ontvang_stembiljet(self, stembiljet):
        self.stembiljetten.append(stembiljet)

class Scanner:
    def controleer_stembiljet(self, stembiljet):
        if stembiljet.keuze:
            print("Stembiljet goedgekeurd")
            return True
        else:
            print("Stembiljet afgekeurd")
            return False

    def controleer_en_registreer_stembiljet(self, stembiljet):
        geldig = self.controleer_stembiljet(stembiljet)
        if geldig:
            stembus.ontvang_stembiljet(stembiljet)

class Stemcomputer:
    def __init__(self, usb_stick):
        self.usb_stick = usb_stick

    def stem(self, kiezer, lijsten):
        if not kiezer.heeft_gestemd:
            gekozen_lijst = random.choice(lijsten)
            gekozen_kandidaat = random.choice(gekozen_lijst.kandidaten)
            kiezer.heeft_gestemd = True
            return Stembiljet(kiezer, gekozen_kandidaat)
        else:
            return None

class Chipkaart:
    def __init__(self, identificatiecode):
        self.identificatiecode = identificatiecode

class USBStick:
    def __init__(self, opstartcodes):
        self.opstartcodes = opstartcodes

def log_stemming(kiezer, kandidaat):
    print(f"Stem van {kiezer.voornaam} {kiezer.achternaam} geregistreerd voor {kandidaat.voornaam} {kandidaat.achternaam}.")

def genereer_html_uitslag(lijsten):
    html_content = "<h1>Stemresultaten</h1>"
    for lijst in lijsten:
        html_content += f"<h2>Lijst {lijst.naam[-1]}</h2>"
        html_content += "<ul>"
        for kandidaat in lijst.kandidaten:
            html_content += f"<li>{kandidaat.voornaam} {kandidaat.achternaam}: {kandidaat.stemmen} stemmen</li>"
        html_content += "</ul>"
    return html_content

if __name__ == "__main__":
    usb_stick = USBStick("opstartcodes")
    stembus = Stembus()
    kiezers = []
    for i in range(1200):
        leeftijd = random.randint(18, 90)
        kiezers.append(Kiezer(fake.first_name(), fake.last_name(), leeftijd))  

    kandidaten = []
    for i in range(1200):
        voornaam = fake.first_name()
        achternaam = fake.last_name()
        partij = f"Partij {random.randint(1, 5)}"
        kandidaten.append(Kandidaat(voornaam, achternaam, partij))

    lijsten = []
    for i in range(5):
        lijsten.append(Lijst(f"Lijst {i+1}", random.sample(kandidaten, 10)))

    stemcomputers = []
    for i in range(3):
        stemcomputers.append(Stemcomputer(usb_stick))

    scanner = Scanner()  

    for kiezer in kiezers:
        stemcomputer = random.choice(stemcomputers)
        stembiljet = stemcomputer.stem(kiezer, lijsten)
        if stembiljet:
            stembus.ontvang_stembiljet(stembiljet)
            scanner.controleer_en_registreer_stembiljet(stembiljet)

    html_content = genereer_html_uitslag(lijsten)

    with open("stemming_uitslag.html", "w") as html_file:
        html_file.write(html_content)
