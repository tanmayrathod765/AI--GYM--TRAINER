from .base import BaseDetector, LEFT_ANKLE, LEFT_ELBOW, LEFT_HIP, LEFT_SHOULDER, LEFT_WRIST, RIGHT_ANKLE, RIGHT_ELBOW, RIGHT_HIP, RIGHT_SHOULDER, RIGHT_WRIST


class ShoulderPressDetector(BaseDetector):
    def process(self, landmarks):
        left_elbow = self._angle(
            landmarks[LEFT_SHOULDER],
            landmarks[LEFT_ELBOW],
            landmarks[LEFT_WRIST],
        )
        right_elbow = self._angle(
            landmarks[RIGHT_SHOULDER],
            landmarks[RIGHT_ELBOW],
            landmarks[RIGHT_WRIST],
        )
        elbow_angle = self._avg([left_elbow, right_elbow])

        torso_angle = self._avg([
            self._angle(
                landmarks[LEFT_SHOULDER],
                landmarks[LEFT_HIP],
                landmarks[LEFT_ANKLE],
            ),
            self._angle(
                landmarks[RIGHT_SHOULDER],
                landmarks[RIGHT_HIP],
                landmarks[RIGHT_ANKLE],
            ),
        ])

        if elbow_angle <= 95:
            self._phase = "down"
        elif elbow_angle >= 160 and self._phase == "down":
            self.reps += 1
            self._phase = "up"

        if elbow_angle >= 165:
            extension_status = "FULL EXTENSION"
        elif elbow_angle >= 140:
            extension_status = "NEAR LOCKOUT"
        else:
            extension_status = "BENT"

        if torso_angle < 150:
            back_arch_status = "Excessive Arch"
        elif torso_angle < 170:
            back_arch_status = "Slight Arch"
        else:
            back_arch_status = "Stable"

        metrics = {
            "reps": self.reps,
            "elbow_angle": round(elbow_angle, 1),
            "extension_status": extension_status,
            "back_arch_status": back_arch_status,
        }

        if back_arch_status == "Excessive Arch":
            metrics["issue"] = "The lower back is arching too much during the press. Brace the core."
        elif back_arch_status == "Slight Arch":
            metrics["issue"] = "There is a slight back arch. Keep the ribs down and core tight."

        return metrics
