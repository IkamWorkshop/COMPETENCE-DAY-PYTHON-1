import cv2
import mediapipe as mp
import numpy as np

# Inisialisasi MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Warna untuk tampilan
COLORS = {
    'background': (40, 40, 40),
    'text': (255, 255, 255),
    'highlight': (0, 255, 255),
    'finger': (0, 200, 0),
    'palm': (100, 100, 255)
}

def count_fingers(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Indeks ujung jari
    finger_states = []
    
    # Deteksi ibu jari
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        finger_states.append(1)
    else:
        finger_states.append(0)
    
    # Deteksi 4 jari lainnya
    for tip in finger_tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            finger_states.append(1)
        else:
            finger_states.append(0)
    
    return sum(finger_states), finger_states

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2100)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1800)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Deteksi tangan
    results = hands.process(rgb_frame)
    total_fingers = 0
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Gambar landmark tangan
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=COLORS['palm'], thickness=1, circle_radius=2),
                mp_drawing.DrawingSpec(color=COLORS['finger'], thickness=1, circle_radius=1))
            
            # Hitung jari
            count, states = count_fingers(hand_landmarks)
            total_fingers += count
            
            # Highlight ujung jari
            for i, state in enumerate(states):
                if state == 1:
                    landmark = hand_landmarks.landmark[[4, 8, 12, 16, 20][i]]
                    cx, cy = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (cx, cy), 8, COLORS['highlight'], -1)
    
    # Tampilkan jumlah jari (teks kecil di sudut)
    cv2.putText(frame, f"Jari: {total_fingers}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORS['text'], 1)
    
    # Tampilkan petunjuk kecil
    cv2.putText(frame, "Tekan 'Q' untuk keluar", (10, frame.shape[0]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['text'], 1)
    
    # Tampilkan frame
    cv2.imshow('Finger Counter - Minimal', frame)
    
    # Keluar dengan 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()