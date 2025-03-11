import tkinter as tk
from tkinter import Listbox, filedialog
from tkinter import ttk
from dotenv import load_dotenv
import os
import uuid
import shutil
import xml.etree.ElementTree as ET

# Cargar variables de entorno desde el archivo .env
load_dotenv()

storage_path = os.getenv('STORAGE_PATH', '')
last_file_uploaded = ""

def cargar():
    global last_file_uploaded
    # Abrir el selector de archivos
    if option_var.get() == "file":
        file_path = filedialog.askopenfilename()
    else:
        file_path = filedialog.askdirectory()
    if file_path:
        label_carga.config(text="Cargando...")
        if os.path.isdir(file_path):
            # Comprimir los archivos en el directorio seleccionado en formato zip
            last_file_uploaded = str(uuid.uuid4()) + '.zip'
            new_file_name = os.path.join(storage_path, last_file_uploaded)
            shutil.make_archive(new_file_name, 'zip', file_path)
        else:
            # Copiar el archivo al directorio de almacenamiento con un nombre aleatorio
            last_file_uploaded = str(uuid.uuid4()) + os.path.splitext(file_path)[1]
            new_file_name = os.path.join(storage_path, last_file_uploaded)
            shutil.copy(file_path, new_file_name)
        # Simular progreso
        label_carga.config(text="Carga finalizada")
        # Guardar en archivo XML
        save_to_xml(file_path, last_file_uploaded)
        # Actualizar la lista
        update_listbox()
        copy_link()

def save_to_xml(original_dir, uploaded_file):
    xml_file = 'file_data.xml'
    if os.path.exists(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
    else:
        root = ET.Element("files")
        tree = ET.ElementTree(root)
    
    file_element = ET.Element("file")
    original_dir_element = ET.SubElement(file_element, "original_dir")
    unique_id = str(uuid.uuid4())[:8]
    original_dir_element.text = unique_id + "_" + original_dir
    #original_dir_element.text = original_dir
    uploaded_file_element = ET.SubElement(file_element, "uploaded_file")
    uploaded_file_element.text = uploaded_file
    root.append(file_element)
    
    tree.write(xml_file)

def update_listbox():
    lista.delete(0, tk.END)
    xml_file = 'file_data.xml'
    if os.path.exists(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for file_element in root.findall('file'):
            original_dir = file_element.find('original_dir').text
            lista.insert(tk.END, original_dir)

def generate_link(file_name):
    return default_domain + file_name

def copy_link():
    # Copiar el link al portapapeles
    root.clipboard_clear()
    root.clipboard_append(generate_link(last_file_uploaded))
    root.update()  # Actualizar el portapapeles
    # Mostrar mensaje de éxito
    tk.messagebox.showinfo("Copiar Link", "Link copiado al portapapeles")

def on_listbox_double_click(event):
    selected_index = lista.curselection()
    if selected_index:
        selected_text = lista.get(selected_index)
        xml_file = 'file_data.xml'
        if os.path.exists(xml_file):
            tree = ET.parse(xml_file)
            xroot = tree.getroot()
            for file_element in xroot.findall('file'):
                original_dir = file_element.find('original_dir').text
                file_generated = file_element.find('uploaded_file').text
                if original_dir == selected_text:
                    root.clipboard_clear()
                    root.clipboard_append(generate_link(file_generated))
                    root.update()
                    tk.messagebox.showinfo("Copiar Link", f"Nombre del archivo '{selected_text}' copiado al portapapeles")
                    break

# Obtener el valor de DEFAULT_DOMAIN desde el archivo .env
default_domain = os.getenv('DEFAULT_DOMAIN', '')

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación Sencilla")
root.geometry("800x800")

# Crear el label y el campo de entrada para "Domain"
label_domain = tk.Label(root, text="Domain")
label_domain.pack(pady=10)
entry_domain = tk.Entry(root)
entry_domain.pack(fill=tk.X, padx=20, pady=10)
entry_domain.insert(0, default_domain)  # Establecer el valor predeterminado

# Crear opciones para seleccionar archivo o directorio
option_var = tk.StringVar(value="dir")

frame_options = tk.Frame(root)
frame_options.pack(pady=10)

radio_file = tk.Radiobutton(frame_options, text="Archivo", variable=option_var, value="file")
radio_file.pack(side=tk.LEFT, padx=10)

radio_dir = tk.Radiobutton(frame_options, text="Directorio", variable=option_var, value="dir")
radio_dir.pack(side=tk.LEFT, padx=10)

# Crear el botón "Cargar"
boton_cargar = tk.Button(root, text="Cargar", command=cargar)
boton_cargar.pack(pady=20)

# Crear el botón "Copiar Link"
boton_cl = tk.Button(root, text="Copiar Link", command=copy_link)
boton_cl.pack(pady=20)

# Crear la barra de progreso
label_carga = tk.Label(root, text="...")
label_carga.pack(pady=10)

# Crear la lista
lista = Listbox(root)
lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)



# Asociar el evento de doble clic a la lista
lista.bind("<Double-1>", on_listbox_double_click)

# Cargar la lista inicial desde el archivo XML
update_listbox()

# Iniciar el bucle principal de la aplicación
root.mainloop()