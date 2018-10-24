import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

from scipy.ndimage.filters import convolve1d

def demofilt2():
  def gaussian(x,sigma):
    g = np.exp(-(x/sigma)**2/2.)
    # normalise
    return (g / g.sum())

  '''
  set up x and y
  where y is a noisy signal
  '''
  nsamp = 200
  x = np.arange(nsamp).astype(float)
  y_clean = 5 + 3 * np.cos(x*np.pi/50.)
  noise = np.random.normal(size=nsamp)
  y = y_clean + noise


  '''
  Plotting set up
  '''
  fig, ax = plt.subplots(2,1,figsize=(7,10))
  ax[0].set_xlim(0,nsamp)
  ax[0].plot(x,y_clean,'r',label='clean signal')
  ax[0].plot(x,y,'k+',label='signal')

  line0, = ax[0].plot([], [], 'b-',label='reconstructed')
  ax[0].legend()

  ax[1].plot(y_clean,y,'ro')
  ax[1].plot([y.min(),y.max()],[y.min(),y.max()],'k--')
  ax[1].set_xlim(y_clean.min(),y_clean.max())
  ax[1].set_ylim(y_clean.min(),y_clean.max())
  ax[1].set_xlabel('clean signal')
  ax[1].set_ylabel('reconstructed signal')
  ax[1].set_aspect('equal')

  line1, = ax[1].plot([], [], 'b+')

  '''
  functionsd for init and animation
  '''
  def init():
    line0.set_data([], [])
    line1.set_data([], [])
    return (line0,line1)

  def animate(i):
    sigma = 10*(i+1)/100.
    # x extent of filter
    xsamp = np.arange(-sigma*3,sigma*3)
    ynew = convolve1d(y, gaussian(xsamp,sigma),mode='wrap')
    #im=plt.plot(x,ynew,'g--',label='reconstructed')
    line0.set_data(x,ynew)
    
    ax[0].set_title(f'$\sigma$ {sigma:5.1f}')
    line1.set_data(y_clean,ynew)
    
    return(line0,line1)
    
  anim = matplotlib.animation.FuncAnimation(fig, animate,init_func=init,
                               frames=100, interval=100, 
                               blit=True)

  return(anim)
