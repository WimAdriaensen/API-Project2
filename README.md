# Basisproject API Development
### Gekozen thema
Het gekozen thema voor mijn API is Thomas More vakken.
Met deze API kan je de lijst met vakken opvragen maar je kan ook enkel de vakken opvragen van een bepaalde richting.
Ook kan je vakken toevoegen door de docent, de naam van het vak en de riching waarin het vak gegeven word mee te geven aan de API. Het laatste wat je kan doen met de API is opvragen wie de maker is van de API met een link naar het Github account van de maker en een link naar de Github repository van de API.

#### Links

| Description | Link |
| --- | --- |
| Hosted API | https://api-wimadriaensen.cloud.okteto.net/ |
| Hosted front-end | https://wimadriaensen.github.io | |
| Repository front-end | https://github.com/WimAdriaensen/wimadriaensen.github.io |

### De front-end
De front-end ziet er als volgt uit.
![image front-end](images/Eerste_zicht_front-end.png)
Bij het laden van de pagina vraagt hij aan de API de huidige lijst van vakken, deze word dan ook getoond op de pagina. onderaan staat een knop 'Refresh' om opnieuw de lijst op te vragen bij de API. <br><br>
Onder de lijst met vakken vind je een lege tabel terug, in deze tabel komen de vakken te staan die je per richting (of klas) vraagt aan de API. Door in het lege veld de richting in te vullen waarvan je de vakken wil zien en vervolgens op de knop 'Search' drukt worden de vakken van deze richting bij de API opgevraagd. <br><br>
Aan de rechterzijde van de pagina kan je een nieuw vak toevoegen door de docent, de naam van het vak en de richting waarin dit vak gegeven word mee te geven aan de API. Door op 'Create course' te drukken worden deze waardes meeggeven aan de API via een POST request. De gegevens die door de API zijn toegevoegd worden daaronder nog eens in het vet weergegeven.<br><br>
Daaronder vind u een knop 'Show maker information', deze knop spreekt de API van github aan en vraagt de Github gegevens op van de eigenaar (ik). Hij geeft de accountnaam van de eigenaar van de Github repository weer als ook de link naar zijn Github account en de link naar de repository.

### Werking API via Postman
Hier zijn enkele screenshots met de werking van de API met de applicatie Postman
![api-get-courses](images/Postman_get_courses.png)
![api-get-courses-class](images/Postman_get_courses_class.png)
