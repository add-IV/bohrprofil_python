from dataclasses import dataclass

@dataclass
class Layer:
    end_depth: float
    texture: str
    description: str

import json

@dataclass
class Bohrprofil:
    title: str
    height: float
    max_depth: float
    layers: list[Layer]

    def sort_layers(self):
        self.layers.sort(key=lambda x: x.end_depth)
    
    def update_max_depth(self):
        self.max_depth = self.layers[-1].end_depth

    def marshal(self):
        return {
            "title": self.title,
            "height": self.height,
            "max_depth": self.max_depth,
            "layers": [
                {
                    "end_depth": layer.end_depth,
                    "texture": layer.texture,
                    "description": layer.description,
                }
                for layer in self.layers
            ],
        }
    
    def unmarshal(data):
        return Bohrprofil(
            data["title"],
            data["height"],
            data["max_depth"],
            [
                Layer(
                    layer["end_depth"],
                    layer["texture"],
                    layer["description"],
                )
                for layer in data["layers"]
            ],
        )
    
    def save(self, filename):
        with open(filename, "w") as f:
            f.write(json.dumps(self.marshal()))

    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            data = json.loads(f.read())
        return Bohrprofil.unmarshal(data)