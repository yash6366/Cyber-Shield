import pytest
from python_agents.classifier_agent import ClassifierAgent
from utils.rag_retrieval import RAGRetrieval

@pytest.fixture
def classifier_agent():
    return ClassifierAgent()

def test_classifier_initialization(classifier_agent):
    assert isinstance(classifier_agent.rag, RAGRetrieval)
    assert isinstance(classifier_agent.labels, list)
    assert len(classifier_agent.labels) > 0

def test_classify_threat(classifier_agent):
    description = "Suspicious traffic detected from IP 192.168.1.100"
    label = classifier_agent.classify(description)
    assert label in classifier_agent.labels

def test_rag_retrieval():
    rag = RAGRetrieval(dimension=128)
    test_vector = [0.1] * 128
    test_doc = "Test document"
    rag.add_document(test_vector, test_doc)
    results = rag.search(test_vector, top_k=1)
    assert len(results) == 1
    assert results[0] == test_doc