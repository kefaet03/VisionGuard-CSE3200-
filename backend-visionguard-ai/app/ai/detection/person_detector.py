"""
Person Detection Module
Adapted from vis-new/p1.py
Uses YOLOv8 for person detection
"""

import cv2
import numpy as np
import logging
import torch
from ultralytics import YOLO


logger = logging.getLogger(__name__)


class PersonDetector:
    """
    YOLOv8-based person detector
    """
    
    def __init__(self, model_path: str, device: str | None = None, conf_threshold: float = 0.45):
        """
        Initialize person detector
        
        Args:
            model_path: Path to YOLOv8 model file
            device: Device to run on ('cuda:0' or 'cpu')
            conf_threshold: Confidence threshold for detections
        """
        self.model = YOLO(model_path)
        chosen_device = device
        if chosen_device is None or str(chosen_device).strip() == "":
            chosen_device = "cuda:0" if torch.cuda.is_available() else "cpu"
        elif str(chosen_device).lower().startswith("cuda") and not torch.cuda.is_available():
            chosen_device = "cpu"

        try:
            self.model.to(chosen_device)
        except Exception as e:
            if str(chosen_device).lower().startswith("cuda"):
                logger.warning("YOLO device '%s' failed (%s); falling back to CPU", chosen_device, e)
                chosen_device = "cpu"
                try:
                    self.model.to(chosen_device)
                except Exception:
                    pass
        self.conf_threshold = conf_threshold
        self.device = str(chosen_device)
    
    def detect(self, frame: np.ndarray):
        """
        Detect persons in a frame
        
        Args:
            frame: BGR image (numpy array)
            
        Returns:
            List of detections: [[[x, y, w, h], confidence], ...]
            where (x, y) is top-left corner, (w, h) is width/height
        """
        results = self.model(frame)
        detections = []
        
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = float(box.conf)
            cls = int(box.cls)
            
            # class 0 = person in COCO dataset
            if cls == 0 and conf > self.conf_threshold:
                detections.append([
                    [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                    conf
                ])
        
        return detections
