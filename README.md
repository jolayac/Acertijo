# Acertijo

Juego educativo tipo "acertijo de melodía" — reproduce una melodía con las teclas indicadas antes de que se acabe el tiempo.

## Qué hace
El juego genera una melodía aleatoria (6 notas) a partir de una lista de notas configurables. El jugador debe reproducir esa secuencia usando las teclas del teclado o haciendo clic en los botones en pantalla. Si reproducen la secuencia completa antes de que termine el temporizador, ganan.

Características principales:
- Interfaz gráfica con botones que representan teclas de piano.
- Reproducción de archivos MP3 por nota.
- Soporta pulsaciones simultáneas sin problemas visuales (sombreado manejado con hilos).
- Estructura MVVM (modelo, vista, viewmodel) para separar responsabilidades.

## Controles

- Teclas de teclado: las teclas configuradas en `mvvm/main.py` (por defecto: `A, S, D, F, G, H, J, K`) se corresponden con las notas configuradas.
- Clic con mouse: cada botón en pantalla reproduce la nota equivalente.
- Space: reproduce la melodía completa.
- R: intentar de nuevo (reinicia el juego cuando aparece la pantalla de resultado o haciendo clic en el botón correspondiente).
- Esc: cerrar la aplicación.

## Configuración rápida

1. Edita `acertijo.py` si quieres cambiar las teclas o las notas. Hay dos listas al principio de `Interfaz`:

```python
# en mvvm/main.py (Interfaz.__init__)
self.teclas = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K']  # son las teclas a las que se les será asignada una nota
self.notas = ['C4', 'D4', 'E4', 'F4', 'G4', 'A#4', 'B4', 'C5']
```

La librería busca archivos llamados exactamente `C4.mp3`, `D4.mp3`, etc. para cada entrada en `self.notas`.

## Cómo ejecutar

Desde PowerShell (Windows), sitúate en la carpeta del proyecto y ejecuta el archivo acertijo.py

## Requisitos
Pygame
´´Instalar con pip install pygame´´