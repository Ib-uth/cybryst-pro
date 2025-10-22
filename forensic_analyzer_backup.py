#!/usr/bin/env python3
"""
Automated Knowledge Acquisition Layer for Digital Forensics

This module implements the foundational Automated Knowledge Acquisition Layer for digital forensics,
addressing the manual data structuring bottleneck identified in Ngo & Le-Khac (2023) and Silva et al. (2024).

The system implements a two-stage LLM pipeline leveraging the low-latency Groq API endpoint:
1. Artifact Extractor Module: Identifies and extracts core digital forensic data
2. Reasoning and Mapping Module: Maps artifacts to strategic attack framework with Zero-Shot CoT reasoning

Author: Sulaiman Ibraheem Uthman
Matric Number: 2019/1/76516CS
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Any, Optional, Tuple
from groq import Groq


def load_report(filepath: str) -> str:
    """
    Load and read the content of a forensic report from text files.
    """
    if not os.path.exists(filepath):
        print(f"❌ Error: File '{filepath}' not found")
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        print(f"❌ Error reading file '{filepath}': {e}")
            sys.exit(1)

    print(f"✓ Successfully loaded report from: {filepath}")
    print(f"✓ Report length: {len(content)} characters")
    return content


class ArtifactExtractorModule:
    """
    Stage 1: Artifact Extractor Module
    
    This module implements the first stage of the Automated Knowledge Acquisition Layer.
    It reliably identifies and extracts core digital forensic data (IPs, hashes, malware, tools)
    and their properties from unstructured cybersecurity incident reports.
    """
    
    def __init__(self):
        """Initialize the Artifact Extractor Module with Groq client."""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY is not set. Please export your API key before running.")
        sys.exit(1)
        self.client = Groq(api_key=api_key)
    
    def extract_artifacts(self, report_text: str) -> Dict[str, Any]:
        """
        Extract core digital forensic artifacts from unstructured incident reports.
        
        This method uses a focused prompt to identify and extract essential forensic indicators
        including IPs, hashes, malware, tools, and their contextual properties.
        
        Args:
            report_text (str): Raw, unstructured cybersecurity incident report
            
        Returns:
            Dict[str, Any]: Structured JSON containing extracted artifacts with properties
        """
        extraction_prompt = """
You are an expert Digital Forensics and Incident Response (DFIR) analyst specializing in automated artifact extraction from cybersecurity incident reports. Your task is to identify and extract core digital forensic data and their properties with high precision.

Focus on extracting these critical artifact types:
- IP addresses (IPv4/IPv6) - include geolocation context if available
- File hashes (MD5, SHA1, SHA256, SHA512) - specify hash type
- Malware names and families - include variant information
- Attack tools and utilities - specify tool versions
- Registry keys and values - include hive information
- Domain names and URLs - include TLD context
- Email addresses - include domain context
- File paths and directories - include system context
- Process names and PIDs - include execution context
- Network ports and protocols - include service context
- User accounts and usernames - include privilege context
- Timestamps and dates - include timezone if available
- MITRE ATT&CK technique IDs - include TTP references

For each artifact, provide:
- type: Precise artifact category
- value: Exact artifact value
- properties: Additional metadata (e.g., hash_type, tool_version, privilege_level)
- context: Brief context about discovery location/usage
- confidence: Extraction confidence (high/medium/low)

IMPORTANT: Return your response as a valid JSON object:
{
    "artifacts": [
        {
            "type": "artifact_type",
            "value": "artifact_value",
            "properties": {"key": "value"},
            "context": "discovery_context",
            "confidence": "high|medium|low"
        }
    ],
    "extraction_metadata": {
        "total_artifacts": 0,
        "high_confidence": 0,
        "medium_confidence": 0,
        "low_confidence": 0
    }
}

Be thorough but precise. Only include artifacts that are clearly identifiable and relevant.
"""

    try:
            print("🔍 [Stage 1] Extracting artifacts using Groq Llama 3...")
        
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": extraction_prompt},
                    {"role": "user", "content": f"Extract all relevant digital forensic artifacts from this incident report:\n\n{report_text}"}
            ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=6000
        )
        
        response_text = response.choices[0].message.content.strip()
        
            # Parse JSON response with error handling
        try:
            artifacts_json = json.loads(response_text)
                artifact_count = len(artifacts_json.get('artifacts', []))
                print(f"✓ Successfully extracted {artifact_count} artifacts")
            return artifacts_json
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            print(f"Raw response: {response_text}")
                # Try to extract JSON from markdown formatting
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                if json_end > json_start:
                    json_text = response_text[json_start:json_end].strip()
                    try:
                        artifacts_json = json.loads(json_text)
                            artifact_count = len(artifacts_json.get('artifacts', []))
                            print(f"✓ Successfully extracted {artifact_count} artifacts (from markdown)")
                        return artifacts_json
                    except json.JSONDecodeError:
                        pass
            raise Exception(f"Failed to parse JSON response: {e}")
            
    except Exception as e:
        print(f"❌ Error during artifact extraction: {e}")
        sys.exit(1)


class ReasoningAndMappingModule:
    """
    Stage 2: Reasoning and Mapping Module
    
    This module implements the second stage of the Automated Knowledge Acquisition Layer.
    It enforces Zero-Shot Chain-of-Thought (CoT) reasoning to dynamically map extracted
    artifacts to a strategic attack framework (Tactic/Technique/Phase proxy), establish
    causal and chronological relationships, and generate explicit natural language
    justifications (XAI) for every inference.
    """
    
    def __init__(self):
        """Initialize the Reasoning and Mapping Module with Groq client."""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY is not set. Please export your API key before running.")
        sys.exit(1)
        self.client = Groq(api_key=api_key)
    
    def reason_and_map(self, artifacts_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply Zero-Shot Chain-of-Thought reasoning to map artifacts to strategic attack framework.
        
        This method uses advanced reasoning to:
        1. Analyze artifact relationships and dependencies
        2. Map to strategic attack framework (Tactic/Technique/Phase proxy)
        3. Establish causal and chronological relationships
        4. Generate explicit XAI justifications for every inference
        
        Args:
            artifacts_json (Dict[str, Any]): Structured artifacts from Stage 1
            
        Returns:
            Dict[str, Any]: Validated JSON object with reasoning chains and mappings
        """
        cot_reasoning_prompt = """
You are a senior cyber threat intelligence analyst with expertise in attack pattern analysis and strategic reasoning. Your task is to apply Zero-Shot Chain-of-Thought (CoT) reasoning to map forensic artifacts to a strategic attack framework.

REASONING FRAMEWORK:
1. Analyze each artifact's role in the attack lifecycle
2. Identify tactical relationships between artifacts
3. Establish chronological attack progression
4. Map to strategic attack framework (Tactic/Technique/Phase proxy)
5. Generate explicit justifications for every inference (XAI)

STRATEGIC ATTACK FRAMEWORK MAPPING:
- TACTIC: High-level attack objective (e.g., "Initial Access", "Persistence", "Privilege Escalation")
- TECHNIQUE: Specific method used (e.g., "Phishing", "Registry Run Key", "Process Injection")
- PHASE: Attack lifecycle stage (e.g., "Preparation", "Execution", "Maintenance", "Exfiltration")

CHAIN-OF-THOUGHT REASONING PROCESS:
For each artifact, follow this reasoning chain:
1. What is this artifact's technical function?
2. What attack tactic does it support?
3. What specific technique does it implement?
4. What phase of the attack lifecycle is this?
5. How does it relate to other artifacts chronologically?
6. What is the explicit justification for this mapping?

IMPORTANT: Return your response as a validated JSON object:
{
    "reasoning_chains": [
        {
            "artifact_id": "artifact_identifier",
            "artifact": {
                "type": "artifact_type",
                "value": "artifact_value",
                "properties": {},
                "context": "context"
            },
            "reasoning_steps": [
                {
                    "step": 1,
                    "question": "What is this artifact's technical function?",
                    "analysis": "detailed_analysis",
                    "conclusion": "conclusion"
                },
                {
                    "step": 2,
                    "question": "What attack tactic does it support?",
                    "analysis": "detailed_analysis",
                    "conclusion": "conclusion"
                }
            ],
            "final_mapping": {
                "tactic": "TACTIC_NAME",
                "technique": "TECHNIQUE_NAME", 
                "phase": "PHASE_NAME",
                "confidence": "high|medium|low",
                "explicit_justification": "detailed_natural_language_explanation"
            }
        }
    ],
    "attack_timeline": [
        {
            "phase": "PHASE_NAME",
            "tactic": "TACTIC_NAME",
            "technique": "TECHNIQUE_NAME",
            "artifacts": ["artifact_ids"],
            "chronological_order": 1,
            "causal_relationships": ["relationships_to_other_phases"],
            "phase_justification": "why_this_phase_comes_here"
        }
    ],
    "overall_attack_narrative": "comprehensive_narrative_with_explicit_reasoning",
    "confidence_assessment": {
        "overall_confidence": "high|medium|low",
        "reasoning_quality": "detailed_assessment",
        "mapping_validation": "validation_summary"
    }
}

Apply rigorous reasoning and provide explicit justifications for every inference.
"""

    try:
            print("🧠 [Stage 2] Applying Zero-Shot CoT reasoning using Groq Mixtral...")
        
        # Convert artifacts to a readable format for the AI
        artifacts_text = json.dumps(artifacts_json, indent=2)
        
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
            messages=[
                    {"role": "system", "content": cot_reasoning_prompt},
                    {"role": "user", "content": f"Apply Zero-Shot Chain-of-Thought reasoning to map these artifacts to the strategic attack framework:\n\n{artifacts_text}"}
            ],
                temperature=0.3,  # Balanced temperature for creative reasoning
                max_tokens=8000
        )
        
        response_text = response.choices[0].message.content.strip()
        
            # Parse JSON response with comprehensive error handling
            try:
                reasoning_json = json.loads(response_text)
                chain_count = len(reasoning_json.get('reasoning_chains', []))
                print(f"✓ Successfully applied CoT reasoning with {chain_count} reasoning chains")
                return reasoning_json
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            print(f"Raw response: {response_text}")
                # Try to extract JSON from markdown formatting
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                if json_end > json_start:
                    json_text = response_text[json_start:json_end].strip()
                    try:
                            reasoning_json = json.loads(json_text)
                            chain_count = len(reasoning_json.get('reasoning_chains', []))
                            print(f"✓ Successfully applied CoT reasoning with {chain_count} reasoning chains (from markdown)")
                            return reasoning_json
                    except json.JSONDecodeError:
                        pass
            raise Exception(f"Failed to parse JSON response: {e}")
            
    except Exception as e:
            print(f"❌ Error during reasoning and mapping: {e}")
        sys.exit(1)


def print_analysis_results(reasoning_json: Dict[str, Any]) -> None:
    """
    Print the Automated Knowledge Acquisition Layer analysis results.
    
    Args:
        reasoning_json (Dict[str, Any]): Complete reasoning and mapping results
    """
    print("\n" + "="*80)
    print("🧠 AUTOMATED KNOWLEDGE ACQUISITION LAYER - ANALYSIS RESULTS")
    print("="*80)
    
    # Overall attack narrative
    attack_narrative = reasoning_json.get('overall_attack_narrative', 'No narrative available')
    print(f"\n📋 ATTACK NARRATIVE:")
    print("-" * 40)
    print(attack_narrative)
    
    # Confidence assessment
    confidence = reasoning_json.get('confidence_assessment', {})
    overall_confidence = confidence.get('overall_confidence', 'unknown')
    reasoning_quality = confidence.get('reasoning_quality', 'No assessment available')
    
    print(f"\n🎯 CONFIDENCE ASSESSMENT:")
    print("-" * 40)
    print(f"Overall Confidence: {overall_confidence.upper()}")
    print(f"Reasoning Quality: {reasoning_quality}")
    
    # Attack timeline with strategic framework
    attack_timeline = reasoning_json.get('attack_timeline', [])
    print(f"\n📊 STRATEGIC ATTACK FRAMEWORK TIMELINE:")
    print("-" * 40)
    
    for phase_data in attack_timeline:
        phase_name = phase_data.get('phase', 'Unknown Phase')
        tactic = phase_data.get('tactic', 'Unknown Tactic')
        technique = phase_data.get('technique', 'Unknown Technique')
        chronological_order = phase_data.get('chronological_order', 0)
        phase_justification = phase_data.get('phase_justification', 'No justification provided')
        
        print(f"\n🔸 {chronological_order}. {phase_name.upper()}")
        print(f"   Tactic: {tactic}")
        print(f"   Technique: {technique}")
        print(f"   Justification: {phase_justification}")
    
    # Reasoning chains (detailed XAI)
    reasoning_chains = reasoning_json.get('reasoning_chains', [])
    print(f"\n🧠 REASONING CHAINS (XAI):")
    print("-" * 40)
    
    for i, chain in enumerate(reasoning_chains[:3], 1):  # Show first 3 chains for brevity
        artifact = chain.get('artifact', {})
            artifact_type = artifact.get('type', 'unknown')
            artifact_value = artifact.get('value', 'N/A')
        final_mapping = chain.get('final_mapping', {})
        explicit_justification = final_mapping.get('explicit_justification', 'No justification provided')
        
        print(f"\n🔍 Reasoning Chain {i}:")
        print(f"   Artifact: {artifact_type} = {artifact_value}")
        print(f"   XAI Justification: {explicit_justification}")
    
    if len(reasoning_chains) > 3:
        print(f"\n   ... and {len(reasoning_chains) - 3} more reasoning chains (see JSON output for details)")
    
    print("\n" + "="*80)
    print("✅ AUTOMATED KNOWLEDGE ACQUISITION COMPLETE")
    print("="*80)




def main():
    """
    Main execution function for the Automated Knowledge Acquisition Layer.
    
    This function orchestrates the two-stage LLM pipeline:
    1. Artifact Extractor Module: Extract core digital forensic data
    2. Reasoning and Mapping Module: Apply Zero-Shot CoT reasoning for strategic mapping
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Automated Knowledge Acquisition Layer for Digital Forensics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python forensic_analyzer.py reports/sample_report.txt
  python forensic_analyzer.py reports/sample_report.txt --output-json

Output:
  - Summary reports are automatically saved to 'outputs/' folder
  - Use --output-json to save complete structured JSON analysis
  - Output directories are created automatically if they don't exist

Environment Variables:
  GROQ_API_KEY      Your Groq API key (required)
        """
    )
    
    parser.add_argument(
        'filepath',
        help='Path to the cybersecurity incident report text file to analyze'
    )
    
    parser.add_argument(
        '--output-json',
        action='store_true',
        help='Save the complete structured JSON analysis for ontology ingestion'
    )
    
    args = parser.parse_args()
    
    # Check if the file exists
    if not os.path.exists(args.filepath):
        print(f"❌ Error: File '{args.filepath}' does not exist")
        sys.exit(1)
    
    print("🚀 Starting Automated Knowledge Acquisition Layer...")
    print(f"📁 Analyzing incident report: {args.filepath}")
    
    try:
        # Step 1: Load the incident report
        report_content = load_report(args.filepath)
        
        # Step 2: Initialize and run Stage 1 - Artifact Extractor Module
        artifact_extractor = ArtifactExtractorModule()
        artifacts_result = artifact_extractor.extract_artifacts(report_content)
        
        # Step 3: Initialize and run Stage 2 - Reasoning and Mapping Module
        reasoning_mapper = ReasoningAndMappingModule()
        reasoning_result = reasoning_mapper.reason_and_map(artifacts_result)
        
        # Step 4: Display results
        print_analysis_results(reasoning_result)
        
        # Always save a summary report to outputs folder
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = os.path.splitext(os.path.basename(args.filepath))[0]
        
        # Save summary report
        summary_filename = os.path.join(output_dir, f"knowledge_acquisition_summary_{base_filename}_{timestamp}.txt")
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("AUTOMATED KNOWLEDGE ACQUISITION LAYER - ANALYSIS SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Source File: {args.filepath}\n")
            f.write(f"Analysis Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Tool: Automated Knowledge Acquisition Layer v2.0\n\n")
            
            attack_narrative = reasoning_result.get('overall_attack_narrative', 'No narrative available')
            f.write("ATTACK NARRATIVE:\n")
            f.write("-" * 30 + "\n")
            f.write(attack_narrative + "\n\n")
            
            confidence = reasoning_result.get('confidence_assessment', {})
            f.write("CONFIDENCE ASSESSMENT:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Overall Confidence: {confidence.get('overall_confidence', 'unknown')}\n")
            f.write(f"Reasoning Quality: {confidence.get('reasoning_quality', 'No assessment')}\n\n")
            
            f.write("STRATEGIC ATTACK FRAMEWORK TIMELINE:\n")
            f.write("-" * 30 + "\n")
            attack_timeline = reasoning_result.get('attack_timeline', [])
            for phase_data in attack_timeline:
                phase_name = phase_data.get('phase', 'Unknown Phase')
                tactic = phase_data.get('tactic', 'Unknown Tactic')
                technique = phase_data.get('technique', 'Unknown Technique')
                chronological_order = phase_data.get('chronological_order', 0)
                f.write(f"\n{chronological_order}. {phase_name.upper()}\n")
                f.write(f"   Tactic: {tactic}\n")
                f.write(f"   Technique: {technique}\n")
        
        print(f"\n📄 Summary report saved to: {summary_filename}")
        
        # Optional: Save complete structured JSON for ontology ingestion
        if args.output_json:
            output_filename = os.path.join(output_dir, f"knowledge_acquisition_complete_{base_filename}_{timestamp}.json")

            complete_results = {
                "artifacts": artifacts_result,
                "reasoning_and_mapping": reasoning_result,
                "source_file": args.filepath,
                "analysis_timestamp": timestamp,
                "analysis_tool": "Automated Knowledge Acquisition Layer v2.0",
                "ontology_ready": True
            }

            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(complete_results, f, indent=2, ensure_ascii=False)

            print(f"\n💾 Complete structured analysis saved to: {output_filename}")
            print("📊 JSON output is ready for immediate DFIR ontology ingestion")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
