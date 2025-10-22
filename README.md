# Automated Knowledge Acquisition Layer for Digital Forensics

## Overview

This project implements the foundational Automated Knowledge Acquisition Layer for digital forensics, addressing the manual data structuring bottleneck identified in Ngo & Le-Khac (2023) and Silva et al. (2024). The system autonomously converts raw, unstructured cybersecurity incident reports into structured, ontology-ready knowledge instances using a sophisticated two-stage LLM pipeline.

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

## Usage

### Prerequisites
- Python 3.x
- Groq API key (set as environment variable `GROQ_API_KEY`)
- `groq` Python package

### Installation
```bash
pip install groq
export GROQ_API_KEY="your_groq_api_key_here"
```

### Running the Analysis
```bash
# Basic analysis
python forensic_analyzer.py reports/sample_report.txt

# Analysis with complete JSON output for ontology ingestion
python forensic_analyzer.py reports/sample_report.txt --output-json
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
Matric Number: 2019/1/76516CS

## License

This project is developed for academic research purposes.