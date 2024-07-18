import subprocess
import os
import json
from datetime import datetime

def process_images(job_id):
    input_dir = f"/data/raw/{job_id}/images"
    output_dir = f"/data/processed/{job_id}"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Run COLMAP
    colmap_result = subprocess.run(["colmap", "automatic_reconstructor", 
                    "--image_path", input_dir,
                    "--workspace_path", output_dir],
                    capture_output=True, text=True)

    if colmap_result.returncode != 0:
        raise Exception(f"COLMAP processing failed: {colmap_result.stderr}")

    # Convert to Potree format
    potree_dir = f"/data/potree/{job_id}"
    potree_result = subprocess.run(["PotreeConverter", 
                    f"{output_dir}/dense/fused.ply",
                    "-o", potree_dir,
                    "--generate-page", "index"],
                    capture_output=True, text=True)

    if potree_result.returncode != 0:
        raise Exception(f"Potree conversion failed: {potree_result.stderr}")

    # Update metadata
    update_metadata(job_id, colmap_result, potree_result)

def update_metadata(job_id, colmap_result, potree_result):
    metadata = {
        "job_id": job_id,
        "processing_date": datetime.utcnow().isoformat(),
        "colmap_output": colmap_result.stdout,
        "potree_output": potree_result.stdout,
        "status": "completed",
        "potree_url": f"/potree/{job_id}/index.html"  # Adjust this URL as needed
    }
    
    metadata_file = f"/data/processed/{job_id}/metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)