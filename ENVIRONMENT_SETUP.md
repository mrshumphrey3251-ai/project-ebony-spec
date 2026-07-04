# LOCAL_ENVIRONMENT_SETUP: Deterministic Build Chains & Memory Bounding

**Classification:** Gated Engineering Documentation / Base Build & Compilation Layer
**Target Architecture:** `aarch64-linux-gnu` / Jetson Orin NX / RT-PREEMPT

This technical blueprint profiles the precise software packages, build tools, and local dependencies required to safely cross-compile and flash the sovereign runtime target. Project Ebony requires absolute determinism; the local host environment must compile the C++ firmware without introducing hidden virtual memory dependencies, garbage collection, or unpredictable execution branching.

## 1. Toolchain & Tool Dependencies (Build DAG)
The compilation matrix must be highly optimized and immune to dependency race conditions during parallel compilation. 

* **Cross-Compiler Target:** The system mandates the GNU Compiler Collection (GCC) or LLVM/Clang explicitly configured for the `aarch64-linux-gnu` architecture. This ensures the host (x86_64) generates machine code strictly tailored to the Jetson Orin's ARMv8 instruction set.
* **Build Systems Needed:** CMake (Version 3.28 or later) combined with a Ninja build manager target. 
* **Dependency Graph Compute:** Ninja evaluates the compilation pipeline as a strict Directed Acyclic Graph (DAG). Let the build graph be $G = (V, E)$, where vertices $V$ are compilation tasks and edges $E$ are dependencies. The system achieves high-velocity compilation pipelines by perfectly parallelizing tasks outside the critical path ($P_{critical}$). The theoretical minimum build time ($T_{build}$) is mathematically bounded natively:
  $$T_{build} = \sum_{v \in P_{critical}} C(v)$$
  *(Where $C(v)$ represents the execution time of task $v$ on the critical path).* This guarantees efficient, reproducible builds without linking errors across disconnected environments.

## 2. Target Compilation Flags & Memory Determinism
To survive in a hard real-time physical environment, the resulting binary must be mathematically prevented from allocating dynamic memory unpredictably or relying on virtual page swaps.

* **Strict Hardware Safety Parameters:** The compiler must be invoked with `-O2 -Wall -Werror` to prioritize optimized execution while treating all structural warnings as fatal compilation failures. Furthermore, `-fno-exceptions` and `-fno-rtti` are mandated to prevent unpredictable stack unwinding and runtime overhead.
* **Deterministic Memory Footprint:** The compilation flags must lock runtime memory footprints inside tight deterministic bounds without virtual page pooling. The linker is configured to statically allocate all required memory structures upon initialization. The total memory footprint ($M_{total}$) of all statically linked symbols ($sym_i$) must be mathematically verified at compile time to strictly fall below the available physical RAM ($M_{phys}$):
  $$M_{total} = \sum_{i=1}^{N} \text{sizeof}(sym_i) \le M_{phys}$$
  If $M_{total}$ exceeds the physical bounds, the compilation fails natively. By explicitly disabling virtual memory mapping (no swap space), the kernel guarantees that page fault latency ($\Delta t_{fault}$) is mathematically forced to zero:
  $$\Delta t_{fault} = 0 \text{ ms}$$
  This ensures the Jetson's CPU cycles are entirely dedicated to kinetic control and inference, never waiting on physical disk I/O.
