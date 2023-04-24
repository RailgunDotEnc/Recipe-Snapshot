import tkinter
import tkinter.messagebox
import customtkinter
import Food_Detection_Pretrained_Model as model
import time
import threading
from PIL import Image, ImageTk
import sys
sys.path.insert(0,'Recipe_Bot/')
import Recipe_AI

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.count=0
        self.clock=0
        # configure window
        self.title("Visual Presentation")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Recipe SnapShot", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Reset", command=self.text_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text="Test all", command=self.scanimage)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text="Test ", command=self.set_recipes)
        #self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%","130%", "140%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Food test")
        self.entry.grid(row=3, column=2,rowspan=10, columnspan=10, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Enter", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("end", f">Text Updates\n")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Ingredient 1")
        self.tabview.add("Ingredient 2")
        self.tabview.add("Ingredient 3")
        self.tabview.add("Ingredient 4")
        self.tabview.add("Ingredient 5")
        self.tabview.add("Ingredient 6")
        self.tabview.tab("Ingredient 1").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Ingredient 2").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Ingredient 3").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Ingredient 4").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Ingredient 5").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Ingredient 6").grid_columnconfigure(0, weight=1)

        #self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
        #                                                values=["Value 1", "Value 2", "Value Long Long Long"])
        #self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        #self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
        #                                            values=["Value 1", "Value 2", "Value Long....."])
        #self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        #self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                   command=self.open_input_dialog_event)
        #self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_1 = customtkinter.CTkLabel(self.tabview.tab("Ingredient 1"), text="No ingredient 1")
        self.label_tab_1.grid(row=0, column=0, padx=20, pady=20)
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Ingredient 2"), text="No ingredient 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
        self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("Ingredient 3"), text="No ingredient 3")
        self.label_tab_3.grid(row=0, column=0, padx=20, pady=20)
        self.label_tab_4 = customtkinter.CTkLabel(self.tabview.tab("Ingredient 4"), text="No ingredient 4")
        self.label_tab_4.grid(row=0, column=0, padx=20, pady=20)
        self.label_tab_5 = customtkinter.CTkLabel(self.tabview.tab("Ingredient 5"), text="No ingredient 5")
        self.label_tab_5.grid(row=0, column=0, padx=20, pady=20)
        self.label_tab_6 = customtkinter.CTkLabel(self.tabview.tab("Ingredient 6"), text="No ingredient 6")
        self.label_tab_6.grid(row=0, column=0, padx=20, pady=20)
        

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Image testing:")
        self.label_radio_group.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="")
        #self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="00:00",font=customtkinter.CTkFont(size=40, weight="bold"))
        #self.label_radio_group.grid(row=2, column=5, columnspan=1, padx=10, pady=10, sticky="nsew")
        #self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        #self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        #self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        #self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        #self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        #self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        #self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        #self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        #self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        #self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        #self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        #self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        #self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Recipes")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        #for i in range(100):
        #    switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
        #    switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        #    self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        #self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        #self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        #self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        #self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        #self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        #self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        #self.checkbox_3.configure(state="disabled")
        #self.checkbox_1.select()
        #self.scrollable_frame_switches[0].select()
        #self.scrollable_frame_switches[4].select()
        #self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        #self.optionmenu_1.set("CTkOptionmenu")
        #self.combobox_1.set("CTkComboBox")
        #self.slider_1.configure(command=self.progressbar_2.set)
        #self.slider_2.configure(command=self.progressbar_3.set)
        #self.progressbar_1.configure(mode="indeterminnate")
        #self.progressbar_1.start()
        self.textbox.insert("0.0", "")
        #self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        #self.seg_button_1.set("Value 2")


    def scanimage(self,img=r"ingredients_imgs/bread.jpg"):
        button_image = customtkinter.CTkImage(Image.open(img), size=(156, 156))
        image_button = customtkinter.CTkButton(master=self.radiobutton_frame,text="",image=button_image)
        image_button.grid(row=1, column=1, columnspan=4, pady=10, padx=20, sticky="")
        t1 = threading.Thread(target=model.scanimage, args=(self,img))
        self.text_event("Scanning image")
        t1.start()
    
    def set_recipes(self,food=[
        ["Breakfast Burrito",["Tortillas", "eggs", "cheese", "salsa", "vegetables"],[],"https://example.com/breakfast-burrito" ]
        ,["Huevos Rancheros",["Tortillas", "eggs", "tomato sauce", "beans", "cheese"],[],"https://example.com/huevos-rancheros"]]):
        self.text_event(f"Found {len(food)} Recipes")
        img_size=106
        j=0
        
        
        
        for i in range(len(food)):
            img=customtkinter.CTkImage(Image.open(f"recipies_imgs\\{food[i][0]}.jpg"), size=(img_size, img_size))
            food_img = customtkinter.CTkButton(master=self.scrollable_frame,text="",image=img)
            food_img.grid(row=j, column=0, padx=20, pady=20)
            ingredients=""
            condiments=""
            
            for k in range(len(food[i][1])):
                ingredients=ingredients+ f"{food[i][1][k]}, "
            for k in range(len(food[i][2])):
                condiments=condiments+ f"{food[i][1][k]}, "
            j=j+1
            label = customtkinter.CTkLabel(master=self.scrollable_frame, text=f">{food[i][0]}")
            label.grid(row=j, column=0, padx=20)
            j=j+1
            label1 = customtkinter.CTkLabel(master=self.scrollable_frame, text=f"Ingredients: {ingredients}")
            label1.grid(row=j, column=0, padx=20)
            j=j+1
            label2 = customtkinter.CTkLabel(master=self.scrollable_frame, text=f"Condiments: {condiments}")
            label2.grid(row=j, column=0, padx=20)
            j=j+1
            label3 = customtkinter.CTkLabel(master=self.scrollable_frame, text=f"Website: {food[i][3]}")
            label3.grid(row=j, column=0, padx=20)
            j=j+1
            

    def set_ingredients(self,ingredient_list):
        img_size=106
        dict_img={"bread":customtkinter.CTkImage(Image.open(r"ingredients_imgs\bread.jpg"), size=(img_size, img_size)),
        "eggs":customtkinter.CTkImage(Image.open(r"ingredients_imgs\egg.jpg"), size=(img_size, img_size)),
        "beans":customtkinter.CTkImage(Image.open(r"ingredients_imgs\frijoles.jpg"), size=(img_size, img_size)),
        "milk":customtkinter.CTkImage(Image.open(r"ingredients_imgs\milk.png"), size=(img_size, img_size)),
        "rice":customtkinter.CTkImage(Image.open(r"ingredients_imgs\rice.jpg"), size=(img_size, img_size)),
        "tortillas":customtkinter.CTkImage(Image.open(r"ingredients_imgs\tortilla.jpg"), size=(img_size, img_size))                  
                  }
        
        for i in range(len(ingredient_list)):
            if i==0:
                self.label_tab_1.configure(text = ingredient_list[i])
                food_img1 = customtkinter.CTkButton(master=self.label_tab_1,text="",image=dict_img[ingredient_list[i]])
                food_img1.grid(row=1, column=0, padx=20, pady=20)
            if i==1:
                self.label_tab_2.configure(text = ingredient_list[i])
                food_img2 = customtkinter.CTkButton(master=self.label_tab_2,text="",image=dict_img[ingredient_list[i]])
                food_img2.grid(row=1, column=0, padx=20, pady=20)
            if i==2:
                self.label_tab_3.configure(text = ingredient_list[i])
                food_img3 = customtkinter.CTkButton(master=self.label_tab_3,text="",image=dict_img[ingredient_list[i]])
                food_img3.grid(row=1, column=0, padx=20, pady=20)
            if i==3:
                self.label_tab_4.configure(text = ingredient_list[i])
                label_tab_4 = customtkinter.CTkButton(master=self.label_tab_4,text="",image=dict_img[ingredient_list[i]])
                label_tab_4.grid(row=1, column=0, padx=20, pady=20)
            if i==4:
                self.label_tab_5.configure(text = ingredient_list[i])
                label_tab_5 = customtkinter.CTkButton(master=self.label_tab_5,text="",image=dict_img[ingredient_list[i]])
                label_tab_5.grid(row=1, column=0, padx=20, pady=20)
            if i==5:
                self.label_tab_6.configure(text = ingredient_list[i])
                label_tab_6 = customtkinter.CTkButton(master=self.label_tab_6,text="",image=dict_img[ingredient_list[i]])
                label_tab_6.grid(row=1, column=0, padx=20, pady=20)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def text_event(self,text=""):
        self.textbox.insert("end", f">{text} \n")
        self.count=self.count+1
        time.sleep(.5)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()