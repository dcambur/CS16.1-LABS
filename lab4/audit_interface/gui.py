import glob
import json
import subprocess
import tarfile
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font

import requests

from lab3 import audit_parser

main = Tk()
my_font = Font(family="Helvetica", size=12)
s = ttk.Style()
s.configure('TFrame', background='grey')
main.title("Lab3_CS")
main.geometry("1900x1000")
frame = ttk.Frame(main, width=1900, height=1000, style='TFrame',
                  padding=(4, 4, 450, 450))
frame.grid(column=0, row=0)

previous = []
index = 0
arr = []
matching = []
system_dict = {}
query = StringVar()
vars1 = StringVar()
vars2 = StringVar()
to_file = []
structure = []
success = []
fail = []
unknown = []
to_change = []
arr2 = []
arr2copy = []
failed_selected = []


def make_query(struct):
    query = 'reg query ' + struct['reg_key'] + ' /v ' + struct['reg_item']
    out = subprocess.Popen(query,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    output = out.communicate()[0].decode('ascii', 'ignore')
    str = ''
    for char in output:
        if char.isprintable() and char != '\n' and char != '\r':
            str += char
    output = str
    output = output.split(' ')
    output = [x for x in output if len(x) > 0]
    value = ''
    if 'ERROR' in output[0]:
        unknown.append(struct['reg_key'] + struct['reg_item'])
    for i in range(len(output)):
        if 'REG_' in output[i]:
            for element in output[i + 1:]:
                value = value + element + ' '
            value = value[:len(value) - 1]
            if struct['value_data'][:2] == '0x':
                struct['value_data'] = struct['value_data'][2:]
            struct['value_data'] = hex(int(struct['value_data']))
            p = re.compile('.*' + struct['value_data'] + '.*')
            if p.match(value):
                print('Patern:', struct['value_data'])
                print('Value:', value)
                success.append(struct['reg_key'] + struct[
                    'reg_item'] + '\n' + 'Value:' + value)
            else:
                print('Did not pass: ', struct['value_data'])
                print('Value which did not pass: ', value)
                fail.append([struct, value])


def check():
    for struct in structure:
        if 'reg_key' in struct and 'reg_item' in struct and 'value_data' in struct:
            make_query(struct)

    for i in range(len(fail)):
        item = fail[i]
        arr2.append(' Item:' + item[0]['reg_item'] + ' Value:' + item[
            1] + ' Desired:' + item[0]['value_data'])
        global arr2copy
        arr2copy = arr2
    vars2.set(arr2)

    frame2 = Frame(main, bd=10, bg='#ffffff', highlightthickness=20)
    frame2.config(highlightbackground="Gray")
    frame2.place(relx=0.5, rely=0.1, width=800, relwidth=0.4, relheight=0.8,
                 anchor='n')

    text2 = Text(frame2, bg="#bddfff", width=50, height=27.5,
                 highlightthickness=3)
    text2.place(relx=0.07, rely=0.03, relwidth=0.4, relheight=0.9)
    text2.insert(END, '\n\n'.join(success))

    listbox_fail = Listbox(frame2, bg="#bddfff", font=my_font, fg="white",
                           listvariable=vars2, selectmode=MULTIPLE,
                           width=50, height=27, highlightthickness=3)
    listbox_fail.place(relx=0.5, rely=0.03, relwidth=0.4, relheight=0.9)
    listbox_fail.config(highlightbackground="white")
    listbox_fail.bind('<<ListboxSelect>>', on_select_failed)

    def exit():
        frame2.destroy()

    exit_btn = Button(frame2, text='Back', command=exit, bg="#2d35a6",
                      fg="white", font=my_font, padx='10px',
                      pady='3px')
    exit_btn.place(relx=0.93, rely=0.95)

    def change_failures():
        global arr2copy
        global arr2
        backup()
        for i in range(len(failed_selected)):
            struct = failed_selected[i][0]
            query = 'reg add "' + struct['reg_key'] + '" /v ' + struct[
                'reg_item'] + ' /d "' + struct[
                        'value_data'] + '" /f'
            print(query)
            out = subprocess.Popen(query,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
            output = out.communicate()[0].decode('ascii', 'ignore')
            str = ''
            for char in output:
                if char.isprintable() and char != '\n' and char != '\r':
                    str += char
            output = str
            print(output)
            vars2.set(arr2)
            arr2copy = arr2

    def restore():
        f = open('backup.txt')
        fail = json.loads(f.read())
        print(fail)
        f.close()

        for i in range(len(fail)):
            struct = fail[i][0]
            query = 'reg add ' + struct['reg_key'] + ' /v ' + struct[
                'reg_item'] + ' /d ' + fail[i][1] + ' /f'
            print('Query:', query)
            out = subprocess.Popen(query,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
            output = out.communicate()[0].decode('ascii', 'ignore')
            str = ''
            for char in output:
                if char.isprintable() and char != '\n' and char != '\r':
                    str += char
            output = str
            print(output)

    def backup():
        f = open('backup.txt', 'w')
        backup_string = json.dumps(fail)
        f.write(backup_string)
        f.close()

    change_btn = Button(frame2, text='Change', command=change_failures,
                       bg="#2d35a6", fg="white", font=my_font,
                       padx='10px',
                       pady='3px')
    change_btn.place(relx=0.30, rely=0.95)

    backup_btn = Button(frame2, text='Restore', command=restore, bg="#2d35a6",
                       fg="white", font=my_font,
                       padx='10px',
                       pady='3px')
    backup_btn.place(relx=0.70, rely=0.95)


def on_select_failed(evt):
    w = evt.widget
    actual = w.curselection()

    global failed_selected
    global arr2
    failed_selected = []
    for i in actual:
        failed_selected.append(fail[i])
    local_arr2 = []
    for i in actual:
        local_arr2.append(arr2copy[i])
    arr2 = local_arr2
    arr2 = [x for x in arr2copy if x not in arr2]
    print(failed_selected)


def enter_search(evt):
    search()


def search():
    global structure
    q = query.get()
    arr = [struct['description'] for struct in structure if
           q.lower() in struct['description'].lower()]
    global matching
    matching = [struct for struct in structure if q in struct['description']]
    vars1.set(arr)


def on_select_configuration(evt):
    global previous
    global index
    w = evt.widget
    actual = w.curselection()

    difference = [item for item in actual if item not in previous]
    if len(difference) > 0:
        index = [item for item in actual if item not in previous][0]
    previous = w.curselection()

    text.delete(1.0, END)
    str = '\n'
    for key in matching[index]:
        str += key + ':' + matching[index][key] + '\n'
    text.insert(END, str)


def import_audit():
    global arr
    file_name = fd.askopenfilename(initialdir="../portal_audits")
    if file_name:
        arr = []
    global structure
    structure = audit_parser.main(file_name)
    for element in structure:
        for key in element:
            string_collector = ''
            for char in element[key]:
                if char != '"' and char != "'":
                    string_collector += char
            is_space_first = True
            string_collector2 = ''
            for char in string_collector:
                if char == ' ' and is_space_first:
                    continue
                else:
                    string_collector2 += char
                    is_space_first = False
            element[key] = string_collector2

    global matching
    matching = structure
    if len(structure) == 0:
        f = open(file_name, 'r')
        structure = json.loads(f.read())
        f.close()
    for struct in structure:
        if 'description' in struct:
            arr.append(struct['description'])
        else:
            arr.append('Error in selecting')
    vars1.set(arr)


list_box = Listbox(frame, bg="#ffffff", font=my_font, fg="black",
                   listvariable=vars1, selectmode=MULTIPLE, width=130,
                   height=25, highlightthickness=3)
list_box.config(highlightbackground="white")
list_box.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
list_box.bind('<<ListboxSelect>>', on_select_configuration)


def save_config():
    file_name = fd.asksaveasfilename(filetypes=(("Audit FILES", ".audit"),
                                                ("All files", ".")))
    file_name += '.audit'
    file = open(file_name, 'w')
    selection = list_box.curselection()
    for i in selection:
        to_file.append(matching[i])
    json.dump(to_file, file)
    file.close()


def select_all():
    list_box.select_set(0, END)
    for struct in structure:
        list_box.insert(END, struct)


def deselect_all():
    for struct in structure:
        list_box.selection_clear(0, END)


def download_url(url, save_path, chunk_size=1024):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def extract_download():
    url = "https://www.tenable.com/downloads/api/v1/public/pages/download-all-compliance-audit-files/downloads/7472/download?i_agree_to_tenable_license_agreement=true"
    path = "audits.tar.gz"
    download_url(url, path)
    tf = tarfile.open("audits.tar.gz")
    tf.extractall()
    print(glob.glob("portal_audits/*"))


text = Text(frame, bg="#8eeeff", fg="black", font=my_font, width=60, height=40,
            highlightthickness=3)
text.config(highlightbackground="white")
text.grid(row=0, column=3, columnspan=3, padx=30)
import_button = Button(frame, bg="#2d35a6", fg="white", font=my_font,
                       text="Import", width=7, height=1,
                       command=import_audit).place(relx=0.01, rely=0.849)
download_button = Button(frame, bg="#2d35a6", fg="white", font=my_font,
                         text="Download audits", width=15, height=1,
                         command=extract_download).place(relx=0.070,
                                                         rely=0.849)

save_button = Button(frame, bg="#2d35a6", fg="white", font=my_font,
                     text="Save",
                     width=7, height=1,
                     command=save_config).place(relx=0.01, rely=0.099)
select_all_button = Button(frame, bg="#2d35a6", fg="white", font=my_font,
                           text="Select All", width=7, height=1,
                           command=select_all).place(relx=0.60, rely=0.849)
deselect_all_Button = Button(frame, bg="#2d35a6", fg="white", font=my_font,
                             text="Deselect All", width=10, height=1,
                             command=deselect_all).place(relx=0.524,
                                                         rely=0.849)
global e
e = Entry(frame, bg="#ffe4d1", font=my_font, width=30,
          textvariable=query).place(relx=0.37, rely=0.910)
search_button = Button(frame, bg="#2d35a6", fg="white", font=my_font,
                       text="Search", width=7, height=1,
                       command=search).place(relx=0.54, rely=0.910)

check_button = Button(frame, bg="#2d35a6", fg="white", font=my_font,
                      text="Check", width=7, height=1,
                      command=check).place(relx=0.60, rely=0.910)
main.bind('<Return>', enter_search)
