# 🕹️ Comprobador de Reflejos

Estás ante un pequeño juego que mide el tiempo de reacción del jugador. Ha sido diseñado para exponerlo como proyecto científico en el día de la ciencia en la calle de A Coruña del año 2025. Está hecho para correr en una Raspberry Pi, pero también es compatible con Windows, macOS y Linux.

---

## 🎮 ¿Cómo funciona?

1. **Pantalla de bienvenida**: ingresa tu nombre y mira el ranking.
2. **Pantalla de atención**: espera un tiempo aleatorio entre 3 y 10 segundos (no hay cuentas atrás. Se trata de medir reflejos ante un imprevisto).
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
