import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
'''
Illustration of Gaussian filter
for varying sigma

also, illustration of animation
'''

def demofilt1():
  fig, ax = plt.subplots(figsize=(10,3))
  ax.set_xlim(( -30, 30))
  ax.set_ylim((0, 1))

  line, = ax.plot([], [], lw=2)
  x = np.linspace(-30, 30, 101)
  plt.xlabel('days')

  def init():
    line.set_data([], [])
    return (line,)

  def animate(i):
    sigma = 10*(i+1)/100.
    ax.set_title(f'Gaussian $\sigma$ {sigma}')
    gaussian = np.exp(-(x/sigma)**2/2.)
    line.set_data(x,gaussian)
    return(line,)

  anim = matplotlib.animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, 
                               blit=True)

  return(anim)

