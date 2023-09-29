import tkinter as tk
from tkinter import filedialog
import pyperclip
def select_file():
    # abrir archivos para procesar (transcribir)
    file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("MP3 files", "*.mp3")])
    # si el archivo ya esta seleccionado se transcribe
    if file_path:
        import assemblyai as aai
        # se debe cambiar por el api key del usuario
        aai.settings.api_key = f"3f02520cd10544df9292b2c534da483e"
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        # Crea una ventana 
        transcript_window = tk.Toplevel(root)
        transcript_window.title("biblioIA")
        transcript_window.geometry("800x600")
        # organiza las ventanas
        chat_window = tk.Text(transcript_window)
        chat_window.insert(tk.END, "User: " + transcript.text)
        chat_window.pack()
        # crea boton para cerrar
        close_button = tk.Button(transcript_window, text="Close", command=transcript_window.destroy)
        close_button.pack()
        # crea boton para copiar
        copy_button = tk.Button(transcript_window, text="Copy to clipboard", command=lambda: pyperclip.copy(transcript.text))
        copy_button.pack()
        
# Crea ventana principal
root = tk.Tk()
root.title("Audio Transcription")
root.geometry("400x200")
# Crea boton para seleccionar archivo de audio
select_file_button = tk.Button(root, text="Select an audio file", command=select_file)
select_file_button.pack()
# señala si no se selecciono un archivo
selected_file_label = tk.Label(root, text="No file selected")
selected_file_label.pack()
# crea el label para la transcripcion
transcript_label = tk.Label(root, text="Transcript:")
transcript_label.pack()
# crea una box display
transcript_text_box = tk.Text(root)
transcript_text_box.pack()
# corre el loop principal
root.mainloop()