# File loader

Aplicacion para windows 10, el caso es copiar o comprimir un archivo o carpeta y pasarlo a una carpeta que se sirve en nginx a travez de un tunnel de cloudflare para que los usuarios puedan descargar los archivos.

Para generar el programa
```
pyinstaller .\main.py
```

Se configura las rutas en un archivo .env

- La aplicacion permite seleccionar un archivo o carpeta
- copia el archivo directamente, comprime la carpeta y la guarda en el directorio de storage
- genera el enlace para que se pueda descargar con el dominio configurado
- copia el dominio al portapapeles
- guarda una entrada en la lista en un archivo xml llamado file_data.xml
- en caso selecciona en lista un nombre de archivo o carpeta guardado previamente copia su respectivo link al portapapeles