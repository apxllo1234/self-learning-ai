import random
import re
from collections import defaultdict, Counter

class SimpleMarkovLearner:
    def __init__(self):
        # Markov chain for word transitions: {prefix: {next_word: count}}
        self.chain = defaultdict(Counter)
        # To store responses for specific input patterns
        self.patterns = []
        
    def train(self, text):
        """Train on a piece of text"""
        words = self._tokenize(text)
        if len(words) < 2:
            return
            
        for i in range(len(words) - 1):
            prefix = words[i]
            next_word = words[i+1]
            self.chain[prefix][next_word] += 1
            
    def _tokenize(self, text):
        return re.findall(r"[\w']+|[.,!?;]", text.lower())

    def generate_response(self, input_text, max_length=20):
        """Generate a response based on learned transitions and input"""
        self.train(input_text) # Learn from every input
        
        words = self._tokenize(input_text)
        if not words:
            return "..."
            
        # Start generating from one of the input words if possible
        start_word = random.choice(words)
        if start_word not in self.chain:
            # Fallback to a random known word
            if not self.chain:
                return f"I am learning. You said: {input_text}"
            start_word = random.choice(list(self.chain.keys()))
            
        response = [start_word]
        current_word = start_word
        
        for _ in range(max_length - 1):
            if current_word not in self.chain:
                break
            
            # Weighted choice based on transition counts
            next_words = list(self.chain[current_word].keys())
            weights = list(self.chain[current_word].values())
            current_word = random.choices(next_words, weights=weights)[0]
            response.append(current_word)
            
            if current_word in ".!?":
                break
                
        return " ".join(response).capitalize()

class ScratchAI:
    def __init__(self, memory):
        self.memory = memory
        self.learner = SimpleMarkovLearner()
        self._load_from_memory()
        
    def _load_from_memory(self):
        """Load past experiences from memory system"""
        # Load knowledge items
        all_memories = self.memory.get_all()
        for item in all_memories.get('short_term', []):
            if item['type'] in ['knowledge', 'experience']:
                self.learner.train(item['content'])
        for item in all_memories.get('long_term', {}).values():
            if item['type'] in ['knowledge', 'experience']:
                self.learner.train(item['content'])
                
    def generate_response(self, message):
        # Save input as experience
        self.memory.add(type="experience", content=message)
        
        # Generate response
        response = self.learner.generate_response(message)
        
        # Save response as experience
        self.memory.add(type="experience", content=response)
        
        return response

    def learn_topic(self, topic):
        """Simplified learning: just store the topic as something known"""
        self.memory.learned_topics[topic] = [f"Learned about {topic} at scratch level"]
        self.learner.train(topic)
        return {"topic": topic, "status": "learned"}
