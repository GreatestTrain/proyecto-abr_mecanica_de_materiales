from numpy import pi

class Section:
    def __init__(self, kind):
        self.kind = kind
        self.A = 0
        self.I = 0
        self.max_c = 0
        self.centroid = 0
    def __str__(self) -> str:
        return f"id: {hex(id(self))}\n== Section ==\n- {self.kind} -\nTotal Area:\t{self.A}\nInertia:\t{self.I}\nmax c:\t\t{self.max_c}\ncentroid:\t{self.centroid}"

class IShapedSection(Section):
    def __init__(self, top_width, top_thickness, bottom_width, bottom_thickness, web_height, web_thickness):
        super().__init__(kind="IShaped")
        self.total_height = bottom_thickness + web_height + top_thickness
        A1 = (top_width*top_thickness)
        A2 = (web_height*web_thickness)
        A3 = (bottom_width*bottom_thickness)
        # A4 = ((4-pi)*fillet_radius**2)
        self.A = A1 + A2 + A3
        c1 = bottom_thickness + web_height+ (top_thickness/2)
        c2 = bottom_thickness + (web_height/2)
        c3 = (bottom_thickness/2)
        self.centroid = ((A1 * c1) + (A2 * c2) + (A3 * c3)) / self.A
        I1 = 1/12 * top_width * top_thickness**3
        D1 = self.centroid - c1
        I2 = 1/12 * bottom_width * bottom_thickness**3
        D2 = self.centroid - c2
        I3 = 1/12 * web_thickness * web_height**3
        D3 = self.centroid - c3
        self.I = (I1 + A1*D1**2) + (I2 + A2*D2**2) + (I3 + A3*D3**2)
        if c_max := (self.total_height - self.centroid) > self.centroid:
            self.max_c = c_max
            self.other_c = self.centroid
        else:
            self.max_c = self.centroid
            self.other_c = c_max
