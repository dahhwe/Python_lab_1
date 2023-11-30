import os
import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk

from file_operations import write_data_to_file, read_file_in_binary_mode
from rsa import RSA


class RSAApp(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()
        self.title('RSA Шифрование')
        self.geometry('1200x800')
        self.rsa_length = RSA(47)
        self.create_widgets()

    def create_widgets(self) -> None:
        self.lbl_original_text = ctk.CTkLabel(self, text="Оригинальный текст:")
        self.lbl_original_text.pack(pady=10)

        self.txt_original_text = ctk.CTkTextbox(self, height=100, width=400)
        self.txt_original_text.pack(pady=10)

        # Переменная для хранения пути к выбранному файлу
        self.selected_file_path = tk.StringVar()

        # Текстовое поле для отображения пути выбранного файла
        self.ent_file_path = ctk.CTkEntry(self, textvariable=self.selected_file_path, width=400, state='disabled')
        self.ent_file_path.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для выбора файла
        self.btn_choose_file = ctk.CTkButton(self, text="Выбрать файл", command=self.choose_file)
        self.btn_choose_file.pack(side=tk.LEFT, padx=10, pady=10)

        self.radio_var = tk.IntVar(value=1)

        self.radio_encode = ctk.CTkRadioButton(self, text="Зашифровать", variable=self.radio_var, value=1)
        self.radio_encode.pack(anchor=tk.W, padx=20, pady=10)

        self.radio_decode = ctk.CTkRadioButton(self, text="Расшифровать", variable=self.radio_var, value=2)
        self.radio_decode.pack(anchor=tk.W, padx=20, pady=10)

        self.btn_generate_keys = ctk.CTkButton(self, text="Сгенерировать ключи", command=self.generate_keys)
        self.btn_generate_keys.pack(pady=10)

        # Метки для ключей
        self.lbl_public_key_n = ctk.CTkLabel(self, text="Открытый ключ N:")
        self.lbl_public_key_n.pack(pady=10)
        self.ent_public_key_n = ctk.CTkEntry(self, width=400)
        self.ent_public_key_n.pack(pady=10)

        self.lbl_public_key_s = ctk.CTkLabel(self, text="Открытая экспонента S:")
        self.lbl_public_key_s.pack(pady=10)
        self.ent_public_key_s = ctk.CTkEntry(self, width=400)
        self.ent_public_key_s.pack(pady=10)

        self.lbl_private_key = ctk.CTkLabel(self, text="Закрытый ключ E:")
        self.lbl_private_key.pack(pady=10)
        self.ent_private_key = ctk.CTkEntry(self, width=400)
        self.ent_private_key.pack(pady=10)

        self.btn_perform = ctk.CTkButton(self, text="Выполнить", command=self.perform)
        self.btn_perform.pack(pady=10)

        self.txt_converted_text = ctk.CTkTextbox(self, height=100, width=400)
        self.txt_converted_text.pack(pady=10)
        self.txt_converted_text.bind("<Button-3>", self.show_context_menu)

    def choose_file(self) -> None:
        # Диалог выбора файла
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file_path.set(file_path)  # сохраняем путь к файлу в переменную

    def encrypt_file(self) -> None:
        file_path = self.selected_file_path.get()
        file_data = read_file_in_binary_mode(file_path)
        public_key = (int(self.ent_public_key_n.get()), int(self.ent_public_key_s.get()))

        encrypted_data = RSA.encrypt(file_data, public_key, 'file')
        encrypted_file_path = f"{file_path}.encrypted"
        write_data_to_file(encrypted_file_path, encrypted_data, 'wb')

        messagebox.showinfo("Успех", f"Файл зашифрован и сохранен как {encrypted_file_path}")

    def decrypt_file(self) -> None:
        file_path = self.selected_file_path.get()
        if not file_path.endswith('.encrypted'):
            messagebox.showerror("Ошибка", "Выбранный файл не является зашифрованным файлом")
            return

        encrypted_data = read_file_in_binary_mode(file_path)
        private_key = (int(self.ent_private_key.get()), int(self.ent_public_key_n.get()))

        decrypted_data = RSA.decrypt(encrypted_data, private_key, 'file')

        base = os.path.splitext(file_path)[0]

        original_extension = os.path.splitext(os.path.basename(file_path))[1]
        decrypted_file_path = f"{base}_decrypted{original_extension}"
        write_data_to_file(decrypted_file_path, decrypted_data, 'wb')

        messagebox.showinfo("Успех", f"Файл расшифрован и сохранен как {decrypted_file_path}")

    def show_context_menu(self, event) -> None:
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Копировать", command=lambda: self.copy_text(event))
        context_menu.add_command(label="Вставить", command=lambda: self.paste_text(event))
        context_menu.post(event.x_root, event.y_root)

    def copy_text(self, event) -> None:
        try:
            self.clipboard_clear()
            selected_text = self.txt_converted_text.selection_get()
            self.clipboard_append(selected_text)
        except tk.TclError:
            pass  # Ничего не делаем, если нет выделенного текста

    def paste_text(self, event) -> None:
        try:
            cursor_position = self.txt_converted_text.index(tk.INSERT)
            self.txt_converted_text.insert(cursor_position, self.clipboard_get())
        except tk.TclError:
            pass  # Ничего не делаем, если в буфере обмена нет текста

    def generate_keys(self) -> None:
        public_key, private_key = self.rsa_length.key_gen()
        self.ent_public_key_n.delete(0, tk.END)
        self.ent_public_key_n.insert(0, str(public_key[1]))
        self.ent_public_key_s.delete(0, tk.END)
        self.ent_public_key_s.insert(0, str(public_key[0]))
        self.ent_private_key.delete(0, tk.END)
        self.ent_private_key.insert(0, str(private_key[0]))

    def perform(self) -> None:
        public_key_n = self.ent_public_key_n.get()
        public_key_s = self.ent_public_key_s.get()
        private_key = self.ent_private_key.get()

        # Проверяем, введены ли ключи
        if not (public_key_n and public_key_s and private_key):
            messagebox.showerror("Ошибка", "Все ключи должны быть введены.")
            return

        # Если путь к файлу установлен, шифруем/дешифруем файл
        if self.selected_file_path.get():
            file_path = self.selected_file_path.get()
            if self.radio_var.get() == 1:
                # Шифрование файла
                file_data = read_file_in_binary_mode(file_path)
                encrypted_data = self.rsa_length.encrypt(file_data, (int(public_key_s), int(public_key_n)), 'file')
                encrypted_file_path = file_path + ".encrypted"
                write_data_to_file(encrypted_file_path, encrypted_data, mode='wb')
                messagebox.showinfo("Успех", f"Файл '{file_path}' успешно зашифрован.")
            elif self.radio_var.get() == 2:
                # Дешифрование файла
                encrypted_data = read_file_in_binary_mode(file_path)
                decrypted_data = self.rsa_length.decrypt(encrypted_data, (int(private_key), int(public_key_n)), 'file')
                decrypted_file_path = file_path.replace(".encrypted", ".decrypted")
                write_data_to_file(decrypted_file_path, decrypted_data, mode='wb')
                messagebox.showinfo("Успех", f"Файл '{file_path}' успешно расшифрован.")
        else:
            # Если путь к файлу не установлен, шифруем/дешифруем текст из текстового поля
            text_data = self.txt_original_text.get("1.0", tk.END).strip()
            if self.radio_var.get() == 1:
                # Шифрование текста
                encrypted_data = self.rsa_length.encrypt(text_data, (int(public_key_s), int(public_key_n)), 'str')
                encrypted_text = ' '.join(map(str, encrypted_data))
                self.txt_converted_text.delete("1.0", tk.END)
                self.txt_converted_text.insert("1.0", encrypted_text)
                messagebox.showinfo("Успех", "Текст успешно зашифрован.")
            elif self.radio_var.get() == 2:
                # Дешифрование текста
                encrypted_data = list(map(int, text_data.split()))
                decrypted_text = self.rsa_length.decrypt(encrypted_data, (int(private_key), int(public_key_n)), 'str')
                self.txt_converted_text.delete("1.0", tk.END)
                self.txt_converted_text.insert("1.0", decrypted_text)
                messagebox.showinfo("Успех", "Текст успешно расшифрован.")


if __name__ == "__main__":
    app = RSAApp()
    app.mainloop()
