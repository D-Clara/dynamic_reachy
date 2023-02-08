from reachy_sdk import ReachySDK

def turn_off(reachy=None):
    if reachy==None:
        reachy = ReachySDK('localhost')
    reachy.turn_off_smoothly('reachy')

if __name__ == '__main__':
    turn_off(ReachySDK('localhost'))
    