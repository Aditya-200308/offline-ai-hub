"""
Hardware Monitor & Telemetry Module
Uses psutil to extract real-time CPU, RAM, and hardware utilization metrics.
"""

import os
import platform
import time
import psutil


class HardwareMonitor:
    """Provides real-time system and process telemetry for local AI inference."""

    @staticmethod
    def get_system_specs() -> dict:
        """Retrieves static and baseline system specs."""
        mem = psutil.virtual_memory()
        cpu_freq = psutil.cpu_freq()
        
        # Detect CPU Architecture
        arch = platform.machine()
        processor = platform.processor() or platform.uname().processor or "x86_64 / ARM"
        os_info = f"{platform.system()} {platform.release()}"
        
        return {
            "os": os_info,
            "processor": processor,
            "architecture": arch,
            "physical_cores": psutil.cpu_count(logical=False) or 1,
            "logical_cores": psutil.cpu_count(logical=True) or 1,
            "cpu_freq_mhz": round(cpu_freq.current, 1) if cpu_freq else "N/A",
            "total_ram_gb": round(mem.total / (1024 ** 3), 2),
            "available_ram_gb": round(mem.available / (1024 ** 3), 2),
            "ram_percent": mem.percent
        }

    @staticmethod
    def get_live_metrics() -> dict:
        """Gets instantaneous snapshot of CPU, RAM, and process memory."""
        mem = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        current_process = psutil.Process(os.getpid())
        proc_mem = current_process.memory_info()
        
        return {
            "cpu_percent": cpu_percent,
            "ram_used_gb": round((mem.total - mem.available) / (1024 ** 3), 2),
            "ram_free_gb": round(mem.available / (1024 ** 3), 2),
            "ram_percent": mem.percent,
            "process_rss_mb": round(proc_mem.rss / (1024 ** 2), 2),
            "process_vms_mb": round(proc_mem.vms / (1024 ** 2), 2),
            "timestamp": time.time()
        }

    @staticmethod
    def track_inference(func, *args, **kwargs):
        """
        Executes an inference function while profiling CPU spikes, 
        memory deltas, and elapsed time.
        """
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        start_time = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        mem_after = process.memory_info().rss
        elapsed = end_time - start_time
        mem_delta_mb = round((mem_after - mem_before) / (1024 ** 2), 2)
        
        telemetry = {
            "elapsed_seconds": round(elapsed, 4),
            "memory_delta_mb": mem_delta_mb,
            "end_rss_mb": round(mem_after / (1024 ** 2), 2)
        }
        
        return result, telemetry
