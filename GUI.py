import tkinter as tk
from tkinter import ttk

class SimpleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trade Blotter")
        self.geometry("1000x800")

        #logo
        self.logo_image = tk.PhotoImage(file="logo.png")
        logo_label = tk.Label(self, image=self.logo_image)
        logo_label.pack(anchor='w', padx=10, pady=10)


        # Input section
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Commodity:").grid(row=0, column=1, sticky='e', padx=100)
        self.commodity_var = tk.StringVar()
        self.commodity_dropdown = ttk.Combobox(self.input_frame, textvariable=self.commodity_var, state="readonly")
        self.commodity_dropdown['values'] = ('Power', 'Natural Gas', 'ULSD')
        self.commodity_dropdown.current(None)  # Set default to blank
        self.commodity_dropdown.grid(row=1, column=1, padx=5)
        # self.commodity_entry = tk.Entry(self.input_frame)
        # self.commodity_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.input_frame, text="Trade Type:").grid(row=0, column=2, sticky='e', padx=100)
        self.tt_var = tk.StringVar()
        self.tt_dropdown = ttk.Combobox(self.input_frame, textvariable=self.tt_var, state="readonly")
        self.tt_dropdown['values'] = ('Physical', 'Financial')
        self.tt_dropdown.current(None)  # Set default to the first option
        self.tt_dropdown.grid(row=1, column=2, padx=5)
        # self.tt_entry = tk.Entry(self.input_frame)
        # self.tt_entry.grid(row=1, column=2, padx=5)

        tk.Label(self.input_frame, text="Buy_Sell:").grid(row=0, column=3, sticky='e', padx=100)
        self.buy_sell_var = tk.StringVar()
        self.buy_sell_dropdown = ttk.Combobox(self.input_frame, textvariable=self.buy_sell_var, state="readonly")
        self.buy_sell_dropdown['values'] = ('Buy', 'Sell')
        self.buy_sell_dropdown.current(None)  # Set default to the first option
        self.buy_sell_dropdown.grid(row=1, column=3, padx=5)
        # self.buy_sell_entry = tk.Entry(self.input_frame)
        # self.buy_sell_entry.grid(row=1, column=3, padx=5)
               
        tk.Label(self.input_frame, text="Value:").grid(row=0, column=4, sticky='e', padx=100)
        self.value_entry = tk.Entry(self.input_frame)
        self.value_entry.grid(row=1, column=4, padx=5)

        # save button
        self.save_button = tk.Button(self.input_frame, text="Save", command=self.save_details)
        self.save_button.grid(row=2, column=4, columnspan=2, pady=10)

        # Trades Table display section
        self.trades_frame = tk.Frame(self)
        self.trades_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        tk.Label(self.trades_frame, text="Trades", font=('Arial', 14, 'bold')).pack()

        self.tree = ttk.Treeview(self.trades_frame, columns=("Commodity", "Trade Type", "Buy_Sell", "Value"), show="headings")
        self.tree.heading("Commodity", text="Commodity")
        self.tree.heading("Trade Type", text="Trade Type")
        self.tree.heading("Buy_Sell", text="Buy_Sell")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Position Table
        self.position_frame = tk.Frame(self)
        self.position_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        tk.Label(self.position_frame, text="Position", font=('Arial', 14, 'bold')).pack()

        self.position_tree = ttk.Treeview(self.position_frame, columns=("Subtotal",), show="headings")
        self.position_tree.heading("Subtotal", text="Subtotal")
        self.position_tree.pack(fill=tk.BOTH, expand=True)

        # Subtotal label at the bottom
        self.subtotal_label = tk.Label(self, text="Subtotal: 0.00", font=('Arial', 12, 'bold'))
        self.subtotal_label.pack(pady=5)

    def save_details(self):
        commodity = self.commodity_var.get().strip()
        tt = self.tt_var.get().strip()
        buy_sell = self.buy_sell_var.get().strip()
        value_str = self.value_entry.get().strip()

        if commodity and tt and buy_sell and value_str:
            try:
                numeric_value = float(value_str)
            except ValueError:
                # If the entered value is not a valid number, ignore this entry
                return

            # If the trade is a Sell, make the value negative
            if buy_sell.lower() == "sell":
                numeric_value = -abs(numeric_value)
            else:
                numeric_value = abs(numeric_value)

            # Insert new row into the table
            self.tree.insert("", "end", values=(commodity, tt, buy_sell, numeric_value))
            
            # Reset input fields for next entry
            self.commodity_dropdown.set("")
            self.tt_dropdown.set("")
            self.buy_sell_dropdown.set("")
            self.value_entry.delete(0, tk.END)
            
            # Update the subtotal label
            self.update_subtotal()

    def update_subtotal(self):
            total = 0.0
            # Loop through all items in the treeview
            for item in self.tree.get_children():
                row = self.tree.item(item)['values']
                try:
                    total += float(row[3])
                except (ValueError, IndexError):
                    # In case the value is non-numeric or missing, skip it
                    continue
            self.subtotal_label.config(text=f"Subtotal: {total:.2f}")

            # Update the Position table by clearing it and inserting the new subtotal
            for item in self.position_tree.get_children():
                self.position_tree.delete(item)
            self.position_tree.insert("", "end", values=(f"{total:.2f}",))

if __name__ == "__main__":
    app = SimpleGUI()
    app.mainloop()
