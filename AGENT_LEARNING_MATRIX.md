# AGENT_LEARNING_MATRIX: Local Cognitive Inference & Behavioral Bounding

**Classification:** Gated Engineering Documentation / Cognitive Layer
**Target Architecture:** NVIDIA Jetson Orin NX / Local DLA Cores

This specification details the isolated local model weight execution and deterministic behavioral grading protocols. To guarantee absolute physical safety, large language models (LLMs) and neural networks operating on the edge must be mathematically bounded, ensuring cognitive inference cannot disrupt physical control loops or output out-of-bounds mechanical instructions.

## 1. Edge Inference Isolation & Deterministic Bounding
Cognitive models share the same physical silicon as the primary hydraulic control systems, requiring violent separation of compute resources.

* **Strict `cgroups` Allocation:** As defined in `SECURE_BOOT.md`, all TensorRT engine executions and DLA inferences are strictly sandboxed within **Pool Beta** (`SCHED_OTHER`). 
* **Hardware Starvation Prevention:** The Linux kernel enforces absolute execution throttling on the cognitive threads. Even if a local LLM execution spikes to 100% compute load during a complex risk calculation, the RT-PREEMPT kernel guarantees the physical `SCHED_FIFO` control loops (CAN bus / Modbus) will never suffer CPU starvation or missed physical deadlines.

## 2. Frozen Grammar & Syntactic Masking
Unconstrained generative models are inherently non-deterministic, making them dangerous for physical actuator translation. Project Ebony forces all cognitive outputs through a hardcoded, bare-metal syntax mask.

* **Logit Masking:** Before the model is permitted to sample the next token, the native C++ runtime intercepts the output logits. The system applies a rigid, predefined grammar schema (e.g., restricting outputs exclusively to valid J1939 hexadecimal commands or predefined FlatBuffer structs). 
* **Probability Bounding:** The masked probability distribution is enforced natively via:
  $$P(w_i \mid w_{<i}) = \frac{\exp(l_i + M_i)}{\sum_j \exp(l_j + M_j)}$$
  *(Where $l_i$ represents the raw logit, and the strict-syntax mask $M_i = 0$ for allowed operational tokens, or $M_i = -\infty$ for out-of-bounds characters).* This mathematical constraint physically prevents the neural network from hallucinating syntax.

## 3. Local Experience Accumulation & Zero-Cloud Memory
The edge node continuously refines its behavioral logic based on environmental interactions without relying on external corporate telemetry, remote databases, or cloud-based storage.

* **Encrypted State Histories:** All interaction logs, telemetry deltas, and automated risk calculations are cached strictly within localized NVMe storage. 
* **TPM-Bound Enclaves:** These experience ledgers are written directly to the LUKS2 block-encrypted partitions sealed by the TPM 2.0 hardware root of trust. This architecture guarantees that proprietary operational data, failure histories, and learned risk heuristics remain 100% inaccessible to unauthorized extraction, even if the asset is physically captured by an adversary.
