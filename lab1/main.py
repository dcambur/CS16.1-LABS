import tkinter as tk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText

from base import Base, engine, Session
from model import AuditInfo, AuditNames
from parser import AuditParser

# data base to store values
Base.metadata.create_all(engine)
session = Session()


def get_current_filenames():
    return session.query(AuditNames).order_by("id").all()


def get_current_filename_ids(current_filename):
    file_array = [obj.id for obj in current_filename]
    return file_array


def get_first_filename(filenames_list):
    if not filenames_list:
        return None

    filename_id = filenames_list[0].id
    return session.query(AuditNames).filter_by(id=filename_id).first()


def audit_info_by_filename(filename):
    if not filename:
        return ""

    info = session.query(AuditInfo).filter_by(audit_name_id=filename.id)
    return info


def get_filename_by_id(filename_id):
    if not filename_id:
        return ""

    info = session.query(AuditNames).filter_by(id=filename_id).first()
    return info


class AuditGUI:
    def __init__(self, master):
        self.filetypes = (
            ('audit files', '*.audit'),
        )

        self.all_filenames = get_current_filenames()
        self.current_filename = get_first_filename(self.all_filenames)

        self.current_audit_info = audit_info_by_filename(self.current_filename)

        self.master = master
        self.master.title = "Laboratory Work N1"
        self.master.geometry("1080x720")

        self.menu = tk.Menu(self.master)
        self.file = tk.Menu(self.menu)

        self.text_field = ScrolledText(self.master, wrap=tk.WORD)

        self.master.config(menu=self.menu)

        self.file.add_command(label="Open File", command=self.open_file)
        self.file.add_command(label="Save File", command=self.save_file)
        self.file.add_command(label="Exit", command=exit)

        self.menu.add_cascade(label="File", menu=self.file)

        self.text_field.insert(tk.END, self.audit_info_repr())
        self.text_field.config(state=tk.DISABLED)

        self.text_field.pack()

        self.user_choice = tk.StringVar(self.master)

        if self.list_all_filenames():
            self.user_choice.set(self.list_all_filenames()[0])
        else:
            self.user_choice = ""

        self.naming_list = tk.OptionMenu(self.master, self.user_choice, *self.list_all_filenames(), command=self.change_choice)
        self.naming_list.config(width=90, font=('Helvetica', 12))

        self.naming_list.pack()

    def list_all_filenames(self):
        options = []
        if not self.all_filenames:
            return ['']
        for obj in self.all_filenames:
            options.append([obj.filename, obj.id])

        return options

    def audit_info_repr(self):
        text = ""
        if not self.current_audit_info:
            return ""

        for info in self.current_audit_info:
            text += f"\t{info.title} :\t {info.body}\n\n"

        return text

    def reload_db_data(self):
        self.all_filenames = get_current_filenames()
        self.current_filename = self.all_filenames[0]
        self.user_choice.set(self.list_all_filenames()[0])
        self.naming_list['menu'].delete(0, 'end')
        for name in self.list_all_filenames():
            self.naming_list['menu'].add_command(label=name, command=tk._setit(self.user_choice, name))

    def update_text(self, filename):
        self.current_audit_info = audit_info_by_filename(filename)
        self.text_field.config(state=tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        self.text_field.insert(tk.END, self.audit_info_repr())
        self.text_field.config(state=tk.DISABLED)

    def change_choice(self, selection):
        if selection:
            self.update_text(get_filename_by_id(selection[1]))

    def open_file(self):
        filename = fd.askopenfilename(filetypes=self.filetypes)

        if not filename:
            return
        array = AuditParser(filename).array()

        names = AuditNames(filename=filename[filename.rfind("/") + 1:])
        session.add(names)
        session.commit()

        to_insert = []
        for ele in array:
            for key, value in ele.items():
                info = AuditInfo(key, value, audit_name_id=names.id)
                to_insert.append(info)

        session.bulk_save_objects(to_insert)
        session.commit()

        self.update_text(filename=names)
        self.reload_db_data()

    def save_file(self):
        file_save = fd.asksaveasfilename(filetypes=self.filetypes)
        if file_save:
            with open(file_save, "w") as write_file:
                write_file.write(self.audit_info_repr())

    def start(self):
        self.master.mainloop()


root = tk.Tk()
my_gui = AuditGUI(root)
my_gui.start()
