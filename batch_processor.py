"""Batch processing utilities for handling large datasets."""

import time
from typing import List, Dict
from pathlib import Path


class BatchProcessor:
    """Handles batch processing with progress tracking and error recovery."""
    
    def __init__(self, batch_size: int = 50, save_interval: int = 100):
        self.batch_size = batch_size
        self.save_interval = save_interval
        self.processed_count = 0
        self.error_count = 0
        self.start_time = None
    
    def start(self):
        """Start the batch processor."""
        self.start_time = time.time()
        self.processed_count = 0
        self.error_count = 0
    
    def update_progress(self, current: int, total: int, image_name: str, is_correct: bool = None):
        """Update and display progress."""
        elapsed = time.time() - self.start_time
        rate = current / elapsed if elapsed > 0 else 0
        eta = (total - current) / rate if rate > 0 else 0
        
        status = ""
        if is_correct is not None:
            status = "✓" if is_correct else "✗"
        
        progress_bar = self._create_progress_bar(current, total, width=40)
        
        print(f"\r[{current}/{total}] {progress_bar} {status} {image_name[:30]:30s} | "
              f"Rate: {rate:.1f} img/s | ETA: {self._format_time(eta)}", end="", flush=True)
    
    def _create_progress_bar(self, current: int, total: int, width: int = 40) -> str:
        """Create a text-based progress bar."""
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        percentage = 100 * current / total
        return f"{bar} {percentage:.1f}%"
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds into human-readable time."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds/60)}m {int(seconds%60)}s"
        else:
            return f"{int(seconds/3600)}h {int((seconds%3600)/60)}m"
    
    def finish(self, total: int):
        """Finish batch processing and display summary."""
        elapsed = time.time() - self.start_time
        print(f"\n\n✓ Batch processing complete!")
        print(f"  Total time: {self._format_time(elapsed)}")
        print(f"  Average rate: {total/elapsed:.2f} images/second")
        print(f"  Errors: {self.error_count}")
