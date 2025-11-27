
# Documentación de Clases y Funciones

---

## Modelos

### JuegoPianoModel (`mvvm/Model/juegoPiano.py`)
**Propósito:** Representa el estado y la lógica principal del juego.


- `__init__(teclas, notas, cantidad_notas_melodia=6)`: Inicializa el modelo con soporte para generar melodías de diferentes tamaños según la dificultad.
- `reiniciar(cantidad_notas_melodia=None)`: Reinicia el estado y genera una nueva melodía con tamaño configurable.
---

## ViewModel

### JuegoPianoVM (`mvvm/ViewModel/JuegoPiano_vm.py`)
**Propósito:** Controla la lógica de interacción entre la vista y el modelo, maneja los hilos y la comunicación.

- `__init__(teclas, notas, ruta_notas, vista_juego, vista_resultado_callback)`: Inicializa el ViewModel, crea el modelo y el reproductor de sonidos, y arranca el temporizador.
- `procesar_tecla(tecla)`: Procesa la pulsación de una tecla, reproduce el sonido, actualiza el modelo y verifica si el usuario acertó la melodía.
- `reproducir_melodia()`: Reproduce la melodía generada por el modelo.
- `_hilo_melodia()`: Hilo que reproduce la melodía nota por nota.
- `iniciar_temporizador()`: Inicia el hilo del temporizador.
- `_hilo_temporizador()`: Hilo que actualiza el tiempo restante y muestra el resultado si se acaba el tiempo.
- `reiniciar()`: Reinicia el modelo y el temporizador.

### ReproductorSonidos (`mvvm/ViewModel/ReproductorSonidos_vm.py`)
**Propósito:** Encapsula la reproducción de sonidos usando pygame.

- `__init__(ruta_notas, lista_notas)`: Inicializa pygame y carga los sonidos de las notas.
- `reproducir(nota)`: Reproduce el sonido correspondiente a la nota.

---

## Vistas

### ViewJuego (`mvvm/View/ViewJuego.py`)
**Propósito:** Vista principal del juego, muestra los botones de las teclas y el temporizador.


- `__init__(master, teclas, notas, on_tecla, on_reproducir_melodia, on_mostrar_menu, on_reiniciar)`: Inicializa con layout mejorado en tres frames (superior, central, inferior).
- `_restaurar_boton(btn)`: Restaura botón a estado normal con manejo de excepciones TclError.
### ViewResultado (`mvvm/View/ViewResultado.py`)
**Propósito:** Vista de resultado, muestra el mensaje final y los botones para reintentar o cerrar.

- `__init__(master, mensaje, on_reintentar, on_cerrar)`: Inicializa la vista, muestra el mensaje y los botones, y bindea las teclas R y Escape.

---

## Clase principal

### Interfaz (`MelodiaPiano.py`)
**Propósito:** Ventana principal del juego, gestiona el cambio entre la vista de juego y la de resultado.

- `__init__()`: Inicializa la ventana principal, define las teclas y notas, y muestra la vista de juego.
- `mostrar_juego()`: Muestra la vista de juego y reinicia el ViewModel.
- `mostrar_resultado(mensaje)`: Muestra la vista de resultado y ajusta la geometría de la ventana.
- `on_tecla(tecla)`: Llama al ViewModel para procesar la tecla.
- `on_reproducir_melodia()`: Llama al ViewModel para reproducir la melodía.
- `on_keypress(event)`: Maneja las teclas especiales (Space, R, Escape) y delega las demás al ViewModel.

---



---

# Implementación de hilos en el programa






## ¿Se usan hilos en este programa?

**Sí**, se usan hilos de manera controlada en dos contextos principales: temporizador y reproducción de melodía.

## ¿Dónde y cómo se usan los hilos?

### 1. **Temporizador**
- El método `iniciar_temporizador()` crea un hilo daemon que ejecuta `_hilo_temporizador()`.
- Este hilo descuenta el tiempo cada segundo usando `time.sleep(1)` y actualiza la vista con `after()`.
- Verifica la bandera `_cerrar` para terminar silenciosamente si es necesario.
- Captura excepciones `RuntimeError` si la ventana se cierra.

### 2. **Reproducción de melodía**
- El método `reproducir_melodia()` crea un hilo daemon que ejecuta `_hilo_melodia()`.
- Reproduce las notas con pausas de 0.5 segundos usando `time.sleep(0.5)`.
- Permite interacción durante la reproducción sin congelar la interfaz.

### 3. **Sombreado de teclas**
- **Ya NO usa hilos** en la versión actual (se removió para evitar errores TclError).
- Ahora usa `after()` de Tkinter directamente en la vista.
- Incluye manejo de excepciones `TclError` para widgets destruidos.
## Ventajas de esta implementación


## Resumen de métodos que usan hilos


 Esta arquitectura permite una experiencia de usuario fluida y robusta con control preciso de concurrencia.
 
 - La interfaz **nunca se bloquea** porque operaciones largas se ejecutan en hilos separados.
 - El **temporizador funciona independientemente** sin detener la interacción del usuario.
 - La **reproducción no congela** la interfaz, permitiendo interacción durante su ejecución.
 - Los hilos son **daemon threads** que cierran automáticamente con la aplicación.
 - Las excepciones se capturan para evitar crashes por widgets destruidos.
 
 ## Resumen de métodos que usan hilos
 
 - `JuegoPianoVM.iniciar_temporizador()` → crea hilo daemon para `_hilo_temporizador()`.
 - `JuegoPianoVM._hilo_temporizador()` → hilo que decrementa tiempo y actualiza vista.
 - `JuegoPianoVM.reproducir_melodia()` → crea hilo daemon para `_hilo_melodia()`.
 - `JuegoPianoVM._hilo_melodia()` → hilo que reproduce notas con pausas.