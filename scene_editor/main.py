import json

class SceneEditor:
    def __init__(self):
        self.data = {
            "settings": {
                "speakerAlign": "left",
                "textAlign": "left",
                "textPos.x": 0.11,
                "textPos.y": 0.94,
                "speakerPos.x": 0.10,
                "speakerPos.y": 0.91,
                "screenMult": 1,
                "showBox": 1,
                "fontPath": "assets/arial.ttf",
                "fontSize": 21
            },
            "scenes": {}
        }

    def add_scene(self, scene_name, background):
        self.data["scenes"][scene_name] = {
            "background": background,
            "characters": {},
            "dialogue": []
        }

    def add_character(self, scene_name, name, image, position_x, position_y):
        if scene_name not in self.data["scenes"]:
            return
        
        self.data["scenes"][scene_name]["characters"][name] = {
            "image": image,
            "position": [position_x, position_y],
        }

    def add_dialogue(self, scene_name, speaker, text):
        if scene_name not in self.data["scenes"]:
            return
        
        self.data["scenes"][scene_name]["dialogue"].append({
            "speaker": speaker,
            "text": text
        })

    def save_to_file(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.data, outfile, indent=2)

from tkinter import *

class SceneEditorGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("VNCore Scene Editor")

        self.scene_editor = SceneEditor()
        
        self.scene_name = StringVar()
        self.background_image = StringVar()
        self.character_name = StringVar()
        self.character_image = StringVar()
        self.character_position_x = IntVar()
        self.character_position_y = IntVar()
        self.dialogue_speaker = StringVar()
        self.dialogue_text = StringVar()
        
        Label(self.root, text="Scene Name").grid(row=0, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.scene_name).grid(row=0, column=1, padx=10, pady=10) 
        
        Label(self.root, text="Background Image").grid(row=1, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.background_image).grid(row=1, column=1, padx=10, pady=10) 
        
        Label(self.root, text="Character Name").grid(row=2, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.character_name).grid(row=2, column=1, padx=10, pady=10) 
        
        Label(self.root, text="Character Image").grid(row=3, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.character_image).grid(row=3, column=1, padx=10, pady=10) 
        
        Label(self.root, text="Character Position (X)").grid(row=4, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.character_position_x).grid(row=4, column=1, padx=10, pady=10) 
        
        Label(self.root, text="Character Position (Y)").grid(row=5, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.character_position_y).grid(row=5, column=1, padx=10, pady=10) 
        
        Label(self.root, text="Dialogue Speaker").grid(row=6, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.dialogue_speaker).grid(row=6, column=1, padx=10, pady=10) 
        
        Label(self.root, text="Dialogue Text").grid(row=7, column=0, padx=10, pady=10) 
        Entry(self.root, textvariable=self.dialogue_text).grid(row=7, column=1, padx=10, pady=10) 
        
        save_scene_btn = Button(self.root, text="Add Scene", command=self.add_scene) 
        save_scene_btn.grid(row=8, column=0, pady=10)
        
        add_character_btn = Button(self.root, text="Add Character", command=self.add_character) 
        add_character_btn.grid(row=8, column=1, pady=10)
        
        add_dialogue_btn = Button(self.root, text="Add Dialogue", command=self.add_dialogue) 
        add_dialogue_btn.grid(row=9, column=0, pady=10)
         
        self.root.mainloop()

    def add_scene(self):
        self.scene_editor.add_scene(self.scene_name.get(), self.background_image.get())
        self.save_scene()

    def add_character(self):
        self.scene_editor.add_character(self.scene_name.get(), self.character_name.get(), self.character_image.get(), self.character_position_x.get(), self.character_position_y.get())
        self.save_scene()

    def add_dialogue(self):
        self.scene_editor.add_dialogue(self.scene_name.get(), self.dialogue_speaker.get(), self.dialogue_text.get())
        self.save_scene()
    
    def save_scene(self):
        self.scene_editor.save_to_file("output.json")

editor = SceneEditorGUI()