from .base import BaseDetector, LEFT_ANKLE, LEFT_HIP, LEFT_KNEE, LEFT_SHOULDER, RIGHT_ANKLE, RIGHT_HIP, RIGHT_KNEE, RIGHT_SHOULDER


class LungesDetector(BaseDetector):
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

        front_knee_angle = min(left_knee, right_knee)

        left_torso = self._angle(
            landmarks[LEFT_SHOULDER],
            landmarks[LEFT_HIP],
            landmarks[LEFT_KNEE],
        )
        right_torso = self._angle(
            landmarks[RIGHT_SHOULDER],
            landmarks[RIGHT_HIP],
            landmarks[RIGHT_KNEE],
        )
        torso_angle = self._avg([left_torso, right_torso])

        hip_delta = abs(landmarks[LEFT_HIP].x - landmarks[RIGHT_HIP].x)
        shoulder_delta = abs(landmarks[LEFT_SHOULDER].x - landmarks[RIGHT_SHOULDER].x)

        if front_knee_angle <= 95:
            self._phase = "down"
        elif front_knee_angle >= 160 and self._phase == "down":
            self.reps += 1
            self._phase = "up"

        if hip_delta > 0.20 or shoulder_delta > 0.20:
            balance_status = "OFF BALANCE"
        else:
            balance_status = "STABLE"

        metrics = {
            "reps": self.reps,
            "front_knee_angle": round(front_knee_angle, 1),
            "torso_angle": round(torso_angle, 1),
            "balance_status": balance_status,
        }

        if balance_status == "OFF BALANCE":
            metrics["issue"] = "Balance is off during the lunge. Keep the feet hip-width apart and steady."

        return metrics
