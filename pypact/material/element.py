"""
    Element type
"""
from pypact.material.isotope import Isotope


class Element:

    def __init__(self, name, symbol, z, aeff):
        """
        Create an element.

        Parameters
        ----------
        name : str
            Element name
        symbol : str
            Element symbol
        z : int
            atomic number
        aeff : float
            effective mass of mole (optional)
        """
        self.name = name
        self.symbol = symbol
        self.z = z
        self.aeff = aeff

        self.isotopes = []

    def addisotope(self, isotope, abundance):
        """
        Add an element.

        Parameters
        ----------
        isotope : Isotope
            Isotope type name

        abundance : float
            fraction abundance
        """
        self.isotopes.append((isotope, abundance))

