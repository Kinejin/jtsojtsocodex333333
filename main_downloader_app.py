import tkinter as tk
from tkinter import ttk, messagebox

from favorites_manager import FavoritesManager
from stream_handler import StreamDownloader
from stream_checker import StreamChecker


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Live Stream Downloader')
        self.fav_manager = FavoritesManager()
        self.downloads = []

        self.create_widgets()
        self.stream_checker = StreamChecker(self.fav_manager, self.handle_auto_capture, self.log)
        self.stream_checker.start()

    def create_widgets(self):
        frm_entry = ttk.Frame(self.root)
        frm_entry.pack(fill='x', padx=5, pady=5)

        ttk.Label(frm_entry, text='URL:').pack(side='left')
        self.entry_url = ttk.Entry(frm_entry, width=50)
        self.entry_url.pack(side='left', padx=5)

        self.combo_quality = ttk.Combobox(frm_entry, values=['best'], width=15)
        self.combo_quality.set('best')
        self.combo_quality.pack(side='left', padx=5)

        ttk.Button(frm_entry, text='Obtener Calidades', command=self.get_qualities).pack(side='left', padx=5)
        ttk.Button(frm_entry, text='Iniciar Descarga', command=self.start_download).pack(side='left', padx=5)
        ttk.Button(frm_entry, text='Añadir a Favoritos', command=self.add_favorite).pack(side='left', padx=5)

        frm_fav = ttk.Labelframe(self.root, text='Favoritos')
        frm_fav.pack(fill='both', expand=True, padx=5, pady=5)

        self.list_fav = tk.Listbox(frm_fav, height=6)
        self.list_fav.pack(side='left', fill='both', expand=True)
        self.list_fav.bind('<<ListboxSelect>>', self.on_select_favorite)

        fav_buttons = ttk.Frame(frm_fav)
        fav_buttons.pack(side='left', fill='y')
        ttk.Button(fav_buttons, text='Iniciar Fav.', command=self.start_selected_favorite).pack(fill='x', pady=2)
        ttk.Button(fav_buttons, text='Quitar Fav.', command=self.remove_selected_favorite).pack(fill='x', pady=2)

        self.text_log = tk.Text(self.root, height=10)
        self.text_log.pack(fill='both', expand=True, padx=5, pady=5)

        self.refresh_favorites()

    def log(self, msg):
        self.text_log.insert('end', msg + '\n')
        self.text_log.see('end')

    def get_qualities(self):
        url = self.entry_url.get().strip()
        if not url:
            return
        output = StreamDownloader.get_available_qualities(url)
        self.log(output)

    def start_download(self):
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showerror('Error', 'Ingrese una URL')
            return
        quality = self.combo_quality.get()
        downloader = StreamDownloader(url, quality, log_callback=self.log)
        self.downloads.append(downloader)
        downloader.start()
        self.log(f'Descarga iniciada: {url}')

    def add_favorite(self):
        url = self.entry_url.get().strip()
        if not url:
            return
        name = url
        fav = self.fav_manager.add_favorite(name, url, self.combo_quality.get())
        self.refresh_favorites()
        self.log(f'Favorito agregado: {fav["name"]}')

    def refresh_favorites(self):
        self.list_fav.delete(0, 'end')
        for fav in self.fav_manager.favorites:
            self.list_fav.insert('end', fav['name'])

    def on_select_favorite(self, event):
        if not self.list_fav.curselection():
            return
        index = self.list_fav.curselection()[0]
        fav = self.fav_manager.favorites[index]
        self.entry_url.delete(0, 'end')
        self.entry_url.insert(0, fav['url'])
        self.combo_quality.set(fav.get('quality', 'best'))

    def start_selected_favorite(self):
        if not self.list_fav.curselection():
            return
        index = self.list_fav.curselection()[0]
        fav = self.fav_manager.favorites[index]
        downloader = StreamDownloader(fav['url'], fav.get('quality', 'best'), log_callback=self.log)
        self.downloads.append(downloader)
        downloader.start()
        self.log(f'Descarga iniciada: {fav["name"]}')

    def remove_selected_favorite(self):
        if not self.list_fav.curselection():
            return
        index = self.list_fav.curselection()[0]
        fav = self.fav_manager.favorites[index]
        self.fav_manager.remove_favorite(fav['id'])
        self.refresh_favorites()
        self.log(f'Favorito eliminado: {fav["name"]}')

    def handle_auto_capture(self, fav):
        downloader = StreamDownloader(fav['url'], fav.get('quality', 'best'), log_callback=self.log)
        self.downloads.append(downloader)
        downloader.start()
        self.log(f'Auto captura iniciada: {fav["name"]}')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.mainloop()
