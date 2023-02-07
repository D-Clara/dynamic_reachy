from flask import Flask, render_template, request, redirect
from reproduce_traj import reproduce_traj
import atexit
from turn_off import turn_off


app = Flask(__name__)
app.template_folder = 'template'

trajectories = {
    '1': '/home/reachy/dynamic_reachy/traj/2023-01-30_17:41:16_test.npz',
	'2': '/home/reachy/dynamic_reachy/traj/2023-02-01_08:28:47_test.npz',
	'3': '/home/reachy/dynamic_reachy/traj/2023-02-01_08:27:25_test.npz',
	'4': '/home/reachy/dynamic_reachy/traj/2023-02-01_08:26:32_test.npz',
	'5': '/home/reachy/dynamic_reachy/traj/2023-02-01_16:14:07_test.npz',
	'6': '/home/reachy/dynamic_reachy/traj/2023-02-01_08:29:04_test.npz'
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        param = request.form['param']
        run_script(param)
        return redirect('/')
    return render_template('index.html')


def run_script(param):
    reproduce_traj(trajectories[param], reachy, preprocessing=True)
    return redirect('/')


def cleanup_func():
    turn_off(reachy)
    print("Api is closed")


if __name__ == '__main__':
    from reachy_sdk import ReachySDK
    reachy = ReachySDK('localhost')
    atexit.register(cleanup_func)
    app.run()
