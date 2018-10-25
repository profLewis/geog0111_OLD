import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

from scipy.ndimage.filters import convolve1d

def demofilt3():
  def gaussian(x,sigma):
    g = np.exp(-(x/sigma)**2/2.)
    # normalise
    return (g / g.sum())

  '''
  set up x and y
  where y is a noisy signal
  '''
  nsamp = 100
  x = np.arange(nsamp).astype(float)
  y_clean = 5 + 3 * np.cos(x*np.pi/(nsamp/4.))
  noise = np.random.normal(size=nsamp)
  y = y_clean + noise


  '''
  Plotting set up
  '''
  lines = []
  points = []
  noises = []
  fig, ax = plt.subplots(2,1,figsize=(10,6))

  lab = ['filter','filtered signal']

  for i in range(2):
    ax[i].set_xlim(0,nsamp)
    ax[i].plot(x,y_clean,'r',label='clean signal')
    ax[i].plot(x,y,'k+',label='signal')

    noise0, = ax[i].plot([],[],'gx')
    point0, = ax[i].plot([], [], 'go')
    line0, = ax[i].plot([], [], 'g-',label=lab[i],lw=2)
    ax[i].legend(loc='upper right')
    lines.append(line0)
    points.append(point0)
    noises.append(noise0)

  point0,point1 = points
  line0,line1 = lines
  noise0,noise1 = noises

  '''
  functions for init and animation
  '''
  def init():
    line0.set_data([], [])
    line1.set_data([], [])
    point0.set_data([], [])
    point1.set_data([], [])

    return (line0,line1,point0,point1,\
		noise0,noise1)

  def animate(i):
    sigma = 6.0 * float(nsamp) / 200.
    # x extent of filter
    xsamp = np.arange(-sigma*3,sigma*3)
    ynew = convolve1d(y, gaussian(xsamp,sigma),mode='wrap')
    line1.set_data(x[:i],ynew[:i])
    ax[0].set_title(f'$\sigma$ {sigma:5.1f} $x_c = {i}$')

    xsamp = np.arange(-i,nsamp-i).astype(float) 
    filt = gaussian(xsamp,sigma) 

    line0.set_data(x,5*filt/filt.max())
    point0.set_data([i],[5])
    point1.set_data([i],[ynew[i]]) 

    # ones to show
    some = filt > 0.01
    noise0.set_data(x[some],y[some])
    noise1.set_data(x[some],y[some])

    return(line0,line1,point0,point1,\
		noise0,noise1)
    
  anim = matplotlib.animation.FuncAnimation(fig, animate,init_func=init,
                               frames=nsamp, interval=200, 
                               blit=True)

  return(anim)
