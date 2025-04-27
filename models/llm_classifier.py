from transformers import pipeline

class LLMClassifier:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def classify(self, text, candidate_labels=None):
        if candidate_labels is None:
            candidate_labels = ["Brute Force Attack", "Data Exfiltration", "Malware", "Phishing"]
        result = self.classifier(text, candidate_labels)
        return result

if __name__ == "__main__":
    llm_classifier = LLMClassifier()
    test_text = "Multiple failed login attempts detected from IP 192.168.1.10"
    result = llm_classifier.classify(test_text)
    print(f"Classification result: {result['labels'][0]} with score {result['scores'][0]:.4f}")
