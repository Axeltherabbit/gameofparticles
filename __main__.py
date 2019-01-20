import pygame
import random


#screen size, it'll be a square 
surface_sz=500

# rules
# r is red, g is green, b is guess
# play with the values 
# if x_y : 1 x is attracted by y
# if x_y : -1 x is rejected by y
# if x_y : 0 x nothing happens
# you even have x_x don't forget
# have fun!
rules = {"b_r":1,"b_g":-1,"b_b":-1,"g_g":1,"g_r":-1,"g_b":1,"r_r":1,"r_b":-1,"r_g":1}

def applyrules(a,b):
    return rules[a[0]+"_"+b[0]]


rgb={"red":(255,0,0),"green":(0,255,0),"blue":(0,0,255)}

def distance(a,b):
    #it just return the distance between two points
    return ((a.posx-b.posx)**2+\
            (a.posy-b.posy)**2)**0.5

class GenerateParticle():
    #it just generate a random particle in a random posizion
    def __init__(self):
        self.radius=3
        
        #the particle position is decided here,
        #it's the crucial step
        self.posy=random.randint(surface_sz/4,surface_sz/2+surface_sz/4)
        self.posx=random.randint(surface_sz/4,surface_sz/2+surface_sz/4)
        
        self.pos=(self.posx,self.posy)
        self.color=random.choice([*rgb])

   
def main():
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use

    # Create surface of surface_sz
    main_surface = pygame.display.set_mode((surface_sz, surface_sz))
    
    #generete the particles
    points= [GenerateParticle()for _ in range(250)] 
    #attraction speed
    speed = 2
    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
    
        #clean the screen from the previous frame
        main_surface.fill((0,0,0))
        
        #the most important part
        #sums store near particles effect to a particle
        sums = []
        for point in points:
            #init movement effects 
            #to (x = +0, y = +0)
            sums.append((0,0)) 
            for other in points:
                if other is point: #skip itself
                    continue
                dis=distance(point,other)
                if 1 < dis <= 50: #distance range
                    direction_x = (other.posx-point.posx) / dis
                    direction_y = (other.posy-point.posy) / dis
                    
                    #get particles attraction,rejection,neutral rule
                    rule=applyrules(point.color,other.color)
                    
                    sums[-1]=(sums[-1][0]+ (direction_x*rule*speed),
                              sums[-1][1]+ (direction_y*rule*speed))
        #apply the effects to each particle
        for n in range(len(points)):
            points[n].posx+=sums[n][0]
            points[n].posy+=sums[n][1]
            
            #pop up any particle that cross
            #the screen border to the other side of
            #the screen
            if points[n].posx < 0:
                points[n].posx += surface_sz 
            elif points[n].posx > surface_sz:
                points[n].posx-=surface_sz
            elif points[n].posy < 0:
                points[n].posy += surface_sz
            elif points[n].posy > surface_sz:
                points[n].posy -=surface_sz
            
            points[n].pos=(int(points[n].posx),int(points[n].posy))
            
            #and just print the particle
            pygame.draw.circle(main_surface, rgb[points[n].color], points[n].pos ,points[n].radius)

        #Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

    pygame.quit()     # Once we leave the loop, close the window.


if __name__=="__main__":
    main()
