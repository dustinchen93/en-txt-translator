import tkinter as tk
from tkinter import filedialog
import os
import time
from tkinter import ttk
from translator import translate as _translate

# Create window
root = tk.Tk()
root.title("en-txt-translator")
root.geometry("500x200+{}+{}".format(int(root.winfo_screenwidth()/2 - 200), int(root.winfo_screenheight()/2 - 100)))

# Create 3 text input box
text1 = tk.Entry(root, width=60)
text2 = tk.Entry(root, width=60)
text3 = tk.Entry(root, width=60)


# Create label for information
label = tk.Label(root, text="Progress:-/-")
def update_label(finished="-",task_num="-"):
    label.config(text="Progress:{}/{}".format(finished,task_num))
    
info = tk.Text(root, wrap=tk.WORD, width=40, borderwidth=0, height=5)
info.insert(tk.END, '''This is a small program that translates English documents into Chinese.
You need to select the translation model folder (with a config.json file in it), input file, and output file in the top three lines.
Then click the Translate button to run, and you can see the current progress on the left sideof the Translate button.
If you encounter any problems during use, please explain in https://github.com/dustinchen93/en-txt-translator/issues.''')
info.config(state="disabled")


def translate():
    model_file = text1.get()
    input_file = text2.get()
    output_file = text3.get()
    if not os.path.exists(model_file):
        info.config(state="normal")
        info.insert('1.0','''Invalid path for model:\"'''+text1.get()+'\"\n')
        info.config(state="disabled")
        return 1
    
    if not os.path.exists(input_file):
        info.config(state="normal")
        info.insert('1.0','''Invalid path for input file:\"'''+text2.get()+'\"\n')
        info.config(state="disable")
        return 1
    
    if not os.path.exists(os.path.dirname(output_file)):
        info.config(state="normal")
        info.insert('1.0','''Invalid path for output file:\"'''+text3.get()+'\"\n')
        info.config(state="disable")
        return 1
    _translate(model_file,input_file,output_file,update_progress=update_label)

def buttonFunc(text,open_type="file"):
    def _buttonFunc():
        file_path =""
        if open_type == "file":
            file_path = filedialog.askopenfilename()
        elif open_type == "folder":
            file_path = filedialog.askdirectory()
        file_name = os.path.basename(file_path)
        folder_path = os.path.dirname(file_path)
        full_path = os.path.abspath(file_path)

        text.delete(0, tk.END)
        text.insert(0, full_path)
    return _buttonFunc

button1 = tk.Button(root, text="Choose model file", command=buttonFunc(text1,open_type="folder"))
button2 = tk.Button(root, text="Choose input file", command=buttonFunc(text2))
button3 = tk.Button(root, text="Choose output file", command=buttonFunc(text3))
button4 = tk.Button(root, text="Translate", command=translate)


text1.grid(row=0, column=0)
button1.grid(row=0, column=1)
text2.grid(row=1, column=0)
button2.grid(row=1, column=1)
text3.grid(row=2, column=0)
button3.grid(row=2, column=1)
label.grid(row=3, column=0)
button4.grid(row=3, column=1)
info.grid(row=4,column=0)


root.mainloop()

