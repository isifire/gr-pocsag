# POCSAG Sender via HackRF

Este proyecto permite enviar mensajes POCSAG utilizando GNU Radio y un HackRF One.

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

## Instalación

### 1. Instalar dependencias

Ejecuta los siguientes comandos en la terminal:

```sh
sudo apt update && sudo apt install -y gnuradio python3-pip
pip3 install numpy bitstring
```

Si usas Arch Linux:

```sh
sudo pacman -S gnuradio python-pip
pip install numpy bitstring
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

1. Conecta el HackRF One a tu PC y asegúrate de que está detectado con `hackrf_info`.
2. Ejecuta el script `pocsag_sender.py` con los parámetros deseados:

### Parámetros disponibles:
- `--RIC`: Número RIC del receptor
- `--SubRIC`: SubRIC del receptor
- `--Text`: Mensaje POCSAG a enviar
- `--pagerfreq`: Frecuencia del receptor
- `--pocsagbitrate`: Bitrate del receptor

Ejemplo:

```sh
./pocsag_sender.py --RIC 1122551 --SubRIC 1 --Text "Hola Mundo" --pagerfreq 148625000 --pocsagbitrate 2400
```

## Solución de problemas

- **HackRF no detectado**: Ejecuta `hackrf_info` para verificar la conexión.
- **GNU Radio no funciona**: Reinstala las dependencias con `sudo apt install --reinstall gnuradio`.
- **Problemas de permisos**: Asegúrate de ejecutar con `sudo` si es necesario.

## Créditos

- Basado en el trabajo de ON1ARF & Tauebenuss

## Licencia

Este proyecto está licenciado bajo GPL v3.
