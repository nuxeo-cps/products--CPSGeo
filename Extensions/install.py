
from Products.CPSInstaller.CPSInstaller import CPSInstaller

class MyInstaller(CPSInstaller):
        
    product_name = 'CPSGeo'

    def install(self):
        self.log("Starting CPSGeo install")
        # Do the installing here
        self.finalize()
        self.log("End of specific CPSGeo install")

def install(self):
    installer = MyInstaller(self)
    installer.install()
    return installer.logResult()

