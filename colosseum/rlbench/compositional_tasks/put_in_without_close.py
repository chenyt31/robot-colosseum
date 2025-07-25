from typing import List, Tuple

import numpy as np
from pyrep.objects.dummy import Dummy
from pyrep.objects.joint import Joint
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.task import Task


class PutInWithoutClose(Task):

    def init_task(self) -> None:
        self._options = ['bottom', 'middle', 'top']
        self._anchors = [Dummy('waypoint_anchor_%s' % opt)
                         for opt in self._options]
        self._joints = [Joint('drawer_joint_%s' % opt)
                        for opt in self._options]
        self._mark = Dummy('mark')
        self._item = Shape('item')
        self.register_graspable_objects([self._item])

    def init_episode(self, index) -> List[str]:
        option = self._options[index]
        anchor = self._anchors[index]
        self._mark.set_position(anchor.get_position())
        success_sensor = ProximitySensor('success_' + option)
        self.register_success_conditions(
            [DetectedCondition(self._item, success_sensor)])

        # formatted_desc = {
        #     "vanilla": [
        #         f"put the block in the {option} drawer"
        #     ],
        #     "oracle_half": [
        #         f"grasp the {option} drawer handle\npull the {option} drawer open\npick up the block on the drawer's surface\nplace the block in the {option} drawer"
        #     ],
        #     "oracle_full": [
        #         f"open the {option} drawer\nput the block in the {option} drawer"
        #     ]
        # }
        return [
            f"grasp the {option} drawer handle\npull the {option} drawer open\npick up the block on the drawer's surface\nplace the block in the {option} drawer"
        ]

    def variation_count(self) -> int:
        return 3

    def base_rotation_bounds(self) -> Tuple[List[float], List[float]]:
        return [0, 0, - np.pi / 8], [0, 0, np.pi / 8]
