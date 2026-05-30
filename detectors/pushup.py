from .base import BaseDetector, LEFT_ANKLE, LEFT_ELBOW, LEFT_HIP, LEFT_SHOULDER, LEFT_WRIST, RIGHT_ANKLE, RIGHT_ELBOW, RIGHT_HIP, RIGHT_SHOULDER, RIGHT_WRIST


class PushUpDetector(BaseDetector):
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

        left_body = self._angle(
            landmarks[LEFT_SHOULDER],
            landmarks[LEFT_HIP],
            landmarks[LEFT_ANKLE],
        )
        right_body = self._angle(
            landmarks[RIGHT_SHOULDER],
            landmarks[RIGHT_HIP],
            landmarks[RIGHT_ANKLE],
        )
        body_angle = self._avg([left_body, right_body])

        if elbow_angle <= 95:
            self._phase = "down"
        elif elbow_angle >= 160 and self._phase == "down":
            self.reps += 1
            self._phase = "up"

        if body_angle >= 155:
            body_alignment = "Good Form"
        else:
            body_alignment = "Poor Form"

        hip_center_y = (landmarks[LEFT_HIP].y + landmarks[RIGHT_HIP].y) / 2
        shoulder_center_y = (landmarks[LEFT_SHOULDER].y + landmarks[RIGHT_SHOULDER].y) / 2

        if hip_center_y > shoulder_center_y + 0.08:
            hip_status = "SAGGING"
        elif hip_center_y < shoulder_center_y - 0.12:
            hip_status = "PIKED UP"
        else:
            hip_status = "ALIGNED"

        metrics = {
            "reps": self.reps,
            "elbow_angle": round(elbow_angle, 1),
            "body_alignment": body_alignment,
            "hip_status": hip_status,
        }

        if body_alignment == "Poor Form":
            metrics["issue"] = "The body is not staying straight during the push-up."
        elif hip_status == "SAGGING":
            metrics["issue"] = "The hips are sagging too low during the push-up."
        elif hip_status == "PIKED UP":
            metrics["issue"] = "The hips are too high. Keep the body in a straight line."

        return metrics
