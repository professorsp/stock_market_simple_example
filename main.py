import csv
import requests
import ttkbootstrap as tb
from Personalization import *
from tkinter import filedialog
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview


data_text = None


def search():
    global data_text
    r_set = list()
    l1 = list()
    params = {
        "apikey": " HGT1BF9MJAKCDR8W",
        "datatype": "csv",
        "function": f"{func_combo.get()}",
        "symbol": f"{symbol_entry.get().strip()}",
    }
    respone = requests.get(f"https://www.alphavantage.co/query", params=params)
    data_text = respone.text
    dataList = list(data_text.split("\n"))
    l1 = list(dataList.pop(0).split(","))
    for data in dataList: r_set.append(list(data.split(",")))
    dt.build_table_data(l1, r_set)


def import_csv():
    r_set = list()
    file_name = filedialog.askopenfilename(filetypes=(("Text files", "*csv*"), ("all files", "*.*")))
    with open(file_name, 'r') as f:
        dataList = list(f.read().split("\n"))
        l1 = list(dataList.pop(0).split(","))
        for data in dataList: r_set.append(data.split(","))
        f.close()

    dt.build_table_data(l1, r_set)


def export_csv():
    header = list()
    dataList = list()
    rowData = dict()
    file = filedialog.asksaveasfile(defaultextension=[('All Files', '*.csv*')], filetypes=[('All Files', '*.csv*')])
    with open(file.name, "w", newline="") as f:
        for colum in dt.get_columns(): header.append(colum.headertext.replace("\r", ""))
        csvFile = csv.DictWriter(f, fieldnames=header)
        csvFile.writeheader()
        for row in dt.get_rows():
            if len(row.values) != len(header): continue
            for i in range(len(header)):
                rowData[header[i]] = row.values[i].replace("\r", "")
            csvFile.writerow(rowData)

root = tb.Window()
root.resizable(0,0)
searchbar = tb.Frame(root)
searchbar.pack()

func_combo = tb.Combobox(searchbar, values=["TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"])
func_combo.set("TIME_SERIES_DAILY")
func_combo.grid(row=0, column=1, padx=10, pady=20)

searchButton = tb.Button(searchbar, text="Search", command=search)
searchButton.grid(row=0, column=2, padx=10, pady=20)

symbol_entry = Entry_Placeholder(searchbar, placeholder="symbol")
symbol_entry.grid(row=0, column=0, padx=10, pady=20)

dt = Tableview(
    master=root,
    paginated=True,
    pagesize=15,
    bootstyle=PRIMARY,
    height=15,
)
dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

mb = tb.Menubutton(root, text="Tools", bootstyle=PRIMARY)
mb.pack()

menu = tb.Menu(mb)
menu.add_command(label="Import as .csv", command=import_csv)
menu.add_command(label="Export as .csv", command=export_csv)
mb["menu"] = menu
root.mainloop()
