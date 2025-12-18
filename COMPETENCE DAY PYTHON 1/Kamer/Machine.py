"""
Sistem Klasifikasi Bentuk Kepala
Menggunakan OpenCV dan MediaPipe untuk deteksi dan klasifikasi bentuk kepala
"""

import cv2
import mediapipe as mp
import numpy as np
import math
from typing import Tuple, Dict, List, Optional

class HeadShapeClassifier:
    def __init__(self):
        """Inisialisasi MediaPipe Face Mesh dan Face Detection"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Inisialisasi Face Mesh untuk landmark detection
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Landmark indices untuk pengukuran
        self.FOREHEAD_TOP = 10
        self.CHIN_BOTTOM = 152
        self.LEFT_CHEEK = 234
        self.RIGHT_CHEEK = 454
        self.LEFT_JAW = 172
        self.RIGHT_JAW = 397
        self.LEFT_TEMPLE = 21
        self.RIGHT_TEMPLE = 251
        self.NOSE_TIP = 1
        
    def calculate_distance(self, point1: Tuple[float, float], 
                          point2: Tuple[float, float]) -> float:
        """Menghitung jarak Euclidean antara dua titik"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def calculate_angle(self, point1: Tuple[float, float], 
                       point2: Tuple[float, float], 
                       point3: Tuple[float, float]) -> float:
        """Menghitung sudut antara tiga titik"""
        vector1 = (point1[0] - point2[0], point1[1] - point2[1])
        vector2 = (point3[0] - point2[0], point3[1] - point2[1])
        
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
        magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
        
        if magnitude1 * magnitude2 == 0:
            return 0
        
        cos_angle = dot_product / (magnitude1 * magnitude2)
        cos_angle = max(-1, min(1, cos_angle))
        angle = math.acos(cos_angle)
        return math.degrees(angle)
    
    def extract_features(self, landmarks, img_width: int, 
                        img_height: int) -> Dict[str, float]:
        """Ekstrak fitur-fitur untuk klasifikasi bentuk kepala"""
        # Konversi landmark ke koordinat pixel
        points = {}
        landmark_indices = {
            'forehead_top': self.FOREHEAD_TOP,
            'chin_bottom': self.CHIN_BOTTOM,
            'left_cheek': self.LEFT_CHEEK,
            'right_cheek': self.RIGHT_CHEEK,
            'left_jaw': self.LEFT_JAW,
            'right_jaw': self.RIGHT_JAW,
            'left_temple': self.LEFT_TEMPLE,
            'right_temple': self.RIGHT_TEMPLE,
            'nose_tip': self.NOSE_TIP
        }
        
        for name, idx in landmark_indices.items():
            landmark = landmarks.landmark[idx]
            points[name] = (int(landmark.x * img_width), 
                          int(landmark.y * img_height))
        
        # Hitung pengukuran
        face_length = self.calculate_distance(
            points['forehead_top'], points['chin_bottom']
        )
        face_width = self.calculate_distance(
            points['left_cheek'], points['right_cheek']
        )
        forehead_width = self.calculate_distance(
            points['left_temple'], points['right_temple']
        )
        jaw_width = self.calculate_distance(
            points['left_jaw'], points['right_jaw']
        )
        
        # Hitung rasio
        length_width_ratio = face_length / face_width if face_width > 0 else 0
        forehead_jaw_ratio = forehead_width / jaw_width if jaw_width > 0 else 0
        
        # Hitung sudut rahang
        jaw_angle_left = self.calculate_angle(
            points['left_temple'], points['left_jaw'], points['chin_bottom']
        )
        jaw_angle_right = self.calculate_angle(
            points['right_temple'], points['right_jaw'], points['chin_bottom']
        )
        avg_jaw_angle = (jaw_angle_left + jaw_angle_right) / 2
        
        # Hitung tonjolan tulang pipi
        cheekbone_width = self.calculate_distance(
            points['left_cheek'], points['right_cheek']
        )
        cheekbone_prominence = cheekbone_width / face_width if face_width > 0 else 0
        
        features = {
            'length_width_ratio': length_width_ratio,
            'forehead_jaw_ratio': forehead_jaw_ratio,
            'jaw_angle': avg_jaw_angle,
            'cheekbone_prominence': cheekbone_prominence,
            'face_width': face_width,
            'face_length': face_length,
            'forehead_width': forehead_width,
            'jaw_width': jaw_width
        }
        
        return features, points
    
    def classify_head_shape(self, features: Dict[str, float]) -> Tuple[str, float]:
        """Klasifikasi bentuk kepala berdasarkan fitur"""
        lw_ratio = features['length_width_ratio']
        fj_ratio = features['forehead_jaw_ratio']
        jaw_angle = features['jaw_angle']
        cheek_prom = features['cheekbone_prominence']
        
        # Sistem scoring untuk setiap bentuk
        scores = {
            'Oval': 0,
            'Bulat': 0,
            'Persegi': 0,
            'Hati': 0,
            'Lonjong': 0,
            'Belah Ketupat': 0
        }
        
        # Oval: Panjang lebih besar dari lebar, proporsi seimbang
        if 1.3 <= lw_ratio <= 1.6:
            scores['Oval'] += 40
        if 0.95 <= fj_ratio <= 1.1:
            scores['Oval'] += 30
        if 130 <= jaw_angle <= 150:
            scores['Oval'] += 30
        
        # Bulat: Rasio panjang-lebar mendekati 1
        if 1.0 <= lw_ratio <= 1.2:
            scores['Bulat'] += 40
        if 0.95 <= fj_ratio <= 1.05:
            scores['Bulat'] += 30
        if 140 <= jaw_angle <= 160:
            scores['Bulat'] += 30
        
        # Persegi: Rahang lebar, sudut tajam
        if 1.0 <= lw_ratio <= 1.3:
            scores['Persegi'] += 30
        if 0.85 <= fj_ratio <= 1.05:
            scores['Persegi'] += 30
        if 100 <= jaw_angle <= 130:
            scores['Persegi'] += 40
        
        # Hati: Dahi lebar, dagu runcing
        if 1.2 <= lw_ratio <= 1.5:
            scores['Hati'] += 30
        if fj_ratio >= 1.15:
            scores['Hati'] += 40
        if 130 <= jaw_angle <= 160:
            scores['Hati'] += 30
        
        # Lonjong: Panjang jauh lebih besar dari lebar
        if lw_ratio >= 1.6:
            scores['Lonjong'] += 50
        if 0.9 <= fj_ratio <= 1.1:
            scores['Lonjong'] += 30
        if 130 <= jaw_angle <= 150:
            scores['Lonjong'] += 20
        
        # Belah Ketupat: Tulang pipi menonjol, dahi dan rahang sempit
        if 1.2 <= lw_ratio <= 1.5:
            scores['Belah Ketupat'] += 30
        if cheek_prom >= 0.95:
            scores['Belah Ketupat'] += 40
        if 0.8 <= fj_ratio <= 0.95:
            scores['Belah Ketupat'] += 30
        
        # Tentukan bentuk dengan skor tertinggi
        max_shape = max(scores, key=scores.get)
        confidence = min(scores[max_shape], 100) / 100.0
        
        return max_shape, confidence
    
    def draw_landmarks(self, image, points: Dict[str, Tuple[int, int]]):
        """Gambar landmark pada gambar"""
        for name, point in points.items():
            cv2.circle(image, point, 3, (0, 255, 0), -1)
    
    def draw_measurements(self, image, points: Dict[str, Tuple[int, int]]):
        """Gambar garis pengukuran"""
        # Panjang wajah
        cv2.line(image, points['forehead_top'], points['chin_bottom'], 
                (255, 0, 0), 2)
        # Lebar wajah
        cv2.line(image, points['left_cheek'], points['right_cheek'], 
                (0, 255, 255), 2)
        # Lebar dahi
        cv2.line(image, points['left_temple'], points['right_temple'], 
                (255, 0, 255), 2)
        # Lebar rahang
        cv2.line(image, points['left_jaw'], points['right_jaw'], 
                (0, 165, 255), 2)
    
    def process_frame(self, frame, show_measurements: bool = True):
        """Proses satu frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        annotated_frame = frame.copy()
        detections = []
        
        if results.multi_face_landmarks:
            h, w = frame.shape[:2]
            
            for face_landmarks in results.multi_face_landmarks:
                # Ekstrak fitur
                features, points = self.extract_features(face_landmarks, w, h)
                
                # Klasifikasi
                shape, confidence = self.classify_head_shape(features)
                
                # Simpan deteksi
                detections.append({
                    'shape': shape,
                    'confidence': confidence,
                    'features': features,
                    'points': points
                })
                
                # Gambar mesh wajah (opsional, bisa dikomentari untuk performa lebih baik)
                self.mp_drawing.draw_landmarks(
                    image=annotated_frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_tesselation_style()
                )
                
                # Gambar landmark penting
                self.draw_landmarks(annotated_frame, points)
                
                # Gambar pengukuran
                if show_measurements:
                    self.draw_measurements(annotated_frame, points)
                
                # Gambar bounding box
                x_coords = [p[0] for p in points.values()]
                y_coords = [p[1] for p in points.values()]
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                
                padding = 20
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)
                
                cv2.rectangle(annotated_frame, (x_min, y_min), 
                            (x_max, y_max), (0, 255, 0), 2)
                
                # Tampilkan label
                label = f"{shape} ({confidence:.2f})"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 
                                            0.7, 2)[0]
                cv2.rectangle(annotated_frame, (x_min, y_min - label_size[1] - 10),
                            (x_min + label_size[0], y_min), (0, 255, 0), -1)
                cv2.putText(annotated_frame, label, (x_min, y_min - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
                # Tampilkan fitur detail
                y_offset = y_max + 25
                info_lines = [
                    f"L/W Ratio: {features['length_width_ratio']:.2f}",
                    f"Dahi/Rahang: {features['forehead_jaw_ratio']:.2f}",
                    f"Sudut Rahang: {features['jaw_angle']:.1f}"
                ]
                
                for line in info_lines:
                    cv2.putText(annotated_frame, line, (x_min, y_offset),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    y_offset += 20
        
        return annotated_frame, detections
    
    def process_image(self, image_path: str, output_path: Optional[str] = None):
        """Proses gambar statis"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Tidak dapat membaca gambar dari {image_path}")
            return
        
        annotated_image, detections = self.process_frame(image)
        
        if detections:
            print(f"\n{'='*50}")
            print(f"Ditemukan {len(detections)} wajah:")
            for i, det in enumerate(detections, 1):
                print(f"\nWajah {i}:")
                print(f"  Bentuk: {det['shape']}")
                print(f"  Kepercayaan: {det['confidence']:.2%}")
                print(f"  Fitur:")
                for key, value in det['features'].items():
                    print(f"    {key}: {value:.2f}")
        else:
            print("Tidak ada wajah yang terdeteksi dalam gambar.")
        
        cv2.imshow('Klasifikasi Bentuk Kepala', annotated_image)
        
        if output_path:
            cv2.imwrite(output_path, annotated_image)
            print(f"\nHasil disimpan ke: {output_path}")
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def process_webcam(self, show_measurements: bool = True):
        """Proses video real-time dari webcam"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Tidak dapat membuka webcam")
            return
        
        print("\nMode Webcam Aktif")
        print("Tekan 'q' untuk keluar")
        print("Tekan 's' untuk screenshot")
        print("Tekan 'm' untuk toggle pengukuran")
        
        show_meas = show_measurements
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            annotated_frame, detections = self.process_frame(frame, show_meas)
            
            # Tampilkan informasi
            info_text = f"Wajah: {len(detections)} | 'q':Keluar 's':Screenshot 'm':Ukuran"
            cv2.putText(annotated_frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Klasifikasi Bentuk Kepala - Webcam', annotated_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"head_shape_capture_{cv2.getTickCount()}.jpg"
                cv2.imwrite(filename, annotated_frame)
                print(f"Screenshot disimpan: {filename}")
            elif key == ord('m'):
                show_meas = not show_meas
                print(f"Pengukuran: {'ON' if show_meas else 'OFF'}")
        
        cap.release()
        cv2.destroyAllWindows()
    
    def process_video(self, video_path: str, output_path: Optional[str] = None):
        """Proses file video"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Tidak dapat membuka video {video_path}")
            return
        
        # Setup video writer jika output path disediakan
        writer = None
        if output_path:
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
        
        print(f"\nMemproses video: {video_path}")
        print("Tekan 'q' untuk berhenti")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            annotated_frame, _ = self.process_frame(frame)
            
            if writer:
                writer.write(annotated_frame)
            
            cv2.imshow('Klasifikasi Bentuk Kepala - Video', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        if writer:
            writer.release()
            print(f"Video output disimpan: {output_path}")
        cv2.destroyAllWindows()
    
    def __del__(self):
        """Cleanup"""
        self.face_mesh.close()


def main():
    """Fungsi utama"""
    classifier = HeadShapeClassifier()
    
    print("=" * 60)
    print("SISTEM KLASIFIKASI BENTUK KEPALA")
    print("=" * 60)
    print("\nPilih mode:")
    print("1. Proses gambar")
    print("2. Webcam real-time")
    print("3. Proses video")
    print("4. Keluar")
    
    choice = input("\nPilihan Anda (1-4): ").strip()
    
    if choice == '1':
        image_path = input("Masukkan path gambar: ").strip()
        save = input("Simpan hasil? (y/n): ").strip().lower()
        output_path = None
        if save == 'y':
            output_path = input("Path output (default: output.jpg): ").strip()
            if not output_path:
                output_path = "output.jpg"
        classifier.process_image(image_path, output_path)
    
    elif choice == '2':
        classifier.process_webcam()
    
    elif choice == '3':
        video_path = input("Masukkan path video: ").strip()
        save = input("Simpan hasil? (y/n): ").strip().lower()
        output_path = None
        if save == 'y':
            output_path = input("Path output (default: output.mp4): ").strip()
            if not output_path:
                output_path = "output.mp4"
        classifier.process_video(video_path, output_path)
    
    elif choice == '4':
        print("Terima kasih!")
        return
    
    else:
        print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()
