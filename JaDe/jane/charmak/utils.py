import random


def random_colors(number): 
    """
        Generate a random palette of x colors, where x is the number of colors
        needed. 

        Parameters 
        -----------
            number: int
                number of color to generate
        
        Returns 
        --------
            colors: list
                list of random colors
    """
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for i in range(number)]
    
    return colors
