# Martin Gerardo Tanori Sitten 
# 1 de mayo de 2025

# Dependencias
from abc import ABC, abstractmethod


from abc import ABC, abstractmethod

class Garment(ABC):
    def __init__(self, fabric=None, fit=None, length=None):
        self.fabric = fabric
        self.fit = fit
        self.length = length

    @abstractmethod
    def accept(self, visitor):
        pass

class Pants(Garment):
    def __init__(self, fabric=None, fit=None, length=None, waist=None):
        super().__init__(fabric, fit, length)
        self.waist = waist

    def __str__(self):
        return f"Pants with {self.fabric} fabric, {self.fit} fit, and {self.length} length."

    def accept(self, visitor):
        return visitor.visit_pants(self)

class Shirt(Garment):
    def __init__(self, fabric=None, fit=None, length=None, chest=None):
        super().__init__(fabric, fit, length)
        self.chest = chest

    def __str__(self):
        return f"Shirt with {self.fabric} fabric, {self.fit} fit, and {self.length} length."

    def accept(self, visitor):
        return visitor.visit_shirt(self)


# =========================================================================================
# Visitor
# =========================================================================================
class GarmentVisitor(ABC):
    @abstractmethod
    def visit_pants(self, pants):
        pass

    @abstractmethod
    def visit_shirt(self, shirt):
        pass

class SizeCalculator(GarmentVisitor):
    def visit_pants(self, pants):
        if(pants.waist < 28):
            return "S"
        elif(pants.waist < 30):
            return "M"
        elif(pants.waist < 33):
            return "L"
        elif(pants.waist < 36):
            return "XL"
        else:
            return "XXL"
        

    def visit_shirt(self, shirt):
        if shirt.chest < 33:
            return "S"
        elif shirt.chest < 36:
            return "M"
        elif shirt.chest < 40:
            return "L"
        elif shirt.chest < 44:
            return "XL"
        else:
            return "XXL"

   
# =========================================================================================
# Builder
# =========================================================================================
class PantsBuilder:
    def __init__(self):
        self.fabric = None
        self.fit = None
        self.length = None
        self.waist = None

    def set_fabric(self, fabric):
        self.fabric = fabric
        return self

    def set_fit(self, fit):
        self.fit = fit
        return self

    def set_length(self, length):
        self.length = length
        return self
    
    def set_waist(self, waist):
        self.waist = waist
        return self

    def build(self):
        return Pants(self.fabric, self.fit, self.length, self.waist)
    
builder = PantsBuilder()
class PantsDirector:
    def __init__(self, builder):
        self._builder = builder

    def make_redPants(self):
        return self._builder.set_fabric("corduroy").set_fit("relaxed").set_length("regular").set_waist(32).build()

    def make_bluePants(self):
        return self._builder.set_fabric("denim").set_fit("skinny").set_length("cropped").set_waist(35).build()
    
    def make_whitePants(self):
        return self._builder.set_fabric("linen").set_fit("relaxed").set_length("ankle").set_waist(27).build()
    
    def make_pinkPants(self):
        return self._builder.set_fabric("corduroy").set_fit("straight").set_length("cropped").set_waist(28).build()

class ShirtBuilder:
    def __init__(self):
        self.fabric = None
        self.fit = None
        self.length = None
        self.chest = None

    def set_fabric(self, fabric):
        self.fabric = fabric
        return self

    def set_fit(self, fit):
        self.fit = fit
        return self

    def set_length(self, length):
        self.length = length
        return self
    
    def set_chest(self, chest):
        self.chest = chest
        return self

    def build(self):
        return Shirt(self.fabric, self.fit, self.length, self.chest)
    
builder = ShirtBuilder()
class ShirtDirector:
    def __init__(self, builder):
        self._builder = builder

    def make_longSleeveShirt(self):
        return self._builder.set_fabric("flannel").set_fit("slim").set_length("regular").set_chest(32).build()

    def make_poloShirt(self):
        return self._builder.set_fabric("cotton").set_fit("skinny").set_length("cropped").set_chest(30).build()
    
    def make_crewNeckShirt(self):
        return self._builder.set_fabric("cotton").set_fit("regular").set_length("muscle").set_chest(37).build()
    
    def make_VNeckShirt(self):
        return self._builder.set_fabric("linen").set_fit("skinny").set_length("muscle").set_chest(44).build()


# ========================================================================================= 
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
    def __init__(self, name: str, garment: Garment, price: float):
        self.name = name
        self.garment = garment
        self.price = price

    def get_price(self) -> float:
        return self.price

    def display(self, indent: str = "") -> None:
        size = self.garment.accept(SizeCalculator())
        description = str(self.garment)
        print(f"{indent}- $ {self.price:5.2f} | {self.name} (Size: {size})\n{indent}{indent}{indent}{indent}{indent}{description}")

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
        print(f"\n{indent}+ {self.name} (${self.get_price():.2f})")
        for component in self.components:
            component.display(indent + "  ")


# =========================================================================================
# Decorator
# =========================================================================================
class GarmentDecorator(Garment):
    def __init__(self, garment: Garment):
        self._garment = garment

    def accept(self, visitor):
        return self._garment.accept(visitor)

    def __str__(self):
        return str(self._garment)

class EcoFriendly(GarmentDecorator):
    def __str__(self):
        return f"{super().__str__()} *Note: Eco-friendly."

class NeverWorn(GarmentDecorator):
    def __str__(self):
        return f"{super().__str__()} *Note: Never worn."

class HandWash(GarmentDecorator):
    def __str__(self):
        return f"{super().__str__()} *Note: Always hand wash."


# PANTALONES
# Crear los elementos
builder = PantsBuilder()
director = PantsDirector(builder)
redPants = CatalogItem("Fashionable Red Pants", EcoFriendly(director.make_redPants()), 6.50)
bluePants = CatalogItem("Cute Vintage Jeans", NeverWorn(director.make_bluePants()), 8.00)
pinkPants = CatalogItem("Hot Pink Pants", HandWash(director.make_pinkPants()), 29.99)
whitePants = CatalogItem("Futuristic White Pants", NeverWorn(EcoFriendly(director.make_whitePants())), 12.50)
# Crear las secciones
pants = CatalogSection("Pants")
pants.add(redPants)
pants.add(bluePants)
pants.add(pinkPants)
pants.add(whitePants)


# CAMISAS
# Crear los elementos
builder = ShirtBuilder()
director = ShirtDirector(builder)
crewNeckShirt = CatalogItem("Modern Printed Tee", HandWash(EcoFriendly(director.make_crewNeckShirt())), 1.50)
poloShirt = CatalogItem("Aesthetic Shirt", HandWash(director.make_poloShirt()), 22.00)
VNeckShirt = CatalogItem("Hot Vintage Shirt", NeverWorn(director.make_VNeckShirt()), 9.99)
longSleeveShirt = CatalogItem("Chic White Shirt", EcoFriendly(director.make_longSleeveShirt()), 14.00)
# Crear las secciones
shirts = CatalogSection("Shirts")
shirts.add(crewNeckShirt)
shirts.add(poloShirt)
shirts.add(VNeckShirt)
shirts.add(longSleeveShirt)


# CLOSET
main_catalog = CatalogSection("Closet")
main_catalog.add(pants)
main_catalog.add(shirts)
main_catalog.display()
print()
