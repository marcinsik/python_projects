import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("Ostrzeżenie: pyperclip nie jest dostępny")
from password_manager import PasswordManager
from generator import PasswordGenerator
import threading
import os

class SecurePassGUI:
    """Główna klasa interfejsu użytkownika dla SecurePass."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SecurePass - Menedżer Haseł")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Inicjalizacja komponentów
        self.manager = PasswordManager()
        self.generator = PasswordGenerator()
        
        # Style
        self.setup_styles()
        
        # Sprawdzenie czy sejf istnieje
        if self.manager.vault_exists():
            self.show_unlock_screen()
        else:
            self.show_setup_screen()
    
    def setup_styles(self):
        """Ustawienia wyglądu interfejsu."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Kolory
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
    
    def show_setup_screen(self):
        """Ekran pierwszego uruchomienia."""
        self.clear_window()
        
        # Główny frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tytuł
        title_label = ttk.Label(main_frame, text="🔐 Witaj w SecurePass", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Instrukcje
        info_text = """Pierwszy raz używasz SecurePass!

Musisz utworzyć hasło główne, które będzie używane do szyfrowania wszystkich Twoich haseł.

WAŻNE:
• Hasło główne powinno być silne i łatwe do zapamiętania
• Jeśli zapomnisz hasło główne, stracisz dostęp do wszystkich danych
• Nie ma możliwości odzyskania hasła głównego"""
        
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(pady=(0, 30))
        
        # Formularz hasła głównego
        form_frame = ttk.LabelFrame(main_frame, text="Utwórz hasło główne", padding="20")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Hasło główne
        ttk.Label(form_frame, text="Hasło główne:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.master_password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.master_password_var, show="*", width=40)
        password_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Powtórz hasło
        ttk.Label(form_frame, text="Powtórz hasło główne:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.confirm_password_var = tk.StringVar()
        confirm_entry = ttk.Entry(form_frame, textvariable=self.confirm_password_var, show="*", width=40)
        confirm_entry.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Przycisk pokaż/ukryj hasło
        show_password_var = tk.BooleanVar()
        def toggle_password():
            if show_password_var.get():
                password_entry.config(show="")
                confirm_entry.config(show="")
            else:
                password_entry.config(show="*")
                confirm_entry.config(show="*")
        
        show_check = ttk.Checkbutton(form_frame, text="Pokaż hasła", 
                                   variable=show_password_var, command=toggle_password)
        show_check.grid(row=4, column=0, sticky=tk.W, pady=(0, 20))
        
        form_frame.columnconfigure(0, weight=1)
        
        # Przyciski
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        create_button = ttk.Button(button_frame, text="Utwórz sejf", command=self.create_vault)
        create_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Generator hasła
        generate_button = ttk.Button(button_frame, text="Wygeneruj hasło główne", 
                                   command=self.generate_master_password)
        generate_button.pack(side=tk.RIGHT)
        
        # Focus na pierwsze pole
        password_entry.focus()
        
        # Bind Enter
        password_entry.bind('<Return>', lambda e: confirm_entry.focus())
        confirm_entry.bind('<Return>', lambda e: self.create_vault())
    
    def show_unlock_screen(self):
        """Ekran logowania do sejfu."""
        self.clear_window()
        
        # Główny frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tytuł
        title_label = ttk.Label(main_frame, text="🔐 SecurePass", style='Title.TLabel')
        title_label.pack(pady=(50, 30))
        
        # Formularz odblokowywania
        form_frame = ttk.LabelFrame(main_frame, text="Odblokuj sejf", padding="20")
        form_frame.pack(anchor=tk.CENTER)
        
        ttk.Label(form_frame, text="Hasło główne:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.unlock_password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.unlock_password_var, 
                                 show="*", width=30)
        password_entry.grid(row=1, column=0, pady=(0, 20))
        
        unlock_button = ttk.Button(form_frame, text="Odblokuj", command=self.unlock_vault)
        unlock_button.grid(row=2, column=0, pady=(0, 10))
        
        # Status
        self.status_var = tk.StringVar()
        status_label = ttk.Label(form_frame, textvariable=self.status_var, style='Error.TLabel')
        status_label.grid(row=3, column=0)
        
        # Focus i bind Enter
        password_entry.focus()
        password_entry.bind('<Return>', lambda e: self.unlock_vault())
    
    def show_main_screen(self):
        """Główny ekran aplikacji po zalogowaniu."""
        self.clear_window()
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Plik", menu=file_menu)
        file_menu.add_command(label="Nowy wpis", command=self.show_add_entry_dialog, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Eksportuj...", command=self.export_data)
        file_menu.add_command(label="Importuj...", command=self.import_data)
        file_menu.add_separator()
        file_menu.add_command(label="Zablokuj sejf", command=self.lock_vault, accelerator="Ctrl+L")
        file_menu.add_command(label="Wyjście", command=self.root.quit)
        
        # Menu Tools
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Narzędzia", menu=tools_menu)
        tools_menu.add_command(label="Generator haseł", command=self.show_password_generator)
        tools_menu.add_command(label="Statystyki sejfu", command=self.show_vault_stats)
        
        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pomoc", menu=help_menu)
        help_menu.add_command(label="O programie", command=self.show_about)
        
        # Toolbar
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="➕ Nowy wpis", command=self.show_add_entry_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔧 Generator", command=self.show_password_generator).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔒 Zablokuj", command=self.lock_vault).pack(side=tk.RIGHT, padx=5)
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Główny content
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Wyszukiwarka
        search_frame = ttk.Frame(content_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Szukaj:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        clear_button = ttk.Button(search_frame, text="Wyczyść", command=self.clear_search)
        clear_button.pack(side=tk.LEFT)
        
        # Lista haseł
        self.setup_password_list(content_frame)
        
        # Ładowanie danych
        self.refresh_password_list()
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.show_add_entry_dialog())
        self.root.bind('<Control-l>', lambda e: self.lock_vault())
        self.root.bind('<F5>', lambda e: self.refresh_password_list())
    
    def setup_password_list(self, parent):
        """Konfiguruje listę haseł."""
        # Frame dla listy
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ('service', 'username', 'created', 'updated')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Nagłówki
        self.tree.heading('service', text='Serwis')
        self.tree.heading('username', text='Użytkownik')
        self.tree.heading('created', text='Utworzono')
        self.tree.heading('updated', text='Zaktualizowano')
        
        # Szerokości kolumn
        self.tree.column('service', width=200)
        self.tree.column('username', width=150)
        self.tree.column('created', width=120)
        self.tree.column('updated', width=120)
        
        # Scrollbary
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Kopiuj hasło", command=self.copy_password)
        self.context_menu.add_command(label="Kopiuj nazwę użytkownika", command=self.copy_username)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edytuj", command=self.edit_entry)
        self.context_menu.add_command(label="Usuń", command=self.delete_entry)
        
        # Bindings
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Return>', self.copy_password)
    
    def create_vault(self):
        """Tworzy nowy sejf."""
        password = self.master_password_var.get()
        confirm = self.confirm_password_var.get()
        
        if not password:
            messagebox.showerror("Błąd", "Hasło główne nie może być puste!")
            return
        
        if len(password) < 8:
            messagebox.showerror("Błąd", "Hasło główne musi mieć co najmniej 8 znaków!")
            return
        
        if password != confirm:
            messagebox.showerror("Błąd", "Hasła nie są identyczne!")
            return
        
        # Sprawdzenie siły hasła
        strength = self.generator.check_password_strength(password)
        if strength['score'] < 40:
            result = messagebox.askyesno("Słabe hasło", 
                f"Hasło jest {strength['level'].lower()}.\n\n"
                f"Sugestie:\n" + "\n".join(strength['feedback'][:3]) + 
                "\n\nCzy mimo to chcesz kontynuować?")
            if not result:
                return
        
        # Tworzenie sejfu
        if self.manager.create_vault(password):
            messagebox.showinfo("Sukces", "Sejf został utworzony pomyślnie!")
            self.show_main_screen()
        else:
            messagebox.showerror("Błąd", "Nie udało się utworzyć sejfu!")
    
    def generate_master_password(self):
        """Generuje hasło główne."""
        password = self.generator.generate_password(
            length=16,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_special=True,
            exclude_similar=True
        )
        
        # Wyświetl hasło w oknie dialogowym
        dialog = tk.Toplevel(self.root)
        dialog.title("Wygenerowane hasło główne")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrowanie okna
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Wygenerowane hasło główne:", style='Heading.TLabel').pack(pady=(0, 10))
        
        # Entry z hasłem (tylko do odczytu)
        password_var = tk.StringVar(value=password)
        password_entry = ttk.Entry(frame, textvariable=password_var, state='readonly', width=50)
        password_entry.pack(pady=(0, 10))
        
        # Przycisk kopiuj
        def copy_to_clipboard():
            if CLIPBOARD_AVAILABLE:
                try:
                    pyperclip.copy(password)
                    messagebox.showinfo("Skopiowano", "Hasło zostało skopiowane do schowka!")
                except Exception:
                    # Fallback - pokaż hasło w oknie
                    show_password_dialog(password)
            else:
                show_password_dialog(password)
        
        def show_password_dialog(pwd):
            pwd_dialog = tk.Toplevel(dialog)
            pwd_dialog.title("Hasło do skopiowania")
            pwd_dialog.geometry("400x150")
            pwd_dialog.transient(dialog)
            pwd_dialog.grab_set()
            
            frame = ttk.Frame(pwd_dialog, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="Skopiuj hasło ręcznie:").pack(pady=(0, 10))
            
            pwd_var = tk.StringVar(value=pwd)
            pwd_entry = ttk.Entry(frame, textvariable=pwd_var, state='readonly', width=50)
            pwd_entry.pack(pady=(0, 10))
            pwd_entry.select_range(0, tk.END)
            pwd_entry.focus()
            
            ttk.Button(frame, text="Zamknij", command=pwd_dialog.destroy).pack()
        
        ttk.Button(frame, text="Kopiuj do schowka", command=copy_to_clipboard).pack(pady=(0, 10))
        
        # Analiza siły
        strength = self.generator.check_password_strength(password)
        
        ttk.Label(frame, text=f"Siła hasła: {strength['level']} ({strength['score']}/100)", 
                 style='Success.TLabel').pack(pady=(0, 10))
        
        if strength['feedback']:
            feedback_text = "Uwagi:\n" + "\n".join(strength['feedback'])
            ttk.Label(frame, text=feedback_text, justify=tk.LEFT).pack(pady=(0, 10))
        
        # Przyciski
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def use_password():
            self.master_password_var.set(password)
            self.confirm_password_var.set(password)
            dialog.destroy()
        
        ttk.Button(button_frame, text="Użyj tego hasła", command=use_password).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Zamknij", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def unlock_vault(self):
        """Odblokowuje sejf."""
        password = self.unlock_password_var.get()
        
        if not password:
            self.status_var.set("Wprowadź hasło główne!")
            return
        
        if self.manager.unlock_vault(password):
            self.show_main_screen()
        else:
            self.status_var.set("Nieprawidłowe hasło główne!")
            self.unlock_password_var.set("")
    
    def lock_vault(self):
        """Blokuje sejf."""
        result = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz zablokować sejf?")
        if result:
            self.manager.lock_vault()
            self.show_unlock_screen()
    
    def refresh_password_list(self):
        """Odświeża listę haseł."""
        # Wyczyść listę
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Dodaj wpisy
        entries = self.manager.get_entries()
        for i, entry in enumerate(entries):
            # Formatowanie dat
            created = entry.created_at[:10] if entry.created_at else ""
            updated = entry.updated_at[:10] if entry.updated_at else ""
            
            self.tree.insert('', tk.END, values=(
                entry.service,
                entry.username,
                created,
                updated
            ), tags=(str(i),))
    
    def on_search(self, event=None):
        """Obsługuje wyszukiwanie."""
        query = self.search_var.get()
        
        # Wyczyść listę
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not query:
            self.refresh_password_list()
            return
        
        # Wyszukaj i wyświetl pasujące wpisy
        indices = self.manager.search_entries(query)
        entries = self.manager.get_entries()
        
        for i in indices:
            entry = entries[i]
            created = entry.created_at[:10] if entry.created_at else ""
            updated = entry.updated_at[:10] if entry.updated_at else ""
            
            self.tree.insert('', tk.END, values=(
                entry.service,
                entry.username,
                created,
                updated
            ), tags=(str(i),))
    
    def clear_search(self):
        """Czyści wyszukiwanie."""
        self.search_var.set("")
        self.refresh_password_list()
    
    def show_add_entry_dialog(self):
        """Wyświetla dialog dodawania nowego wpisu."""
        self.show_entry_dialog()
    
    def show_entry_dialog(self, entry_index=None):
        """Wyświetla dialog dodawania/edycji wpisu."""
        # Określ czy to edycja czy dodawanie
        is_edit = entry_index is not None
        title = "Edytuj wpis" if is_edit else "Nowy wpis"
        
        # Pobierz dane wpisu jeśli edycja
        entry_data = None
        if is_edit:
            entries = self.manager.get_entries()
            if 0 <= entry_index < len(entries):
                entry_data = entries[entry_index]
        
        # Utwórz dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrowanie okna
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Główny frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Formularz
        # Serwis
        ttk.Label(main_frame, text="Serwis/Strona:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        service_var = tk.StringVar(value=entry_data.service if entry_data else "")
        service_entry = ttk.Entry(main_frame, textvariable=service_var, width=40)
        service_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Nazwa użytkownika
        ttk.Label(main_frame, text="Nazwa użytkownika/E-mail:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        username_var = tk.StringVar(value=entry_data.username if entry_data else "")
        username_entry = ttk.Entry(main_frame, textvariable=username_var, width=40)
        username_entry.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Hasło
        ttk.Label(main_frame, text="Hasło:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        password_var = tk.StringVar(value=entry_data.password if entry_data else "")
        password_entry = ttk.Entry(main_frame, textvariable=password_var, show="*", width=30)
        password_entry.grid(row=5, column=0, sticky=tk.W+tk.E, pady=(0, 5))
        
        # Przycisk generuj hasło
        def generate_password():
            password = self.generator.generate_password()
            password_var.set(password)
        
        generate_btn = ttk.Button(main_frame, text="Generuj", command=generate_password)
        generate_btn.grid(row=5, column=1, padx=(5, 0), pady=(0, 5))
        
        # Pokaż hasło
        show_var = tk.BooleanVar()
        def toggle_password():
            password_entry.config(show="" if show_var.get() else "*")
        
        show_check = ttk.Checkbutton(main_frame, text="Pokaż hasło", variable=show_var, command=toggle_password)
        show_check.grid(row=6, column=0, sticky=tk.W, pady=(0, 10))
        
        # Notatki
        ttk.Label(main_frame, text="Notatki:").grid(row=7, column=0, sticky=tk.W, pady=(0, 5))
        notes_text = tk.Text(main_frame, width=40, height=5)
        notes_text.grid(row=8, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 20))
        
        if entry_data and entry_data.notes:
            notes_text.insert(tk.END, entry_data.notes)
        
        # Konfiguracja grid
        main_frame.columnconfigure(0, weight=1)
        
        # Przyciski
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        def save_entry():
            service = service_var.get().strip()
            username = username_var.get().strip()
            password = password_var.get()
            notes = notes_text.get(1.0, tk.END).strip()
            
            if not service:
                messagebox.showerror("Błąd", "Nazwa serwisu jest wymagana!")
                return
            
            if not username:
                messagebox.showerror("Błąd", "Nazwa użytkownika jest wymagana!")
                return
            
            if not password:
                messagebox.showerror("Błąd", "Hasło jest wymagane!")
                return
            
            # Zapisz wpis
            if is_edit:
                success = self.manager.update_entry(entry_index, service, username, password, notes)
            else:
                success = self.manager.add_entry(service, username, password, notes)
            
            if success:
                self.refresh_password_list()
                dialog.destroy()
                messagebox.showinfo("Sukces", f"Wpis został {'zaktualizowany' if is_edit else 'dodany'} pomyślnie!")
            else:
                if is_edit:
                    messagebox.showerror("Błąd", "Nie udało się zaktualizować wpisu!")
                else:
                    messagebox.showerror("Błąd", "Wpis dla tego serwisu i użytkownika już istnieje!")
        
        ttk.Button(button_frame, text="Zapisz", command=save_entry).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Anuluj", command=dialog.destroy).pack(side=tk.RIGHT)
        
        # Focus na pierwsze pole
        if not is_edit:
            service_entry.focus()
        else:
            password_entry.focus()
    
    def on_double_click(self, event):
        """Obsługuje podwójne kliknięcie na wpis."""
        self.copy_password()
    
    def show_context_menu(self, event):
        """Wyświetla menu kontekstowe."""
        selection = self.tree.selection()
        if selection:
            self.context_menu.post(event.x_root, event.y_root)
    
    def copy_password(self, event=None):
        """Kopiuje hasło do schowka."""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Pobierz indeks wpisu
        item = self.tree.item(selection[0])
        tags = item['tags']
        if not tags:
            return
        
        entry_index = int(tags[0])
        entries = self.manager.get_entries()
        
        if 0 <= entry_index < len(entries):
            password = entries[entry_index].password
            
            if CLIPBOARD_AVAILABLE:
                try:
                    pyperclip.copy(password)
                    self.show_temporary_status("Hasło skopiowane do schowka!", 2000)
                    return
                except Exception:
                    pass
            
            # Fallback - pokaż hasło w oknie dialogowym
            self.show_password_dialog(password)
    
    def show_password_dialog(self, password):
        """Wyświetla hasło w oknie dialogowym jako fallback."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Hasło")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrowanie okna
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Skopiuj hasło ręcznie:").pack(pady=(0, 10))
        
        password_var = tk.StringVar(value=password)
        password_entry = ttk.Entry(frame, textvariable=password_var, state='readonly', width=50)
        password_entry.pack(pady=(0, 10))
        password_entry.select_range(0, tk.END)
        password_entry.focus()
        
        ttk.Button(frame, text="Zamknij", command=dialog.destroy).pack()
    
    def copy_username(self):
        """Kopiuje nazwę użytkownika do schowka."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        tags = item['tags']
        if not tags:
            return
        
        entry_index = int(tags[0])
        entries = self.manager.get_entries()
        
        if 0 <= entry_index < len(entries):
            username = entries[entry_index].username
            
            if CLIPBOARD_AVAILABLE:
                try:
                    pyperclip.copy(username)
                    self.show_temporary_status("Nazwa użytkownika skopiowana do schowka!", 2000)
                    return
                except Exception:
                    pass
            
            # Fallback - pokaż username w oknie dialogowym
            self.show_username_dialog(username)
    
    def show_username_dialog(self, username):
        """Wyświetla nazwę użytkownika w oknie dialogowym jako fallback."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nazwa użytkownika")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrowanie okna
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Skopiuj nazwę użytkownika ręcznie:").pack(pady=(0, 10))
        
        username_var = tk.StringVar(value=username)
        username_entry = ttk.Entry(frame, textvariable=username_var, state='readonly', width=50)
        username_entry.pack(pady=(0, 10))
        username_entry.select_range(0, tk.END)
        username_entry.focus()
        
        ttk.Button(frame, text="Zamknij", command=dialog.destroy).pack()
    
    def edit_entry(self):
        """Edytuje wybrany wpis."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        tags = item['tags']
        if not tags:
            return
        
        entry_index = int(tags[0])
        self.show_entry_dialog(entry_index)
    
    def delete_entry(self):
        """Usuwa wybrany wpis."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        tags = item['tags']
        if not tags:
            return
        
        entry_index = int(tags[0])
        entries = self.manager.get_entries()
        
        if 0 <= entry_index < len(entries):
            entry = entries[entry_index]
            result = messagebox.askyesno("Potwierdzenie", 
                f"Czy na pewno chcesz usunąć wpis dla '{entry.service}'?")
            
            if result:
                if self.manager.delete_entry(entry_index):
                    self.refresh_password_list()
                    messagebox.showinfo("Sukces", "Wpis został usunięty!")
                else:
                    messagebox.showerror("Błąd", "Nie udało się usunąć wpisu!")
    
    def show_password_generator(self):
        """Wyświetla generator haseł."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Generator haseł")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrowanie okna
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Opcje generatora
        options_frame = ttk.LabelFrame(main_frame, text="Opcje generatora", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Długość
        ttk.Label(options_frame, text="Długość hasła:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        length_var = tk.IntVar(value=16)
        length_spin = ttk.Spinbox(options_frame, from_=4, to=128, textvariable=length_var, width=10)
        length_spin.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        # Checkboxy
        uppercase_var = tk.BooleanVar(value=True)
        lowercase_var = tk.BooleanVar(value=True)
        digits_var = tk.BooleanVar(value=True)
        special_var = tk.BooleanVar(value=True)
        exclude_similar_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Wielkie litery (A-Z)", variable=uppercase_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Małe litery (a-z)", variable=lowercase_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Cyfry (0-9)", variable=digits_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Znaki specjalne (!@#$...)", variable=special_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Wyklucz podobne znaki (0,O,l,1)", variable=exclude_similar_var).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Wygenerowane hasło
        result_frame = ttk.LabelFrame(main_frame, text="Wygenerowane hasło", padding="10")
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        password_var = tk.StringVar()
        password_entry = ttk.Entry(result_frame, textvariable=password_var, state='readonly', width=50)
        password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Analiza siły
        strength_var = tk.StringVar()
        strength_label = ttk.Label(result_frame, textvariable=strength_var, style='Success.TLabel')
        strength_label.pack(pady=(0, 10))
        
        feedback_var = tk.StringVar()
        feedback_label = ttk.Label(result_frame, textvariable=feedback_var, justify=tk.LEFT)
        feedback_label.pack()
        
        def generate():
            try:
                password = self.generator.generate_password(
                    length=length_var.get(),
                    use_uppercase=uppercase_var.get(),
                    use_lowercase=lowercase_var.get(),
                    use_digits=digits_var.get(),
                    use_special=special_var.get(),
                    exclude_similar=exclude_similar_var.get()
                )
                password_var.set(password)
                
                # Analiza siły
                strength = self.generator.check_password_strength(password)
                strength_var.set(f"Siła hasła: {strength['level']} ({strength['score']}/100)")
                
                if strength['feedback']:
                    feedback_var.set("Uwagi: " + ", ".join(strength['feedback'][:3]))
                else:
                    feedback_var.set("Hasło spełnia wszystkie kryteria bezpieczeństwa!")
                
            except ValueError as e:
                messagebox.showerror("Błąd", str(e))
        
        def copy_password():
            password = password_var.get()
            if password:
                if CLIPBOARD_AVAILABLE:
                    try:
                        pyperclip.copy(password)
                        messagebox.showinfo("Skopiowano", "Hasło zostało skopiowane do schowka!")
                        return
                    except Exception:
                        pass
                
                # Fallback - pokaż hasło do ręcznego skopiowania
                copy_dialog = tk.Toplevel(dialog)
                copy_dialog.title("Skopiuj hasło")
                copy_dialog.geometry("400x150")
                copy_dialog.transient(dialog)
                copy_dialog.grab_set()
                
                copy_frame = ttk.Frame(copy_dialog, padding="20")
                copy_frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(copy_frame, text="Zaznacz i skopiuj hasło ręcznie:").pack(pady=(0, 10))
                
                pwd_var = tk.StringVar(value=password)
                pwd_entry = ttk.Entry(copy_frame, textvariable=pwd_var, state='readonly', width=50)
                pwd_entry.pack(pady=(0, 10))
                pwd_entry.select_range(0, tk.END)
                pwd_entry.focus()
                
                ttk.Button(copy_frame, text="Zamknij", command=copy_dialog.destroy).pack()
        
        # Przyciski
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Generuj", command=generate).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Kopiuj", command=copy_password).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Zamknij", command=dialog.destroy).pack(side=tk.RIGHT)
        
        # Wygeneruj pierwsze hasło
        generate()
    
    def export_data(self):
        """Eksportuje dane do pliku."""
        filename = filedialog.asksaveasfilename(
            title="Eksportuj dane",
            defaultextension=".enc",
            filetypes=[("Pliki zaszyfrowane", "*.enc"), ("Wszystkie pliki", "*.*")]
        )
        
        if filename:
            if self.manager.export_data(filename):
                messagebox.showinfo("Sukces", f"Dane zostały wyeksportowane do pliku:\n{filename}")
            else:
                messagebox.showerror("Błąd", "Nie udało się wyeksportować danych!")
    
    def import_data(self):
        """Importuje dane z pliku."""
        filename = filedialog.askopenfilename(
            title="Importuj dane",
            filetypes=[("Pliki zaszyfrowane", "*.enc"), ("Wszystkie pliki", "*.*")]
        )
        
        if filename:
            result = messagebox.askyesno("Potwierdzenie", 
                "Import danych doda nowe wpisy do istniejącego sejfu.\n"
                "Wpisy z takimi samymi danymi (serwis + użytkownik) zostaną pominięte.\n\n"
                "Czy chcesz kontynuować?")
            
            if result:
                if self.manager.import_data(filename):
                    self.refresh_password_list()
                    messagebox.showinfo("Sukces", "Dane zostały zaimportowane pomyślnie!")
                else:
                    messagebox.showerror("Błąd", 
                        "Nie udało się zaimportować danych!\n"
                        "Sprawdź czy plik jest prawidłowy i czy używasz poprawnego hasła głównego.")
    
    def show_vault_stats(self):
        """Wyświetla statystyki sejfu."""
        stats = self.manager.get_vault_stats()
        
        if not stats:
            messagebox.showinfo("Statystyki", "Brak danych do wyświetlenia.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Statystyki sejfu")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrowanie okna
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📊 Statystyki sejfu", style='Title.TLabel').pack(pady=(0, 20))
        
        # Statystyki
        stats_text = f"""
Łączna liczba wpisów: {stats.get('total_entries', 0)}

Słabe hasła (< 8 znaków): {stats.get('weak_passwords', 0)}

Duplikaty haseł: {stats.get('duplicate_passwords', 0)}
"""
        
        if stats.get('total_entries', 0) > 0:
            oldest = stats.get('oldest_entry', '')[:10] if stats.get('oldest_entry') else 'Brak'
            newest = stats.get('newest_entry', '')[:10] if stats.get('newest_entry') else 'Brak'
            
            stats_text += f"""
Najstarszy wpis: {oldest}

Najnowszy wpis: {newest}
"""
        
        ttk.Label(main_frame, text=stats_text, justify=tk.LEFT).pack(pady=(0, 20))
        
        # Rekomendacje
        recommendations = []
        if stats.get('weak_passwords', 0) > 0:
            recommendations.append("• Zmień słabe hasła na silniejsze")
        if stats.get('duplicate_passwords', 0) > 0:
            recommendations.append("• Użyj unikalnych haseł dla każdego serwisu")
        
        if recommendations:
            ttk.Label(main_frame, text="🔒 Rekomendacje bezpieczeństwa:", style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
            rec_text = "\n".join(recommendations)
            ttk.Label(main_frame, text=rec_text, justify=tk.LEFT, style='Warning.TLabel').pack(anchor=tk.W, pady=(0, 20))
        else:
            ttk.Label(main_frame, text="✅ Wszystkie hasła spełniają podstawowe kryteria bezpieczeństwa!", 
                     style='Success.TLabel').pack(pady=(10, 20))
        
        ttk.Button(main_frame, text="Zamknij", command=dialog.destroy).pack()
    
    def show_about(self):
        """Wyświetla informacje o programie."""
        about_text = """🔐 SecurePass v1.0

Bezpieczny menedżer haseł z szyfrowaniem AES-256

Funkcje:
• Szyfrowanie AES-256 z PBKDF2
• Generator silnych haseł
• Intuicyjny interfejs graficzny
• Eksport/import danych
• Wyszukiwanie wpisów

© 2025 Wszystkie prawa zastrzeżone"""
        
        messagebox.showinfo("O programie", about_text)
    
    def show_temporary_status(self, message, duration=3000):
        """Wyświetla tymczasowy status na pasku."""
        # Prosta implementacja - można rozbudować
        self.root.after(100, lambda: print(f"Status: {message}"))
    
    def clear_window(self):
        """Czyści okno z wszystkich widgetów."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Usuń menu
        self.root.config(menu="")
    
    def run(self):
        """Uruchamia aplikację."""
        self.root.mainloop()

def main():
    """Główna funkcja aplikacji."""
    global CLIPBOARD_AVAILABLE
    
    # Sprawdź czy pyperclip jest dostępny
    if CLIPBOARD_AVAILABLE:
        try:
            import pyperclip
            pyperclip.copy("")  # Test
            print("Kopiowanie do schowka: DOSTĘPNE")
        except Exception as e:
            CLIPBOARD_AVAILABLE = False
            print(f"Ostrzeżenie: Funkcja kopiowania nie jest dostępna: {e}")
            print("Hasła będą wyświetlane w oknach dialogowych do ręcznego skopiowania.")
    else:
        print("Ostrzeżenie: pyperclip nie jest zainstalowany. Hasła będą wyświetlane w oknach dialogowych.")
    
    app = SecurePassGUI()
    app.run()

if __name__ == "__main__":
    main()
