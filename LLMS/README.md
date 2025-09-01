# LLM Assignment: Hands-On Exploration

This project demonstrates the practical implementation and evaluation of Large Language Models (LLMs) for the Visa Mock Interview System (VMIS). The assignment covers text generation, sentiment analysis, masked language modeling, evaluation metrics, and custom prompt engineering.

## 📁 Project Structure

```
LLMS/
├── Large Language Models_ Architecture and Processing.pdf  # Task 1: LLM Basics Report
├── text_generation.py                    # Task 2a: Text Generation with GPT-2
├── sentiment_analysis.py                 # Task 2b: Sentiment Analysis with BERT
├── masked_language_modeling.py           # Task 2c: Masked Language Modeling
├── evaluation_metrics.py                 # Task 4: BLEU, ROUGE, Perplexity
├── custom_prompts.py                     # Task 3: Custom Prompt Engineering
├── main_runner.py                        # Orchestrates all tasks
├── README.md                             # This documentation
└── Output Files (generated after running):
    ├── test_cases.txt                    # Input prompts and LLM outputs
    ├── evaluation_results.txt            # BLEU/ROUGE scores and perplexity
    ├── comprehensive_results.json        # Detailed results in JSON format
    ├── assignment_summary.txt            # Summary report
    └── llm_assignment_log.txt            # Execution logs
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Internet connection for downloading pre-trained models

### Installation

1. **Install Required Packages:**

   ```powershell
   C:/Users/mslal/AppData/Local/Programs/Python/Python312/python.exe -m pip install transformers torch datasets evaluate rouge-score sacrebleu nltk numpy pandas
   ```

2. **Navigate to the LLMS Directory:**
   ```powershell
   cd "c:\Users\mslal\Edubot\LLMS"
   ```

### Running the Assignment

#### Option 1: Run All Tasks at Once (Recommended)

```powershell
C:/Users/mslal/AppData/Local/Programs/Python/Python312/python.exe main_runner.py
```

#### Option 2: Run Individual Tasks

**Text Generation:**

```powershell
C:/Users/mslal/AppData/Local/Programs/Python/Python312/python.exe text_generation.py
```

**Sentiment Analysis:**

```powershell
C:/Users/mslal/AppData/Local/Programs/Python/Python312/python.exe sentiment_analysis.py
```

**Masked Language Modeling:**

```powershell
C:/Users/mslal/AppData/Local/Programs/Python/Python312/python.exe masked_language_modeling.py
```

**Evaluation Metrics:**

```powershell
C:/Users/mslal/AppData/Local/Programs/Python/Python312/python.exe evaluation_metrics.py
```

**Custom Prompts:**

```powershell
C:/Users/mslal/AppData/Local/Programs/Python/Python312/python.exe custom_prompts.py
```

## 📊 Task Descriptions

### Task 1: Understanding LLMs ✅

- **File:** `Large Language Models_ Architecture and Processing.pdf`
- **Content:** Comprehensive report on LLM architectures, transformers, attention mechanisms, embeddings, and popular models (GPT, BERT, T5)

### Task 2: Hands-On Exploration

#### 2a. Text Generation (`text_generation.py`)

- **Model:** GPT-2
- **Capabilities:**
  - Generate interview questions based on prompts
  - Create feedback for interview performance
  - Summarize interview notes into strengths/weaknesses
- **Features:**
  - Temperature control for creativity
  - Configurable output length
  - Multiple generation strategies

#### 2b. Sentiment Analysis (`sentiment_analysis.py`)

- **Model:** RoBERTa-based sentiment classifier
- **Capabilities:**
  - Classify sentiment of feedback (Positive/Negative/Neutral)
  - Map sentiment to performance ratings
  - Batch processing of feedback
  - Confidence scoring
- **VMIS Integration:** Automatically categorize interview feedback for HR reports

#### 2c. Masked Language Modeling (`masked_language_modeling.py`)

- **Model:** BERT
- **Capabilities:**
  - Predict missing words in sentences
  - Context-aware predictions
  - Interview-specific vocabulary understanding
  - Multiple prediction candidates with confidence scores

### Task 3: Custom Prompts (`custom_prompts.py`)

- **Specialized Prompts for VMIS:**
  - Interview feedback generation
  - Interview summarization
  - Follow-up question creation
  - Behavioral question generation
  - Technical assessment questions
  - Performance rating with detailed feedback

### Task 4: Evaluation Metrics (`evaluation_metrics.py`)

- **Metrics Implemented:**
  - **BLEU Score:** Measures n-gram overlap between reference and generated text
  - **ROUGE Scores:** Recall-oriented evaluation (ROUGE-1, ROUGE-2, ROUGE-L)
  - **Perplexity:** Measures fluency and coherence of generated text
- **Features:**
  - Single text evaluation
  - Batch evaluation with averages
  - Real-time generation and evaluation

### Task 5: Integration (`main_runner.py`)

- **Orchestration:** Runs all tasks sequentially
- **Logging:** Comprehensive execution logs
- **Results Management:** Generates multiple output formats
- **Error Handling:** Graceful failure recovery

## 📈 Expected Outputs

### 1. `test_cases.txt`

Contains input prompts and corresponding LLM outputs for all tasks:

```
Test Case 1:
Task: text_generation
Prompt: Generate a technical interview question about Python programming:
Output: What are the key differences between lists and tuples in Python...
```

### 2. `evaluation_results.txt`

Documents BLEU/ROUGE scores and perplexity values:

```
AVERAGE METRICS:
Average Perplexity: 25.43
Average BLEU Score: 0.3421
Average ROUGE-1: 0.4567
Average ROUGE-2: 0.2834
Average ROUGE-L: 0.3945
```

### 3. `comprehensive_results.json`

Detailed results in structured JSON format for programmatic access.

### 4. `assignment_summary.txt`

High-level summary of task completion and key metrics.

## 🔧 Configuration Options

### Model Selection

- **GPT-2 Variants:** `gpt2`, `gpt2-medium`, `gpt2-large`
- **BERT Variants:** `bert-base-uncased`, `bert-large-uncased`
- **Sentiment Models:** Various pre-trained sentiment classifiers

### Generation Parameters

- **Temperature:** Controls randomness (0.1-1.0)
- **Max Length:** Maximum tokens to generate
- **Top-p/Top-k:** Nucleus/top-k sampling
- **No Repeat N-gram:** Prevents repetitive output

## 🎯 VMIS Integration Examples

### Interview Feedback Generation

```python
Input: "The candidate demonstrates strong analytical skills but lacks communication abilities."
Output: "Strengths: Excellent analytical thinking and problem-solving approach.
         Areas for improvement: Communication skills and presentation clarity."
```

### Sentiment-Based Performance Rating

```python
Feedback: "Outstanding candidate! Strong technical background, excellent presentation skills."
Sentiment: POSITIVE (Confidence: 0.94)
Performance Rating: Excellent
```

### Intelligent Follow-up Questions

```python
Previous Response: "I used Python and machine learning algorithms to solve the data analysis problem."
Follow-up: "Can you walk me through the specific machine learning algorithms you chose and why?"
```

## 📊 Performance Benchmarks

Based on typical runs, you can expect:

- **Text Generation:** 50-100 interview questions/feedback items
- **Sentiment Analysis:** 95%+ accuracy on clear positive/negative feedback
- **Masked Language Modeling:** Top-3 accuracy of 60-80% for context-appropriate words
- **BLEU Scores:** 0.2-0.4 (typical for text generation tasks)
- **ROUGE Scores:** 0.3-0.5 (varies by task complexity)
- **Perplexity:** 15-40 (lower is better for fluency)

## 🚨 Troubleshooting

### Common Issues:

1. **Memory Errors:**

   - Use smaller models (`gpt2` instead of `gpt2-large`)
   - Reduce batch sizes
   - Close other applications

2. **Slow Performance:**

   - First run downloads models (5-10 minutes)
   - Subsequent runs are faster
   - Consider using GPU if available

3. **Import Errors:**

   - Ensure all packages are installed
   - Check Python version compatibility
   - Restart terminal after installation

4. **Model Download Issues:**
   - Check internet connection
   - Clear Hugging Face cache: `~/.cache/huggingface/`
   - Retry with different model variants

## 📚 Educational Value

This assignment demonstrates:

1. **LLM Architecture Understanding:** Practical experience with transformers, attention, and embeddings
2. **Multi-task Learning:** Different models for different NLP tasks
3. **Evaluation Methodologies:** Industry-standard metrics for text generation
4. **Prompt Engineering:** Crafting effective prompts for specific domains
5. **Real-world Application:** Direct relevance to interview systems and HR tech

## 🔮 Future Enhancements

Potential improvements:

- Fine-tuning models on interview-specific data
- Multi-modal integration (video/audio analysis)
- Real-time feedback generation
- Advanced prompt optimization
- Custom evaluation metrics for interview quality

## 📞 Support

For issues or questions:

1. Check the execution log: `llm_assignment_log.txt`
2. Review error messages in terminal output
3. Ensure all prerequisites are met
4. Try running individual scripts to isolate issues

## 📄 License

This project is for educational purposes as part of the LLM coursework assignment.

---

**Note:** First execution may take 10-15 minutes due to model downloads. Subsequent runs are significantly faster.
