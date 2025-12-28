import random
from tkinter import *
from tkinter import messagebox
class BillApp:
def __init__(self, root):
self.root = root
self.root.geometry("1350x700+0+0")
self.root.configure(bg="#0A7CFF")
self.root.title("Restaurant Billing System")
title = Label(self.root, text="Restaurant Billing System", bd=12, relief=RIDGE,
font=("Arial Black", 20), bg="#A569BD", fg="white").pack(fill=X)
# Variables
self.samosa = IntVar()
self.paneer_tikka = IntVar()
self.chicken_tikka = IntVar()
self.veg_pakora = IntVar()
self.papdi_chaat = IntVar()
self.tomato_soup = IntVar()
self.masala_papad = IntVar()
self.butter_chicken = IntVar()
self.pasta = IntVar()
self.basmati_rice = IntVar()
self.paneer_masala = IntVar()
self.palak_paneer = IntVar()
self.dal = IntVar()
self.chole_bhature = IntVar()
self.noodles = IntVar()
self.aloo_tikki_chaat = IntVar()
self.dahi_vada = IntVar()
self.pav_bhaji = IntVar()
self.bhel_puri = IntVar()
self.soup = IntVar()
self.pokara = IntVar()
self.total_starter_price = StringVar()
self.total_main_course_price = StringVar()
self.total_snacks_price = StringVar()
self.cgst = StringVar()
self.sgst = StringVar()
self.total_tax = StringVar()
self.customer_name = StringVar()
self.phone = StringVar()
self.bill_no = StringVar()
x = random.randint(1, 100)
self.bill_no.set(str(x))
# Customer Details Frame
details = LabelFrame(self.root, text="Customer Details", font=("Arial Black", 12),
bg="#A569BD", fg="white", relief=GROOVE, bd=10)
details.place(x=0, y=80, relwidth=1)
cust_name = Label(details, text="Customer Name", font=("Arial Black", 14),
bg="#A569BD", fg="white").grid(row=0, column=0, padx=15)
cust_entry = Entry(details, borderwidth=4, width=30, textvariable=self.customer_name).grid(row=0, column=1, padx=8)
contact_name = Label(details, text="Contact No.", font=("Arial Black", 14),
bg="#A569BD", fg="white").grid(row=0, column=2, padx=10)
contact_entry = Entry(details, borderwidth=4, width=30, textvariable=self.phone).grid(row=0, column=3, padx=8)
bill_name = Label(details, text="Bill No.", font=("Arial Black", 14),
bg="#A569BD", fg="white").grid(row=0, column=4, padx=10)
bill_entry = Entry(details, borderwidth=4, width=30, textvariable=self.bill_no).grid(row=0, column=5, padx=8)
# Restaurant Menu Frames
starter = LabelFrame(self.root, text="Starter", font=("Arial Black", 12),
bg="#E5B4F3", fg="#6C3483", relief=GROOVE, bd=10)
starter.place(x=5, y=180, height=380, width=325)
# Starter Items
items = [
("Samosa", self.samosa),
("Paneer Tikka", self.paneer_tikka),
("Chicken Tikka", self.chicken_tikka),
("Vegetable Pakora", self.veg_pakora),
("Papdi Chaat", self.papdi_chaat),
("Tomato Soup", self.tomato_soup),
("Masala Papad", self.masala_papad)
]
for i, (item, var) in enumerate(items):
Label(starter, text=item, font=("Arial Black", 11), bg="#E5B4F3", fg="#6C3483").grid(row=i, column=0, pady=11)
Entry(starter, borderwidth=2, width=15, textvariable=var).grid(row=i, column=1, padx=10)
# Main Course Frame
main_course = LabelFrame(self.root, text="Main Course", font=("Arial Black", 12),
relief=GROOVE, bd=10, bg="#E5B4F3", fg="#6C3483")
main_course.place(x=340, y=180, height=380, width=325)
main_course_items = [
("Butter Chicken", self.butter_chicken),
("Pasta", self.pasta),
("Basmati Rice", self.basmati_rice),
("Paneer Masala", self.paneer_masala),
("Palak Paneer", self.palak_paneer),
("Dal", self.dal),
("Chole Bhature", self.chole_bhature)
]
for i, (item, var) in enumerate(main_course_items):
Label(main_course, text=item, font=("Arial Black", 11), bg="#E5B4F3", fg="#6C3483").grid(row=i, column=0, pady=11)
Entry(main_course, borderwidth=2, width=15, textvariable=var).grid(row=i, column=1, padx=10)
# Snacks Frame
snacks = LabelFrame(self.root, text="Snacks", font=("Arial Black", 12),
relief=GROOVE, bd=10, bg="#E5B4F3", fg="#6C3483")
snacks.place(x=677, y=180, height=380, width=325)
snacks_items = [
("Noodles", self.noodles),
("Aloo Tikki Chaat", self.aloo_tikki_chaat),
("Dahi Vada", self.dahi_vada),
("Pav Bhaji", self.pav_bhaji),
("Bhel Puri", self.bhel_puri),
("Soup", self.soup),
("Pokara", self.pokara)
]
for i, (item, var) in enumerate(snacks_items):
Label(snacks, text=item, font=("Arial Black", 11), bg="#E5B4F3", fg="#6C3483").grid(row=i, column=0, pady=11)
Entry(snacks, borderwidth=2, width=15, textvariable=var).grid(row=i, column=1, padx=10)
# Bill Area Frame
bill_area = Frame(self.root, bd=10, relief=GROOVE, bg="#E5B4F3")
bill_area.place(x=1010, y=188, width=330, height=372)
bill_title = Label(bill_area, text="Bill Area", font=("Arial Black", 17), bd=7, relief=GROOVE,
bg="#E5B4F3", fg="#6C3483").pack(fill=X)
scrol_y = Scrollbar(bill_area, orient=VERTICAL)
self.txtarea = Text(bill_area, yscrollcommand=scrol_y.set)
scrol_y.pack(side=RIGHT, fill=Y)
scrol_y.config(command=self.txtarea.yview)
self.txtarea.pack(fill=BOTH, expand=1)
# Billing Menu Frame
billing_menu = LabelFrame(self.root, text="Billing Summary", font=("Arial Black", 12),
relief=GROOVE, bd=10, bg="#A569BD", fg="white")
billing_menu.place(x=0, y=560, relwidth=1, height=137)
labels = [
("Total Starter Price", self.total_starter_price),
("Total Main Course Price", self.total_main_course_price),
("Total Snacks Price", self.total_snacks_price),
("CGST", self.cgst),
("SGST", self.sgst),
("Total Tax", self.total_tax)
]
for i, (label_text, var) in enumerate(labels):
row, col = divmod(i, 2)
Label(billing_menu, text=label_text, font=("Arial Black", 11), bg="#A569BD", fg="white").grid(row=row, column=col*2)
Entry(billing_menu, width=30, borderwidth=2, textvariable=var).grid(row=row, column=col*2+1, padx=10, pady=7)
button_frame = Frame(billing_menu, bd=7, relief=GROOVE, bg="#6C3483")
button_frame.place(x=830, width=500, height=95)
Button(button_frame, text="Total Bill", font=("Arial Black", 15), pady=10,
bg="#E5B4F3", fg="#6C3483", command=self.total).grid(row=0, column=0, padx=12)
Button(button_frame, text="Clear Field", font=("Arial Black", 15), pady=10,
bg="#E5B4F3", fg="#6C3483", command=self.clear).grid(row=0, column=1, padx=10, pady=6)
Button(button_frame, text="Exit", font=("Arial Black", 15), pady=10, bg="#E5B4F3",
fg="#6C3483", width=8, command=self.exit_app).grid(row=0, column=2, padx=10, pady=6)
self.intro()
def total(self):
if self.customer_name.get() == "" or self.phone.get() == "":
messagebox.showerror("Error", "Fill the complete Customer Details!!!!!!!!!")
return
# Starter calculations
starter_prices = {
"samosa": 20,
"paneer_tikka": 50,
"chicken_tikka": 60,
"veg_pakora": 80,
"papdi_chaat": 50,
"tomato_soup": 90,
"masala_papad": 100
}
total_starter_price = sum(getattr(self, item).get() * price for item, price in starter_prices.items())
self.total_starter_price.set(f"Rs.{total_starter_price}")
# Main Course calculations
main_course_prices = {
"butter_chicken": 200,
"pasta": 150,
"basmati_rice": 100,
"paneer_masala": 180,
"palak_paneer": 170,
"dal": 100,
"chole_bhature": 220
}
total_main_course_price = sum(getattr(self, item).get() * price for item, price in main_course_prices.items())
self.total_main_course_price.set(f"Rs.{total_main_course_price}")
# Snacks calculations
snacks_prices = {
"noodles": 80,
"aloo_tikki_chaat": 180,
"dahi_vada": 130,
"pav_bhaji": 150,
"bhel_puri": 100,
"soup": 120,
"pokara": 120
}
total_snacks_price = sum(getattr(self, item).get() * price for item, price in snacks_prices.items())
self.total_snacks_price.set(f"Rs.{total_snacks_price}")
# Total calculations
total_price = total_starter_price + total_main_course_price + total_snacks_price
cgst = round(total_price * 0.09, 2) # Assuming CGST is half of the total GST
sgst = round(total_price * 0.09, 2) # Assuming SGST is half of the total GST
total_tax = round(cgst + sgst, 2)
self.cgst.set(f"Rs.{cgst:.2f}")
self.sgst.set(f"Rs.{sgst:.2f}")
self.total_tax.set(f"Rs.{total_tax:.2f}")
self.total_bill = total_price + total_tax
self.total_bill_str = f"Rs.{self.total_bill:.2f}"
self.bill_area()
def intro(self):
self.txtarea.delete(1.0, END)
self.txtarea.insert(END, "\t 5 STAR RESTAURANT\n\tPhone-No. 8072977912")
self.txtarea.insert(END, f"\n\nBill no.: {self.bill_no.get()}")
self.txtarea.insert(END, f"\nCustomer Name: {self.customer_name.get()}")
self.txtarea.insert(END, f"\nPhone No.: {self.phone.get()}")
self.txtarea.insert(END, "\n====================================\n")
self.txtarea.insert(END, "\nProduct\t\tQty\tPrice\n")
self.txtarea.insert(END, "====================================\n")
def bill_area(self):
self.intro()
starter_items = [
("Samosa", self.samosa, self.samosa.get() * 20),
("Paneer Tikka", self.paneer_tikka, self.paneer_tikka.get() * 50),
("Chicken Tikka", self.chicken_tikka, self.chicken_tikka.get() * 60),
("Vegetable Pakora", self.veg_pakora, self.veg_pakora.get() * 80),
("Papdi Chaat", self.papdi_chaat, self.papdi_chaat.get() * 50),
("Tomato Soup", self.tomato_soup, self.tomato_soup.get() * 90),
("Masala Papad", self.masala_papad, self.masala_papad.get() * 100)
]
main_course_items = [
("Butter Chicken", self.butter_chicken, self.butter_chicken.get() * 200),
("Pasta", self.pasta, self.pasta.get() * 150),
("Basmati Rice", self.basmati_rice, self.basmati_rice.get() * 100),
("Paneer Masala", self.paneer_masala, self.paneer_masala.get() * 180),
("Palak Paneer", self.palak_paneer, self.palak_paneer.get() * 170),
("Dal", self.dal, self.dal.get() * 100),
("Chole Bhature", self.chole_bhature, self.chole_bhature.get() * 220)
]
snacks_items = [
("Noodles", self.noodles, self.noodles.get() * 80),
("Aloo Tikki Chaat", self.aloo_tikki_chaat, self.aloo_tikki_chaat.get() * 180),
("Dahi Vada", self.dahi_vada, self.dahi_vada.get() * 130),
("Pav Bhaji", self.pav_bhaji, self.pav_bhaji.get() * 150),
("Bhel Puri", self.bhel_puri, self.bhel_puri.get() * 100),
("Soup", self.soup, self.soup.get() * 120),
("Pokara", self.pokara, self.pokara.get() * 120)
]
for category, items in [("Starter", starter_items), ("Main Course", main_course_items), ("Snacks", snacks_items)]:
for item, var, price in items:
if var.get() != 0:
self.txtarea.insert(END, f"{item}\t\t{var.get()}\t{price}\n")
self.txtarea.insert(END, "------------------------------------\n")
self.txtarea.insert(END, f"CGST: {self.cgst.get()}\n")
self.txtarea.insert(END, f"SGST: {self.sgst.get()}\n")
self.txtarea.insert(END, f"Total Tax: {self.total_tax.get()}\n")
self.txtarea.insert(END, f"Total Bill Amount: {self.total_bill_str}\n")
self.txtarea.insert(END, "------------------------------------\n")
def clear(self):
op = messagebox.askyesno("Exit", "Do you really want to clear it?")
if op > 0:
# Starter
for var in [self.samosa, self.paneer_tikka, self.chicken_tikka, self.veg_pakora, self.papdi_chaat,
self.tomato_soup, self.masala_papad]:
var.set(0)
# Main Course
for var in [self.butter_chicken, self.pasta, self.basmati_rice, self.paneer_masala, self.palak_paneer,
self.dal, self.chole_bhature]:
var.set(0)
# Snacks
for var in [self.noodles, self.aloo_tikki_chaat, self.dahi_vada, self.pav_bhaji, self.bhel_puri,
self.soup, self.pokara]:
var.set(0)
# Total
for var in [self.total_starter_price, self.total_main_course_price, self.total_snacks_price,
self.cgst, self.sgst, self.total_tax]:
var.set("")
# Customer Details
self.customer_name.set("")
self.phone.set("")
x = random.randint(1, 100)
self.bill_no.set(str(x))
self.intro()
def exit_app(self):
op = messagebox.askyesno("Exit", "Do you really want to exit?")
if op > 0:
self.root.destroy()
root = Tk()
app = BillApp(root)
root.mainloop()
