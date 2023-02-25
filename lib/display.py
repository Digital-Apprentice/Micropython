class Display:    
    def __init__(self, width=31, height=7, x0=0, y0=0):
         self.width = width
         self.height = height
         self.x0 = x0
         self.y0 = y0
         #self.x1 = x0
         #self.y1 = y0
     
    def init_neopix_aled(self,aled_data_pin,leds_in_col=8,num_of_cols=32):
        try:
            from lib.neopix import NeoPix
            self.leds_in_col = leds_in_col
            self.num_of_cols = num_of_cols
            leds_count = leds_in_col * num_of_cols
            self.led = NeoPix(aled_data_pin, 'chain_matrix', leds_in_col, num_of_cols)
        except ImportError:
            print("The neopix library is required and has not been imported")
         
    def update_position(self, position,velocity, color_on,color_off=(0,0,0), edges = False):
        #led.clear_all()
        #self.edges = edges # jeżeli mają być wykrywane krawędzie ustawić na True
        self.position = position
        self.velocity = velocity
        self.color_on = color_on
        self.color_off = color_off
        self.edges = edges
        self.check_edges(self.edges)
    
    def check_edges(self, edges) :
        if edges is True:
            if self.position.x > self.width:
                self.velocity.x *= -1
                self.position.x = self.width
            elif  self.position.x < self.x0:
                self.velocity.x *= -1
                self.position.x = self.x0
                
            if self.position.y > self.height:
                self.velocity.y *= -1 
                self.position.y = self.height
            elif self.position.y < self.y0:
                self.position.y = self.y0
                self.velocity *= -1
            self.out_of_matrix = False           
        else:
            if self.position.x > self.width or self.position.x < self.x0 or self.position.y > self.height or self.position.y < self.y0:
                self.out_of_matrix = True
            else:
                self.out_of_matrix = False
                
    def update_aled(self):
        if self.out_of_matrix is False:
            x = self.position.x
            y = self.position.y
            if isinstance(x,float): x = round(x)
            if isinstance(y,float): y = round(y)
            self.led.set_matrix_pixel(x,y,self.led.color_wheel(self.color_on))
    
    def round_coordinates(self, coordinates):
        points_rounded = []
        for point in coordinates:
            points_rounded.append((round(point[0]),round(point[1])))
        return points_rounded  
    
    def display_fbuf_on_aled(self, fbuf):    
        for y in range(self.leds_in_col):
            for x in range(self.num_of_cols):
                    #color = fbuf[(y*self.num_of_cols+x) * 2] | (fbuf_view[(y*self.num_of_cols+x) * 2 + 1] << 8)
                    color = self.led.rgb565_to_rgb(fbuf.pixel(x,y))
                    index = self.led.get_matrix_index(x,y)
                    self.led.aled.__setitem__(index,color)
        self.led.show()
        
    
    def led_on(self):
        self.led.show()
    
    def clear_aled(self):
        self.led.clear_all()
    
    def set_area(self, width, height, x0=0, y0=0):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
    
    def rotate_matrix_90(matrix):# rotacja macierzy o 90 stopni
        n = len(matrix)
        m = len(matrix[0])
        rotated = [[0 for x in range(n)] for y in range(m)]
        for i in range(n):
            for j in range(m):
                rotated[j][n-i-1] = matrix[i][j]
        return rotated
    
    def rotate_matrix(matrix, angle, point=(0, 0)): # obrót macierzy o dowolny kąt
        angle = math.radians(angle)
        rot_mat = [[math.cos(angle), -math.sin(angle), point[0]], 
                   [math.sin(angle), math.cos(angle), point[1]], 
                   [0, 0, 1]]
        res = []
        for i in range(len(matrix)):
            res.append([])
            for j in range(len(matrix[0])):
                res[i].append(0)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                for k in range(len(rot_mat)):
                    res[i][j] += matrix[i][k] * rot_mat[k][j]
        return res
    

