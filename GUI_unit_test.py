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


    # def test_force_fail(self):
    #     """A test case that always fails to simulate a failure."""
    #     self.fail("This is an intentionally failed test case.")

    def neg_test_incorrect_subtotal_fail(self):
        """This test intentionally asserts an incorrect subtotal."""
        # Add a Buy trade of 200.
        self.app.commodity_dropdown.set("Natural Gas")
        self.app.tt_dropdown.set("Physical")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "200")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Retrieve the subtotal from the position table.
        pos_items = self.app.position_tree.get_children()
        self.assertEqual(len(pos_items), 1)
        subtotal = self.app.position_tree.item(pos_items[0])['values'][0]
        # Intentionally assert an incorrect subtotal to force a failure.
        self.assertEqual(subtotal, "150.00", "Expected subtotal to be 150.00, but it's not.")

    def neg_test_no_trade_added_fail(self):
        """This test intentionally expects a trade when one should not be added."""
        # Leave the commodity field empty (invalid input).
        self.app.tt_dropdown.set("Physical")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "100")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Since commodity is missing, no trade should be added.
        # This assertion is intentionally wrong to force a failure.
        trades = self.app.tree.get_children()
        self.assertEqual(len(trades), 1, "Expected a trade to be added despite missing commodity.")

    # --- Additional Passing Tests ---

    def neg_test_invalid_numeric_value_no_trade(self):
        """Ensure that a non-numeric value does not add a trade."""
        self.app.commodity_dropdown.set("ULSD")
        self.app.tt_dropdown.set("Financial")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "not_a_number")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        trades = self.app.tree.get_children()
        self.assertEqual(len(trades), 0, "No trade should be added for a non-numeric value.")
        
        # Verify that the subtotal remains unchanged.
        subtotal_text = self.app.subtotal_label.cget("text")
        self.assertEqual(subtotal_text, "Subtotal: 0.00")

    def test_clear_inputs_after_save(self):
        """Check that input fields are cleared after saving a trade."""
        self.app.commodity_dropdown.set("Power")
        self.app.tt_dropdown.set("Physical")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "75")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Verify that all input fields have been reset.
        self.assertEqual(self.app.commodity_dropdown.get(), "", "Commodity field should be cleared.")
        self.assertEqual(self.app.tt_dropdown.get(), "", "Trade Type field should be cleared.")
        self.assertEqual(self.app.buy_sell_dropdown.get(), "", "Buy/Sell field should be cleared.")
        self.assertEqual(self.app.value_entry.get(), "", "Value field should be cleared.")

    def test_three_trades_subtotal(self):
        """Add three trades and verify that the subtotal is computed correctly."""
        # First trade: Buy of 120.
        self.app.commodity_dropdown.set("Natural Gas")
        self.app.tt_dropdown.set("Physical")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "120")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Second trade: Sell of 30.
        self.app.commodity_dropdown.set("ULSD")
        self.app.tt_dropdown.set("Financial")
        self.app.buy_sell_dropdown.set("Sell")
        self.app.value_entry.insert(0, "30")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Third trade: Buy of 80.
        self.app.commodity_dropdown.set("Power")
        self.app.tt_dropdown.set("Physical")
        self.app.buy_sell_dropdown.set("Buy")
        self.app.value_entry.insert(0, "80")
        self.app.save_button.invoke()
        self.app.update_idletasks()
        self.app.update()
        
        # Expected subtotal: 120 + (-30) + 80 = 170.00.
        pos_items = self.app.position_tree.get_children()
        self.assertEqual(len(pos_items), 1)
        subtotal = self.app.position_tree.item(pos_items[0])['values'][0]
        self.assertEqual(subtotal, "170.00", "Subtotal should be 170.00 after three trades.")
        
if __name__ == "__main__":
    unittest.main()
