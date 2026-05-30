import math

LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28


class BaseDetector:
    def __init__(self):
        self.reps = 0
        self._phase = "up"

    def _landmark(self, landmarks, index):
        return landmarks[index]

    def _angle(self, a, b, c):
        ax, ay = a.x, a.y
        bx, by = b.x, b.y
        cx, cy = c.x, c.y

        radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
        angle = abs(math.degrees(radians))
        if angle > 180:
            angle = 360 - angle
        return angle

    def _avg(self, values):
        values = [value for value in values if value is not None]
        return sum(values) / len(values) if values else 0
