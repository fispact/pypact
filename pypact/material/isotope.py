"""
    Isotope type
"""


class Isotope:

    def __init__(self, name, z, n, a=0.0, m=0):
        """
        Create an isotope.

        Parameters
        ----------
        name : str
            Isotope name
        z : int
            atomic number
        n : int
            number of nucleons
        a : float
            mass of mole (optional)
        m : int
            isomer level (optional)
        """
        self.name = name
        self.z = z
        self.n = n
        self.a = a
        self.m = m

