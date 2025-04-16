# 🕹️ Comprobador de Reflejos

Estás ante un pequeño juego que mide el tiempo de reacción del jugador. Ha sido diseñado para exponerlo como proyecto científico en el día de la ciencia en la calle de A Coruña del año 2025. Está hecho para correr en una Raspberry Pi, pero también es compatible con Windows, macOS y Linux.

![image](https://picsur.matas.com.es/i/2c442874-16c8-4563-bbb2-a575e6b70f71.jpg)

---

## 🎮 ¿Cómo funciona?

1. **Pantalla de bienvenida**: ingresa tu nombre para empezar a jugar y mira el ranking. A la derecha tendrás las estadísticas de todos los que han participado en el juego (Se guardan en un archivo .json por separado). 
2. **Pantalla de atención**: espera un tiempo aleatorio entre 3 y 10 segundos (no hay cuentas atrás. Se trata de medir reflejos ante un imprevisto, por lo que hemos eliminado cualquier posibilidad de prever el momento en que hay que pulsar el botón).
3. **¡Pantalla roja!**: cuando aparezca, pulsa una tecla lo más rápido que puedas.
4. **Pantalla de resultados**: mostrará tu tiempo, la media humana, el mejor tiempo histórico y un histograma con los resultados de todos los jugadores.
5. Si tardas demasiado o pulsas antes de tiempo... ¡pierdes!

---

## 💾 Requisitos

- Python 3.x
- pygame
- Intentaremos poner una versión .exe para ejecutarla en Windows

Dependencias necesarias antes de correr el juego:

```bash
pip install pygame
```

Ejecución del juego:
```bash
python3 juego.py
```
