from abc import ABC, abstractmethod


class Boton(ABC):
    @abstractmethod
    def renderizar(self):
        pass

class Menu(ABC):
    @abstractmethod
    def renderizar(self):
        pass
class CheckBox(ABC):
    @abstractmethod
    def renderizar(self):
        pass


class BotonWindows(Boton):
    def renderizar(self):
        print("Boton estilo Windows..")

class MenuWindows(Menu):
    def renderizar(self):
        print("Menu estilo Windows")
class CheckBoxWindows(CheckBox):
    def renderizar(self):
        print("Checkbox estilo Windows")

class BotonMac(Boton):
    def renderizar(self):
        print("Boton estilo Mac")

class MenuMac(Menu):
    def renderizar(self):
        print("Menu estilo Mac")

class CheckBoxMac(CheckBox):
    def renderizar(self):
        print("CheckBox estilo Mac")

class UIFactoryABC(ABC):
    @abstractmethod
    def crearBoton(self):  
        pass

    @abstractmethod
    def crearMenu(self):   
        pass

    @abstractmethod
    def crearCheckBox(self):
        pass

# --- Fábricas Concretas ---
class WindowsFactory(UIFactoryABC):
    def crearBoton(self):  
        return BotonWindows()

    def crearMenu(self):   
        return MenuWindows()
    def crearCheckBox(self):
        return CheckBoxWindows()

class MacFactory(UIFactoryABC):
    def crearBoton(self): 
        return BotonMac()

    def crearMenu(self):  
        return MenuMac()

    def crearCheckBox(self):
        return CheckBoxMac()

def crearUI(factory: UIFactoryABC):
    boton = factory.crearBoton()
    menu = factory.crearMenu()
    checkbox= factory.crearCheckBox()
    boton.renderizar()
    menu.renderizar()
    checkbox.renderizar()

def main():
    sistema = "Mac"

    if sistema == 'Windows':
        factory = WindowsFactory()
    elif sistema == 'Mac':
        factory = MacFactory()

    crearUI(factory)

if __name__ == "__main__":
    main()