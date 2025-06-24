import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import math

class GraphicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Grafis 2D - Transformasi & Clipping")
        self.root.geometry("1200x800")
        
        # Canvas setup
        self.canvas_width = 800
        self.canvas_height = 600
        
        # Drawing variables
        self.current_tool = "point"
        self.current_color = "#000000"
        self.current_thickness = 2
        self.objects = []  # Store all drawn objects
        self.temp_line = None
        self.start_x = None
        self.start_y = None
        
        # Undo/Delete variables
        self.history = []  # Store history for undo
        self.delete_mode = False
        
        # Windowing variables
        self.window_mode = False
        self.window_coords = None
        self.windowed_objects = []
        
        # Transformation variables
        self.selected_object = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        control_frame = tk.Frame(main_frame, width=350, bg='lightgray')
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)
        
        # Canvas frame
        canvas_frame = tk.Frame(main_frame, bg='white')
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, 
                               height=self.canvas_height, bg='white', 
                               highlightthickness=1, highlightbackground='black')
        self.canvas.pack()
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        self.setup_controls(control_frame)
        
    def setup_controls(self, parent):
        # Title
        title_label = tk.Label(parent, text="KONTROL GRAFIS 2D", 
                              font=("Arial", 14, "bold"), bg='lightgray')
        title_label.pack(pady=10)
        
        # Tool selection
        tool_frame = tk.LabelFrame(parent, text="Pilih Alat Gambar", bg='lightgray')
        tool_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tools = [("Titik", "point"), ("Garis", "line"), 
                ("Persegi", "rectangle"), ("Ellipse", "ellipse")]
        
        self.tool_var = tk.StringVar(value="point")
        for text, value in tools:
            rb = tk.Radiobutton(tool_frame, text=text, variable=self.tool_var,
                               value=value, command=self.change_tool, bg='lightgray')
            rb.pack(anchor=tk.W)
        
        # Color selection
        color_frame = tk.LabelFrame(parent, text="Warna & Ketebalan", bg='lightgray')
        color_frame.pack(fill=tk.X, padx=10, pady=5)
        
        color_btn = tk.Button(color_frame, text="Pilih Warna", 
                             command=self.choose_color, bg='white')
        color_btn.pack(pady=5)
        
        self.color_display = tk.Label(color_frame, width=20, height=2, 
                                     bg=self.current_color, relief=tk.RAISED)
        self.color_display.pack(pady=5)
        
        # Thickness
        tk.Label(color_frame, text="Ketebalan:", bg='lightgray').pack()
        self.thickness_var = tk.IntVar(value=2)
        thickness_scale = tk.Scale(color_frame, from_=1, to=10, 
                                  variable=self.thickness_var, 
                                  orient=tk.HORIZONTAL, command=self.change_thickness)
        thickness_scale.pack(fill=tk.X, padx=5)
        
        # Transformation controls
        transform_frame = tk.LabelFrame(parent, text="Transformasi", bg='lightgray')
        transform_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(transform_frame, text="Pilih Objek", 
                 command=self.select_object_mode).pack(fill=tk.X, pady=2)
        
        # Translation
        trans_frame = tk.Frame(transform_frame, bg='lightgray')
        trans_frame.pack(fill=tk.X, pady=2)
        tk.Label(trans_frame, text="Translasi (dx,dy):", bg='lightgray').pack()
        
        trans_input_frame = tk.Frame(trans_frame, bg='lightgray')
        trans_input_frame.pack()
        self.dx_entry = tk.Entry(trans_input_frame, width=8)
        self.dx_entry.pack(side=tk.LEFT, padx=2)
        self.dy_entry = tk.Entry(trans_input_frame, width=8)
        self.dy_entry.pack(side=tk.LEFT, padx=2)
        tk.Button(trans_input_frame, text="Translasi", 
                 command=self.translate_object).pack(side=tk.LEFT, padx=2)
        
        # Rotation
        rot_frame = tk.Frame(transform_frame, bg='lightgray')
        rot_frame.pack(fill=tk.X, pady=2)
        tk.Label(rot_frame, text="Rotasi (derajat):", bg='lightgray').pack()
        
        rot_input_frame = tk.Frame(rot_frame, bg='lightgray')
        rot_input_frame.pack()
        self.angle_entry = tk.Entry(rot_input_frame, width=8)
        self.angle_entry.pack(side=tk.LEFT, padx=2)
        tk.Button(rot_input_frame, text="Rotasi", 
                 command=self.rotate_object).pack(side=tk.LEFT, padx=2)
        
        # Scaling
        scale_frame = tk.Frame(transform_frame, bg='lightgray')
        scale_frame.pack(fill=tk.X, pady=2)
        tk.Label(scale_frame, text="Skala (sx,sy):", bg='lightgray').pack()
        
        scale_input_frame = tk.Frame(scale_frame, bg='lightgray')
        scale_input_frame.pack()
        self.sx_entry = tk.Entry(scale_input_frame, width=8)
        self.sx_entry.pack(side=tk.LEFT, padx=2)
        self.sy_entry = tk.Entry(scale_input_frame, width=8)
        self.sy_entry.pack(side=tk.LEFT, padx=2)
        tk.Button(scale_input_frame, text="Skala", 
                 command=self.scale_object).pack(side=tk.LEFT, padx=2)
        
        # Windowing and Clipping
        window_frame = tk.LabelFrame(parent, text="Windowing & Clipping", bg='lightgray')
        window_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(window_frame, text="Mode Windowing", 
                 command=self.toggle_window_mode).pack(fill=tk.X, pady=2)
        tk.Button(window_frame, text="Clip Objek Windowing", 
                 command=self.clip_windowed_objects).pack(fill=tk.X, pady=2)
        tk.Button(window_frame, text="Reset Windowing", 
                 command=self.reset_windowing).pack(fill=tk.X, pady=2)
        
        # Utility buttons
        util_frame = tk.LabelFrame(parent, text="Utilitas", bg='lightgray')
        util_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(util_frame, text="Undo", 
                 command=self.undo_last_action).pack(fill=tk.X, pady=2)
        tk.Button(util_frame, text="Mode Hapus Objek", 
                 command=self.toggle_delete_mode).pack(fill=tk.X, pady=2)
        tk.Button(util_frame, text="Hapus Semua", 
                 command=self.clear_canvas).pack(fill=tk.X, pady=2)
        tk.Button(util_frame, text="Info Objek", 
                 command=self.show_objects_info).pack(fill=tk.X, pady=2)
        
    def change_tool(self):
        self.current_tool = self.tool_var.get()
        
    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color
            self.color_display.config(bg=color)
            
    def change_thickness(self, value):
        self.current_thickness = int(value)
        
    def on_canvas_click(self, event):
        x, y = event.x, event.y
        
        if self.delete_mode:
            self.delete_object_at_position(x, y)
        elif self.window_mode:
            self.start_window(x, y)
        elif self.current_tool == "point":
            self.draw_point(x, y)
        else:
            self.start_x, self.start_y = x, y
            
    def on_canvas_drag(self, event):
        if self.window_mode and self.start_x is not None:
            self.update_window_preview(event.x, event.y)
        elif self.current_tool != "point" and self.start_x is not None:
            self.update_preview(event.x, event.y)
            
    def on_canvas_release(self, event):
        if self.window_mode:
            self.finish_window(event.x, event.y)
        elif self.current_tool != "point" and self.start_x is not None:
            self.finish_drawing(event.x, event.y)
            
    def draw_point(self, x, y):
        # Save state for undo
        self.save_state()
        
        obj_id = self.canvas.create_oval(x-2, y-2, x+2, y+2, 
                                        fill=self.current_color, 
                                        outline=self.current_color,
                                        width=self.current_thickness)
        obj_data = {
            'id': obj_id,
            'type': 'point',
            'coords': [x, y],
            'color': self.current_color,
            'thickness': self.current_thickness,
            'original_color': self.current_color
        }
        self.objects.append(obj_data)
        
    def update_preview(self, x, y):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
            
        if self.current_tool == "line":
            self.temp_line = self.canvas.create_line(self.start_x, self.start_y, x, y,
                                                    fill=self.current_color,
                                                    width=self.current_thickness)
        elif self.current_tool == "rectangle":
            self.temp_line = self.canvas.create_rectangle(self.start_x, self.start_y, x, y,
                                                         outline=self.current_color,
                                                         width=self.current_thickness,
                                                         fill="")
        elif self.current_tool == "ellipse":
            self.temp_line = self.canvas.create_oval(self.start_x, self.start_y, x, y,
                                                    outline=self.current_color,
                                                    width=self.current_thickness,
                                                    fill="")
            
    def finish_drawing(self, x, y):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
            
        # Save state for undo
        self.save_state()
            
        obj_id = None
        if self.current_tool == "line":
            obj_id = self.canvas.create_line(self.start_x, self.start_y, x, y,
                                            fill=self.current_color,
                                            width=self.current_thickness)
        elif self.current_tool == "rectangle":
            obj_id = self.canvas.create_rectangle(self.start_x, self.start_y, x, y,
                                                 outline=self.current_color,
                                                 width=self.current_thickness,
                                                 fill="")
        elif self.current_tool == "ellipse":
            obj_id = self.canvas.create_oval(self.start_x, self.start_y, x, y,
                                            outline=self.current_color,
                                            width=self.current_thickness,
                                            fill="")
        
        if obj_id:
            obj_data = {
                'id': obj_id,
                'type': self.current_tool,
                'coords': [self.start_x, self.start_y, x, y],
                'color': self.current_color,
                'thickness': self.current_thickness,
                'original_color': self.current_color
            }
            self.objects.append(obj_data)
            
        self.temp_line = None
        self.start_x = self.start_y = None
        
    def select_object_mode(self):
        messagebox.showinfo("Mode Pilih Objek", 
                           "Klik pada objek yang ingin ditransformasi")
        self.canvas.bind("<Button-1>", self.select_object)
        
    def select_object(self, event):
        # Find object at click position
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        
        # Find corresponding object in our list
        for obj in self.objects:
            if obj['id'] == clicked_item:
                self.selected_object = obj
                # Highlight selected object
                self.canvas.create_rectangle(self.canvas.bbox(clicked_item), 
                                           outline="red", width=2, dash=(5, 5))
                messagebox.showinfo("Objek Dipilih", 
                                  f"Objek {obj['type']} telah dipilih untuk transformasi")
                break
                
        # Restore normal canvas binding
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
    def translate_object(self):
        if not self.selected_object:
            messagebox.showwarning("Peringatan", "Pilih objek terlebih dahulu!")
            return
            
        try:
            dx = float(self.dx_entry.get() or 0)
            dy = float(self.dy_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai numerik yang valid!")
            return
            
        # Save state for undo
        self.save_state()
            
        # Clear highlight
        self.canvas.delete("all")
        self.redraw_all_objects()
        
        # Apply translation
        obj = self.selected_object
        if obj['type'] == 'point':
            obj['coords'][0] += dx
            obj['coords'][1] += dy
        else:
            for i in range(0, len(obj['coords']), 2):
                obj['coords'][i] += dx
                obj['coords'][i+1] += dy
                
        self.redraw_all_objects()
        self.selected_object = None
        
    def rotate_object(self):
        if not self.selected_object:
            messagebox.showwarning("Peringatan", "Pilih objek terlebih dahulu!")
            return
            
        try:
            angle = float(self.angle_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai numerik yang valid!")
            return
            
        # Save state for undo
        self.save_state()
            
        angle_rad = math.radians(angle)
        obj = self.selected_object
        
        # Calculate center point
        if obj['type'] == 'point':
            cx, cy = obj['coords'][0], obj['coords'][1]
        else:
            coords = obj['coords']
            cx = (coords[0] + coords[2]) / 2
            cy = (coords[1] + coords[3]) / 2
            
        # Clear highlight
        self.canvas.delete("all")
        self.redraw_all_objects()
        
        # Apply rotation around center
        if obj['type'] == 'point':
            # Points don't need rotation
            pass
        else:
            new_coords = []
            for i in range(0, len(obj['coords']), 2):
                x, y = obj['coords'][i], obj['coords'][i+1]
                # Translate to origin
                x -= cx
                y -= cy
                # Rotate
                new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
                new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
                # Translate back
                new_x += cx
                new_y += cy
                new_coords.extend([new_x, new_y])
            obj['coords'] = new_coords
            
        self.redraw_all_objects()
        self.selected_object = None
        
    def scale_object(self):
        if not self.selected_object:
            messagebox.showwarning("Peringatan", "Pilih objek terlebih dahulu!")
            return
            
        try:
            sx = float(self.sx_entry.get() or 1)
            sy = float(self.sy_entry.get() or 1)
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai numerik yang valid!")
            return
            
        # Save state for undo
        self.save_state()
            
        obj = self.selected_object
        
        # Calculate center point
        if obj['type'] == 'point':
            cx, cy = obj['coords'][0], obj['coords'][1]
        else:
            coords = obj['coords']
            cx = (coords[0] + coords[2]) / 2
            cy = (coords[1] + coords[3]) / 2
            
        # Clear highlight
        self.canvas.delete("all")
        self.redraw_all_objects()
        
        # Apply scaling around center
        if obj['type'] == 'point':
            # Points don't need scaling
            pass
        else:
            new_coords = []
            for i in range(0, len(obj['coords']), 2):
                x, y = obj['coords'][i], obj['coords'][i+1]
                # Scale relative to center
                new_x = cx + (x - cx) * sx
                new_y = cy + (y - cy) * sy
                new_coords.extend([new_x, new_y])
            obj['coords'] = new_coords
            
        self.redraw_all_objects()
        self.selected_object = None
        
    def toggle_window_mode(self):
        self.window_mode = not self.window_mode
        if self.window_mode:
            messagebox.showinfo("Mode Windowing", 
                               "Drag mouse untuk membuat window")
        else:
            messagebox.showinfo("Mode Normal", 
                               "Kembali ke mode menggambar normal")
            
    def start_window(self, x, y):
        self.start_x, self.start_y = x, y
        
    def update_window_preview(self, x, y):
        if hasattr(self, 'window_preview'):
            self.canvas.delete(self.window_preview)
        self.window_preview = self.canvas.create_rectangle(
            self.start_x, self.start_y, x, y,
            outline="blue", width=2, dash=(3, 3))
            
    def finish_window(self, x, y):
        if hasattr(self, 'window_preview'):
            self.canvas.delete(self.window_preview)
            
        # Store window coordinates
        self.window_coords = [min(self.start_x, x), min(self.start_y, y),
                             max(self.start_x, x), max(self.start_y, y)]
        
        # Draw permanent window
        self.canvas.create_rectangle(self.window_coords[0], self.window_coords[1],
                                   self.window_coords[2], self.window_coords[3],
                                   outline="blue", width=3)
        
        # Check which objects are inside window and change their color
        self.windowed_objects = []
        for obj in self.objects:
            if self.is_object_in_window(obj):
                self.windowed_objects.append(obj)
                # Change color to indicate windowing
                if obj['type'] == 'point':
                    self.canvas.itemconfig(obj['id'], fill="red", outline="red")
                else:
                    self.canvas.itemconfig(obj['id'], outline="red")
                    
        self.window_mode = False
        messagebox.showinfo("Windowing Selesai", 
                           f"{len(self.windowed_objects)} objek terkena windowing")
        
    def is_object_in_window(self, obj):
        if not self.window_coords:
            return False
            
        wx1, wy1, wx2, wy2 = self.window_coords
        
        if obj['type'] == 'point':
            x, y = obj['coords']
            return wx1 <= x <= wx2 and wy1 <= y <= wy2
        else:
            coords = obj['coords']
            # Check if any part of the object is inside the window
            for i in range(0, len(coords), 2):
                x, y = coords[i], coords[i+1]
                if wx1 <= x <= wx2 and wy1 <= y <= wy2:
                    return True
            return False
            
    def clip_windowed_objects(self):
        if not self.window_coords or not self.windowed_objects:
            messagebox.showwarning("Peringatan", 
                                 "Buat window dan pilih objek terlebih dahulu!")
            return
            
        # Remove objects that are outside the window
        objects_to_remove = []
        for obj in self.windowed_objects:
            if not self.is_object_fully_in_window(obj):
                objects_to_remove.append(obj)
                self.canvas.delete(obj['id'])
                
        # Remove from objects list
        for obj in objects_to_remove:
            if obj in self.objects:
                self.objects.remove(obj)
            if obj in self.windowed_objects:
                self.windowed_objects.remove(obj)
                
        messagebox.showinfo("Clipping Selesai", 
                           f"{len(objects_to_remove)} objek di-clip")
        
    def is_object_fully_in_window(self, obj):
        if not self.window_coords:
            return False
            
        wx1, wy1, wx2, wy2 = self.window_coords
        
        if obj['type'] == 'point':
            x, y = obj['coords']
            return wx1 <= x <= wx2 and wy1 <= y <= wy2
        else:
            coords = obj['coords']
            # Check if all points of the object are inside the window
            for i in range(0, len(coords), 2):
                x, y = coords[i], coords[i+1]
                if not (wx1 <= x <= wx2 and wy1 <= y <= wy2):
                    return False
            return True
            
    def reset_windowing(self):
        # Remove window rectangle
        self.canvas.delete("all")
        
        # Reset object colors
        for obj in self.windowed_objects:
            if obj['type'] == 'point':
                self.canvas.itemconfig(obj['id'], fill=obj['original_color'], 
                                     outline=obj['original_color'])
            else:
                self.canvas.itemconfig(obj['id'], outline=obj['original_color'])
                
        self.window_coords = None
        self.windowed_objects = []
        self.redraw_all_objects()
        
    def redraw_all_objects(self):
        self.canvas.delete("all")
        
        for obj in self.objects:
            if obj['type'] == 'point':
                x, y = obj['coords']
                obj['id'] = self.canvas.create_oval(x-2, y-2, x+2, y+2,
                                                   fill=obj['color'],
                                                   outline=obj['color'],
                                                   width=obj['thickness'])
            elif obj['type'] == 'line':
                obj['id'] = self.canvas.create_line(obj['coords'],
                                                   fill=obj['color'],
                                                   width=obj['thickness'])
            elif obj['type'] == 'rectangle':
                obj['id'] = self.canvas.create_rectangle(obj['coords'],
                                                        outline=obj['color'],
                                                        width=obj['thickness'],
                                                        fill="")
            elif obj['type'] == 'ellipse':
                obj['id'] = self.canvas.create_oval(obj['coords'],
                                                   outline=obj['color'],
                                                   width=obj['thickness'],
                                                   fill="")
        
        # Redraw window if exists
        if self.window_coords:
            self.canvas.create_rectangle(self.window_coords[0], self.window_coords[1],
                                       self.window_coords[2], self.window_coords[3],
                                       outline="blue", width=3)
        
    def clear_canvas(self):
        # Save state for undo
        self.save_state()
        
        self.canvas.delete("all")
        self.objects = []
        self.windowed_objects = []
        self.window_coords = None
        self.selected_object = None
        
    def show_objects_info(self):
        info = f"Total objek: {len(self.objects)}\n"
        info += f"Objek dalam window: {len(self.windowed_objects)}\n\n"
        
        for i, obj in enumerate(self.objects):
            info += f"Objek {i+1}: {obj['type']}\n"
            info += f"  Koordinat: {obj['coords']}\n"
            info += f"  Warna: {obj['color']}\n"
            info += f"  Ketebalan: {obj['thickness']}\n\n"
            
        messagebox.showinfo("Informasi Objek", info)

    def save_state(self):
        """Save current state for undo functionality"""
        state = {
            'objects': [obj.copy() for obj in self.objects],
            'windowed_objects': [obj.copy() for obj in self.windowed_objects],
            'window_coords': self.window_coords.copy() if self.window_coords else None
        }
        self.history.append(state)
        
        # Limit history to last 10 actions to save memory
        if len(self.history) > 10:
            self.history.pop(0)
    
    def undo_last_action(self):
        """Undo the last action"""
        if not self.history:
            messagebox.showinfo("Undo", "Tidak ada aksi yang bisa di-undo!")
            return
            
        # Restore previous state
        previous_state = self.history.pop()
        self.objects = previous_state['objects']
        self.windowed_objects = previous_state['windowed_objects']
        self.window_coords = previous_state['window_coords']
        
        # Redraw everything
        self.redraw_all_objects()
        messagebox.showinfo("Undo", "Aksi terakhir telah di-undo!")
    
    def toggle_delete_mode(self):
        """Toggle delete mode on/off"""
        self.delete_mode = not self.delete_mode
        if self.delete_mode:
            messagebox.showinfo("Mode Hapus", 
                               "Mode hapus aktif! Klik objek untuk menghapusnya.\n" +
                               "Klik 'Mode Hapus Objek' lagi untuk keluar dari mode ini.")
            # Change cursor to indicate delete mode
            self.canvas.config(cursor="X_cursor")
        else:
            messagebox.showinfo("Mode Normal", "Kembali ke mode normal")
            self.canvas.config(cursor="")
    
    def delete_object_at_position(self, x, y):
        """Delete object at the clicked position"""
        # Find object at click position
        clicked_item = self.canvas.find_closest(x, y)[0]
        
        # Find corresponding object in our list
        object_to_delete = None
        for obj in self.objects:
            if obj['id'] == clicked_item:
                object_to_delete = obj
                break
        
        if object_to_delete:
            # Save state for undo
            self.save_state()
            
            # Remove from canvas
            self.canvas.delete(object_to_delete['id'])
            
            # Remove from objects list
            self.objects.remove(object_to_delete)
            
            # Remove from windowed objects if it's there
            if object_to_delete in self.windowed_objects:
                self.windowed_objects.remove(object_to_delete)
            
            messagebox.showinfo("Objek Dihapus", 
                               f"Objek {object_to_delete['type']} telah dihapus!")
        else:
            messagebox.showwarning("Tidak Ada Objek", 
                                 "Tidak ada objek di posisi yang diklik!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsApp(root)
    root.mainloop()