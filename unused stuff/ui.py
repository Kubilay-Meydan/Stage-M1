import tkinter as tk
from tkinter import filedialog
import pandas as pd

class CSVEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("CSV Editor")

        # Frame for Row Display and User Input
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Label to show the first column's value
        self.value_label = tk.Label(self.frame, text="Row Value: ", font=('Arial', 12))
        self.value_label.grid(row=0, column=0)

        # Text Entry for user input
        self.user_input = tk.Entry(self.frame, width=20, font=('Arial', 12))
        self.user_input.grid(row=1, column=0, pady=5)

        # Button to save input and go to the next row
        self.next_button = tk.Button(self.frame, text="Next Row", command=self.next_row)
        self.next_button.grid(row=2, column=0, pady=10)

        # Button to load a CSV file
        self.load_button = tk.Button(self.master, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.BOTTOM, pady=10)

        self.df = None
        self.current_row = 0

    def load_csv(self):
        # File dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.show_row()

    def show_row(self):
        if self.df is not None and self.current_row < len(self.df):
            # Show the first column's value
            self.value_label.config(text=f"Row Value: {self.df.iloc[self.current_row, 0]}")
            self.user_input.delete(0, tk.END)
        else:
            # No more rows or file isn't loaded
            self.value_label.config(text="No more rows or file not loaded.")
            self.user_input.delete(0, tk.END)

    def next_row(self):
        if self.df is not None and self.current_row < len(self.df):
            # Save the user input to the fifth column
            self.df.at[self.current_row, 'FifthColumn'] = self.user_input.get()
            self.current_row += 1
            self.show_row()
            
            # If we're at the end, save the modified DataFrame
            if self.current_row == len(self.df):
                self.save_csv()

    def save_csv(self):
        # Save the DataFrame back to a new CSV file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df.to_csv(file_path, index=False)
            tk.messagebox.showinfo("Data Saved", "CSV file has been updated and saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditor(root)
    root.mainloop()
