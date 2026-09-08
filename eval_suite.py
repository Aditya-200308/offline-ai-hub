"""
Standalone Automated Evaluation & Test Suite for OfflineAI Hub
Runs programmatic tests for:
1. Hardware telemetry extraction
2. In-memory document indexing & retrieval
3. Privacy and PII redaction scanner
4. Local transaction audit logs
5. Inference latency & speed profiling
"""

import sys
import io
import time

# Ensure UTF-8 output encoding on Windows consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.hardware_monitor import HardwareMonitor
from src.local_llm import LocalLLMEngine
from src.document_vault import LocalDocumentVault
from src.privacy_auditor import PrivacyAuditor
from src.benchmarks import BenchmarkRunner


def run_all_tests():
    print("=" * 65)
    print("  [OfflineAI Hub] LOCAL AI ASSISTANT & BENCHMARK EVALUATION")
    print("=" * 65)

    passed = 0
    total = 5

    # Test 1: Hardware Telemetry
    print("\n[TEST 1/5] Testing Hardware Telemetry Extraction...")
    specs = HardwareMonitor.get_system_specs()
    live = HardwareMonitor.get_live_metrics()
    if specs.get("total_ram_gb", 0) > 0 and "cpu_percent" in live:
        print(f"  ✅ PASS: Detected {specs['total_ram_gb']}GB RAM, {specs['physical_cores']} Physical Cores.")
        passed += 1
    else:
        print("  ❌ FAIL: Could not retrieve system hardware metrics.")

    # Test 2: Local Document Vault & Vector Indexer
    print("\n[TEST 2/5] Testing In-Memory Document Ingestion & TF-IDF Search...")
    vault = LocalDocumentVault()
    vault.ingest_file("sample_clinical.txt", b"Trial protocol ABC-123 indicates patient recovery rate of 94.2% within 8 weeks.")
    vault.ingest_file("server_config.txt", b"Database master node is located at internal IP 10.0.4.15 on subnet Alpha.")
    results = vault.search("patient recovery rate", top_k=1)
    if results and "ABC-123" in results[0][0]["text"]:
        print(f"  ✅ PASS: Retrieved relevant chunk with similarity score: {results[0][1]}")
        passed += 1
    else:
        print("  ❌ FAIL: Vector search failed to retrieve ground truth.")

    # Test 3: Privacy & PII Scanner
    print("\n[TEST 3/5] Testing PII & Secret Redaction Scanner...")
    leak_test = "Patient SSN is 123-45-6789 and API key is sk-1234567890abcdef1234567890abcdef."
    scan_res = PrivacyAuditor.scan_for_leaks(leak_test)
    if scan_res["has_leaks"] and scan_res["leak_count"] >= 2:
        print(f"  ✅ PASS: Successfully detected {scan_res['leak_count']} sensitive entities.")
        passed += 1
    else:
        print("  ❌ FAIL: PII scanner failed to detect test credentials.")

    # Test 4: Local Transaction Audit Log
    print("\n[TEST 4/5] Testing Local Transaction Hash Generation...")
    cert = PrivacyAuditor.generate_privacy_certificate("query", "response", "llama3.2")
    if cert.get("sha256_hash") and len(cert["sha256_hash"]) == 64:
        print(f"  ✅ PASS: Generated transaction ID {cert['certificate_id']} with SHA-256 hash.")
        passed += 1
    else:
        print("  ❌ FAIL: Hash generation failed.")

    # Test 5: Inference Latency & Speed Profiling
    print("\n[TEST 5/5] Testing LLM Generation & Telemetry Pipeline...")
    engine = LocalLLMEngine()
    res = engine.generate("Respond with 'OK' only.", temperature=0.1)
    if "tokens_per_sec" in res and res.get("total_latency_s", 0) > 0:
        print(f"  ✅ PASS: Engine '{res['engine']}' completed in {res['total_latency_s']}s ({res['tokens_per_sec']} t/s).")
        passed += 1
    else:
        print("  ❌ FAIL: LLM engine generation failed.")

    print("\n" + "=" * 65)
    print(f"  TEST RESULTS: {passed}/{total} PASSED ({round(passed/total*100, 1)}%)")
    print("=" * 65)

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
