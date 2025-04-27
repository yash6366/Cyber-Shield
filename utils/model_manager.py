import os
import json
import torch
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from .logger import setup_logger

logger = setup_logger('ModelManager')

class ModelManager:
    def __init__(self, base_path: str = "models"):
        self.base_path = base_path
        self.metadata_file = os.path.join(base_path, "model_metadata.json")
        self._ensure_directories()
        self.metadata = self._load_metadata()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "hunter"), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "classifier"), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "archives"), exist_ok=True)

    def _load_metadata(self) -> Dict:
        """Load model metadata from JSON file."""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {"models": {}}

    def _save_metadata(self):
        """Save model metadata to JSON file."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def save_model(self, model: torch.nn.Module, model_type: str, 
                  version: str, metrics: Dict[str, float],
                  hyperparameters: Optional[Dict[str, Any]] = None) -> str:
        """Save a model with its metadata."""
        timestamp = datetime.now().isoformat()
        model_dir = os.path.join(self.base_path, model_type)
        model_path = os.path.join(model_dir, f"{model_type}_v{version}.pt")
        
        # Save model state
        torch.save({
            'state_dict': model.state_dict(),
            'hyperparameters': hyperparameters or {}
        }, model_path)

        # Update metadata
        model_id = f"{model_type}_v{version}"
        self.metadata["models"][model_id] = {
            "type": model_type,
            "version": version,
            "path": model_path,
            "timestamp": timestamp,
            "metrics": metrics,
            "hyperparameters": hyperparameters or {}
        }
        self._save_metadata()
        logger.info(f"Saved model {model_id} with metrics: {metrics}")
        return model_id

    def load_model(self, model_type: str, version: str = "latest") -> Dict[str, Any]:
        """Load a model by type and version."""
        if version == "latest":
            # Find latest version
            versions = [m for m in self.metadata["models"].keys() 
                       if m.startswith(model_type)]
            if not versions:
                raise ValueError(f"No models found for type {model_type}")
            model_id = max(versions)
        else:
            model_id = f"{model_type}_v{version}"

        if model_id not in self.metadata["models"]:
            raise ValueError(f"Model {model_id} not found")

        model_info = self.metadata["models"][model_id]
        model_path = model_info["path"]

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        checkpoint = torch.load(model_path)
        logger.info(f"Loaded model {model_id}")
        return {
            "state_dict": checkpoint["state_dict"],
            "metadata": model_info,
            "hyperparameters": checkpoint["hyperparameters"]
        }

    def archive_model(self, model_type: str, version: str):
        """Archive an old model version."""
        model_id = f"{model_type}_v{version}"
        if model_id not in self.metadata["models"]:
            raise ValueError(f"Model {model_id} not found")

        model_info = self.metadata["models"][model_id]
        src_path = model_info["path"]
        dst_path = os.path.join(self.base_path, "archives", 
                               f"{model_type}_v{version}_{datetime.now().strftime('%Y%m%d')}.pt")

        shutil.move(src_path, dst_path)
        model_info["path"] = dst_path
        model_info["archived"] = True
        model_info["archive_date"] = datetime.now().isoformat()
        self._save_metadata()
        logger.info(f"Archived model {model_id}")

    def get_model_metrics(self, model_type: str, version: str = "latest") -> Dict[str, float]:
        """Get metrics for a specific model version."""
        if version == "latest":
            versions = [m for m in self.metadata["models"].keys() 
                       if m.startswith(model_type)]
            if not versions:
                raise ValueError(f"No models found for type {model_type}")
            model_id = max(versions)
        else:
            model_id = f"{model_type}_v{version}"

        if model_id not in self.metadata["models"]:
            raise ValueError(f"Model {model_id} not found")

        return self.metadata["models"][model_id]["metrics"]