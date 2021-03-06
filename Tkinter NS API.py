from tkinter import *
import requests
import xmltodict

def station():
    """dit laat alles tikken, deze functie wordt aangeroepen door het klikken op de "plannen" knop in de interface"""
    gebruikers_bestemming = ''
    Gebruiker_vertrekstation = vertreklocatie.get()
    gebruiker_aankomststation = aankomstlocatie.get()

    def api(station):
        Reistekst['text'] = ''
        """station functie zet gebruiker input bij het "van" veld om naar de stations API en vervolgens naar XML"""
        auth_details = ('janpaulmoolen99@gmail.com', 'BL03juvmVIkzP65x1p8F4iTokVclbRUFv04Icuejr3GW45fGPLsnEA')
        api_url = 'http://webservices.ns.nl/ns-api-avt?station={}'.format(station)
        response = requests.get(api_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)
        return vertrekXML

    vertrekXML = api(Gebruiker_vertrekstation)
    for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
        """Routetekst is om tussenstops te vinden als die er zijn"""
        if 'RouteTekst' in vertrek:
            bestemmingen = vertrek['RouteTekst']
            bestemmingen.replace(" ", "")
            for bestemming in bestemmingen.split(','):
                if gebruiker_aankomststation.title() in bestemming:
                    gebruikers_bestemming = bestemming

        """vertrekvertragingtekst is er om vertraging te vinden als het bij een reis staat"""
        if 'VertrekVertragingTekst' in vertrek:
            vertragings = vertrek['VertrekVertragingTekst']

        """hier gebruiken wij de orderdicts om vertrektijd, eindbestemming, treinsoort etc. op te halen"""
        eindbestemming = vertrek['EindBestemming']
        vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
        vertrektijd = vertrektijd[11:16]  # 18:36
        vertrekspoor = vertrek['VertrekSpoor']
        treintype = vertrek['TreinSoort']

        def geenvertraging():
            """deze functie is de output als er geen vertraging is"""
            if 'RouteTekst' in vertrek:
                if gebruiker_aankomststation.title() in bestemmingen:
                    Reistekst["text"] += '{0}'.format('Om {0} vertrekt er een {1} naar {2} vanaf spoor {3}\n'.format(vertrektijd, treintype, gebruikers_bestemming, vertrekspoor[('#text')]))
            if gebruiker_aankomststation.title() in eindbestemming:
                Reistekst["text"] += '{0}'.format('Om {0} vertrekt er een {1} naar {2} vanaf spoor {3}\n'.format(vertrektijd, treintype, eindbestemming, vertrekspoor[('#text')]))

        def vertraging():
            """deze functie is de output als er wel een trein is met vertraging"""
            if 'RouteTekst' in vertrek:
                if gebruiker_aankomststation.title() in bestemmingen:
                    Reistekst["text"] += '{0}'.format('Om {0} ({1}) vertrekt er een {2} naar {3} vanaf spoor {4}\n'.format(vertrektijd, vertragings, treintype, gebruikers_bestemming, vertrekspoor[('#text')]))
            elif gebruiker_aankomststation.title() in eindbestemming:
                Reistekst["text"] += '{0}'.format('Om {0} ({1}) vertrekt er een {2} naar {3} vanaf spoor {4}\n'.format(vertrektijd, vertragings, treintype, eindbestemming, vertrekspoor[('#text')]))

        """de if en elif zijn er om te kiezen tussen de geenvertraging en vertraging functies"""
        if '#text' in vertrekspoor and 'VertrekVertragingTekst' in vertrek:
            vertraging()
        elif '#text' in vertrekspoor:
            geenvertraging()

"""hier wordt Tkinter opgeroepen en de interface master is root"""
root = Tk()
root.title('NS reisplanner')
root.configure(background='#FFCA1F')

"""dit zijn de afbeeldingen die wij gebruiken"""
nsplanner = PhotoImage(file='images\\nsplanner.png')
buttonphoto = PhotoImage(file='images\\nsplannenknop.png')
vanphoto = PhotoImage(file='images\\van.png')
naarphoto = PhotoImage(file='images\\naar.png')

"""dit is 1 van de afbeeldingen die wij gebruiken"""
nsplannerfoto = Label(root, image=nsplanner, borderwidth=0)
nsplannerfoto.place(x=-250, y=-250, relwidth=1, relheight=1)
nsplannerfoto.lower(belowThis=None)
nsplannerfoto.grid(row=0, column=1)

"""deze knop roept de station functie aan"""
button = Button(root, image=buttonphoto, command=station, fg="white", borderwidth=-2)
button.place(x=1018, y=154)
button.configure(background='#FFCA1F')

"""dit zijn de 2 entry's die wij gebruiken voor de vertrek en aankomstlocatie"""
vertreklocatie = Entry(root, font=('Aldhabi', 14), borderwidth=0)
vertreklocatie.place(x=100, y=105)
vertreklocatie.configure(background='white')

aankomstlocatie = Entry(root, font=('Aldhabi', 14), borderwidth=0)
aankomstlocatie.place(x=685, y=105)
aankomstlocatie.configure(background='white')


def windowsize():
    """Hier kan je met een pixel width en height de windowsize aanpassen"""
    width = 1170
    height = 550
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    return root.geometry("{}x{}+{}+{}".format(width, height, x, y))

"""deze for-loop scaled de output met hoeveel regels die moet laten zien"""
heighttekst = [0]
Reistekst = ""

for reis in Reistekst:
    heighttekst += 1

Reistekst = Label(root, text='', font=('frutiger', 13,), height=heighttekst, justify=LEFT)
Reistekst.place(x=-270, y=227, width=1170)
Reistekst.configure(background='#FFCA1F', height=heighttekst)

windowsize()

root.mainloop()