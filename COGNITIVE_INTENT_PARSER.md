# COGNITIVE_INTENT_PARSER: Offline NLP & Syntactic Bounding

**Classification:** Gated Engineering Documentation / Cognitive Layer
**Target Architecture:** INT8 Tensor Cores / Local Transformer Pipeline

This specification handles the offline linguistic processing, local intent classification, and syntax-bound command routing layers. Project Ebony fundamentally rejects cloud-based natural language APIs (e.g., Siri, Alexa, or cloud LLMs). All human-to-machine verbal and text interactions must be parsed, classified, and executed natively on the edge hardware, guaranteeing operational sovereignty and zero-latency inference in disconnected environments.

## 1. Offline Natural Language Comprehension & Local Inference
To extract intent from unstructured operator input, the node relies on an embedded, heavily optimized transformer architecture.

* **Local Parsing Pipeline:** Raw acoustic commands are converted to text via a localized Speech-To-Text (STT) model. These tokens are ingested by an INT8-quantized transformer module running directly on the NVIDIA Jetson Orin's Tensor Cores.
* **Native Attention Compute:** The system evaluates operator intent locally by computing the scaled dot-product attention natively on the edge silicon:
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
  *(Where $Q, K, V$ represent the query, key, and value token matrices derived from the operator's input, and $d_k$ is the scaling dimension).* This allows the node to extract contextual mechanical directives from natural human speech without transmitting audio to a remote server.

## 2. Strict Grammar Constraining & Deterministic Mapping
Transformers are inherently probabilistic, which is unacceptable for kinetic control. The parser mathematically binds all natural language outputs into strict, pre-approved execution structures.

* **Frozen Command Schemas:** The node forces the output tokens to compile against a hardcoded, immutable system command schema ($\mathcal{G}$).
* **Constrained Probability Decoding:** The parsing engine evaluates the raw language input ($U$) and maps it exclusively to a deterministic system action ($C$). The system calculates the maximum probability of a command sequence strictly bounded by the allowed grammar:
  $$\hat{C} = \arg\max_{C \in \mathcal{G}} P(C \mid U)$$
  If the human input attempts to instruct an action that does not exist within $\mathcal{G}$ (e.g., an unauthorized override or out-of-bounds mechanical actuation), the probability computes to zero, the input is discarded, and the node registers a syntax error without engaging the physical actuators.

## 3. Deterministic Resource Bounding & Kernel Isolation
Natural Language Processing is computationally expensive and poses a severe threat to real-time physical control loops if left unmanaged.

* **`cgroups` Hardware Execution Lanes:** The entire cognitive parsing engine is strictly confined within localized Linux kernel `cgroups` (Pool Beta - `SCHED_OTHER`). 
* **Preemption Guarantee:** The RT-PREEMPT kernel enforces absolute compute isolation. Even if the transformer module maxes out its allocated Tensor Cores attempting to parse a complex, garbled acoustic input, it is mathematically incapable of stealing CPU cycles from the `SCHED_FIFO` threads governing the J1939 CAN bus or Modbus RTU telemetry loops. Physical safety is completely insulated from cognitive processing.
