from .base import BaseDetector, LEFT_ELBOW, LEFT_HIP, LEFT_KNEE, LEFT_SHOULDER, LEFT_WRIST, RIGHT_ELBOW, RIGHT_HIP, RIGHT_KNEE, RIGHT_SHOULDER, RIGHT_WRIST


class BicepsCurlDetector(BaseDetector):
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

        left_drift = abs(landmarks[LEFT_ELBOW].x - landmarks[LEFT_SHOULDER].x)
        right_drift = abs(landmarks[RIGHT_ELBOW].x - landmarks[RIGHT_SHOULDER].x)
        drift = max(left_drift, right_drift)

        torso_angle = self._avg([
            self._angle(
                landmarks[LEFT_SHOULDER],
                landmarks[LEFT_HIP],
                landmarks[LEFT_KNEE],
            ),
            self._angle(
                landmarks[RIGHT_SHOULDER],
                landmarks[RIGHT_HIP],
                landmarks[RIGHT_KNEE],
            ),
        ])

        if elbow_angle <= 60:
            self._phase = "up"
        elif elbow_angle >= 150 and self._phase == "up":
            self.reps += 1
            self._phase = "down"

        shoulder_status = "STABLE"
        if drift > 0.18:
            shoulder_status = "ELBOW DRIFTING"

        swing_status = "CONTROLLED"
        if torso_angle < 150 or abs(landmarks[LEFT_SHOULDER].x - landmarks[LEFT_HIP].x) > 0.20:
            swing_status = "SWINGING"

        metrics = {
            "reps": self.reps,
            "elbow_angle": round(elbow_angle, 1),
            "shoulder_status": shoulder_status,
            "swing_status": swing_status,
        }

        if swing_status == "SWINGING":
            metrics["issue"] = "The torso is swinging during the curl. Keep the body still."
        elif shoulder_status == "ELBOW DRIFTING":
            metrics["issue"] = "The elbow is drifting away from the side during the curl."

        return metrics
