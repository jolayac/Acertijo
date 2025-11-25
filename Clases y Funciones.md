
# Documentación de Clases y Funciones

---

## Modelos

### JuegoPianoModel (`mvvm/Model/juegoPiano.py`)
**Propósito:** Representa el estado y la lógica principal del juego.

- `__init__(teclas, notas)`: Inicializa el modelo con las teclas y notas, genera la melodía aleatoria y prepara el estado inicial.
- `reiniciar()`: Reinicia el estado del juego y genera una nueva melodía.
- `agregar_nota_usuario(nota)`: Añade una nota a la secuencia del usuario y mantiene solo las últimas N notas.
- `usuario_acerto()`: Devuelve `True` si la secuencia del usuario coincide con la melodía generada.

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

- `__init__(master, teclas, notas, on_tecla, on_reproducir_melodia)`: Inicializa la vista, crea los botones y el temporizador.
- `actualizar_tiempo(tiempo)`: Actualiza la etiqueta del temporizador.
- `sombrear_tecla(tecla, duracion_ms=200)`: Sombrea el botón de la tecla por un tiempo y luego lo restaura.

### ViewResultado (`mvvm/View/ViewResultado.py`)
**Propósito:** Vista de resultado, muestra el mensaje final y los botones para reintentar o cerrar.

- `__init__(master, mensaje, on_reintentar, on_cerrar)`: Inicializa la vista, muestra el mensaje y los botones, y bindea las teclas R y Escape.

---

## Clase principal

### Interfaz (`acertijo.py`)
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

El uso de hilos (threading) en este proyecto es fundamental para mantener la interfaz gráfica responsiva y evitar bloqueos al realizar tareas que requieren tiempo, como el temporizador y la reproducción de melodías.

## ¿Dónde y cómo se usan los hilos?

- **Temporizador:**
	- El método `iniciar_temporizador()` en el ViewModel (`JuegoPianoVM`) crea un hilo (`Thread`) que ejecuta el método privado `_hilo_temporizador`. Este hilo descuenta el tiempo restante cada segundo y actualiza la vista usando `after` para no bloquear la interfaz principal.
	- Si el usuario cierra la ventana o reinicia el juego, se utiliza una bandera (`_cerrar`) para que el hilo termine silenciosamente y no intente acceder a widgets destruidos.

- **Sombreado de teclas:**
	- Cuando el usuario presiona una tecla, se crea un hilo que ejecuta la función de sombrear el botón correspondiente por un tiempo breve (200 ms). Esto permite que varias teclas se puedan sombrear/desombrear simultáneamente sin bloquear la interfaz.

- **Reproducción de melodía:**
	- Al pulsar la barra espaciadora o el botón de reproducir melodía, se crea un hilo que reproduce la secuencia de notas generada por el modelo, con pausas entre cada nota. Así, el usuario puede seguir interactuando con la interfaz mientras se reproduce la melodía.

## Ventajas de esta implementación

- La interfaz gráfica nunca se bloquea, incluso si el temporizador está corriendo o se están reproduciendo sonidos.
- Permite manejar múltiples acciones simultáneas (por ejemplo, pulsar varias teclas rápidamente).
- Los hilos se gestionan cuidadosamente para evitar errores al cerrar o reiniciar la ventana, usando banderas y excepciones controladas.

## Resumen de métodos que usan hilos

- `JuegoPianoVM.iniciar_temporizador()` → hilo para el temporizador.
- `JuegoPianoVM.procesar_tecla()` → hilo para sombrear teclas.
- `JuegoPianoVM.reproducir_melodia()` → hilo para reproducir la melodía.

Esta arquitectura permite una experiencia de usuario fluida y robusta en aplicaciones gráficas con Python y Tkinter.