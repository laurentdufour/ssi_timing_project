import numpy as np
import matplotlib.pyplot as plt

import units

resolution_velo = 1. * units.mm
granularity_velo = 0.01 * units.mm

resolution_timing_detector = 10 * units.ps
granularity_timing_detector = 0.5 * units.ps

def get_velo_detector_response( txyz_at_detector ):
    '''
    Function which returns the detector response of
    the VELO, a measurement in "z"

        [t,x,y,z] -> number (measured z)
    '''
    true_position = txyz_at_detector[3]

    measured_position_without_granularity = np.random.normal( true_position, resolution_velo )

    return measured_position_without_granularity - measured_position_without_granularity % granularity_velo

def get_timing_detector_response (txyz_at_detector):
    '''
    Function which returns the time measurement

        [t,x,y,z] -> number (measured time)
    '''

    true_time = txyz_at_detector[0]
    measured_time_without_granularity = np.random.normal( true_time, resolution_timing_detector, 1 )[0]

    return measured_time_without_granularity - measured_time_without_granularity % granularity_timing_detector

def test_velo_detector_response( nTrials, tTrial, zTrial ):
    '''
    Runs the velo detector response 200 times and generates a 1D histogram
    with the response function.

    As an input, puts the (t,x,y,z) at (50,0,0,7)
    '''

    responseSet = [0] * nTrials

    for tryId in range(0, nTrials):
        responseSet[ tryId ] = get_velo_detector_response( [ tTrial, 0, 0, zTrial ] )

    hist, bins = np.histogram(responseSet, bins=40)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    plt.bar(center, hist, align='center', width=width)
    plt.title("Measured z (input position: %s)" % zTrial)

    plt.show()


def test_timing_detector_response( nTrials, tTrial, zTrial ):
    responseSet = [0] * nTrials

    for tryId in range(0, nTrials):
        responseSet[ tryId ] = get_timing_detector_response( [ tTrial, 0, 0, zTrial ] )

    hist, bins = np.histogram(responseSet, bins=40)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    plt.bar(center, hist, align='center', width=width)
    plt.title("Measured timing (input time: %s)" % tTrial)

    plt.plot(bins, 1/(resolution_timing_detector * np.sqrt(2 * np.pi)) *
              np.exp( - (bins - tTrial)**2 / (2 * resolution_timing_detector**2) ),
          linewidth=2, color='r')

    plt.show()

if __name__ == '__main__':
    test_velo_detector_response( 3000, 5, 7)
    test_timing_detector_response( 3000, 5, 7)