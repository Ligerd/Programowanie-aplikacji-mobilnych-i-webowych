# Instrukcja
Proszę o zklonowanie repozytorium.
## Postawienie aplikacji
Aby postawić aplikację proszę o uruchomienie skryptu o nazwie up.sh. Za pomocą polecenia:
```
bash up.sh
```
W tle zostaną postawione i uruchomione kontenery dla klienta oraz serwera. Początkowa strona z logowanie będzie dostępna pod adresem:
```
http://localhost:3001
```
Jako admina dodałem użytkowanika o następującym loginie i hasłe:
```
Login: admin
Hasło: admin
```
## Rejestracja
Aby zarejestrować się wystarczy podać login i hasło oraz nacisnąć przycisk zarejestrów.
## Wyłączenie aplikacji
Aby aby wyłączyć aplikację proszę o uruhomienie skryptu o nazwie down.sh.  Za pomocą polecenia:
```
bash down.sh
```
## P.S aby skryptu zadziałali proszę o nadanie im odpowiednich uprawień. 
Polecenie do nadania uprawień 
```
chmod -x down.sh up.sh
```