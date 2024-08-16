
# StitchSketch

## Description

## Diagram

```mermaid
graph TD
    A[Client] --> B[API Gateway]
    B --> C[Image Processing Service]
    B --> D[3D Reconstruction Service]
    B --> E[Upholstery Service]
    B --> F[Visualization Service]
    B --> G[User and Project Management Service]
    
    C --> H[(Image Storage)]
    D --> I[(3D Model Storage)]
    E --> J[(Pattern Storage)]
    F --> K[(Render Storage)]
    G --> L[(User/Project DB)]

    M[Docker Host]
    M --> B
    M --> C
    M --> D
    M --> E
    M --> F
    M --> G
    ```
