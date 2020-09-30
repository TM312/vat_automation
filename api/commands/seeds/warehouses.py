from datetime import datetime
#https: // www.amalyze.com/en/glossar/amazon-fulfillment-center/
warehouses = [
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'FRA1',
        'type_code': '',
        'address': 'Amazon Logistik GmbH, Am Schloss Eichhof 1, 36251 Bad Hersfeld',
        'size_m2': 42_000,
        'opening_date': datetime.strptime('01-01-1999', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'FRA3',
        'type_code': '',
        'address': 'Amazon Logistik GmbH, Obere Kuehnbach/Amazonstr. 1, 36251 Bad Hersfeld',
        'size_m2': 110_000,
        'opening_date': datetime.strptime('01-01-2009', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'STR1',
        'type_code': '',
        'address': 'Amazon Pforzheim GmbH, Amazonstrasse 1, 75177 Pforzheim',
        'size_m2': 110_000,
        'opening_date': datetime.strptime('01-01-2012', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'BER3',
        'type_code': '',
        'address': 'Amazon Logistik Potsdam GmbH, Havellandstraße 5, 14656 Brieselang',
        'size_m2': 65_000,
        'opening_date': datetime.strptime('01-01-2013', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'EDE4 & EDE5',
        'type_code': '',
        'address': 'Amazon Logistik Werne GmbH, Wahrbrink 25, 59368 Werne',
        'size_m2': 138_000,
        'opening_date': datetime.strptime('01-01-2010', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'DUS2',
        'type_code': '',
        'address': 'Amazon Fulfillment Germany GmbH, Amazonstr. 1, 47495 Rheinberg',
        'size_m2': 110_000,
        'opening_date': datetime.strptime('01-01-2011', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'LEJ1',
        'type_code': '',
        'address': 'Amazon Distribution GmbH, Amazonstr. 1, 04347 Leipzig',
        'size_m2': 75_000,
        'opening_date': datetime.strptime('01-01-2006', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'CGN1',
        'type_code': '',
        'address': 'Amazon Koblenz GmbH, Amazonstr. 1, 56068 Koblenz',
        'size_m2': 110_000,
        'opening_date': datetime.strptime('01-01-2012', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'MUC3',
        'type_code': '',
        'address': 'Amazon FC Graben GmbH, Amazonstr. 1, 86836 Graben',
        'size_m2': 110_000,
        'opening_date': datetime.strptime('01-01-2011', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': 'PAD1',
        'type_code': '',
        'address': 'Amazon Logistik Oelde GmbH, AUREA 10, 59302 Oelde, Deutschland',
        'size_m2': 110_000,
        'opening_date': datetime.strptime('01-06-2020', '%d-%m-%Y').date(),

    },
    {
        'platform_code': 'AMA',
        'active': True,
        'name_code': '',
        'type_code': '',
        'address': 'Amazon Logistik Suelzetal GmbH, Bielefelder Str. 9, 39171 Sülzetal, Germany',
        'size_m2': 97_000,
        'opening_date': datetime.strptime('03-08-2020', '%d-%m-%Y').date(),

    },





# https: // www.aboutamazon.de/logistikzentrum/unsere-logistikzentren/unser-logistiknetzwerk
# Sortable“: In „Sortable“-Logistikzentren, die ca. 74.000 Quadratmeter groß sind, können bis zu 1.500 Vollzeitangestellte arbeiten. In diesen Gebäuden werden Kundenbestellungen wie Bücher, Spielwaren und Haushaltswaren von Amazon Mitarbeitern zusammengestellt, verpackt und verschickt. Häufig arbeiten sie dabei mit der Technologie von Amazon Robotics zusammen, erwerben dadurch neue Kompetenzen und tragen so zu einem effizienteren Ablauf bei, der unserer hohen Kundennachfrage gerecht wird.
# „Non-Sortable“: „Non-Sortable“-Logistikzentren können 56.000 bis ca. 110.000 Quadratmeter groß sein und bieten über 1.000 Vollzeitarbeitsplätze. In diesen Gebäuden werden für die Bestellungen sperrige oder große Artikel wie Gartengeräte, Outdoor-Ausrüstungen oder Teppiche von Amazon Mitarbeitern herausgesucht, verpackt und verschickt.
# Sortierzentren: In den Sortierzentren werden Kundenbestellungen von Mitarbeitern zur schnelleren Lieferung nach den Bestimmungsorten sortiert und auf Lkws verteilt. In den Sortierzentren von Amazon gibt es Karrieremöglichkeiten in Voll- und Teilzeit.
# „Receive“-Zentrum: „Receive“-Zentren tragen zur effizienten Erfüllung von Kundenwünschen bei, denn sie nehmen große Mengen an Waren an, für die eine hohe Nachfrage herrscht. Von den „Receive“-Zentren aus werden sie an die Logistikzentren aus dem Amazon Netzwerk verteilt. In diesen rund 56.000 Quadratmeter großen Gebäuden sind Vollzeit- und Teilzeitstellen verfügbar.
# „Speciality“-Zentren: Zum Amazon Logistiknetzwerk gehören noch weitere Gebäudearten, in denen spezielle Kategorien von Artikeln bearbeitet werden oder die während Zeiten mit besonders starker Kundennachfrage, etwa der Weihnachtszeit, mit erhöhten Kapazitäten betrieben werden.
# Verteilzentren: In den Verteilzentren bereiten wir Kundenbestellungen für die „letzte Meile“ der Zustellung vor. Sie ermöglichen unseren schnellen täglichen Versand.
