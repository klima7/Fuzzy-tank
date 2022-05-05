import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import Antecedent, Consequent, Rule
import matplotlib.pyplot as plt

vel = Antecedent(np.linspace(0, 10, 40), 'vel')
dist = Antecedent(np.linspace(0, 8, 80), 'dist')
new_vel = Consequent(np.linspace(-0.5, 10, 80), 'new_vel')

vel.automf(3, names=['l', 'm', 'h'])

dist['zero'] = fuzz.trapmf(dist.universe, [0, 0, 1, 1])
dist['l'] = fuzz.trapmf(dist.universe, [1, 1, 1.5, 2.5])
dist['m'] = fuzz.trapmf(dist.universe, [1.5, 2.5, 3, 4])
dist['h'] = fuzz.trapmf(dist.universe, [3, 4, 10, 10])

# new_vel.automf(3, names=['l', 'm', 'h'])
new_vel['zero'] = fuzz.trapmf(new_vel.universe, [-0.5, -0.5, 0.5, 0.5])
new_vel['l'] = fuzz.trapmf(new_vel.universe, [0.5, 0.5, 2, 4])
new_vel['m'] = fuzz.trimf(new_vel.universe, [2, 4, 6])
new_vel['h'] = fuzz.trapmf(new_vel.universe, [4, 6, 10, 10])

rules = [
    Rule(dist['h'] & dist['m'], new_vel['h']),
    Rule(dist['l'], new_vel['m']),
    Rule(dist['zero'], new_vel['zero']),
]

tank_ctrl = ctrl.ControlSystem(rules)
tank_system = ctrl.ControlSystemSimulation(tank_ctrl)


def get_new_sharp_velocity(velocity, distance):
    # tank_system.input['vel'] = velocity
    tank_system.input['dist'] = distance
    tank_system.compute()
    new_velocity = tank_system.output['new_vel']
    if new_velocity < 0.1:
        return 0
    return new_velocity


# quick test
if __name__ == '__main__':
    print(get_new_sharp_velocity(velocity=5, distance=0.1))
