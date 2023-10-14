import tkinter as tk
from tkinter import filedialog
import assemblyai as aai
import spacy
import pyperclip
from summarizer import Summarizer
import warnings

# Inicializa la ventana principal
root = tk.Tk()
root.title("Audio Transcription")
root.geometry("1000x600")
root.configure(bg="#151515")  # Color de fondo de la ventana (morado)

# Inicializa el modelo de procesamiento de lenguaje natural de spaCy (brissa debes tener spaCy instalado y el modelo de lenguaje adecuado)
nlp = spacy.load("es_core_news_sm")

# Variable para rastrear el estado de la transcripción
transcription_ready = False

# Función para seleccionar archivos locales y realizar la transcripción
def select_file():
    global transcription_ready
    file_path = filedialog.askopenfilename(title="Seleccionar archivo de audio", filetypes=[("Archivos de audio", "*.mp3")])
    if file_path:
        aai.settings.api_key = "29eff150e4254d59a914ffb355d6756c"
        transcriber = aai.Transcriber()
        with warnings.catch_warnings():  # Suprimir las advertencias
            warnings.simplefilter("ignore")
            transcript = transcriber.transcribe(file_path)
        # Agregar la transcripción al cuadro de texto
        transcript_text_box.delete("1.0", tk.END)
        transcript_text_box.insert(tk.END, "Transcripción: " + transcript.text)
        transcription_ready = True
        generate_summary()  # Llama a la función para generar el resumen automáticamente

# Función para generar un resumen de la transcripción
def generate_summary():
    transcript_text = transcript_text_box.get("1.0", "end-1c")  # Obtener la transcripción
    model = Summarizer()
    summary_text = model(transcript_text, min_length=50, max_length=400)  # Genera un resumen con límites de longitud
    summary_text_box.delete("1.0", tk.END)
    summary_text_box.insert(tk.END, "Resumen: " + summary_text)
    copy_summary_button.config(state=tk.NORMAL)  # Habilitar el botón de copia

# Función para copiar el resumen al portapapeles
def copy_summary_to_clipboard():
    summary_text = summary_text_box.get("1.0", "end-1c")  # Obtener el resumen
    pyperclip.copy(summary_text)

# Cuadro de texto para mostrar la transcripción (en la parte izquierda)
frame_left = tk.Frame(root, bg="#151515")
frame_left.pack(side="left", fill="both", expand=True)

transcript_text_box = tk.Text(frame_left, bg="#F781F3", fg="#151515")
transcript_text_box.pack(fill="both", expand=True)

# Contenedor para los botones
button_container = tk.Frame(frame_left, bg="#151515")
button_container.pack(side="bottom")

select_file_button = tk.Button(button_container, text="Seleccionar archivo local", command=select_file, bg="#F781F3", fg="#151515", relief=tk.RAISED, borderwidth=5)
select_file_button.pack(side="left", padx=10, pady=10)  # Utiliza padx y pady para agregar espacio interno

# Cuadro de texto para mostrar el resumen (en la parte derecha)
frame_right = tk.Frame(root, bg="#151515")
frame_right.pack(side="right", fill="both", expand=True)

summary_text_box = tk.Text(frame_right, bg="#F781F3", fg="#151515")
summary_text_box.pack(fill="both", expand=True)

# Botón para copiar el resumen al portapapeles (aparecerá cuando haya una transcripción)
copy_summary_button = tk.Button(frame_right, text="Copiar Resumen al Portapapeles", command=copy_summary_to_clipboard, bg="#F781F3", fg="#151515", relief=tk.RAISED, borderwidth=5, state=tk.DISABLED)
copy_summary_button.pack(side="top", padx=10, pady=10)  # Utiliza padx y pady para agregar espacio interno

# Ejecutar la ventana principal
root.mainloop()
