# StitchSketch Architecture

StitchSketch is an open-source photogrammetry solution designed specifically for upholstery shops. It aims to democratize access to 3D scanning by providing a cost-effective alternative to expensive laser-based 3D scanning systems.

## **System Architecture**

StitchSketch follows a microservices pattern, with each service responsible for a specific aspect of the photogrammetry and upholstery calculation process.

### Diagram

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
```

### Key Components

1. [API Gateway](api_gateway.md): Serves as the entry point for all client requests.
2. [Image Processing Service](image_processing_service.md): Handles image ingestion and preprocessing.
3. [3D Reconstruction Service](reconstruction_service.md): Creates 3D models from processed images.
4. [Upholstery Service](upholstery_service.md): Manages pattern calculations and digital reupholstery prototyping.
5. [Visualization Service](visualization_service.md): Generates Gaussian Splat reconstructions and other visualizations.
6. [User and Project Management Service](user_project_service.md): Handles user accounts and project metadata.

## Data Flow

1. The client uploads images through the API Gateway.
2. The Image Processing Service prepares the images for 3D reconstruction.
3. The 3D Reconstruction Service generates a 3D model from the processed images.
4. The Upholstery Service uses the 3D model to calculate patterns and create digital prototypes.
5. The Visualization Service generates various views and reconstructions of the 3D model.
6. The User and Project Management Service tracks all this information for each user's project.

## Technology Stack

- [ ] TODO: Tech Stack Discovery & Decisions

- Backend: *Python (varied API hosts for specialized Python microservices)*
- Frontend: *Web-based (Python preferred)*
- Databases: *Structured, Unstructured, and Vectorized/Tokenizable database types. Needs RAG support. NoSQL for small local things?*
- Storage: *MinIO or something similar for raw images and large files*

For detailed information on each service, please refer to the individual service documentation linked above.
