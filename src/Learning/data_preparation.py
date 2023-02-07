import glob
import numpy as np
from traj_characterizor import TrajectoryCharacterizor

PATH_TO_DATA = './data/'  # not existing yet


def load_data():
    """
    Wildcard search for .npz trajectory files in the PATH_TO_DATA directory.
    Applying trajectory characterization
    :return: ndarray of tuples (velocity, release_point)
    """
    # Load joint positions data for each trajectory
    raw_data = np.array([np.load(file, allow_pickle=True)['traj']
                        for file in glob.glob(PATH_TO_DATA + '*.npz')])
    print("raw data : ", raw_data.shape)

    # Characterize each trajectory
    data = np.array([TrajectoryCharacterizor(raw, reachy).process() for raw in raw_data])
    print("data : ", data.shape)
    return data


if __name__ == '__main__':
    from reachy_sdk import ReachySDK
    reachy = ReachySDK('localhost')

    load_data()
