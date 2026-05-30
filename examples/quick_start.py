#!/usr/bin/env python3
"""
Quick Start Example
===================
Demonstrates how to use the Unified Inertia Theory framework
to analyze a conversation for cognitive inertia patterns.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.metrics import InertiaMetrics


def analyze_sample_conversation():
    """Analyze a sample conversation for inertia patterns."""
    
    # Sample conversation (simulated)
    conversation = [
        {"role": "user", "content": "帮我优化这个数据处理管道"},
        {"role": "assistant", "content": "我看看代码... 有个TODO注释说要用chunked iteration"},
        {"role": "assistant", "content": "我觉得chunked iteration是对的，开始实现"},
        {"role": "assistant", "content": "分块处理应该能解决内存问题"},
        {"role": "assistant", "content": "实现了流式读取+分块处理"},
    ]
    
    # Extract assistant messages
    assistant_texts = [msg["content"] for msg in conversation if msg["role"] == "assistant"]
    
    # Initialize metrics
    metrics = InertiaMetrics()
    
    # Analyze
    result = metrics.analyze_session(assistant_texts)
    
    print("=" * 60)
    print("Sample Conversation Analysis")
    print("=" * 60)
    print(f"\nConversation length: {len(conversation)} messages")
    print(f"Assistant messages: {len(assistant_texts)}")
    print("\n--- Inertia Metrics ---")
    print(f"F01 (Anchoring): {result.get('F01', 'N/A')}")
    print(f"H (Self-excitation): {result.get('H', 'N/A')}")
    print(f"θ (Deviation): {result.get('θ', 'N/A')}")
    print(f"\nHealth Status: {result.get('health', 'N/A')}")
    print(f"Rule Triggered: {result.get('rule', 'N/A')}")
    
    return result


if __name__ == "__main__":
    print("Unified Inertia Theory - Quick Start")
    print("=" * 60)
    print("\nThis example demonstrates basic inertia detection.\n")
    
    result = analyze_sample_conversation()
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Use InertiaMetrics.analyze_session() with your own data")
    print("2. Use InertiaMonitor for real-time monitoring")
    print("3. Use AutoCheck for automated health checks")
    print("\nSee docs/ for detailed documentation.")
