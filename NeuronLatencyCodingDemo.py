#--------------------------------------------------------------------------------------------
# Title:        Neuron Latency Coding Demo
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
animationSpeed      = 15               # Speed of the animation - the number of shifts on the x-axis per frame (this costs less data compared to changing FPS)
numFrames           = 600             # Number of frames in the animation - too few and it will start to repeat early
frameInterval       = 20               # Time interval between frames in milliseconds - sets the FPS of the animation?
saveDirectory       = 'F:/OneDrive_files/Newcastle University/Neuroprosthesis lab - General/Code - Python/Teaching simulations/LatencyCoding.gif'

# Action Potential variables
sineFrequency       = 1                # Frequency of the sine wave
AP_Duration         = 5                # Time period for the action potential (ms)
AP_PosAmplitude     = 4                # Positive amplitude of the action potential
AP_NegAmplitude     = -0.4             # Negative amplitude of the action potential
AP_PosWidth         = 0.35             # Positive width of the action potential
AP_NegWidth         = 0.75             # Negative width of the action potential
AP_threshold        = 100              # Threshold for the action potential

# --------------------------------------------------------------------------------------------
# Define the Functions
# --------------------------------------------------------------------------------------------

# we will represent the information as a sequence of pulses with increasing amplitude
def information_signal(decayCoeff):

    pulseInterval   = 800
    PulseTime       = 1200

    informationSig = []
    informationSigDecay = []

    #for i in range(len(t/1000)):
    for i in range(4):
        
        # individual components of the information signal
        zeroVals = np.zeros(int(pulseInterval))
        oneVals  = np.ones(int(PulseTime)) * ((i+1)/4)

        # decay the signal
        seq = np.linspace(0, PulseTime-1, PulseTime) 
        decaySig = np.exp(-decayCoeff*seq) * np.sqrt((i+1)/4)

        # combine for each repetition
        combined      = np.concatenate((zeroVals, oneVals))
        combinedDecay = np.concatenate((zeroVals, decaySig))

        # Combine to the output signal
        informationSig      = np.concatenate((informationSig, combined))
        informationSigDecay = np.concatenate((informationSigDecay, combinedDecay))

    # add zeros to the end of the signal
    informationSig = np.concatenate((informationSig, zeroVals))
    informationSigDecay = np.concatenate((informationSigDecay, zeroVals))

    return informationSig, informationSigDecay


# Convert the information signal to action potentials
def timeToFirstSpike(informationSig, singlePulse, AP_Duration, AP_threshold):
    
    # Convert the information signal to action potentials by obtaining the times of action potentials
    AP_Occurance = [0]
    integralValue = 0
    for i in range(len(informationSig)):

        if informationSig[i] > 0:

            # only integrate during the positive stimuli
            integralValue = integralValue + informationSig[i]
        else:
            # Resetn once the stimulus goes back to zero
            integralValue = 0

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
    lengthDiff = len(informationSig) - len(ApSig)
    if lengthDiff > 0:
        ApSig = np.concatenate((ApSig, np.zeros(lengthDiff)))

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
    t_updated = timeBase - i * animationSpeed
    
    # Update the line data which then gets plotted by the animation function
    line1.set_data(t_updated, informationSig)
    #line1.set_data(t_updated, informationSigDecay)
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
ax1.set_xlim(0, 2000)                    # Adjust x-axis limits to 0-500 (milliseconds)
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
ax2.set_xlim(0, 2000)                    # Adjust x-axis limits to 0-500 (milliseconds)
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
informationSig, informationSigDecay  = information_signal(decayCoeff = 0.001)

# Define a single action potential pulse
singlePulse = AP_SinglePulse(AP_Duration, AP_PosAmplitude, AP_NegAmplitude, AP_PosWidth, AP_NegWidth)

# Create the action potential series
AP_Stream = timeToFirstSpike(informationSigDecay, singlePulse, AP_Duration, AP_threshold)

# create the timebase
timeBase = np.linspace(0, len(informationSig)-1, len(informationSig))

# Plot the information on a static plot
#ax1.plot(Info_base, informationSig)
#ax1.plot(Info_base, informationSigDecay)
#ax2.plot(AP_tbase, AP_Stream)

# Create and plot the animation
ani = FuncAnimation(fig, animate, numFrames, interval=frameInterval, blit=True)

# save the animation
ani.save(saveDirectory, writer='pillow', fps=25)

# Display the animation
plt.show()