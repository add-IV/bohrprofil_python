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