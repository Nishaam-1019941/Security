# Werkplaats 2 2023 - TestGPT

# Inleiding
Deze opdracht hebben we aangenomen van Test-Correct (https://www.test-correct.nl/). Test-Correct maakt een toetsplatform gericht op een andere manier van leren. Zij leggen de nadruk op het gezamelijk nakijken en bespreken van toetsen. Daarvoor dienen de toetsen zelf dus ook uitgevoerd te worden in het test-correct platform. En daaruit volgt dat ook de vragen in het test-correct platform moeten worden ingevoerd.

Test-Correct probeert daarin de docenten zo veel mogelijk te helpen, met bijvoorbeeld een enorme databank met vragen die ze kunnen gebruiken. Maar het bedenken en uitschrijven is nog steeds een enorme klus. Om docenten daarin tegemoet te komen is Test-Correct van plan om een AI taalmodel in te schakelen. Dat wordt een dure onderneming en daarvoor hebben ze ons gevraagd om een proof-of-concept te maken. Die kunnen ze laten zien aan hun klanten en aan de hand van de feedback daarop kunnen ze dan beslissen of ze deze ontwikkeling willen inzetten. 

In de aanloop moet je even bedenken dat docenten hun vragen vaak maken op de bestaande stof. Dat is een stuk tekst, bijvoorbeeld een hoofdstuk uit een boek. Daaruit halen ze dan de vragen. Het is dus niet zo dat ze een vraag bedenken en dan een stuk tekst schrijven om die vraag te beantwoorden. Het is vaak andersom.

Wat docenten ook veel doen is, als ze een relevant stuk tekst tegenkomen ergens, dat ze dat dan opslaan. Ergens in een Word document, of een browser bookmark. Dat kan dan later van pas komen als ze de toetsvragen maken. 

En die twee zaken denken de mensen van Test-Correct te kunnen combineren. Ze willen een tool aanbieden waar docenten hun stukken tekst kunnen opslaan. En dan kunnen ze daar later vragen bij laten genereren, die vanuit het tool rechtstreeks in het Test-Correct platform kunnen worden ingevoerd.

# Opdracht & requirements
We gaan dus een web applicatie maken waarin docenten stukken tekst kunnen opslaan. Vanuit deze notities kunnen ze vragen kunnen laten genereren met behulp van AI. Kort door de bocht wil een docent ongeveer het volgende kunnen doen:
- Een stuk tekst opslaan, met een aantal kenmerken zoals de bron en een categorie. 
- Een docent wil door zijn notities kunnen zoeken
- Een docent wil het systeem toetsvragen laten genereren uit die notities

We kunnen deze eisen opdelen in een aantal deelcomponenten:

### Notities opslaan
Het belangrijkste component van onze applicatie is het opslaan van notities. We willen dat een docent een stuk tekst kan opslaan. Dat kan een stuk tekst zijn dat hij zelf heeft geschreven, of een stuk tekst dat hij ergens heeft gevonden.

Een notitie heeft: 
- Een (optionele) *titel*. Is er geen titel, dan gebruiken we de eerste 20 woorden van de notitie als titel.
- Een *bron*. Dit is de bron van de notitie. Bijvoorbeeld een URL verwijzend naar een website, een boek, een website of een artikel.
- Een *categorie*. Dit is een categorie die de docent uit een lijstje kan kiezen. Bijvoorbeeld "Wiskunde", "Geschiedenis" of "Biologie". Een docent mag zelf categorieën toevoegen of de naam wijzigen in deze lijst. 
- Een optie *"Publiek beschikbaar"* die standaard actief is. Als deze optie aan staat, dan kunnen andere docenten de notitie ook zien. Als deze optie uit staat, dan is de notitie alleen zichtbaar voor de docent die hem heeft opgeslagen.
- Een *aanmaakdatum*. Dit is de datum waarop de notitie is aangemaakt. Datums zijn moeilijke dingen om mee te werken, de datum is niet wijzigbaar, maar we willen dat die wel wordt getoond bij een notitie, in "jaar - maand - dag uur:minuut" formaat.
- Natuurlijk de *tekst* van de notitie zelf.

Het invullen van een notitie moet zo gemakkelijk mogelijk zijn. De categorie zou bijvoorbeeld het beste een opzoeklijst kunnen zijn, en dan met voorkeur al gevuld met de laatst gebruikte. Dat zou ook betekenen dat je (ergens anders) een CRUD scherm moet hebben voor categorieën.

### Notities doorzoeken
Docenten die de applicatie openen willen we in eerste instantie hun eigen notities laten zien, in pagina's van 20. Ze moeten vanuit daar de notities kunnen openen, verwijderen en bewerken. Daarnaast willen we de lijst kunnen filteren op zoekwoorden, per categorie en willen we de optie "Van alle docenten" kunnen toevoegen.

Een voorbeeld van hoe de lijst er uit zou kunnen zien:

![notities_lijst.png](docs%2Fimages%2Fnotities_lijst.png)

Het staat je vrij om de lijst anders in te delen of andere gegevens te tonen.  

### Stijl en opmaak
Test-correct heeft een huisstijl, met een exact kleurenpalet en lettertype. We willen dat je deze huisstijl gebruikt, maar we hebben deze niet meegekregen van de opdrachtgever, je zult dus zelf een stylesheet moeten maken (of deels kopiëren). Je kunt je laten inspireren door https://www.test-correct.nl/welcome.

### Vragen generen 
Onder een notitie willen we de optie hebben om één of meerdere open vragen te genereren. We willen dat de web applicatie daarop de vraag genereert en dat je het resultaat laat zien, wijzigbaar voor de docent. Zie ook het kopje "ChatGPT" voor meer uitleg over de bron van de vraag. 

De docent kan de gegenereerde vraag wijzigen en vervolgens opslaan.

Verder:
- De knop om vragen te genereren blijft beschikbaar bij de notitie, ook als er al vragen zijn gegenereerd.
- Indien er al een vraag is gegenereerd voor een notitie moet die meteen getoond worden bij de notitie en gewijzigd kunnen worden als men de notitie wijzigt. 
- We willen een optie hebben om vragen bij een notitie te verwijderen.

Ook moet de filter optie van de lijst worden uitgebreid met een "Met vragen" aan/uit optie. 

### Exporteren
Vanuit een notitie moet de docent de vragen kunnen exporteren naar Test-Correct. Dit is slechts de opzet, dus voor nu willen we dat de vraag geëxporteerd kan worden in CSV formaat. Zie het kopje "CSV" voor meer uitleg. 

Liefst zouden we deze knop ook in een lijst willen hebben, om de huidige resultaten van een lijst als CSV te kunnen exporteren.

### Login
Om de notities te kunnen organiseren willen we dat docenten alleen de eigen notities kunnen zien. De meest gebruikelijke oplossing is door een login te maken, met een wachtwoord. Er zal dan ook een admin account of rol moeten komen die nieuwe gebruikers kan aanmaken, bekijken en verwijderen en alle notities kan bekijken. Bij een notitie willen we dus ook kunnen terug zien wie de notitie heeft gemaakt.   

### Gebruiksgemak notities
De eerste requirement stelt dat we notities kunnen opslaan, maar dit is heel basaal. We moeten het docenten zo gemakkelijk mogelijk maken om notities op te slaan. We hebben een aantal verbeteringen bedacht: 
- Waarschijnlijk zijn docenten bezig met één vak / categorie tegelijk. We willen dat als eerst de laatst gebruikte categorie van een docent wordt geselecteerd in nieuwe notities.
- Het zou ook mooi zijn als we meerdere categorieën kunnen toekennen aan een notitie.  
- De URL zou bij bekijken van een notitie klikbaar moeten zijn

Gebruiksgemak is belangrijk, probeer je in te leven in de docenten die de applicatie gaan gebruiken. Andere verbeteringen zijn welkom en zouden onder deze requirement kunnen vallen. 

### Multiple choice vragen
We hebben gesteld dat we open vragen willen hebben, maar we zouden ook graag een optie willen hebben om multiple choice vragen te genereren. Deze zouden verder dezelfde regels volgen als de open vragen.  

### Antwoorden opslaan
Wat ook mooi zou zijn is als we de open vragen die we gegenereerd hebben terug aanbieden aan ChatGPT en meteen een antwoord laten genereren. Dat antwoord zou dan ook opgeslagen kunnen worden bij de vraag in een apart veld. 

# Technische details

### Over de requirements
De lijst met functionaliteiten is opgesteld in volgorde van prioriteit. Dat wil zeggen, de opdrachtgever vind de eerste zaken in de lijst het belangrijkst. Hou daar rekening mee in de planning - verzoeken die klinken als "zou willen" of "het zou mooi zijn als" zou je bijvoorbeeld in een latere sprint uitvoeren dan de zaken die klinken als "moet". 

We gaan leren werken met scrum. De requirements zijn niet één op één vertaalbaar naar stories. Vaak zul je zaken tegenkomen in de requirements die een eigen story nodig hebben. Discussieer met je team over hoe je stories zo klein mogelijk kunt maken met een duidelijke "definition of done".

### CSV
Een bekende manier om gegevens te exporteren is CSV. Dat is een tekstbestand waarin de gegevens als tabel worden opgeslagen en de kolommen gescheiden zijn door een puntkomma. De eerste rij is gereserveerd voor de kolomnamen. CSV bestanden zijn makkelijk in te lezen en te verwerken in code en Microsoft Excel ziet een CSV bestand ook als gewoon rekenblad. 

Een voorbeeld van CSV uitvoer: 
```
Vraag;Type;A;B;C;D;Antwoord
Welke van deze dieren is een reptie?;MC;Krokodil;Kikker;Koe;Kat;A
Wat onderscheid een reptiel van een amfibie?;Open;;;; 
```
Je ziet dat de eerste rij kolomnamen bevat. In de laatste rij zijn een aantal kolommen leeg, weergegeven met een dubbele puntkomma.

### ChatGPT
Om vragen te genereren willen we gebruik maken van een AI taalmodel. We hebben gekozen voor ChatGPT, een heel bekend model dat is getraind op conversaties. Je kunt zelf rechtstreeks ChatGPT aanspreken (via hun "API"), maar we hebben een Python module gemaakt die je ook kunt gebruiken om vragen te genereren. Deze heeft iets van een wachtwoord nodig in de vorm van een API key. We vragen je deze zelf aan te maken, als volgt: 
- Maak een account aan op https://platform.openai.com/account/api-keys
- Op https://platform.openai.com/account/api-keys, "Create new secret key". 
- Kopieer de key naar een veilige plek. Deze is niet meer terug te halen op de OpenAI site!
- Zet de key in een extern bestand in je Git repository, *zorg ervoor dat dit bestand nooit wordt geüpload naar Github!*

Met de API key kun je nu de volgende code gebruiken: 
```python
from lib.testgpt.testgpt import TestGPT  # Deze module is dus al in jouw Github project aanwezig

my_api_key = "<jouw API key>"  # Deze code mag NIET worden gecommit naar github!
test_gpt = TestGPT(my_api_key)
open_question = test_gpt.generate_open_question(
    "De grutto is een oer-Hollandse weidevogel."
)
print(open_question)  # Dit zal iets zijn als "Geef een voorbeeld van een Hollandse weidevogel."
```
Deze gratis accounts zijn niet permanent bruikbaar, je krijgt een beperkt aantal gratis tokens (de hoeveelheid tekst die je kunt invoeren) per maand. Je kunt dus niet onbeperkt vragen genereren en we raden aan om in eerste instantie de code een vast antwoord terug te laten geven om te voorkomen dat je tokens op raken.

Onze ChatGPT aanpak is heel kort door de bocht. Waarschijnlijk kun je door hier dieper in te duiken veel betere resultaten krijgen. Je kunt de code in `lib/testgpt/testgpt.py` aanpassen om te experimenteren en het staat je geheel vrij om een eigen bibliotheek te kiezen, andere prompts te gebruiken, etcetera.

### Database
We maken gebruik van SQLite. Dit is een database die je in een bestand opslaat. Anders dan bijvoorbeeld "MySQL" heb je 
geen netwerk adres en geen gebruikersnaam en wachtwoord nodig en je kunt de database in je Git repository 
opslaan. Dat is niet iets wat je normaal zou doen, maar in deze opdracht is dat wel de handigste manier om samen te werken.

Wij hebben dit bestand nu in de map "databases" geplaatst, als testgpt.db. Het staat je vrij om deze aan te passen naar
jouw eigen behoeften en om de naam, locatie etcetera te wijzigen. De structuur daar is zoals wij denken dat die handig
is voor de eerste werkzaamheden, maar je bent er niet aan gebonden. Sommige requirements vragen ook om wijzigingen in
de database, dus je zult deze sowieso moeten aanpassen.

Een klein voorbeeld om database gebruik aan te tonen: 
```python
import sqlite3

# Locatie van het database bestand
database_file = "databases/testgpt.db"
# Maak verbinding met het database bestand
conn = sqlite3.connect(database_file)   
# Maak een cursor object waarmee je SQL statements kan uitvoeren
c = conn.cursor()
# Voer een SQL statement uit
result = c.execute("SELECT count(*) FROM teachers")
# Nu niet nodig, maar stel dat dit een UPDATE statement was, dan had je nu moeten committen
# conn.commit()
number_of_teachers = result.fetchone()[0]  
print(f"Er zijn {number_of_teachers} docenten in de database")
# Sluit de verbinding met de database, is netjes, moet niet
conn.close()
```

In lib/databases/database_generator.py vind je een script dat de database aanmaakt en vult met een aantal testgegevens.
Je kunt de SQL in dit script aanpassen om de database opnieuw te genereren en te wijzigen. Let erop dat deze de bestaande
database altijd overschrijft. Je bent de huidige data dus *kwijt* als je dit script uitvoert. Je zou eventueel dit script
kunnen uitbreiden met extra testdata.

# Technische requirements

### Technieken
Er komen een aantal verplichte technieken kijken bij deze opdracht: 
- HTML/CSS
- SQL en database gebruik 
- HTML genereren met Jinja2
- De Python Flask module, in een virtual environment
We verwachten in ieders individuele bijdrage al deze zaken terug te zien.

Daarnaast zijn er een aantal zaken die we je vragen NIET te gebruiken: 
- ORM (Object Relational Mapping) zoals SQLAlchemy. Je zult veel tutorials tegenkomen, maar we willen dat je in deze opdracht de SQL statements zelf schrijft. In volgende werkplaatsen mag je wel ORM  gebruiken.
- Javascript. De webapplicatie wordt veel beter van javascript gebruik, maar we hebben voorgaande jaren gezien dat niet iedereen in de teams kan meekomen met zo veel nieuwe techniek in één blok. Als het hele team al ervaring heeft met javascript is gebruik toegestaan.  
- Andere Python web frameworks. In latere werkplaatsen mag je wel afwijken van Flask.

Voor de verdere specifieke requirements verwijzen we je naar de WP2 introductie presentatie op Teams.

### Producten
We verwachten dat je de volgende producten oplevert in deze werkplaats:
- Een werkende web applicatie in Flask, die voldoet aan de technische en functionele requirements
- HTML pagina's met een correcte opmaak en huisstijl, gegenereerd met Jinja2
- Een SQLite database bestand met de juiste structuur en testdata
- Een README.md bestand in de root van je Git repository, met daarin een aantal zaken: 
  - Een korte beschrijving van de applicatie
  - Een lijst met gebruikte bronnen zoals tutorials, documentatie, ChatGPT prompts etcetera. Gebruik de APA7 standaard. 
  - Een uitleg met hoe een virtual environment te creëren en de applicatie te starten
- De Github issues moeten een goed overzicht geven van de stories die je hebt gemaakt en de taken die je hebt uitgevoerd. Als je geen Github stories hebt gebruikt dien je een export in te voegen met een overzicht van de taken die je hebt uitgevoerd.

### Code kwaliteitseisen
We verwachten dat je code netjes is en dat je je aan de Python conventies houdt. Dat betekent onder andere:
- De code voldoet aan de WP1 regels rondom "spaghetti code" en code duplicatie. Gebruik functies, correcte benamingen, geen "magic numbers", etcetera.
- De code voldoet aan de PEP8 standaard. Je kunt de PEP8 standaard controleren met de `flake8` module.
- De code gebruikt het MVC patroon om de code te scheiden in lagen. 
 
Ook voor de verdere eisen rondom opleveren en code kwaliteit verwijzen we je naar de WP2 introductie presentatie op Teams.


# Appendix

### Database ERD
De initiële database structuur is als volgt:

![database_erd.png](docs%2Fimages%2Fdatabase_erd.png)
