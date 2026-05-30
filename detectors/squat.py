from .base import BaseDetector, LEFT_ANKLE, LEFT_HIP, LEFT_KNEE, LEFT_SHOULDER, RIGHT_ANKLE, RIGHT_HIP, RIGHT_KNEE, RIGHT_SHOULDER


class SquatDetector(BaseDetector):
    def process(self, landmarks):
        left_knee = self._angle(
            landmarks[LEFT_HIP],
            landmarks[LEFT_KNEE],
            landmarks[LEFT_ANKLE],
        )
        right_knee = self._angle(
            landmarks[RIGHT_HIP],
            landmarks[RIGHT_KNEE],
            landmarks[RIGHT_ANKLE],
        )
        knee_angle = self._avg([left_knee, right_knee])

        left_back = self._angle(
            landmarks[LEFT_SHOULDER],
            landmarks[LEFT_HIP],
            landmarks[LEFT_KNEE],
        )
        right_back = self._angle(
            landmarks[RIGHT_SHOULDER],
            landmarks[RIGHT_HIP],
            landmarks[RIGHT_KNEE],
        )
        back_angle = self._avg([left_back, right_back])

        if knee_angle <= 95:
            depth_status = "DEEP"
            self._phase = "down"
        elif knee_angle <= 120:
            depth_status = "GOOD DEPTH"
        else:
            depth_status = "TOO HIGH"

        if self._phase == "down" and knee_angle >= 160:
            self.reps += 1
            self._phase = "up"

        metrics = {
            "reps": self.reps,
            "knee_angle": round(knee_angle, 1),
            "back_angle": round(back_angle, 1),
            "depth_status": depth_status,
        }

        if depth_status == "TOO HIGH":
            metrics["issue"] = "The squat is too shallow. Lower your hips a little more."
        elif back_angle < 135:
            metrics["issue"] = "The back is leaning too far forward during the squat."

        return metrics
