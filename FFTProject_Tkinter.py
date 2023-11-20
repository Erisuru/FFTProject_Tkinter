import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
from tkinter import Toplevel

from matplotlib.image import imread
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import os

from PIL import Image
import io

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    class popup_done(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.title("Promt")
            self.geometry("150x100")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # ============ create_frames ============
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.frame = customtkinter.CTkFrame(master=self)
            self.frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

            self.label_promt = customtkinter.CTkLabel(master=self.frame,text="DONE")
            self.label_promt.grid(row=0, column=1, columnspan=2, pady=10, padx=5, sticky="")

        def on_closing(self, event=0):
            self.destroy()
            
    class popup_failed(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.title("Promt")
            self.geometry("150x100")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)

            # ============ create_frames ============
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.frame = customtkinter.CTkFrame(master=self)
            self.frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

            self.label_promt = customtkinter.CTkLabel(master=self.frame,text="FAILED")
            self.label_promt.grid(row=0, column=1, columnspan=1, pady=5, padx=5, sticky="")

        def on_closing(self, event=0):
            self.destroy()
    
    
    def __init__(self):
        super().__init__()

        self.title("FFT Demo")
        #self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ============ create_frames ============
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_main ===============
        self.label_info = customtkinter.CTkLabel(master=self.frame, text="Phần mềm demo Fast Fourier Transform vào nén ảnh")

        self.label_info.grid(row=0, column = 0, columnspan=6, pady=5, padx=5, sticky="")

        self.label_addimg = customtkinter.CTkLabel(master=self.frame,text="Add Image")

        self.label_addimg.grid(row=1, column = 0, columnspan=2, pady=15, padx=5, sticky="")
        
        self.label_addimg_info = customtkinter.CTkLabel(master=self.frame, text="Src",
                                                      height=15,
                                                      corner_radius=6,
                                                      fg_color=("white", "gray38"),
                                                      justify=tkinter.LEFT)
        
        self.label_addimg_info.grid(column=2, row=1, sticky="", padx=10, pady=15, columnspan=2)

        self.button_addimg_path = customtkinter.CTkButton(master=self.frame,
                                                        text="Add",
                                                        command=self.button_event_addimg_path)

        self.button_addimg_path.grid(column=4, row=1, padx=10, pady=10, columnspan=2)

        self.button_save= customtkinter.CTkButton(master=self.frame,
                                                        text="Save",
                                                        command=self.button_save_addimg)
        self.button_save.grid(column=0, row=3, padx=10, pady=10, columnspan=6)

        

    def update_image(self, image, title):
        plt.title(title)
        plt.imshow(image, cmap='gray')
        fig = plt.gcf()
        img = self.fig2img(fig)
        
        self.image = customtkinter.CTkImage(light_image=img, size=img.size)

        self.image_label = customtkinter.CTkLabel(master=self.frame, image=self.image, text="")

        self.image_label.grid(column=3, row=2, sticky="", padx=10, pady=15, columnspan=3)

        #WIDTH = App.WIDTH + img.size[0] + 100
        #HEIGHT = App.HEIGHT + img.size[1] 
        #self.geometry(f"{WIDTH}x{HEIGHT}")
        #self.update()


    def slider_event(self, value):
        if value != 0:
            keep = value / (10000 / (value * 100)) / 100
            print(keep)

            title = ('Compressed Image: Keep = ' + str(keep * 100) +'%')
            gray_scaled_transform = np.fft.fft2(self.gray_scaled)
            gray_scaled_transform_sort = np.sort(np.abs(gray_scaled_transform.reshape(-1)))
        
            thresh = gray_scaled_transform_sort[int(np.floor((1 - keep) * len(gray_scaled_transform_sort)))]
            index = np.abs(gray_scaled_transform) > thresh
            
            gray_scaled_transform_low = gray_scaled_transform * index
            self.src_img_low = np.fft.ifft2(gray_scaled_transform_low).real
            self.update_image(self.src_img_low, title)
              

    def button_event_addimg_path(self):
        global filename
        filename = filedialog.askopenfilename(initialdir="/",title="Chon file hinh anh",
                                                   filetypes=(("All supported files","*.bmp;*.dib;*.jpeg;*.jpg;*.jpe;*.jp2;*.png;*.webp;*.pbm;*.pgm;*.ppm;*.pxm;*.pnm;*.tiff;*.tif;*.exr;*.hdr;*.pic"),
                                                              ("All files","*.*")) )
        self.label_addimg_info = customtkinter.CTkLabel(master=self.frame, text=filename,
                                                      height=15,
                                                      corner_radius=6,
                                                      fg_color=("white", "gray38"),
                                                      justify=tkinter.LEFT)
        
        self.label_addimg_info.grid(column=2, row=1, sticky="", padx=10, pady=15, columnspan=2)

        self.src_img = imread(filename)
        self.gray_scaled = np.mean(self.src_img, -1)
        self.src_img_low = self.gray_scaled
        
        plt.title('Original gray-scaled image')
        plt.imshow(self.gray_scaled, cmap='gray')
        fig = plt.gcf()
        src_img = self.fig2img(fig)


        self.image_src = customtkinter.CTkImage(light_image= src_img , size=src_img.size)
        self.image_src_label = customtkinter.CTkLabel(master=self.frame, image=self.image_src, text="")
        self.image_src_label.grid(column=0, row=2, sticky="", padx=10, pady=15, columnspan=3)
        self.update_image(self.gray_scaled, "")

        self.slider_label = customtkinter.CTkLabel(master=self.frame, text="Kéo slider để thay đổi mức độ compression")
        self.slider_label.grid(column=0, row=4, padx=10, pady=15, columnspan=6)

        self.slider = customtkinter.CTkSlider(master=self.frame, from_=1, to=100, command=self.slider_event) #command=slider_event)
        self.slider.set(100)

        self.slider.grid(column=0, row=5, padx=10, pady=15, columnspan=6)


    def fig2img(self, fig):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        import io
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        return img

    def fig2imgsave(self, fig):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        import io
        buf = io.BytesIO()
        plt.axis('off')
        plt.title('')
        fig.savefig(buf, bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        img = Image.open(buf)
        plt.axis('on')
        return img
    
    
    def button_save_addimg(self):
        try:
            plt.imshow(self.src_img_low, cmap='gray')
            fig = plt.gcf()
            img = self.fig2imgsave(fig)
            img = img.convert('RGB')

            types = [("Jpg Files", "*.jpg"),
                        ("All Files", "*.*")]

            savename = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=types)
            if not savename:
                return

            img.save(savename)

            pop = self.popup_done()
            pop.mainloop()

        except:
            print('Failed')
            pop = self.popup_failed()
            pop.mainloop()
            

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
    
