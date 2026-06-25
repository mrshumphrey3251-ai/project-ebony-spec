# Real-Time Media Streaming & Frame Ingestion Specification

This document details the hardware-accelerated video streaming loops, RTP payload packing, and dynamic bitrate adaptations for local video nodes.

## 1. Zero-Copy Frame Ingestion
* **Direct DMA Stream Mapping:** Bypasses intermediate OS kernel memory buffers by copying raw camera frames directly into hardware encoder pipelines via DMA allocations.
* **H.265/HEVC Hardware Encoding:** Utilizes dedicated onboard video processing cores to compress high-definition surveillance matrices with minimal end-to-end latency (<30ms).

## 2. Dynamic Bitrate Control Loops
* Tracks packet delivery feedback loops across the sub-GHz or local network to automatically scale down frame rates and encoding quality if transport lines experience degradation.
