MOTOR = None
ENCODER = None


def get_robot_hooks(m, e):
    global MOTOR, ENCODER
    MOTOR = m
    ENCODER = e


# MOTOR.set(value)
#     [-1, 1]

# ENCODER.get_position()

def setup():
    pass


def loop():
    pass
