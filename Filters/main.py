import cv2
import mediapipe as mp

from hand_tracking import INDEX_TIP, THUMB_TIP
from geometry import render_portal, portal_width, ClosingGestureDetector
from filters import FILTERS


def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Could not open the camera. Check the camera index or permissions.."
        )

    filter_index = 0
    closing_detector = ClosingGestureDetector()

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        left_hand = None
        right_hand = None

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                raw_label = handedness.classification[0].label
                label = "Right" if raw_label == "Left" else "Left"

                if label == "Left":
                    left_hand = hand_landmarks
                else:
                    right_hand = hand_landmarks

        if left_hand is not None and right_hand is not None:
            lm_left = left_hand.landmark
            lm_right = right_hand.landmark

            p1 = (lm_left[INDEX_TIP].x * w, lm_left[INDEX_TIP].y * h)
            p2 = (lm_left[THUMB_TIP].x * w, lm_left[THUMB_TIP].y * h)
            p3 = (lm_right[INDEX_TIP].x * w, lm_right[INDEX_TIP].y * h)
            p4 = (lm_right[THUMB_TIP].x * w, lm_right[THUMB_TIP].y * h)

            width = portal_width(p1, p2, p3, p4)

            if closing_detector.update(width, w):
                filter_index = (filter_index + 1) % len(FILTERS)

            frame = render_portal(frame, p1, p2, p3, p4, FILTERS[filter_index])

        cv2.imshow(" ", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:  # 27 is ESC key
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()