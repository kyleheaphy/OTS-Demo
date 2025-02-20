import unittest
import tkinter as tk
from GUI import SimpleGUI  # Adjust this import as needed

class TestSimpleGUI(unittest.TestCase):
    def setUp(self):
        # Create an instance of the GUI without calling mainloop.
        self.app = SimpleGUI()
        # Force initialization.
        self.app.update()

    def tearDown(self):
        # Destroy the GUI instance after each test.
        self.app.destroy()

    def test_save_details_buy(self):
        # Simulate a "Buy" trade that should be positive.
        self.app.commodity_dropdown.set("Power")
        self.app.tt_dropdown.set("Physical")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "100")
        
        # Simulate clicking the save button.
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()

        # Verify that one trade was added.
        trades = self.app.tree.get_children()
        self.assertEqual(len(trades), 1)
        
        # Verify the trade details.
        trade = self.app.tree.item(trades[0])['values']
        self.assertEqual(trade[0], "Power")
        self.assertEqual(trade[1], "Physical")
        self.assertEqual(trade[2], "Buy")
        self.assertEqual(float(trade[3]), 100.0)  # Convert to float for comparison

        # Verify the position (subtotal) is updated correctly.
        pos_items = self.app.position_tree.get_children()
        self.assertEqual(len(pos_items), 1)
        subtotal = self.app.position_tree.item(pos_items[0])['values'][0]
        self.assertEqual(subtotal, "100.00")

    def test_save_details_sell(self):
        # Simulate a "Sell" trade that should be negative.
        self.app.commodity_dropdown.set("ULSD")
        self.app.tt_dropdown.set("Financial")
        self.app.buy_sell_dropdown.set("Sell")
        self.app.value_entry.insert(0, "50")
        
        # Simulate clicking the save button.
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()

        # Verify that one trade was added.
        trades = self.app.tree.get_children()
        self.assertEqual(len(trades), 1)
        
        # Verify the trade details.
        trade = self.app.tree.item(trades[0])['values']
        self.assertEqual(trade[0], "ULSD")
        self.assertEqual(trade[1], "Financial")
        self.assertEqual(trade[2], "Sell")
        self.assertEqual(float(trade[3]), -50.0)  # Convert to float for comparison

        # Verify the position (subtotal) is updated correctly.
        pos_items = self.app.position_tree.get_children()
        self.assertEqual(len(pos_items), 1)
        subtotal = self.app.position_tree.item(pos_items[0])['values'][0]
        self.assertEqual(subtotal, "-50.00")

    def test_multiple_trades(self):
        # Add a Buy trade of 100.
        self.app.commodity_dropdown.set("Power")
        self.app.tt_dropdown.set("Physical")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "100")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Add a Sell trade of 20.
        self.app.commodity_dropdown.set("Natural Gas")
        self.app.tt_dropdown.set("Financial")
        self.app.buy_sell_dropdown.set("Sell")
        self.app.value_entry.insert(0, "20")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Expect a subtotal of 100 + (-20) = 80.00.
        pos_items = self.app.position_tree.get_children()
        self.assertEqual(len(pos_items), 1)
        subtotal = self.app.position_tree.item(pos_items[0])['values'][0]
        self.assertEqual(subtotal, "80.00")

if __name__ == "__main__":
    unittest.main()
