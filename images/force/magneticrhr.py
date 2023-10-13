import random
import numpy as np
import collections
import matplotlib.pyplot as plt
plt.ioff()

class MagneticRHR():
    '''An ipywidget for students to test their knowledge of the magnetic force
    right-hand-rule in Jupyter notebooks.  Calling the class will
    start the self-test, which will run until the notebook is quit.

    Only the simplest cases are currently handled. I.e., magnetic
    fields and particle velocities are along the x-, y-, or z-axes.

    '''
    def __init__(self, charge_type):
        '''Initialize the test.  It is automatically ready to be displayed.
        Args:
            charge_type: 
                (str) 'particle' or 'current'.  Charges for 
                'particle' can be positive or negative.  'current' is 
                always in the direction of the current.    
        '''
        self.charge_type = charge_type
        self.fig, self.ax = plt.subplots(figsize=(4,4))
        
        if charge_type not in ['particle', 'current']:
            raise ValueError('`charge_type` must be "particle" or "current"')
        
        self.directions = collections.OrderedDict(
            {( 0, 0, 0):'none',
             ( 1, 0, 0):'right', 
             (-1, 0, 0):'left', 
             ( 0, 1, 0):'up', 
             ( 0,-1, 0):'down',
             ( 0, 0, 1):'out of Page',
             ( 0, 0, -1):'into Page'})

        
    def display_problem(self, charge, unknown_choice, known1Vec, known2Vec):
        '''
        Generates and displays the next problem
        '''
        choices = ['magnetic force', 'magnetic field', 'particle', 'current']
        if unknown_choice not in choices:
            raise ValueError('`unknown_choice` must be one of '+', '.join(choices)+f' not {unknown_choice}')
            
        self.ax.clear()
        
        # set the correct answer for the unknown value and display the knowns.
        if unknown_choice == 'magnetic force':
            # self.correct = self.directions[tuple(force)]
            known1 = 'velocity'
            known2 = 'magnetic field'
            self._draw_B_field(known2Vec)
            self._draw_particle_current_force(charge, known1Vec, force=False)
        elif unknown_choice == 'magnetic field':
            # self.correct = self.directions[tuple(B_field)]
            known1 = 'magnetic force'
            known2 = 'velocity'
            self._draw_particle_current_force(charge, known1Vec, force=True)
            self._draw_particle_current_force(charge, known2Vec, force=False)
        elif unknown_choice in ['particle', 'current']:
            # self.correct = self.directions[tuple(velocity)]
            known1 = 'magnetic field'
            known2 = 'magnetic force'
            self._draw_B_field(known1Vec)
            self._draw_particle_current_force(charge, known2Vec, force=True)

        self.ax.axis('off')
        self.ax.set_axis_off()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.legend(loc = 'upper right', framealpha=1)
         
        # display the plot
        chargeSign = 'positive' if charge > 0 else 'negative'
        known1Dir = '['+','.join([str(x) for x in known1Vec])+']'
        known2Dir = '['+','.join([str(x) for x in known2Vec])+']'
        self.fig.savefig(f'{self.charge_type}_{chargeSign}_{known1}-{known1Dir}_{known2}-{known2Dir}.png',
                         bbox_inches='tight', pad_inches=0)


    def _draw_particle_current_force(self, charge, vector, force):
        '''
        Draws a vector for the particle/current velocity/force vector and label
        
        Args:
            charge:
                (-1 or 1)
            force:
                (list of ints) force vector
        '''
        if force:
            color='C2'
            label = 'Force on'
            va='bottom'
            width = 7
        else:
            color='C0'
            label = 'Direction of'
            va='top'
            width = 7
        
        if self.charge_type == 'particle':
            if charge >0:
                label += ' Positive Particle'
            else:
                label += ' Negative Particle'
        else:
            if force:
                label += ' Wire'
            else:
                label += ' Current'

        # into and out of the page require special treatment since we
        # use special vector symbols in these cases
        if np.sum(np.abs(vector[:2])) > 0:
            self.ax.quiver(
                *list(-np.array(vector[:2])/2), 
                *list(vector[:2]), 
                color=color, 
                scale=1, scale_units='xy', 
                units = 'dots', width=width, label=label)
            rotation='horizontal'
            if vector[1]!=0:
                rotation='vertical'
        elif vector[2] < 0:
            self.ax.scatter([0],[0], marker='x', s=200,  facecolors=color, edgecolors = color, label=label)
        elif vector[2] > 0:
            self.ax.scatter([0],[0], marker=r'$\bigodot$', s=200, 
                            facecolors=color, edgecolors=color, label=label)
            
    def _draw_B_field(self, direction):
        '''
        Draws the B-field vector
        
        Args:
            direction:
                (list of ints) direction vector
        '''
        color='C1'
        label = 'Magnetic field'
        nvectors = 11

        # into and out of the page require special treatment since we
        # use special vector symbols in these cases. Also, up/down and
        # left/right need special treatment

        if direction[0] != 0:
            self.ax.quiver(
                np.full([nvectors], -direction[0]), 
                np.linspace(-1, 1, nvectors), 
                np.full([nvectors], direction[0]), 
                np.zeros([nvectors]),
                color=color, 
                scale=0.5, scale_units='x', label=label)
        elif direction[1] != 0:
            self.ax.quiver(
                np.linspace(-1, 1, nvectors), 
                np.full([nvectors], -direction[1]), 
                np.zeros([nvectors]),
                np.full([nvectors], direction[1]), 
                color=color, 
                scale=0.5, scale_units='y', label=label)
        elif direction[2] < 0:
            X, Y = np.meshgrid(np.linspace(-1, 1, nvectors), np.linspace(-1, 1, nvectors))
            self.ax.scatter(X,Y, marker='x', s=200, facecolors = color,edgecolors=color, label=label)
        elif direction[2] > 0:
            X, Y = np.meshgrid(np.linspace(-1, 1, nvectors), np.linspace(-1, 1, nvectors))
            self.ax.scatter(X, Y, marker=r'$\bigodot$', s=200, 
                            facecolors=color, edgecolors=color, label=label)


    def _guess(self, change):
        '''Update the student and let them know if they are right or not.

        '''
        self.output_widget.clear_output()
        with self.output_widget:
            if change['new']==self.correct:
                print('Correct!')
            else:
                print('Try again.')

    def _set_unknown(self, unknown_choice):
        '''Record the user's choice of what to look for and generate a new problem.
        '''
        self.unknown_choice = unknown_choice['new']
        self.next(None)