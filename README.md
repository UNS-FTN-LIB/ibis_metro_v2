# IBIS Projekat

Pokretanje projekta lokalno:
```
docker build -t mqtt ./MQTT
docker build -t simulator ./Simulator
docker-compose up
```

Pokretanje projekta korišćenjem publikovanih docker image-a:
```
docker pull djordje99/simulator
docker pull djordje99/mqtt
docker-compose up
```