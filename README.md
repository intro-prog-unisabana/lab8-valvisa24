[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/3hpwbxq9)
# Laboratorio 8 

## Problema 1: Distribución de Carga

### Contexto

En ingeniería estructural, la **distribución de carga** es fundamental al diseñar puentes, edificios y soportes mecánicos. Este ejercicio aplica los conceptos de CLI y manejo de errores a un problema de ingeniería.

### Tu Tarea

Crea un script `question1.py` que:

1. Reciba **dos argumentos** de línea de comandos:
   - Carga total en Newtons (N)
   - Número de puntos de soporte

2. Calcule la carga por punto de soporte:
   ```python
   load_per_support = total_load / num_supports
   ```

3. Maneje los siguientes errores:

| Situación | Mensaje de Error |
|-----------|------------------|
| Entrada no numérica | `Error: Invalid input! Enter numeric values only.` |
| Missing arguments | `Error: Invalid input! Enter numeric values only.` |
| División por cero | `Error: Cannot divide by zero! Supports must be greater than zero.` |

### Formato de Salida

```plaintext
Load per support point: <value> N
```

El valor debe mostrarse con **2 decimales**.

### Casos de Prueba

**Entrada válida:**

```bash
python question1.py 1000 4
```

```plaintext
Load per support point: 250.00 N
```

**Cero soportes:**

```bash
python question1.py 500 0
```

```plaintext
Error: Cannot divide by zero! Supports must be greater than zero.
```

**Entrada no numérica:**

```bash
python question1.py 1000 five
```

```plaintext
Error: Invalid input! Enter numeric values only.
```

> **Pistas:**
> - Usa `sys.argv` para obtener los argumentos.
> - Envuelve las conversiones de tipo en `try-except` para capturar `ValueError`.
> - Verifica si el divisor es cero **antes** de dividir.
> - Usa f-strings con formato: `f"{value:.2f}"` para mostrar 2 decimales.

## Problema 2: Gestor de Lista de Tareas

En este laboratorio construirás un **gestor de lista de tareas (to-do list)** que se ejecuta desde la terminal. El programa permitirá a los usuarios:

- Guardar tareas en un archivo de texto
- Ver las tareas existentes
- Agregar nuevas tareas
- Eliminar tareas completadas

A lo largo del laboratorio, aplicarás conceptos de **manejo de excepciones** y **argumentos de línea de comandos** para crear un programa robusto que no se bloquee ante entradas inesperadas.

---

## Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `todo_manager.py` | Contiene las funciones `read_todo_file()` y `write_todo_file()`. **Modificarás este archivo en la Parte 1.** |
| `main.py` | Programa principal con la interfaz CLI. **Modificarás este archivo en las Partes 2-5.** |

---

## Parte 1: Manejo de Archivos Faltantes

### Contexto

Tu aplicación necesita cargar tareas desde un archivo. Sin embargo, si el archivo no existe (por ejemplo, es la primera vez que el usuario ejecuta el programa), Python lanzará un `FileNotFoundError` y el programa se bloqueará.

### Objetivo

Modificar la función `read_todo_file()` para que maneje elegantemente el caso cuando el archivo no existe.

### Código Original

```python
def read_todo_file(file_path):
    """Reads tasks from a file. Returns a list of tasks."""
    with open(file_path, 'r') as file:
        return file.read().splitlines()
```

### Tu Tarea

Modifica la función para que:

1. Intente abrir el archivo normalmente.
2. Si el archivo **no existe**, en lugar de bloquearse:
   - Imprima el mensaje: `File <file_path> not found! Returning an empty to-do list.`
   - Retorne una lista vacía `[]`
3. Si el archivo **sí existe**, lea y retorne su contenido como antes.

> **Pista:** Usa un bloque `try-except` para capturar `FileNotFoundError`.

### Casos de Prueba

**Caso 1: El archivo existe**

```python
# Archivo p1e1.txt contiene:
# Buy groceries
# Do laundry

tasks = read_todo_file("p1e1.txt")
print(tasks)
```

```plaintext
['Buy groceries', 'Do laundry']
```

**Caso 2: El archivo no existe**

```python
tasks = read_todo_file("archivo_inexistente.txt")
print(tasks)
```

```plaintext
File archivo_inexistente.txt not found! Returning an empty to-do list.
[]
```

---

## Parte 2: Recibiendo Argumentos de Línea de Comandos

### Contexto

Ahora crearás la interfaz de línea de comandos (CLI) en `main.py`. Los usuarios ejecutarán el programa pasando argumentos desde la terminal:

```bash
python3 main.py tasks.txt view
```

### Configuración Inicial

En `main.py`, agrega los imports necesarios:

```python
import sys
from todo_manager import read_todo_file, write_todo_file
```

### Tu Tarea

Implementa la validación de argumentos:

1. **Verifica que se proporcione al menos un argumento** (la ruta del archivo).
   - `sys.argv[0]` es el nombre del script (se ignora).
   - `sys.argv[1]` debe ser la ruta del archivo.

2. **Si faltan argumentos**, lanza un `IndexError` con el mensaje:
   ```plaintext
   Insufficient arguments provided!
   ```

3. **Si los argumentos son válidos**, imprime:
   - Los argumentos recibidos (sin incluir el nombre del script)
   - Las tareas leídas del archivo

> **Importante:** Envuelve el código que puede lanzar excepciones en bloques `try-except` para que el programa no termine de forma abrupta.

### Formato de Salida

```plaintext
Command-line arguments:
<arg1>
<arg2>
...

Tasks:
<tarea1>
<tarea2>
...
```

### Casos de Prueba

**Caso 1: Argumentos válidos**

```bash
python3 main.py p2e1.txt
```

```plaintext
Command-line arguments:
p2e1.txt

Tasks:
Buy groceries
Do laundry
```

**Caso 2: Sin argumentos**

```bash
python3 main.py
```

```plaintext
Insufficient arguments provided!
```

---

## Parte 3: Implementando el Comando `view`

### Contexto

Ahora implementarás el primer comando: `view`. Este comando mostrará todas las tareas guardadas en el archivo.

### Tu Tarea

1. **Comenta** el código de la Parte 2 que imprime los argumentos y tareas.

2. **Verifica si existe un tercer argumento** (`sys.argv[2]`):
   - Si **es `view`**: lee el archivo y muestra las tareas.
   - Si **es otro valor**: lanza un `ValueError` con el mensaje `Command not found!`
   - Si **no existe**: el programa termina silenciosamente (sin hacer nada).

### Formato de Salida para `view`

```plaintext
Tasks:
<tarea1>
<tarea2>
...
```

### Casos de Prueba

**Caso 1: Comando `view`**

```bash
python3 main.py p3e1.txt view
```

```plaintext
Tasks:
Buy groceries
Do laundry
```

**Caso 2: Comando inválido**

```bash
python3 main.py p3e1.txt delete
```

```plaintext
Command not found!
```

**Caso 3: Sin comando**

```bash
python3 main.py p3e1.txt
```

*(Sin salida — el programa termina silenciosamente)*

---

## Parte 4: Implementando los Comandos `add` y `remove`

### Parte 4A: Comando `add`

#### Objetivo

Permitir al usuario agregar una nueva tarea desde la terminal:

```bash
python3 main.py tasks.txt add "Buy milk"
```

#### Tu Tarea

Extiende la lógica del comando para manejar `add`:

1. **Si el comando es `add`**:
   - Verifica que exista un cuarto argumento (la descripción de la tarea).
   - Si **existe**: agrega la tarea, guarda el archivo, e imprime `Task "<task>" added.`
   - Si **falta**: lanza un `IndexError` con el mensaje `Task description required for "add".`

2. **Si el comando es `view`**: ejecuta la lógica de la Parte 3.

3. **Si el comando es otro**: lanza `ValueError` con `Command not found!`

#### Casos de Prueba

**Agregar tarea exitosamente:**

```bash
python3 main.py p4Ae1.txt add "Finish project"
```

```plaintext
Task "Finish project" added.
```

**Falta la descripción:**

```bash
python3 main.py p4Ae1.txt add
```

```plaintext
Task description required for "add".
```

---

### Parte 4B: Comando `remove`

#### Objetivo

Permitir al usuario eliminar una tarea existente:

```bash
python3 main.py tasks.txt remove "Buy milk"
```

#### Tu Tarea

Extiende la lógica para manejar `remove`:

1. **Si el comando es `remove`**:
   - Verifica que exista un cuarto argumento (la tarea a eliminar).
   - Si **existe y está en la lista**: elimínala, guarda el archivo, e imprime `Task "<task>" removed.`
   - Si **existe pero no está en la lista**: imprime `Task "<task>" not found.`
   - Si **falta**: lanza un `IndexError` con el mensaje `Task description required for "remove".`

> **Pista:** Usa el método `.remove(valor)` de las listas. Este método lanza `ValueError` si el elemento no existe, así que necesitarás manejarlo.

#### Casos de Prueba

**Eliminar tarea exitosamente:**

```bash
python3 main.py p4Be1.txt remove "Do laundry"
```

```plaintext
Task "Do laundry" removed.
```

**Tarea no existe:**

```bash
python3 main.py p4Be1.txt remove "Exercise"
```

```plaintext
Task "Exercise" not found.
```

**Falta la descripción:**

```bash
python3 main.py p4Be1.txt remove
```

```plaintext
Task description required for "remove".
```

---

## Parte 5: Procesando Múltiples Comandos

### Contexto

Actualmente, el programa solo ejecuta un comando por ejecución. En esta parte, lo modificarás para procesar **múltiples comandos** en una sola llamada:

```bash
python3 main.py tasks.txt add "Call mom" remove "Buy groceries" view
```

### Requisitos

#### 1. Validación de Entrada

- Si faltan argumentos, lanza el mismo `IndexError` de la Parte 2.
- Si el primer argumento del usuario (`sys.argv[1]`) es `--help`, imprime el mensaje de ayuda:

```python
print("""Usage: python main.py <file_path> <command> [arguments]...

Commands:
  add "task"    - Add a task to the list.
  remove "task" - Remove a task from the list.
  view          - Display all tasks.

Examples:
  python main.py tasks.txt add "Buy groceries"
  python main.py tasks.txt remove "Do laundry"
  python main.py tasks.txt view
  python main.py tasks.txt add "Call mom" remove "Take out trash" view""")
```

#### 2. Procesamiento Secuencial

- Lee el archivo **una vez** al inicio.
- Itera por los argumentos procesando cada comando:
  - `add` requiere un argumento adicional (la tarea).
  - `remove` requiere un argumento adicional (la tarea).
  - `view` no requiere argumentos adicionales.
- Si un comando no es reconocido, lanza `ValueError` con `Command not found!`

#### 3. Escritura Optimizada

- Escribe el archivo **una sola vez** al final, después de procesar todos los comandos.
- Esto mejora el rendimiento al minimizar operaciones de E/S.

### Casos de Prueba

**Múltiples operaciones:**

```bash
python3 main.py tasks.txt add "Call mom" remove "Buy groceries" view
```

```plaintext
Task "Call mom" added.
Task "Buy groceries" removed.
Tasks:
Finish project
Call mom
```

**Archivo resultante (`tasks.txt`):**

```plaintext
Finish project
Call mom
```

---

## Resumen de Comandos

| Comando | Sintaxis | Descripción |
|---------|----------|-------------|
| `view` | `python3 main.py <file_path> view` | Muestra todas las tareas |
| `add` | `python3 main.py <file_path> add "<task>"` | Agrega una nueva tarea |
| `remove` | `python3 main.py <file_path> remove "<task>"` | Elimina una tarea existente |
| `--help` | `python3 main.py --help` | Muestra la ayuda del programa |

---

## Resumen de Errores a Manejar

| Error | Cuándo Ocurre | Mensaje |
|-------|---------------|---------|
| `IndexError` | Faltan argumentos requeridos | `Insufficient arguments provided!` |
| `IndexError` | Falta descripción para `add` | `Task description required for "add".` |
| `IndexError` | Falta descripción para `remove` | `Task description required for "remove".` |
| `ValueError` | Comando no reconocido | `Command not found!` |
| `FileNotFoundError` | Archivo no existe (Parte 1) | `File <file_path> not found! Returning an empty to-do list.` |
