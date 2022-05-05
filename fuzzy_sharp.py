import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import Antecedent, Consequent, Rule
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

vel = Antecedent(np.linspace(0, 10, 100), 'vel')
dist = Antecedent(np.linspace(0, 8, 100), 'dist')
new_vel = Consequent(np.linspace(-2, 10, 100), 'new_vel')

vel.automf(3, names=['l', 'm', 'h'])

dist['l'] = fuzz.sigmf(dist.universe, 0.8, -15)
dist['h'] = fuzz.sigmf(dist.universe, 1, 15)

new_vel['l'] = fuzz.trimf(new_vel.universe, [-2, 0, 2])
new_vel['m'] = fuzz.trimf(new_vel.universe, [0, 2, 4])
new_vel['h'] = fuzz.trapmf(new_vel.universe, [9, 9.5, 10, 10])

rules = [
    Rule(dist['h'] & (vel['l']), new_vel['m']),
    Rule(dist['h'] & (vel['m'] | vel['h']), new_vel['h']),

    Rule(dist['l'], new_vel['l']),
]

tank_ctrl = ctrl.ControlSystem(rules)
tank_system = ctrl.ControlSystemSimulation(tank_ctrl)


def get_new_sharp_velocity(velocity, distance):
    tank_system.input['vel'] = velocity
    tank_system.input['dist'] = distance
    tank_system.compute()
    new_velocity = tank_system.output['new_vel']
    if new_velocity < 0.1:
        return 0
    return new_velocity


def plot_diagram():
    distances = np.linspace(0, 8, 80)

    fig, ax = plt.subplots()
    velocities = [get_new_sharp_velocity(5, d) for d in distances]
    line, = plt.plot(distances, velocities)
    ax.set_xlabel('Distance')
    ax.set_ylabel('New velocity')
    ax.set_title('Fuzzy model visualization')
    ax.grid()
    ax.set_ylim([0, 10])
    fig.show()

    plt.subplots_adjust(left=0.20, bottom=0.15)

    # velocity slider
    ax_vel = plt.axes([0.06, 0.15, 0.0225, 0.73])
    vel_slider = Slider(
        ax=ax_vel,
        label='Velocity',
        valmin=0,
        valmax=9.9,
        valinit=5,
        orientation='vertical',
    )

    def update(val):
        cur_vel = vel_slider.val
        new_vel = [get_new_sharp_velocity(cur_vel, d) for d in distances]
        line.set_ydata(new_vel)
        fig.canvas.draw_idle()

    vel_slider.on_changed(update)
    plt.show()


if __name__ == '__main__':
    dist.view()
    vel.view()
    new_vel.view()
    plot_diagram()
    plt.show()
