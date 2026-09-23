import time
from cc_wrapper.cc_wrapper import cruise_control_CC_design

# cc_wrapper.cc_wrapper only exposes the CC_design controller (class
# cruise_control_CC_design, inputs v_speed/brake/accel/on/res/set_point,
# output throttle) - it does not include the Car_design plant, so there is
# no generated vehicle to close the loop against. v_speed is therefore
# driven here by a small ad hoc Python integrator for demo purposes only;
# it is not the real Car_design.swan model (see evaluate_cc_full_report.py, which
# instead replays pre-computed v_speed traces from scenarios/*.csv).
m = cruise_control_CC_design()

t_switch = 200
v_speed = 0.0

for cycle in range(1000):

    m.inputs.accel = 70.0 if cycle < t_switch else 0.0
    m.inputs.brake = 0.0

    # activate cruise control 110 km/h
    m.inputs.on = cycle >= t_switch
    m.inputs.res = cycle == t_switch

    m.inputs.set_point = 110.0
    m.inputs.v_speed = v_speed

    m.cycle()

    # simplified plant: throttle accelerates, drag decelerates
    v_speed = max(0.0, v_speed + 0.02 * m.outputs.throttle - 0.01 * v_speed)

    print(
        cycle,
        "speed:", str(int(v_speed)),
        "throttle:", str(int(m.outputs.throttle)),
        "cc:", str(m.inputs.on)
    )

    time.sleep(0.05)
