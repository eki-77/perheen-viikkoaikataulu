# Perheen viikkoaikataulu

Projektin tarkoitus on tehdä verkko-sovellus, jonka avulla voi luoda perheelle viikkoaikataulun eli lukujärjestyksen.
Aikataulunäkymä näyttää perheen aikataulun lukujärjestyksen näköisenä kalenterinäkymänä. Järjestelmässä on ylläpitäjiä
ja käyttäjiä.

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi luoda oman viikkoaikataulun.
- Käyttäjä voi luoda viikkoaikataululle perheenjäsenet, joiden aikatauluista on kyse.
- Käyttäjä voi luoda aikatauluun tapahtumia ja muokata ja poistaa niitä.
- Tapahtumalla on nimi, ajankohta (viikonpäivä ja alkamis- ja loppumisajat), siihen osallistuvat perheenjäsenet ja mukaan tarvittavat tavarat.
- Esimerkki tapahtumasta: Esikoisen soittotunti, ti 16-16.30, isä ja esikoinen, mukaan: soitin, nuotit, pyöräilykypärät.
- Käyttäjä voi valita aikataulunäkymästä, keiden perheenjäsenten menot näytetään. Oletuksena näytetään kaikkien menot.
- Klikkaamalla tapahtumaa aikataulunäkymästä näytetään tapahtuman tarkat tiedot.
- Käyttäjä voi antaa toiselle käyttäjälle pääsyn näkemään ja muokkaamaan viikkoaikatauluaan.
- Ylläpitäjä voi tehdä kaikille viikkoaikatauluille samoja asioita kuin käyttäjät itse luomalleen viikkoaikataululle.
- Ylläpitäjä voi poistaa viikkoaikataulun.
- Ylläpitäjä voi poistaa käyttäjältä pääsyn johonkin viikkoaikatauluun.
- Ylläpitäjä voi poistaa käyttäjän.

# Tilanne 17.11.2024

- Luotu tietokantarakenne (schema.sql)
- Luotu moduuleihin jako, toimivat importit ja jonkin verran logiikkaa
- Luotu raakile-etusivu
- Luotu aikataulunäkymä (raakile)

# Tilanne 1.12.2024

- Pahasti on kesken vielä!
- Käyttäjä voi luoda tunnuksen ja kirjautua sisään ja ulos
- Sovelluksessa on yksi ylläpitotunnus (tunnus: admin, salasana: tsoha-admin), joka luodaan etusivulle tultaessa jos sitä ei ole tietokannassa.
- Käyttäjä voi luoda viikkoaikataulun.
- Käyttäjälle näytetään etusivulla ne viikkoaikataulut, joihin hänellä on oikeudet (adminille näytetään kaikki)
- Käyttäjä voi avata viikkoaikataulun.
- Viikkoaikataulussa käyttäjä voi luoda aikatauluun liittyviä henkilöitä.
- Kaikki toiminnot on suojattu sql-injektiolta ja xss- ja csrf-haavoittuvuuksilta.
- Sovelluksessa on virheilmoitussivu, joka näyttää tarkemman virheen kuvauksen.
- Viikkoaikatauluihin liittyvillä sivuilla tarkastetaan, onko käyttäjällä oikeuksia nähdä sivua.
- Eväste pitää tallessa tiedon, mikä viikkoaikataulu on auki (eli mihin luodaan henkilöitä tai tapahtumia).
- Tietokantarakenne ymmärtää tietojen poistamisen päälle (ON DELETE CASCADE).

- Tapahtumia ei voi vielä luoda, eikä niille ole fiksua näyttötapaa.
- Viikkoaikatauluun ei voi vielä antaa oikeuksia muille käyttäjille.
- Mitään lomakkeisiin syötettyjä tietoja ei vielä tarkisteta esim. ylipitkien syötteiden varalta.
- Ylläpitäjä ei voi vielä tehdä oikein mitään mitä kuvauksessa luvataan, ei edes vaihtaa oletussalasanaa (tulossa).

# Lopullinen versio 15.12.2024

- Sovelluksessa on yksi ylläpitotunnus (tunnus: admin), joka luodaan etusivulle tultaessa jos sitä ei ole tietokannassa. 
- Ylläpitotunnuksen ("admin") salasanan voi määritellä .env-tiedostossa. Jos sitä ei ole määritelty siellä, se on "tsoha-admin".

# Testausohjeet 

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain (16 heksadesimaalimerkkiä)>
ADMIN_PW=<admin-tunnuksen salasana>
```

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run
