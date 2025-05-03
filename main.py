# Martin Gerardo Tanori Sitten 
# 1 de mayo de 2025

# Dependencias
from abc import ABC, abstractmethod
from types import NotImplementedType

# =========================================================================================
# Creacional
# Builder
# =========================================================================================
class Pants:
    def __init__(self, fabric=None, fit=None, length=None):
        self.fabric = fabric
        self.fit = fit
        self.length = length

    def __str__(self):
        return f"Pants with {self.fabric} fabric, {self.fit} fit, and {self.length} length."


class PantsBuilder:
    def __init__(self):
        self.fabric = None
        self.fit = None
        self.length = None

    def set_fabric(self, fabric):
        self.fabric = fabric
        return self

    def set_fit(self, fit):
        self.fit = fit
        return self

    def set_length(self, length):
        self.length = length
        return self

    def build(self):
        return Pants(self.fabric, self.fit, self.length)
    
builder = PantsBuilder()
class PantsDirector:
    def __init__(self, builder):
        self._builder = builder

    def make_redPants(self):
        return self._builder.set_fabric("corduroy").set_fit("relaxed").set_length("regular").build()

    def make_bluePants(self):
        return self._builder.set_fabric("denim").set_fit("skinny").set_length("cropped").build()
    
    def make_whitePants(self):
        return self._builder.set_fabric("linen").set_fit("relaxed").set_length("ankle").build()
    
    def make_pinkPants(self):
        return self._builder.set_fabric("corduroy").set_fit("straight").set_length("cropped").build()

builder = PantsBuilder()
director = PantsDirector(builder)


# =========================================================================================
# Estructural 
# Composite
# =========================================================================================
class CatalogComponent(ABC):
    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def display(self, indent: str = "") -> None:
        pass

class CatalogItem(CatalogComponent):
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def get_price(self) -> float:
        return self.price

    def display(self, indent: str = "") -> None:
        print(f"{indent}- ${self.price:.2f} | {self.name}, ({self.description})")

class CatalogSection(CatalogComponent):
    def __init__(self, name: str):
        self.name = name
        self.components: list[CatalogComponent] = []

    def add(self, component: CatalogComponent) -> None:
        self.components.append(component)

    def remove(self, component: CatalogComponent) -> None:
        self.components.remove(component)

    def get_price(self) -> float:
        return sum(component.get_price() for component in self.components)
    
    def display(self, indent: str = "") -> None:
        print(f"{indent}+ {self.name} (${self.get_price():.2f})")
        for component in self.components:
            component.display(indent + "  ")


# Crear los elementos
redPants = CatalogItem("Fashionable Red Pants", director.make_redPants(), 6.50)
bluePants = CatalogItem("Cute Vintage Jeans", director.make_bluePants(), 8.00)
pinkPants = CatalogItem("Hot Pink Pants", director.make_pinkPants(), 29.99)
whitePants = CatalogItem("Futuristic White Pants", director.make_whitePants(), 12.50)

# Crear las secciones
pants = CatalogSection("Pants")
pants.add(redPants)
pants.add(bluePants)
pants.add(pinkPants)
pants.add(whitePants)
main_catalog = CatalogSection("Closet")
main_catalog.add(pants)

# Mostrar todo el catálogo
main_catalog.display()



# =========================================================================================
# Comportamiento
# State
# =========================================================================================
