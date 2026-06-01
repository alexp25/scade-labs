import time
from cc_wrapper import cc_wrapper as w

m = w.main_CC_design()

t_switch = 200

for cycle in range(1000):

    m.inputs.accel = 70.0 if cycle < t_switch else 0.0
    m.inputs.brake = 0.0
    
    # activate cruise control 50 km/h
    m.inputs.on = cycle >= t_switch
    m.inputs.res = cycle == t_switch
    
    m.inputs.set_point = 50.0

    m.cycle()

    print(
        cycle,
        "speed:", str(int(m.outputs._speed_out.value)),
        "gear:", str(int(m.outputs._gear_out.value)),
        "rpm:", str(int(m.outputs._rpm_out.value)),
        "cc:", str(m.inputs._on)
    )
    
    time.sleep(0.05)
