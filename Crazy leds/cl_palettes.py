#from lib.neopix import NeoPix

#Palettes from http://soliton.vm.bytemark.co.uk/pub/cpt-city/index.html , names of the variables correspond to the names of palettes from mentioned webpage

# some common colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
cyan = (0,255,255)
magenta = (255,0,255)
purple = (64,0,128)
orange = (255,109,0)
pink = (255,20,147)
darkslategray = (47,79,79)
darkgreen = (0,100,0)
darkblue = (0,0,139)
darkred = (139,0,0)
darkorange = (255,48,0)
darkmagenta = (139,0,139)
darkcyan = (0,139,139)
darkviolet = (148,0,211)
darkyellow = (240,200,15)
darkyellow2 = (255,215,0)

def_colors = [red, green, blue, yellow, cyan, magenta, purple, orange, pink, darkslategray, darkgreen, darkblue, darkred, darkorange, darkmagenta, darkcyan, darkviolet, darkyellow, darkyellow2, white, black]

color_wheel = [(0, 255, 0), (3, 252, 0), (6, 249, 0), (9, 246, 0), (12, 243, 0), (15, 240, 0),
                 (18, 237, 0), (21, 234, 0), (24, 231, 0), (27, 228, 0), (30, 225, 0), (33, 222, 0),
                 (36, 219, 0), (39, 216, 0), (42, 213, 0), (45, 210, 0), (48, 207, 0), (51, 204, 0),
                 (54, 201, 0), (57, 198, 0), (60, 195, 0), (63, 192, 0), (66, 189, 0), (69, 186, 0),
                 (72, 183, 0), (75, 180, 0), (78, 177, 0), (81, 174, 0), (84, 171, 0), (87, 168, 0),
                 (90, 165, 0), (93, 162, 0), (96, 159, 0), (99, 156, 0), (102, 153, 0), (105, 150, 0),
                 (108, 147, 0), (111, 144, 0), (114, 141, 0), (117, 138, 0), (120, 135, 0), (123, 132, 0),
                 (126, 129, 0), (129, 126, 0), (132, 123, 0), (135, 120, 0), (138, 117, 0), (141, 114, 0),
                 (144, 111, 0), (147, 108, 0), (150, 105, 0), (153, 102, 0), (156, 99, 0), (159, 96, 0), (162, 93, 0),
                 (165, 90, 0), (168, 87, 0), (171, 84, 0), (174, 81, 0), (177, 78, 0), (180, 75, 0), (183, 72, 0),
                 (186, 69, 0), (189, 66, 0), (192, 63, 0), (195, 60, 0), (198, 57, 0), (201, 54, 0), (204, 51, 0),
                 (207, 48, 0), (210, 45, 0), (213, 42, 0), (216, 39, 0), (219, 36, 0), (222, 33, 0), (225, 30, 0),
                 (228, 27, 0), (231, 24, 0), (234, 21, 0), (237, 18, 0), (240, 15, 0), (243, 12, 0), (246, 9, 0),
                 (249, 6, 0), (252, 3, 0), (255, 0, 0), (252, 0, 3), (249, 0, 6), (246, 0, 9), (243, 0, 12), (240, 0, 15),
                 (237, 0, 18), (234, 0, 21), (231, 0, 24), (228, 0, 27), (225, 0, 30), (222, 0, 33), (219, 0, 36),
                 (216, 0, 39), (213, 0, 42), (210, 0, 45), (207, 0, 48), (204, 0, 51), (201, 0, 54), (198, 0, 57),
                 (195, 0, 60), (192, 0, 63), (189, 0, 66), (186, 0, 69), (183, 0, 72), (180, 0, 75), (177, 0, 78),
                 (174, 0, 81), (171, 0, 84), (168, 0, 87), (165, 0, 90), (162, 0, 93), (159, 0, 96), (156, 0, 99),
                 (153, 0, 102), (150, 0, 105), (147, 0, 108), (144, 0, 111), (141, 0, 114), (138, 0, 117), (135, 0, 120),
                 (132, 0, 123), (129, 0, 126), (126, 0, 129), (123, 0, 132), (120, 0, 135), (117, 0, 138), (114, 0, 141),
                 (111, 0, 144), (108, 0, 147), (105, 0, 150), (102, 0, 153), (99, 0, 156), (96, 0, 159), (93, 0, 162),
                 (90, 0, 165), (87, 0, 168), (84, 0, 171), (81, 0, 174), (78, 0, 177), (75, 0, 180), (72, 0, 183),
                 (69, 0, 186), (66, 0, 189), (63, 0, 192), (60, 0, 195), (57, 0, 198), (54, 0, 201), (51, 0, 204),
                 (48, 0, 207), (45, 0, 210), (42, 0, 213), (39, 0, 216), (36, 0, 219), (33, 0, 222), (30, 0, 225),
                 (27, 0, 228), (24, 0, 231), (21, 0, 234), (18, 0, 237), (15, 0, 240), (12, 0, 243), (9, 0, 246),
                 (6, 0, 249), (3, 0, 252), (0, 0, 255), (0, 3, 252), (0, 6, 249), (0, 9, 246), (0, 12, 243), (0, 15, 240),
                 (0, 18, 237), (0, 21, 234), (0, 24, 231), (0, 27, 228), (0, 30, 225), (0, 33, 222), (0, 36, 219),
                 (0, 39, 216), (0, 42, 213), (0, 45, 210), (0, 48, 207), (0, 51, 204), (0, 54, 201), (0, 57, 198),
                 (0, 60, 195), (0, 63, 192), (0, 66, 189), (0, 69, 186), (0, 72, 183), (0, 75, 180), (0, 78, 177),
                 (0, 81, 174), (0, 84, 171), (0, 87, 168), (0, 90, 165), (0, 93, 162), (0, 96, 159), (0, 99, 156),
                 (0, 102, 153), (0, 105, 150), (0, 108, 147), (0, 111, 144), (0, 114, 141), (0, 117, 138), (0, 120, 135),
                 (0, 123, 132), (0, 126, 129), (0, 129, 126), (0, 132, 123), (0, 135, 120), (0, 138, 117), (0, 141, 114),
                 (0, 144, 111), (0, 147, 108), (0, 150, 105), (0, 153, 102), (0, 156, 99), (0, 159, 96), (0, 162, 93),
                 (0, 165, 90), (0, 168, 87), (0, 171, 84), (0, 174, 81), (0, 177, 78), (0, 180, 75), (0, 183, 72),
                 (0, 186, 69), (0, 189, 66), (0, 192, 63), (0, 195, 60), (0, 198, 57), (0, 201, 54), (0, 204, 51),
                 (0, 207, 48), (0, 210, 45), (0, 213, 42), (0, 216, 39), (0, 219, 36), (0, 222, 33), (0, 225, 30),
                 (0, 228, 27), (0, 231, 24), (0, 234, 21), (0, 237, 18), (0, 240, 15), (0, 243, 12), (0, 246, 9),
                 (0, 249, 6), (0, 252, 3), (0, 255, 0)]

full_saturation_spectrum = [(255,  0,  0),(255, 15,  0),(255, 30,  0),(255, 45,  0),(255, 61,  0),(255, 76,  0),(255, 91,  0),
                            (255,106,  0),(255,121,  0),(255,136,  0),(255,151,  0),(255,167,  0),(255,182,  0),(255,197,  0),
                            (255,212,  0),(255,227,  0),(255,242,  0),(252,255,  0),(237,255,  0),(222,255,  0),(207,255,  0),
                            (192,255,  0),(177,255,  0),(162,255,  0),(146,255,  0),(131,255,  0),(116,255,  0),(101,255,  0),
                            ( 86,255,  0),( 71,255,  0),( 56,255,  0),( 40,255,  0),( 25,255,  0),( 10,255,  0),(  0,255,  5),
                            (  0,255, 20),(  0,255, 35),(  0,255, 50),(  0,255, 66),(  0,255, 81),(  0,255, 96),(  0,255,111),
                            (  0,255,126),(  0,255,141),(  0,255,157),(  0,255,172),(  0,255,187),(  0,255,202),(  0,255,217),
                            (  0,255,232),(  0,255,247),(  0,247,255),(  0,232,255),(  0,217,255),(  0,202,255),(  0,187,255),
                            (  0,172,255),(  0,157,255),(  0,141,255),(  0,126,255),(  0,111,255),(  0, 96,255),(  0, 81,255),
                            (  0, 66,255),(  0, 50,255),(  0, 35,255),(  0, 20,255),(  0,  5,255),( 10,  0,255),( 25,  0,255),
                            ( 40,  0,255),( 56,  0,255),( 71,  0,255),( 86,  0,255),(101,  0,255),(116,  0,255),(131,  0,255),
                            (146,  0,255),(162,  0,255),(177,  0,255),(192,  0,255),(207,  0,255),(222,  0,255),(237,  0,255),
                            (252,  0,255),(255,  0,242),(255,  0,227),(255,  0,212),(255,  0,197),(255,  0,182),(255,  0,167),
                            (255,  0,151),(255,  0,136),(255,  0,121),(255,  0,106),(255,  0, 91),(255,  0, 76),(255,  0, 61),
                            (255,  0, 45),(255,  0, 30),(255,  0, 15),(255,  0,  0)]

red_tide =[(252, 46,  0),(255,139, 33),(247,158, 74),(247,216,134),(245, 94, 15),(187, 65, 16),(255,241,127),(187, 65, 16),(251,233,167),
  (255, 94,  9),(140,  8,  6)]

skyline = [( 0,  0,  0),( 12,  7, 62),( 16, 10, 85),( 20, 12,102),( 22, 13,114),( 24, 14,124),( 24, 15,127),( 25, 15,128),( 25, 15,129),
           ( 25, 15,130),( 25, 15,131),( 26, 16,132),( 26, 16,133),( 26, 16,134),( 26, 16,135),( 26, 16,136),( 26, 16,137),( 27, 16,138),
           ( 27, 16,138),( 27, 16,139),( 27, 16,140),( 27, 16,140),( 27, 17,141),( 27, 17,141),( 27, 17,142),( 27, 17,142),( 28, 17,143),
           ( 28, 17,143),( 28, 17,144),( 28, 17,144),( 28, 17,144),( 28, 17,144),( 28, 17,145),( 28, 17,145),( 28, 17,145),( 28, 17,145),
           ( 28, 17,145),( 28, 17,145),(131, 14, 78),(234, 11, 11),(244, 73,  5),(255,136,  0),(247,186, 27),(239,236, 55),(137,101,  8),
           ( 69, 50,  4),(  0,  0,  0)]


## Gradient palettes:

bhw4_057 = (( 62,  0, 13, 0),( 91,  0, 31, 9),( 96,  2, 38, 23),(160,  0, 77, 36), (232, 28, 123, 50),( 91,  0, 31, 80),( 62,  0, 13, 100))
bhw3_07 = ((198, 43, 33, 0), ( 81, 67,205, 12), (141,100,215,21),(180,109,174,29),(249,124,104,33),(156, 30, 23,37),(132, 54,113,46),(141,100,215,51),( 76, 51,159,64),(249,124,104,77),( 23, 23, 80,100))


# Lists with palettes

normal_palettes = (color_wheel, full_saturation_spectrum, skyline, red_tide)
gradient_palettes = (bhw4_057, bhw3_07)

class GammaTable:
    
    def __init__ (self, gamma_factor=2.2, color_space: int = 8):

        self._gamma_factor = gamma_factor
        self._color_space = color_space
        #self.gamma_factor(gamma_factor)
        #self.color_space(color_space)
        self.create_gamma_table(self._gamma_factor,self._color_space)

    def create_gamma_table(self, gamma_factor, color_space):  # 8-bit brightness space, only one table for all colors
        self.gamma_factor(gamma_factor)
        self.color_space(color_space)
        self.gamma_table = [] 
        i = 0
        for i in range(self._color_space):
            self.gamma_table.append(round(self._color_space * (i / self._color_space) ** self._gamma_factor + 0.4))
            
    def _get_gamma(self, position):
        return self.gamma_table[position]
    
    def gamma_cor(self, palette):
        for idx, color in enumerate(palette):
            c1, c2, c3 = color
            c1, c2, c3 = self._get_gamma(c1), self._get_gamma(c2), self._get_gamma(c3)
            palette[idx] = (c1, c2, c3)
        return palette
        #print('after gamma',self.palette)		# debuging purposes only

    def gamma_factor(self, gamma_factor=None):
        if gamma_factor == None:
            return self._gamma_factor
        else:
            self._gamma_factor = gamma_factor
            
    def color_space(self, color_space=None):
        if color_space == None:
            return self._color_space
        else:
            self._color_space = 2**color_space
    def clear_gamma_table(self):
        try:
            self.gamma_table.clear()
        except:
            return
    
class Palette:
    
    def __init__(self, pal_length=None, palette_no=0, gradient = False, order=[1,0,2,3]):
        # order means the order of individual color components red =  0, green = 1, blue = 3, white = 3
        # order [1,0,2,3] means [g,r,b,w]
        # standard for addressable leds WS28111, WS2812 and WS2815
        self.order = order
        self.gradient = gradient
        self.set_palette(pal_length, palette_no, self.gradient)


    def set_palette(self, pal_length=None, palette=0, gradient=False):

        self.palette = []
        self.gradient = gradient
        
        if gradient == False:
            for color in normal_palettes[palette]:
                self.palette.append((color[self.order[0]], color[self.order[1]], color[self.order[2]]))
        else:
            grad_pal_length = len(gradient_palettes[palette])
            if pal_length is None:
                new_length = grad_pal_length*3
            else:
                new_length = pal_length
            grad_pal_length = len(gradient_palettes[palette])
            if new_length <= grad_pal_length:
                for data in gradient_palettes[palette]:
                    color, d = data
                    self.palette.append((color[self.order[0]], color[self.order[1]], color[self.order[2]]))
                    del d
            else:
                stop = grad_pal_length - 1
                i = 1
                while stop > 0:
                    steps = 0
                    dist = 0
                    start = int((gradient_palettes[palette][i - 1][3] / 100) * new_length)
                    end = int((gradient_palettes[palette][i][3] / 100) * new_length)
                    dist = end - start
                    steps = dist - 1
                    color, d = gradient_palettes[palette][i - 1]
                    self.palette.append((color[self.order[0]], color[self.order[1]], color[self.order[2]]))
                    del d
                    while steps > 0:
                        color[0] = int(self.lerp(gradient_palettes[palette][i][0], gradient_palettes[palette][i - 1][0],
                                          steps / dist))
                        color[1] = int(self.lerp(gradient_palettes[palette][i][1], gradient_palettes[palette][i - 1][1],
                                          steps / dist))
                        color[2] = int(self.lerp(gradient_palettes[palette][i][2], gradient_palettes[palette][i - 1][2],
                                          steps / dist))
                        self.palette.append((color[self.order[0]], color[self.order[1]], color[self.order[2]]))
                        steps -= 1
                    i += 1
                    stop -= 1
        self.pal_length = len(self.palette)

    def color_wheel_rgb(self,pos):
        # pos in range [0,255]
        #t = time.ticks_us()
        if pos <= 85:
            return (pos*3, 255-pos*3, 0)
        elif pos <= 170:
            pos -= 85
            return (255-pos*3, 0, pos*3)
        else:
            pos -= 170
            return (0, pos*3, 255-pos*3)

    def color_wheel_grb(self,pos):
        # pos in range [0,255]
        #t = time.ticks_us()
        if pos <= 85:
            return ( 255-pos*3, pos*3, 0)
        elif pos <= 170:
            pos -= 85
            return ( 0, 255-pos*3, pos*3)
        else:
            pos -= 170
            return (pos*3, 0, 255-pos*3)

    def lerp(self, a, b, t):
        return a + (b - a) * t
   
    
    def clear_palette(self):
        try:
            self.palette.clear()
            self.pal_length = len(self.palette)
        except:
            return

    
