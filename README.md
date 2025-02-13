# Friendly POCSAG Sender + HackRF

Este proyecto permite enviar mensajes POCSAG a un Biper utilizando GNU Radio y un HackRF One como base.
Esta herramienta sirve para facilitar el envío de mensajes mediante comandos o GUI, únicamente configurando
los parametros de nuestro busca y el mensaje que queramos enviar sin tediosas configuraciones o programas complejos.
Por ahora no he podido eliminar las dependencias, pero espero poder hacerlo algún día.

**Recomiendo usar la Maquina Virtual de [Instant GNURadio](https://github.com/bastibl/instant-gnuradio)**.


## Requisitos

### Hardware:
- HackRF One
- Antena compatible

### Software:
- GNU Radio 3.10+
- Python 3
- OsmoSDR
- NumPy
- Bitstring
- PyQt6

## Instalación

### 1. Instalar dependencias

Ejecuta los siguientes comandos en la terminal:

```sh
sudo apt update && sudo apt install -y gnuradio python3-pip libxcb-cursor0
pip3 install numpy bitstring PyQt6
```

Si usas Arch Linux:

```sh
sudo pacman -S gnuradio python-pip xcb-util-cursor
pip install numpy bitstring PyQt6
```

### 2. Instalar y configurar OsmoSDR

```sh
sudo apt install -y gr-osmosdr
```

Verifica que GNU Radio detecta tu HackRF:

```sh
gnuradio-companion
```

O ejecuta:

```sh
hackrf_info
```

Si el dispositivo aparece listado, está correctamente configurado.

## Uso

### Uso desde la línea de comandos

1. Conecta el HackRF One a tu PC y asegúrate de que está detectado con `hackrf_info`.
2. Ejecuta el script `pocsag_sender.py` con los parámetros deseados:

#### Parámetros disponibles:
- `--RIC`: Número RIC del receptor
- `--SubRIC`: SubRIC del receptor
- `--Text`: Mensaje POCSAG a enviar (se añade un espacio al final automáticamente)
- `--pagerfreq`: Frecuencia del receptor
- `--pocsagbitrate`: Bitrate del receptor

Ejemplo:

```sh
./pocsag_sender.py --RIC 1107305 --SubRIC 1 --Text "Hola Mundo" --pagerfreq 148625000 --pocsagbitrate 2400
```

### Uso con la interfaz gráfica (GUI)

1. Asegúrate de tener instaladas todas las dependencias de la GUI:

```sh
pip3 install PyQt6
```

2. Ejecuta la aplicación gráfica:

```sh
python3 pocsag_gui.py
```

3. Introduce los parámetros requeridos en los campos de entrada.
4. Presiona el botón "Enviar" para transmitir el mensaje.
5. La salida del proceso se mostrará en la consola de la interfaz.

## Solución de problemas

- **HackRF no detectado**: Ejecuta `hackrf_info` para verificar la conexión.
- **GNU Radio no funciona**: Reinstala las dependencias con `sudo apt install --reinstall gnuradio`.
- **Problemas de permisos**: Asegúrate de ejecutar con `sudo` si es necesario.
- **Problemas con la interfaz gráfica**: Asegúrate de haber instalado `libxcb-cursor0` en Debian/Ubuntu o `xcb-util-cursor` en Arch Linux.

## Créditos

- Basado en el trabajo de ON1ARF & Tauebenuss.

## Aviso

No soy ingeniero en telecomunicaciones (quizá algún día) ni tampoco programador a tiempo completo, solo he adaptado mediante el uso de mis conocimientos
y la IA, el programa original para mantenerlo actualizado y hacer que sea fácil de usar, ya que enviar un mensaje a mi Busca de Coca Cola ha sido un quebradero de cabeza,
espero que sea útil aunque no lo he probado aún con otros modelos.

## Licencia

Este proyecto está licenciado bajo GPL v3.

