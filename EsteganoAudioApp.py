import os
import tkinter as tk
from functools import partial
from tkinter import filedialog, messagebox
from PIL import Image
from pydub import AudioSegment

ffmpeg_path = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"
ffprobe_path = r"C:\Program Files\ffmpeg\bin\ffprobe.exe"


AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

def hide_image_in_audio(audio_path, image_path, output_path):
    try:
        if not os.path.exists(audio_path) or not os.path.exists(image_path):
            raise FileNotFoundError("Arquivo não encontrado.")

        audio = AudioSegment.from_mp3(audio_path)
        image = Image.open(image_path)

        audio_samples = list(audio.get_array_of_samples())

        image_data = image.tobytes()

        if len(image_data) * 8 > len(audio_samples):
            raise ValueError("Imagem é muito grande para o arquivo de áudio.")

        for i, byte in enumerate(image_data):
            for j in range(8):
                bit = (byte >> j) & 1
                audio_samples[i * 8 + j] &= 0xFFFE
                audio_samples[i * 8 + j] |= bit

        modified_audio = AudioSegment(
            samples=audio_samples,
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )

        modified_audio.export(output_path, format="mp3")

        messagebox.showinfo("Sucesso", "Esteganografia concluída com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def browse_file(entry, filetypes):
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

def browse_directory(entry):
    dirpath = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dirpath)

def start_steganography(audio_entry, image_entry, output_entry):
    audio_path = audio_entry.get()
    image_path = image_entry.get()
    output_path = output_entry.get()

    try:
        if not os.path.exists(audio_path) or not os.path.exists(image_path):
            raise FileNotFoundError("Arquivo não encontrado.")

        hide_image_in_audio(audio_path, image_path, output_path)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado.")

app = tk.Tk()
app.title("Esteganografia em Arquivos de Áudio")
audio_label = tk.Label(app, text="Selecione o arquivo de áudio:")
audio_label.pack()

audio_entry = tk.Entry(app)
audio_entry.pack()

audio_button = tk.Button(app, text="Procurar", command=partial(browse_file, audio_entry, [("Arquivos MP3", "*.mp3")]))
audio_button.pack()

image_label = tk.Label(app, text="Selecione a imagem secreta:")
image_label.pack()

image_entry = tk.Entry(app)
image_entry.pack()

image_button = tk.Button(app, text="Procurar", command=partial(browse_file, image_entry, [("Arquivos de Imagem", "*.png *.jpg *.jpeg")]))
image_button.pack()

output_label = tk.Label(app, text="Caminho de saída para o arquivo esteganografado:")
output_label.pack()

output_entry = tk.Entry(app)
output_entry.pack()

output_button = tk.Button(app, text="Procurar", command=partial(browse_directory, output_entry))
output_button.pack()

start_button = tk.Button(app, text="Iniciar Esteganografia", command=partial(start_steganography, audio_entry, image_entry, output_entry))
start_button.pack()

app.mainloop()
