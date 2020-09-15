class Vector2D(list):

    def __init__(self, x = None, y = None):
        
        self.append(x)
        self.append(y)
        self.x = x
        self.y = y

    def __setattr__(self, name, value):

        self.__dict__[name] = value
        if name == 'x':
            super().__setitem__(0, value)
        if name == 'y':
            super().__setitem__(1, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key == 0:
            self.x = value
        if key == 1:
            self.y = value

    def __getitem__(self, key):

        if key == 0:
            return self.x
        if key == 1:
            return self.y
        raise IndexError
    
class Vector3D(Vector2D):

    def __init__(self, x = None, y = None, z = None):

        super().__init__(x, y)
        self.append(z)
        self.z = z
    
    def __setattr__(self, name, value):

        super().__setattr__(name, value)
        if name == 'z':
            super().__setitem__(2, value)
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key == 2:
            self.z = value
    
    def __getitem__(self, key):

        if key == 2:
            return self.z
        return super().__getitem__(key)
