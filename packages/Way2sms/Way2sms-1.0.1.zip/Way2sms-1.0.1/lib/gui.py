import Tkinter as Ui
import way2
import tkMessageBox as Msg
import ttk

MEDIUM_FONT = ('Helvetica', 13)
SMALL_FONT = ('Helvetica', 10, 'bold')
VERY_SMALL = ('Helvetica', 9)
N = Ui.N
W = Ui.W
S = Ui.S
E = Ui.E


class Gui:
    def __init__(self):
        self.root = Ui.Tk()
        self.sms = way2.Way2sms()
        self.style = ttk.Style()
        self.configure = self.style.configure

    def main(self):
        self.root.title('Chat')
        self.root.config(bg='white')
        self.root.resizable(0, 0)
        self.root.minsize(300, 540)
        self.header()
        self.login_ui()
        self.style_elements()
        self.root.mainloop()

    def header(self):
        #photo = Ui.PhotoImage(file='icon.gif')
        label = Ui.Label(self.root, text="dbgvdgv")
        #label['image'] = photo
        label.config(height=50, width=100, compound="bottom")
        #label.grid()

    def login_ui(self):
        frame = ttk.Frame(self.root, padding="70 120 0 0")
        frame.grid(row=0, column=0, sticky=(N, W, E, S))
        label = ttk.Label(frame, text='Username:')
        label.grid(row=2, column=0, sticky=(N, W))
        username = ttk.Entry(frame)
        username.grid(row=3, column=0, padx=3, pady=5, ipadx=3, ipady=3)
        username.config(width="25")
        label2 = ttk.Label(frame, text='Password:')
        label2.grid(row=4, column=0, sticky=(N, W))
        password = ttk.Entry(frame, show='*')
        password.grid(row=5, column=0, padx=3, pady=5, ipadx=3, ipady=3)
        password.config(width="25")
        button = ttk.Button(frame, text="Login", command=lambda: self.login(username, password, frame))
        button.grid(row=6, column=0, pady=5, ipadx=3, ipady=0)
        button.config(width="20")
        username.focus_set()
        username.bind('<Return>', lambda e: password.focus_set())
        password.bind('<Return>', lambda e: button.invoke())

    def login(self, username, password, frame):
        if self.sms.login(username.get(), password.get()):
            frame.destroy()
            self.address_ui()
        else:
            Msg.showerror('Error', 'Something went wrong try later')

    def address_ui(self):
        frame = ttk.Frame(self.root)
        frame.grid()
        contacts = self.sms.contacts('GET')
        add_contacts = ttk.Button(frame, text="+ Add Contacts", command=self.add_contacts, style='add.TButton')
        add_contacts.grid(padx=3, pady=5, row=1, column=0)
        refresh = ttk.Button(frame, text="Refresh", command=lambda: self.refresh(frame), style="refresh.TButton")
        refresh.grid(padx=0, pady=5, row=1, column=1)
        self.root.bind('<F5>', lambda e: refresh.invoke())
        label = ttk.Label(frame, text="Contacts", style="contact.TLabel")
        label.grid(row=2, column=0, sticky=(N, W))
        label.configure(width=15)
        row = 3
        for i in contacts:
            label1 = ttk.Label(frame, text=i.capitalize(), style="number.TLabel")
            label1.grid(row=row, column=0, sticky=W, padx=5, columnspan=1)
            label1.configure(width=12)
            label2 = ttk.Label(frame, text=contacts[i], style="number.TLabel")
            label2.grid(row=row, column=1, columnspan=1)
            label2.configure(width=10)
            button = ttk.Button(frame, text='Message', command=lambda j=contacts[i]: self.message_ui(j),
                                style="add.TButton")
            button.grid(row=row, column=2, pady=5)
            row += row

    def refresh(self, frame):
        frame.destroy()
        self.address_ui()

    def add_contacts(self):
        win = Ui.Toplevel(bg="white")
        win.title('+ Add New contact ')
        name = ttk.Label(win, text="Name:")
        name.grid(row=0, column=0, padx=10, pady=5, sticky=(N, W))
        name_entry = ttk.Entry(win)
        name_entry.configure(width="15")
        name_entry.grid(row=1, column=0, padx=10, pady=5, ipadx=3, ipady=5)
        number = ttk.Label(win, text="Number:")
        number.grid(row=2, column=0, padx=10, pady=5, sticky=(N, W))
        number_entry = ttk.Entry(win)
        number_entry.configure(width=15)
        number_entry.grid(row=3, column=0, padx=10, pady=5, ipadx=3, ipady=5)
        save = ttk.Button(win, text="Save Contact",
                          command=lambda: self.save_contacts(win, data={name_entry.get(): number_entry.get()}))
        save.grid(row=4, column=0, padx=10, pady=5)
        cancel = ttk.Button(win, text="Cancel", command=win.destroy)
        cancel.grid(row=4, column=1, padx=10, pady=5)
        name_entry.focus_set()
        name_entry.bind('<Return>', lambda e: number_entry.focus_set())
        number_entry.bind('<Return>', lambda e: save.invoke())
        win.bind('<Escape>', lambda e: win.destroy())

    def save_contacts(self, win, data):
        self.sms.contacts(method='ADD', data=data)
        win.destroy()

    def message_ui(self, number):
        msg = Ui.Toplevel()
        msg.configure(bg="white")
        msg.title(number)
        msg.minsize(70, 30)
        msg.resizable(0, 0)
        label = ttk.Label(msg, text="Message")
        label.grid(row=0, column=0, sticky=(N, W), padx=10, pady=5)
        text = Ui.Text(msg)
        text.grid(row=1, column=0, padx=15, pady=10)
        text.configure(width=50, height=10, bd=2)
        send = ttk.Button(msg, text="Send",
                          command=lambda: self.send(msg, number, text.get(1.0, Ui.END)))
        send.grid(row=2, column=1, padx=5, pady=10, sticky=(N, W))
        cancel = ttk.Button(msg, text="Cancel", command=msg.destroy)
        cancel.grid(padx=5, pady=10, sticky=W, row=2)
        send.configure(width=20)
        cancel.configure(width=20)
        text.focus_set()
        text.bind('<Return>', lambda e: send.invoke())
        msg.bind('<Escape>', lambda e: msg.destroy())

    def send(self, msg, number, data):
        if self.sms.send_sms(data, number):
            msg.destroy()

    def style_elements(self):
        self.style.theme_use('clam')
        self.configure('TFrame', background="White")
        self.configure('TLabel', background="White", font=MEDIUM_FONT)
        self.configure('TButton', font=SMALL_FONT)
        self.style.map('TButton',
                       background=[('disabled', "grey"), ('active', 'White')],
                       relief=[('pressed', '!disabled', 'sunken')])
        self.style.configure('add.TButton', background="Red", font=VERY_SMALL)
        self.style.configure('refresh.TButton', font=VERY_SMALL, background="white")
        self.style.configure('contact.TLabel', background="grey")
        self.style.configure('number.TLabel', font=SMALL_FONT)
