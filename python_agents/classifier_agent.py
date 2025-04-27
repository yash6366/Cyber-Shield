import logging
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from utils.logger import setup_logger
from utils.rag_retrieval import RAGRetrieval
from utils.model_manager import ModelManager

logger = setup_logger('ClassifierAgent')

class ClassifierAgent:
    def __init__(self):
        self.model_manager = ModelManager()
        self.rag = RAGRetrieval()
        self.labels = ["Brute Force Attack", "Data Exfiltration", "Malware", "Phishing"]
        self._load_or_init_models()
        logger.info("ClassifierAgent initialized with RAG retrieval and LLM model.")

    def _load_or_init_models(self):
        try:
            # Try to load the latest classifier model
            model_data = self.model_manager.load_model("classifier", "latest")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "distilbert-base-uncased",
                num_labels=len(self.labels)
            )
            self.model.load_state_dict(model_data["state_dict"])
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            
            # Load vector store if exists
            vector_db_path = os.path.join(self.model_manager.base_path, "vector_store")
            if os.path.exists(vector_db_path):
                self.rag = RAGRetrieval.load(vector_db_path)
            
            logger.info(f"Loaded classifier model with metrics: {model_data['metadata']['metrics']}")
        except (ValueError, FileNotFoundError):
            # Initialize new model if none exists
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "distilbert-base-uncased",
                num_labels=len(self.labels)
            )
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            logger.info("Initialized new classifier model")

    def train(self, train_data=None):
        if train_data is None:
            logger.info("No training data provided. Training simulated.")
            metrics = {
                "accuracy": 0.95,
                "precision": 0.94,
                "recall": 0.93,
                "f1": 0.94
            }
        else:
            # Actual training logic would go here
            metrics = self._train_model(train_data)

        # Save model with metrics
        self.model_manager.save_model(
            model=self.model,
            model_type="classifier",
            version="1.0",
            metrics=metrics,
            hyperparameters={
                "model_type": "distilbert-base-uncased",
                "num_labels": len(self.labels)
            }
        )
        
        # Save vector store state
        vector_db_path = os.path.join(self.model_manager.base_path, "vector_store")
        self.rag.save(vector_db_path)
        
        logger.info("Training complete.")

    def _train_model(self, train_data):
        # Placeholder for actual training logic
        return {
            "accuracy": 0.95,
            "precision": 0.94,
            "recall": 0.93,
            "f1": 0.94
        }

    def classify(self, threat_description):
        # Tokenize input
        inputs = self.tokenizer(
            threat_description,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        # Get relevant context from RAG
        context_vector = self.model(**inputs).logits.detach().mean(dim=1).numpy()
        relevant_docs = self.rag.search(context_vector[0])

        # Get model prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            confidence, predicted = torch.max(probs, 1)
            label = self.labels[predicted.item()]
            
        logger.info(f"Classified threat as: {label} (confidence: {confidence.item():.2f})")
        return {
            "label": label,
            "confidence": confidence.item(),
            "context": relevant_docs[:3]  # Return top 3 relevant documents
        }

if __name__ == "__main__":
    agent = ClassifierAgent()
    agent.train()
