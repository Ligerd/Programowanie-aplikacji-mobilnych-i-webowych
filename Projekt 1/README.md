# Instrukcja

## Uruchomienie serwera
Aby uruchomić serwer trzeba wejść do folderu o nazwie serwer i zbudować obraz za pomocą polecenia:
```
docker-compose build
```
Po zbudowaniu obrazu trzeba go uruchomić za pomocą polecenia:
```
docker-compose up
open http://localhost:3000
```
## Uruchomienie klienta 
Aby uruchomić klienta trzeba wejść do folderu o nazwie client i zbudować obraz za pomocą polecenia:
```
docker-compose build
```
Po zbudowaniu obrazu trzeba go uruchomić za pomocą polecenia:
```
docker-compose up
```
Strona z formularzem rejestracyjnym będzie dostępna pod adresem:
```
http://localhost:3001
```
## Sprawdzenie działania formularza 
Aby przetestować działanie formularza proszę o wpisanie dowolnego loginu w polu login przykładowo:
```
użytkownik
```
Po wpisaniu logina proszę o przejście do następnego pola. Login zostanie zaakceptowany przez serwer, bo nie ma takiego loginu w bazie serwera. Kolor liter logina zostanie zmieniony na zielony co będzie oznaczać to że jest on zaakceptowany.

Następnie proszę wpisać do polu login: 
```
karolik
```
Login już jest dodany do serwera. Zostanie wypisany komunikat oraz kolor liter loginu zmieni się na czerwony.
