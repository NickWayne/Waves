import pygame,random,math

rands = 50
# max = (0,0,0)
# min = (255,0,0)
# max = (0,0,0)
# min = (0,0,255)
min = (238, 238, 0)
max = (0, 255, 0)
SIZE = (640,480)
class ocean (object):

    def __init__(self):
        self.points = []
        self.num = 10
        self.max = self.num - 1
        self.dire = True

    def populate(self):
        for i in range(self.num+2):
            self.points.append([])
            for g in range(self.num+2):
                a = random.randint(-rands,rands)
                self.points[i].append(point(g-1,i-1,self.max,a))

    def display(self,surface):
        self.dire = True
        for i in range(self.num+1):
            for g in range(self.num+1):
                if self.dire == True:
                    pts = (self.points[i][g],self.points[i+1][g],self.points[i][g+1],self.points[i+1][g+1])
                    pts[0].get_color()
                    pts[1].get_color()
                    pts[2].get_color()
                    r = (pts[0].color[0]+pts[1].color[0]+pts[2].color[0])/3
                    g = (pts[0].color[1]+pts[1].color[1]+pts[2].color[1])/3
                    b = (pts[0].color[2]+pts[1].color[2]+pts[2].color[2])/3
                    color = (r,g,b)
                    pygame.draw.polygon(surface,color,(pts[0].loc,pts[1].loc,pts[2].loc))
                    pts[3].get_color()
                    r = (pts[1].color[0]+pts[2].color[0]+pts[3].color[0])/3
                    g = (pts[1].color[1]+pts[2].color[1]+pts[3].color[1])/3
                    b = (pts[1].color[2]+pts[2].color[2]+pts[3].color[2])/3
                    color = (r,g,b)
                    pygame.draw.polygon(surface,color,(pts[1].loc,pts[2].loc,pts[3].loc))
                    # pygame.draw.line(surface,(255,0,0),pts[1].loc,pts[2].loc,5)
                    self.dire = not self.dire
                elif self.dire == False:
                    pts = (self.points[i][g+1],self.points[i][g],self.points[i+1][g+1],self.points[i+1][g])
                    pts[0].get_color()
                    pts[1].get_color()
                    pts[2].get_color()
                    r = (pts[0].color[0]+pts[1].color[0]+pts[2].color[0])/3
                    g = (pts[0].color[1]+pts[1].color[1]+pts[2].color[1])/3
                    b = (pts[0].color[2]+pts[1].color[2]+pts[2].color[2])/3
                    color = (r,g,b)
                    pygame.draw.polygon(surface,color,(pts[0].loc,pts[1].loc,pts[2].loc))
                    pts[3].get_color()
                    r = (pts[1].color[0]+pts[2].color[0]+pts[3].color[0])/3
                    g = (pts[1].color[1]+pts[2].color[1]+pts[3].color[1])/3
                    b = (pts[1].color[2]+pts[2].color[2]+pts[3].color[2])/3
                    color = (r,g,b)
                    pygame.draw.polygon(surface,color,(pts[1].loc,pts[2].loc,pts[3].loc))
                    # pygame.draw.line(surface,(255,255,0),pts[1].loc,pts[2].loc,5)
                    self.dire = not self.dire

    def redo_mult(self,delta):
        for i in self.points:
            for g in i:
                # if self.points.index(i) != 0 and self.points.index(i) != self.COLOURMAX:
                #     if self.points[self.points.index(i)].index(g) != 0 and self.points[self.points.index(i)].index(g) != self.COLOURMAX:
                g.redo_mult(delta)




class point (object):

    def __init__(self,layer,height,num,mult):
        self.num = num
        self.x = layer
        self.y = height
        self.div = (SIZE[0]/num,SIZE[1]/num)
        self.loc_base = (self.x*self.div[0],self.y*self.div[1])
        self.color = (0,100,200)
        if self.y != 0 and self.y != self.num:
            if self.x != 0 and self.x != self.num-1:
                self.mult = mult
                self.loc = (self.loc_base[0],self.loc_base[1]+self.mult)
            else:
                self.mult = 0
                self.loc = self.loc_base
        else:
            self.mult = 0
            self.loc = self.loc_base

    def redo_mult(self,delta):
        self.loc = self.loc_base
        self.mult = (math.cos(self.x / 2 + delta / 2) + math.sin(self.y - delta * 2)) * .5 * rands
        # self.height_mult = -20
        self.loc = (self.loc[0],self.loc[1]+self.mult)

    def lerp(self,t, a, b):
        return a + t * (b - a)

    def get_color(self):
        perc = (self.mult + rands)/float(2*rands)
        self.color = (self.lerp(perc,max[0],min[0]),self.lerp(perc,max[1],min[1]),self.lerp(perc,max[2],min[2]))



def run():
    tps = 0
    pygame.init()

    size = SIZE
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    done = False

    water = ocean()
    water.populate()

    pygame.key.set_repeat(200,200)
    while not done:
        time_passed_seconds = clock.tick(120)/1000.0
        tps += time_passed_seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_SPACE:
                    pass

        water.redo_mult(tps)

        screen.fill((0, 0, 0))
        water.display(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run()