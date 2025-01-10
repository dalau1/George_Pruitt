import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import tkinter as tk
from tkinter import filedialog
import csv
# 
# Function to open file dialog and read CSV file
def open_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    return file_path

# Function to load data and return headers and rows
def load_data(file_path):
    headers = []
    rows = []

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read headers
            for row in reader:
                rows.append(row)
        return headers, rows
    except Exception as e:
        print(f"Error loading data: {e}")
        return [], []

# Function to select columns for X, Y, and Z
def select_columns(headers):
    print("\nAvailable columns:")
    for idx, header in enumerate(headers):
        print(f"{idx + 1}: {header}")

    try:
        x_col = int(input("Select the column number for X-axis: ")) - 1
        y_col = int(input("Select the column number for Y-axis: ")) - 1
        z_col = int(input("Select the column number for Z-axis: ")) - 1
        return x_col, y_col, z_col
    except ValueError:
        print("Invalid selection. Please enter numeric values.")
        return None, None, None

# Function to process selected columns into grid format
def process_columns(rows, x_col, y_col, z_col):
    x_vals = set()
    y_vals = set()
    z_dict = {}

    try:
        for row in rows:
            if len(row) <= max(x_col, y_col, z_col):
                print("Skipping invalid row:", row)
                continue
            try:
                x, y, z = float(row[x_col]), float(row[y_col]), float(row[z_col])
                x_vals.add(x)
                y_vals.add(y)
                z_dict[(x, y)] = z
            except ValueError:
                print("Invalid data encountered in row:", row)
                continue

        # Sort x and y values
        x_vals = np.array(sorted(x_vals))
        y_vals = np.array(sorted(y_vals))

        # Create grid for X, Y, and Z
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.array([[z_dict.get((x, y), np.nan) for x in x_vals] for y in y_vals])
        return X, Y, Z
    except Exception as e:
        print(f"Error processing columns: {e}")
        return None, None, None

# Plot with Matplotlib
def plot_matplotlib(X, Y, Z, headers, x_col, y_col, z_col):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel(headers[x_col])  # Use selected header for X-axis
    ax.set_ylabel(headers[y_col])  # Use selected header for Y-axis
    ax.set_zlabel(headers[z_col])  # Use selected header for Z-axis
    plt.colorbar(surf)
    plt.title("3D Surface Plot (Matplotlib)")
    plt.show()

# Plot with Plotly
def plot_plotly(x_vals, y_vals, Z, headers, x_col, y_col, z_col):
    fig = go.Figure(data=[go.Surface(z=Z, x=x_vals, y=y_vals)])
    fig.update_layout(
        title="Interactive 3D Surface Plot",
        scene=dict(
            xaxis_title=headers[x_col],  # Use selected header for X-axis
            yaxis_title=headers[y_col],  # Use selected header for Y-axis
            zaxis_title=headers[z_col]   # Use selected header for Z-axis
        ),
        autosize=True
    )
    fig.show()

# Main execution
file_path = open_file()
if not file_path:
    print("No file selected. Exiting.")
else:
    # Load data
    headers, rows = load_data(file_path)
    if headers and rows:
        # Select columns
        x_col, y_col, z_col = select_columns(headers)
        if x_col is not None and y_col is not None and z_col is not None:
            # Process selected columns
            X, Y, Z = process_columns(rows, x_col, y_col, z_col)
            if X is not None and Y is not None and Z is not None:
                # Ask user which plot to generate
                print("Choose plot type:")
                print("1: Matplotlib 3D Surface Plot")
                print("2: Plotly Interactive 3D Surface Plot")
                print("3: Both")
                choice = input("Enter your choice (1/2/3): ").strip()

                if choice == "1":
                    plot_matplotlib(X, Y, Z, headers, x_col, y_col, z_col)
                elif choice == "2":
                    plot_plotly(X[0], Y[:, 0], Z, headers, x_col, y_col, z_col)
                elif choice == "3":
                    plot_matplotlib(X, Y, Z, headers, x_col, y_col, z_col)
                    plot_plotly(X[0], Y[:, 0], Z, headers, x_col, y_col, z_col)
                else:
                    print("Invalid choice. Exiting.")
            else:
                print("Failed to process data into a grid.")
        else:
            print("Column selection failed.")
    else:
        print("Failed to load data.")
