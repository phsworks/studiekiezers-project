# HBO-ICT x Studiekiezers

In deze repository vind je het startersproject om mee aan de slag te gaan vanaf sprint 2. Dit doe je in een tweetal, waarbij je samenwerkt aan een project. In dit project ga je aan de slag met een interactieve ervaring om toekomstige HBO-ICT studenten, studiekiezers noemen we die, te helpen bij het kiezen van een opleiding. 

## 📁 Project structuur

In de bestanden van dit project vind je de volgende mappen:

- `docs`: Hierin kan je de documentatie kwijt van jullie project. Hiervan wordt een website gegenereerd die je kan vinden onder 'Pages' (Deploy > Pages).
- `teamdocs`: Hierin kan je de documentatie kwijt die specifiek is voor jouw team. Denk hierbij aan de teamrollen, teamafspraken en de teamplanning. Hiervan wordt geen website gegenereerd.
- `arduino`: Hierin kan je de code kwijt voor jouw project wat te maken heeft met jullie embedded systeem, code geschreven in Arduino.
- `webserver`: Hierin vind je een basis Python Flask applicatie met een templates folder voor de HTML, CSS en Javascript.
- `docker`: Hierin kan je de configuratie vinden van de docker containers die we gebruiken voor jullie web-applicatie.

In dit project vind je ook de User Stories en de bijbehorende boards (Plan > Issue boards).

## Vereisten

- Docker
    - https://www.docker.com/get-started/
- Optioneel
    - Visual Studio Code
        - https://code.visualstudio.com/
    - Python
        - https://www.python.org/downloads/

## Aan de slag

1. Clone de repository
2. Start de applicatie:

```bash
docker compose up
```

## 📦 Docker

Binnen dit project vind je een `docker compose`-script waarmee je makkelijk een webserver en database kunt opzetten op je computer. Wanneer je deze werkend hebt (zie hierboven)kan je de volgende services benaderen:

- Webserver: [http://localhost/](http://localhost/)
- Database:
    - Web Client: [http://localhost/phpmyadmin/](http://localhost/phpmyadmin/)
    - MySQL Client:
        - Host: localhost
        - Port: 3306
        - Username: root
        - Password: [wachtwoord uit .env-bestand]