from ultralytics import YOLO
import cv2
import serial
import time
import os

arduino = serial.Serial('COM6', 9600)

# Wait for Arduino initialization
time.sleep(2)

# =====================================
# SYSTEM ANALYZING
# =====================================

arduino.write(b"ANALYZING\n")

# =====================================
# LOAD YOLO MODEL
# =====================================

model = YOLO("yolov8n.pt")

# =====================================
# LOAD TRAFFIC VIDEO
# =====================================

cap = cv2.VideoCapture("traffic_video.mp4")

# =====================================
# VEHICLE CLASS IDS
# =====================================

# car = 2
# motorcycle = 3
# bus = 5
# truck = 7

vehicle_classes = [2, 3, 5, 7]



# =====================================
# AUTOMATIC ROI
# =====================================

# =====================================
# USER ROI SELECTION
# =====================================

ret, first_frame = cap.read()

if not ret:
    print("Unable to read video")
    exit()

# Show original frame first
cv2.namedWindow(
    "Select Traffic ROI",
    cv2.WINDOW_NORMAL
)

cv2.imshow(
    "Select Traffic ROI",
    first_frame
)

cv2.waitKey(1)

print("\nDraw ROI using mouse")
print("Press ENTER after selecting ROI")
print("Press C to cancel and redraw\n")

roi = cv2.selectROI(
    "Select Traffic ROI",
    first_frame,
    showCrosshair=True,
    fromCenter=False
)

roi_x1 = int(roi[0])
roi_y1 = int(roi[1])

roi_x2 = int(roi[0] + roi[2])
roi_y2 = int(roi[1] + roi[3])

cv2.destroyWindow(
    "Select Traffic ROI"
)

# Restart video from beginning
cap.set(
    cv2.CAP_PROP_POS_FRAMES,0
    
)
# =====================================
# ROI AREA
# =====================================

roi_area = (
    (roi_x2 - roi_x1)
    *
    (roi_y2 - roi_y1)
)

# =====================================
# SIGNAL REFERENCE LINE
# =====================================

signal_line_y = roi_y2

# =====================================
# EXPONENTIAL SMOOTHING FACTOR
# =====================================

alpha = 0.05

# =====================================
# INITIAL SMOOTHED VALUES
# =====================================

smoothed_vehicle_count = 0
smoothed_occupancy_ratio = 0
smoothed_queue_depth = 0

# =====================================
# MAIN VIDEO LOOP
# =====================================

while True:

    # Read frame
    ret, frame = cap.read()

    # Stop if video ends
    if not ret:
        break

    # =====================================
    # DRAW ROI
    # =====================================

    cv2.rectangle(frame,
                  (roi_x1, roi_y1),
                  (roi_x2, roi_y2),
                  (0, 0, 255),
                  3)
    cv2.line(
        frame,
        (roi_x1, roi_y2),
        (roi_x2, roi_y2),
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        "Signal Reference Line",
        (roi_x1, roi_y2 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2
    )

    cv2.putText(frame,
                "QUEUE ROI",
                (roi_x1, roi_y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2)

    # =====================================
    # YOLO DETECTION
    # =====================================

    results = model(frame)

    # =====================================
    # INITIAL PARAMETERS
    # =====================================

    vehicle_count = 0
    total_occupied_area = 0

    # Store queue depths
    queue_depths = []

    # =====================================
    # PROCESS DETECTIONS
    # =====================================

    for result in results:

        boxes = result.boxes

        for box in boxes:

            # Get class ID
            cls = int(box.cls[0])

            # Detect only vehicles
            if cls in vehicle_classes:

                # Bounding box coordinates
                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # Vehicle center point
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # =====================================
                # CHECK IF VEHICLE INSIDE ROI
                # =====================================

                if (roi_x1 < cx < roi_x2 and
                    roi_y1 < cy < roi_y2):

                    # Vehicle count
                    vehicle_count += 1

                    # Draw vehicle box
                    cv2.rectangle(frame,
                                  (x1, y1),
                                  (x2, y2),
                                  (0, 255, 0),
                                  2)

                    # =====================================
                    # VEHICLE AREA
                    # =====================================

                    width = x2 - x1
                    height = y2 - y1

                    vehicle_area = (
                        width * height
                    )

                    # =====================================
                    # TOTAL OCCUPIED AREA
                    # =====================================

                    total_occupied_area += (
                        vehicle_area
                    )

                    # =====================================
                    # QUEUE DEPTH
                    # =====================================

                    queue_depth = (
                        signal_line_y - cy
                    )

                    queue_depths.append(
                        queue_depth
                    )

    # =====================================
    # OCCUPANCY RATIO
    # =====================================

    occupancy_ratio = (
        total_occupied_area / roi_area
    )

    # =====================================
    # ADVANCED QUEUE DEPTH
    # TOP-3 FARTHEST VEHICLES
    # =====================================

    if len(queue_depths) >= 3:

        queue_depths.sort(
            reverse=True
        )

        final_queue_depth = (
            queue_depths[0]
            +
            queue_depths[1]
            +
            queue_depths[2]
        ) / 3

    elif len(queue_depths) > 0:

        final_queue_depth = (
            sum(queue_depths)
            /
            len(queue_depths)
        )

    else:

        final_queue_depth = 0

    # =====================================
    # EXPONENTIAL SMOOTHING
    # =====================================

    smoothed_vehicle_count = (
        alpha * vehicle_count
        +
        (1 - alpha)
        *
        smoothed_vehicle_count
    )

    smoothed_occupancy_ratio = (
        alpha * occupancy_ratio
        +
        (1 - alpha)
        *
        smoothed_occupancy_ratio
    )

    smoothed_queue_depth = (
        alpha * final_queue_depth
        +
        (1 - alpha)
        *
        smoothed_queue_depth
    )

    # =====================================
    # DISPLAY PARAMETERS
    # =====================================

    cv2.putText(frame,
                f"Vehicle Count: {round(smoothed_vehicle_count)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                3)

    cv2.putText(frame,
                f"Occupancy Ratio: {smoothed_occupancy_ratio:.2f}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                3)

    cv2.putText(frame,
                f"Queue Depth: {smoothed_queue_depth:.1f}px",
                (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3)

    # =====================================
    # SHOW VIDEO
    # =====================================

    cv2.imshow(
        "AI Traffic Management System",
        frame
    )

    # Quit using Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =====================================
# FINAL PARAMETERS
# =====================================

final_vehicle_count = round(
    smoothed_vehicle_count
)

final_occupancy_ratio = (
    smoothed_occupancy_ratio
)

final_queue_depth = (
    smoothed_queue_depth
)

# =====================================
# NORMALIZATION
# =====================================

normalized_vehicle_count = (
    final_vehicle_count / 20
)

normalized_queue_depth = (
    final_queue_depth / 500
)
# No meaningful traffic

if final_vehicle_count < 3:

    congestion_score = 0

else:

    congestion_score = (

        0.40 * final_occupancy_ratio

        +

        0.40 * normalized_queue_depth

        +

        0.20 * normalized_vehicle_count
    )




# =====================================
# CONGESTION CLASSIFICATION
# =====================================

if (
    congestion_score >= 0.3
    and
    final_vehicle_count >= 5
    and
    final_queue_depth >= 130
):
    congestion_status = "HIGH"

else:
    congestion_status = "LOW"

# =====================================
# SEND FINAL STATUS TO ARDUINO
# =====================================

time.sleep(1)

arduino.write(
    (congestion_status + "\n").encode()
)

# =====================================
# CLEAR TERMINAL
# =====================================

os.system("cls")

# =====================================
# FINAL DASHBOARD
# =====================================

print("====================================")
print(" FINAL TRAFFIC ANALYSIS ")
print("====================================\n")

print(f"Vehicle Count       : {final_vehicle_count}\n")

print(f"Occupancy Ratio     : {final_occupancy_ratio:.2f}\n")

print(f"Queue Depth         : {final_queue_depth:.1f} px\n")

print(f"Congestion Score    : {congestion_score:.2f}\n")

print(f"Congestion Status   : {congestion_status}\n")

print("====================================")

# =====================================
# CONTINUOUS SIGNAL OPERATION
# =====================================

print("\nTraffic Signal Running...")
print("Press Q then ENTER to stop.\n")

try:
    while True:
        arduino.write(
            (congestion_status + "\n").encode()
        )

        user_input = input()

        if user_input.lower() == "q":
            arduino.write(b"STOP\n")
            time.sleep(1)
            break

except KeyboardInterrupt:
    pass

# =====================================
# RELEASE RESOURCES
# =====================================

cap.release()

cv2.destroyAllWindows()

arduino.close()