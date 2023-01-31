# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from std_msgs.msg import String
# from std_msgs.msg import int32
# from std_msgs.msg import uint8
import numpy as np


class MinimalPublisher(Node):

    def __init__(self, param_1, param_2):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(
            SetPosition, '/set_position', 10)
        timer_period = param_1  # seconds
        self.sig = param_2  # input signals
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):

        msg = SetPosition()
        if self.i == 0:
            for j in range(self.sig.shape[0]):  # per motor signal
                msg.id.append(j+1)
                msg.position.append(0)
        else:
            for j in range(self.sig.shape[0]):  # per motor signal
                msg.id.append(j+1)
                msg.position.append(self.sig[j][self.i-1])
                self.get_logger().info('Motor %d: %s' %
                                       (j+1, type(int(self.sig[j][self.i-1]))))
        self.i += 1
        if (self.i >= self.sig.shape[1]):
            self.i = 0
        self.publisher_.publish(msg)
        # self.get_logger().info(msg)


def APRBS(a_range, b_range, nstep):
    # random signal generation
    # range for amplitude
    a = np.random.rand(nstep) * (a_range[1]-a_range[0]) + a_range[0]
    # range for frequency
    b = np.random.rand(nstep) * (b_range[1]-b_range[0]) + b_range[0]
    b = np.round(b)
    b = b.astype(int)

    b[0] = 0

    for i in range(1, np.size(b)):
        b[i] = b[i-1]+b[i]

    # Random Signal
    i = 0
    random_signal = np.zeros(nstep)
    while b[i] < np.size(random_signal):
        k = b[i]
        random_signal[k:] = a[i]
        i = i+1

    # PRBS
    a = np.zeros(nstep)
    j = 0
    while j < nstep:
        a[j] = 5
        a[j+1] = -5
        j = j+2

    i = 0
    prbs = np.zeros(nstep)
    while b[i] < np.size(prbs):
        k = b[i]
        prbs[k:] = a[i]
        i = i+1
    return random_signal


def multiple_aprbs(a_range, b_range, nstep, ninput, type='float', factor=1.0):
    u = np.zeros([ninput, nstep])
    for i in range(ninput):
        u[i, :] = APRBS(a_range, b_range, nstep)*factor
    if type == 'int':
        u = u.astype('int32')
    return u


def main(args=None):
    rclpy.init(args=args)

    ninput = 3
    nstep = 100
    a_range = [0, 4]
    b_range = [0, 5]
    # form the random signal to motors
    u = multiple_aprbs(a_range, b_range, nstep,
                       ninput, type='int', factor=1000.0)

    minimal_publisher = MinimalPublisher(0.5, u)

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
