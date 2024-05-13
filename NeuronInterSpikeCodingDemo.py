#--------------------------------------------------------------------------------------------
# Title:        Neuron Inter-spike Coding Demo
# Description:  This script demonstrates the concept of latency coding in neurons as part of 
#               the EEE8116 Bioelectronics MSc/MEng module at Newcastle University.
# Author:       Prof. Patrick Degenaar
# Date:         2024-05-13
# Version:      1.0
# Usage:        Run the script and observe the animation of the information signal and the
#               action potential signal.
# License:      Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
#--------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --------------------------------------------------------------------------------------------
# Define the parameters
# --------------------------------------------------------------------------------------------

# animation variables
animationSpeed      = 4
numFrames           = 1000             # Number of frames in the animation - too few and it will start to repeat early
frameInterval       = 5               # Time interval between frames in milliseconds - sets the FPS of the animation?
saveDirectory       = 'F:/OneDrive_files/Newcastle University/Neuroprosthesis lab - General/Code - Python/Teaching simulations/InterSpikeCoding.gif'

# Action Potential variables
sineFrequency       = 1.5                # Frequency of the sine wave
AP_Duration         = 5                # Time period for the action potential (ms)
AP_PosAmplitude     = 4                # Positive amplitude of the action potential
AP_NegAmplitude     = -0.4             # Negative amplitude of the action potential
AP_PosWidth         = 0.35             # Positive width of the action potential
AP_NegWidth         = 0.75             # Negative width of the action potential
AP_threshold        = 30                # Threshold for the action potential

# Define the time period between pulses
timeBase    = np.linspace(0, 20000, 20001)                # The fundamental time base for the simulation
AP_dT       = np.linspace(0, AP_Duration, AP_Duration)  # pulse period for the action potential (ms)

# --------------------------------------------------------------------------------------------
# Define the Functions
# --------------------------------------------------------------------------------------------

# we will represent the information signal as a simple sine wave - This can be changed to any
# arbitrary function that represents an information signal
def information_signal(t, F):

    informationSig = 0.5 + (0.5 * np.sin(2 * np.pi * F * t/1000))  # Frequency of 10 Hz

    return informationSig


# Convert the information signal to action potentials using an integrate and fire method
def integrate_and_fire(informationSig, singlePulse, AP_Duration, AP_threshold):
    
    # Convert the information signal to action potentials by obtaining the times of action potentials
    AP_Occurance = [0]
    integralValue = 0
    for i in range(len(informationSig)):

        # Integrate the information signal
        integralValue = integralValue + informationSig[i]
        
        # Check to see if the integral value has reached the threshold
        if integralValue >= AP_threshold:
            AP_Occurance = np.concatenate((AP_Occurance, [i]))

            integralValue = 0   # reset the integral value

    # Start with a zero action potential signal from which to time subsequent pulses
    ApSig = [0]   
    
    # Now create the action potential signal
    for i in range(len(AP_Occurance)-1):
        
        # Calculate period between pulses
        dT = AP_Occurance[i+1] - AP_Occurance[i] # period between pulses in milliseconds 
        t_remaining = dT - AP_Duration           # calculate the remaining time period
        if AP_Duration < 0:                      # if the remaining time period is negative, set it to zero
            AP_Duration = 0
        interAPVals = np.zeros(int(t_remaining)) # set y vals to zero in the remaining time period
        
        # now append the interval zeros to the action potential signal
        ApSig = np.concatenate((ApSig, interAPVals))

        # now add the next action potential pulse
        ApSig = np.concatenate((ApSig, singlePulse))

        # make sure the action potential signal is the same length as the information signal
        '''lengthDiff = len(informationSig) - len(ApSig)
        if lengthDiff > 0:
            ApSig = np.concatenate((ApSig, np.zeros(lengthDiff)))'''

    return ApSig 


# Define the Action Potential pulse function
# This function uses a short Gaussian pulse for both positive and negative phases of the action potential
def AP_SinglePulse(AP_Duration, AP_PosAmplitude, AP_NegAmplitude, AP_PosWidth, AP_NegWidth):

    # time sequence for the action potential (ms)
    AP_timeBase       = np.linspace(0, AP_Duration, AP_Duration)   

    # Create the action potential pulse from positive and negative Gaussian pulses
    pos_pulse = AP_PosAmplitude * np.exp(-0.5 * ((AP_timeBase - 2) / AP_PosWidth)**2)
    neg_pulse = AP_NegAmplitude * np.exp(-0.5 * ((AP_timeBase - 3) / AP_NegWidth)**2)
    return pos_pulse + neg_pulse

   
# Animation function
# This function will be called for each frame of the animation
# It simply shifts the time values to the left by a certain amount
def animate(i):

    # Shift the time values to the left by a certain amount, according to the animation speed
    t_sinUpdate  = timeBase - i * animationSpeed
    t_updated    = AP_tbase - i * animationSpeed
    
    # Update the line data which then gets plotted by the animation function
    line1.set_data(t_sinUpdate, informationSig)
    line2.set_data(t_updated, AP_Stream)

    return line1, line2

# --------------------------------------------------------------------------------------------
# Set up the figure and axis
# --------------------------------------------------------------------------------------------
#fig,(ax1, ax2) = plt.subplots(2, 1)    # Create two subplots
fig = plt.figure(figsize=(8, 6))

# Create a subplot and plot some data
(ax1, ax2) = fig.subplots(2, 1)

#fig, ax = plt.subplots(figsize=(8, 6))
#ax1.set_xlabel('Time (ms)')             # Set x-axis label
#ax1.set_title('Information state')      # Set plot title
ax1.set_ylabel('Information value')      # Set y-axis label
ax1.set_xlim(0, 1000)                    # Adjust x-axis limits to 0-500 (milliseconds)
ax1.set_ylim(0, 1)                       # Adjust y-axis limits to -1.5 to 1.5 (arbitrary units)

# Remove the spines (figure box)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(True)
ax1.set_xticks([])                       # Hide x-axis ticks and labels
ax1.set_yticks([])                       # Hide x-axis ticks and labels

#ax2.set_title('Cosine Wave Animation')  # Set the title for the bottom plot
ax2.set_xlabel('time (ms)')              # Set the x-axis label for the bottom plot
ax2.set_ylabel('Amplitude')              # Set the y-axis label for the bottom plot
ax2.set_xlim(0, 1000)                    # Adjust x-axis limits to 0-500 (milliseconds)
ax2.set_ylim(-1.25, 1.25)                # Adjust y-axis limits to -1.5 to 1.5 (arbitrary units)

# Remove the spines (figure box)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(True)
ax2.spines['left'].set_visible(True)
ax2.set_yticks([])                       # Hide x-axis ticks and labels

line1, = ax1.plot([], [], color='red',linestyle='dotted', lw=2)  # Create a line object
line2, = ax2.plot([], [], color='black', lw=2)                   # Create a line object

# --------------------------------------------------------------------------------------------
# Run the program
# --------------------------------------------------------------------------------------------

# Define the information signal
informationSig = information_signal(timeBase, sineFrequency)

# Define a single action potential pulse
singlePulse = AP_SinglePulse(AP_Duration, AP_PosAmplitude, AP_NegAmplitude, AP_PosWidth, AP_NegWidth)

# Create the action potential series
AP_Stream = integrate_and_fire(informationSig, singlePulse, AP_Duration, AP_threshold)

# Reset the timebase to the information signal
timeBase = np.linspace(0, len(informationSig)-1, len(informationSig))

AP_tbase = np.linspace(0, len(AP_Stream)-1, len(AP_Stream))

# Create the animation
ani = FuncAnimation(fig, animate, numFrames, interval=frameInterval, blit=True)

# save the animation
#ani.save(saveDirectory, writer='pillow', fps=25)

# Display the animation
plt.show()