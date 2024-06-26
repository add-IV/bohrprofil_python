from dataclasses import dataclass

@dataclass
class Layer:
    end_depth: float
    texture: str
    description: str

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

    @staticmethod
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
    
    @staticmethod
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