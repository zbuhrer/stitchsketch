
# Pointcloud Data File Structure

Organize this directory thusly

```shell
.pointcloud-data/
├── raw/
│   ├── job_001/
│   │   ├── images/
│   │   │   ├── image1.jpg
│   │   │   ├── image2.jpg
│   │   │   └── ...
│   │   └── metadata.json
│   └── job_002/
│       └── ...
├── processed/
│   ├── job_001/
│   │   ├── sparse/
│   │   ├── dense/
│   │   ├── mesh/
│   │   └── metadata.json
│   └── job_002/
│       └── ...
└── potree/
    ├── job_001/
    │   ├── pointcloud.js
    │   ├── metadata.json
    │   └── ...
    └── job_002/
        └── ...
```
