import torch
import os
import cv2
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_yolo_model(model_name='yolov5s'):
    """
    Load the YOLOv5 model.

    Parameters:
    model_name (str): The version of YOLOv5 to load (e.g., 'yolov5s').

    Returns:
    model: The loaded YOLOv5 model.
    """
    return torch.hub.load('ultralytics/yolov5', model_name)
def process_images(model, image_folder, output_folder):
    """
    Process images in a folder to perform object detection.

    Parameters:
    model: The YOLOv5 model.
    image_folder (str): Path to the folder containing images.
    output_folder (str): Path to the folder to save results.

    Returns:
    list: A list of dictionaries containing detection data.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    detection_data = []

    for img_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_name)
        try:
            img = cv2.imread(img_path)
            results = model(img)
            detections = results.xyxy[0]
            class_names = model.names
            results.render()
            detection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if len(detections) > 0:
                result_img_path = os.path.join(output_folder, img_name)
                cv2.imwrite(result_img_path, img)

                for *box, conf, cls in detections:
                    class_name = class_names[int(cls.item())]
                    confidence_score = conf.item()
                    
                    detection_data.append({
                        "image_name": img_name,
                        "confidence_score": confidence_score,
                        "class_name": class_name,
                        "bbox_coordinates": [box[0].item(), box[1].item(), box[2].item(), box[3].item()],
                        "result_image_path": result_img_path,
                        "detection_time": detection_time
                    })
                    
                    print(f"Detected {class_name} with confidence {confidence_score:.2f}")

        except Exception as e:
            print(f"Error processing {img_name}: {e}")

    return detection_data

def save_detections_to_csv(detection_data, output_folder):
    """
    Save detection data to a CSV file.

    Parameters:
    detection_data (list): List of detection data dictionaries.
    output_folder (str): Path to the folder to save the CSV file.
    """
    df = pd.DataFrame(detection_data, columns=['image_name', 'confidence_score', 'class_name', 
                                               'bbox_coordinates', 'result_image_path', 'detection_time'])
    df.to_csv(os.path.join(output_folder, 'detections.csv'), index=False)
    print("Detections saved to CSV and images saved in results folder.")