import tkinter as tk
import re
from tkinter import filedialog


class EmailHeaderParser:
    def __init__(self):
        self.sender = ""
        self.recipient = ""
        self.subject = ""
        self.date = ""
        self.email_service = ""

    def parse_header(self, header):
        pattern_sender = re.compile(r"From:\s*(.*)")
        self.sender = re.search(pattern_sender, header).group(1)

        pattern_recipient = re.compile(r"To:\s*(.*)")
        self.recipient = re.search(pattern_recipient, header).group(1)

        pattern_subject = re.compile(r"Subject:\s*(.*)")
        self.subject = re.search(pattern_subject, header).group(1)

        pattern_date = re.compile(r"Date:\s*(.*)")
        self.date = re.search(pattern_date, header).group(1)


class EmailHeaderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Email Header Parser")

        self.email_parser = EmailHeaderParser()

        # Create the UI elements
        self.lbl_header = tk.Label(self.master, text="Email Header")
        self.lbl_header.pack()

        self.txt_header = tk.Text(self.master, height=10, width=100)
        self.txt_header.pack()

        self.btn_parse = tk.Button(self.master, text="Parse", command=self.parse_header)
        self.btn_parse.pack()

        self.btn_import = tk.Button(self.master, text="Import", command=self.import_file)
        self.btn_import.pack()

        self.lbl_sender = tk.Label(self.master, width=100, text="Sender:")
        self.lbl_sender.pack()

        self.txt_sender = tk.Entry(self.master)
        self.txt_sender.pack()

        self.lbl_recipient = tk.Label(self.master, text="Recipient:")
        self.lbl_recipient.pack()

        self.txt_recipient = tk.Entry(self.master)
        self.txt_recipient.pack()

        self.lbl_subject = tk.Label(self.master, text="Subject:")
        self.lbl_subject.pack()

        self.txt_subject = tk.Entry(self.master)
        self.txt_subject.pack()

        self.lbl_date = tk.Label(self.master, text="Date:")
        self.lbl_date.pack()

        self.txt_date = tk.Entry(self.master)
        self.txt_date.pack()

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Email files", "*.eml")])
        if file_path:
            with open(file_path, "r") as f:
                email_text = f.read()
            self.txt_header.delete("1.0", tk.END)
            self.txt_header.insert(tk.END, email_text)

    def parse_header(self):
        header = self.txt_header.get("1.0", "end-1c")
        self.email_parser.parse_header(header)

        self.txt_sender.delete(0, tk.END)
        self.txt_sender.insert(0, self.email_parser.sender)

        self.txt_recipient.delete(0, tk.END)
        self.txt_recipient.insert(0, self.email_parser.recipient)

        self.txt_subject.delete(0, tk.END)
        self.txt_subject.insert(0, self.email_parser.subject)

        self.txt_date.delete(0, tk.END)
        self.txt_date.insert(0, self.email_parser.date)

        self.check_email_service(header)

    def check_email_service(self, header):
        if "X-Originating-IP" in header:
            self.email_service = "Outlook"
        elif "X-Google-Original-Message-ID" in header:
            self.email_service = "Gmail"

if __name__ == "__main__":
    root = tk.Tk()
    email_gui = EmailHeaderGUI(root)
    root.mainloop()
