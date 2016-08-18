import numpy as np
import matplotlib.pyplot as plt

import units

"""
 Settings for the VELO detector
"""
velo = {"resolution": 1 * units.mm,
        "granularity": 0.01 * units.mm,
        "position_z": 0 * units.meter}

"""
 Settings for the TIMING detector
"""
timing_detector = {"resolution": 10 * units.ps,
                   "granularity": 0.5 * units.ps,
                   "position_z": 5 * units.meter}

def get_velo_detector_response( txyz_at_detector ):
    '''
    Function which returns the detector response of
    the VELO, a measurement in "z"

        [t,x,y,z] -> number (measured z)
    '''
    true_position = txyz_at_detector[3]

    measured_position_without_granularity = np.random.normal( true_position, velo["resolution"] )

    return measured_position_without_granularity - measured_position_without_granularity % velo["granularity"]

def get_timing_detector_response (txyz_at_detector):
    '''
    Function which returns the time measurement

        [t,x,y,z] -> number (measured time)
    '''

    true_time = txyz_at_detector[0]
    measured_time_without_granularity = np.random.normal( true_time, timing_detector["resolution"], 1 )[0]

    return measured_time_without_granularity - measured_time_without_granularity % timing_detector["granularity"]

def test_detector_response( detector_response_function, detector_name, n_trials, t_trial, z_trial ):
    '''
    Runs the detector response 200 times and generates a 1D histogram
    with the response function.
    '''

    responseSet = [0] * n_trials

    for tryId in range(0, n_trials):
        responseSet[ tryId ] = detector_response_function( [ t_trial, 0, 0, z_trial ] )

    hist, bins = np.histogram(responseSet, bins=40)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    plt.bar(center, hist, align='center', width=width)
    plt.title( "Measured {} response [input position: ({}, 0, 0, {})]". format(detector_name, t_trial, z_trial) )

    plt.show()

if __name__ == '__main__':
    test_detector_response( get_velo_detector_response, "velo", 3000, 5, 7)
    test_detector_response( get_timing_detector_response, "timing", 3000, 5, 7)