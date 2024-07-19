import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

def encrypt_image(image_path, key):
    # Open the image path not secure soaaaryab 
    img = Image.open(image_path)
    img = img.convert('RGB')  # Ensure image is in RGB format
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Encrypt the image by adding the key to each pixel value
    encrypted_array = (img_array + key) % 256
    
    # Convert back to Image object
    encrypted_img = Image.fromarray(encrypted_array.astype('uint8'), 'RGB')
    
    return encrypted_img

def decrypt_image(encrypted_img, key):
    # Convert encrypted image to numpy array
    encrypted_array = np.array(encrypted_img)
    
    # Decrypt the image by subtracting the key from each pixel value
    decrypted_array = (encrypted_array - key) % 256
    
    # Convert back to Image object
    decrypted_img = Image.fromarray(decrypted_array.astype('uint8'), 'RGB')
    
    return decrypted_img

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        input_image_path.set(file_path)
        display_image(file_path, original_image_label)

def save_file(image, default_extension):
    file_path = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("Bitmap files", "*.bmp")])
    if file_path:
        image.save(file_path)
        messagebox.showinfo("Success", f"Image saved as {file_path}")

def encrypt_action():
    try:
        key = int(encryption_key.get())
        encrypted_img = encrypt_image(input_image_path.get(), key)
        display_image(encrypted_img, encrypted_image_label)
        save_file(encrypted_img, ".jpg")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_action():
    try:
        key = int(encryption_key.get())
        encrypted_img = Image.open(input_image_path.get())
        decrypted_img = decrypt_image(encrypted_img, key)
        display_image(decrypted_img, decrypted_image_label)
        save_file(decrypted_img, ".jpg")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_image(image, label):
    if isinstance(image, str):
        image = Image.open(image)
    image.thumbnail((200, 200))
    img = ImageTk.PhotoImage(image)
    label.config(image=img)
    label.image = img

# Create the main windo
root = tk.Tk()
root.title("Image Encryptor/Decryptor")

# Create variables
input_image_path = tk.StringVar()
encryption_key = tk.StringVar(value="50")

# Create and place widgets
tk.Label(root, text="Select Image:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=input_image_path, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=open_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Encryption Key:").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=encryption_key, width=10).grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Encrypt and Save", command=encrypt_action).grid(row=2, column=0, columnspan=3, pady=10)
tk.Button(root, text="Decrypt and Save", command=decrypt_action).grid(row=3, column=0, columnspan=3, pady=10)

original_image_label = tk.Label(root)
original_image_label.grid(row=4, column=0, padx=5, pady=5)
encrypted_image_label = tk.Label(root)
encrypted_image_label.grid(row=4, column=1, padx=5, pady=5)
decrypted_image_label = tk.Label(root)
decrypted_image_label.grid(row=4, column=2, padx=5, pady=5)

# Start the main loop and 
root.mainloop()