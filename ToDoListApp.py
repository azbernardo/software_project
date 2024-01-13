from ToDoList_Gui import ToDoListApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)

    # Set the geometry
    root.geometry("800x700")


    root.mainloop()