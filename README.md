# Cybryst Pro - AI-Powered Digital Forensics Analysis

## Overview

Cybryst Pro is an advanced AI-powered digital forensics analysis tool that addresses the manual data structuring bottleneck identified in Ngo & Le-Khac (2023) and Silva et al. (2024). The system autonomously converts raw, unstructured cybersecurity incident reports into structured, ontology-ready knowledge instances using a sophisticated two-stage LLM pipeline.

## Key Features

- **Two-Stage LLM Pipeline**: Artifact extraction followed by reasoning and mapping
- **Zero-Shot Chain-of-Thought Reasoning**: Advanced reasoning with explicit justifications
- **Strategic Attack Framework Mapping**: Maps to Tactic/Technique/Phase proxy framework
- **Explainable AI (XAI)**: Natural language justifications for every inference
- **Low-Latency Processing**: Optimized for Groq API with Llama 3 and Mixtral models
- **Ontology-Ready Output**: Structured JSON suitable for immediate DFIR ontology ingestion

## Architecture

### Stage 1: Artifact Extractor Module
- Extracts core digital forensic data (IPs, hashes, malware, tools)
- Uses Llama 3.1-70B-Versatile for consistent artifact identification
- Provides confidence assessments for each extraction

### Stage 2: Reasoning and Mapping Module
- Applies Zero-Shot CoT reasoning for strategic mapping
- Establishes causal and chronological relationships
- Uses Mixtral-8x7B-32768 for advanced reasoning capabilities
- Generates explicit XAI justifications for every inference

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Groq API key (get one from [Groq Console](https://console.groq.com/))

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ib-uth/cybryst-pro.git
   cd cybryst-pro
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install groq
   ```

4. **Set up your Groq API key**
   ```bash
   # Option 1: Export as environment variable (temporary)
   export GROQ_API_KEY="your_groq_api_key_here"

   #option 2 (for windows): Export as environmental variable (temporary on powershell)
   $env:GROQ_API_KEY = "your_groq_api_key_here"
   
   # Option 3: Add to your shell profile (permanent)
   echo 'export GROQ_API_KEY="your_groq_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   
   # Option 4: Create a .env file (if you add python-dotenv support)
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

5. **Verify installation**
   ```bash
   python cybryst_pro.py --help
   ```

### Running the Analysis

1. **Basic analysis with summary report**
   ```bash
   python cybryst_pro.py reports/sample_report.txt
   ```

2. **Complete analysis with JSON output for ontology ingestion**
   ```bash
   python cybryst_pro.py reports/sample_report.txt --output-json
   ```

3. **Analyze your own report**
   ```bash
   # Place your incident report in the reports/ folder
   python cybryst_pro.py reports/your_report.txt --output-json
   ```

### Output
- **Summary Report**: Human-readable analysis summary saved to `outputs/` folder
- **Complete JSON**: Structured analysis ready for ontology ingestion (with `--output-json` flag)

## Output Structure

The system generates a comprehensive JSON structure containing:

- **Artifacts**: All extracted forensic indicators with metadata
- **Reasoning Chains**: Complete XAI documentation for every inference
- **Attack Timeline**: Chronologically ordered attack progression
- **Confidence Assessment**: Quality metrics for all mappings
- **Strategic Framework Mapping**: Tactic/Technique/Phase classifications

## Documentation

- **how_it_works.md**: Comprehensive technical documentation for Chapter 4
- **README.md**: This overview document

## Research Context

This system addresses critical bottlenecks in digital forensics:
- Manual structuring of unstructured incident reports
- Knowledge acquisition challenges in DFIR workflows
- Lack of automated reasoning for artifact mapping
- Need for explainable AI in forensic applications

## Author

**Sulaiman Ibraheem Uthman**  
Final Year Project - Cyber Security Science  
Federal University of Technology, Minna 2025

## License

This project is developed for academic research purposes.
