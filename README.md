# StitchSketch

## Description
------------------

StitchSketch is a digital platform for reupholstering furniture. It uses computer vision and machine learning to provide users with accurate measurements, material estimates, and high-quality visualizations of their projects.

## Diagram
------------------

````mermaid
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
````

## Getting Started
------------------

To build the project, run `docker-compose up --build` in your terminal. This will create a containerized environment for the StitchSketch platform.
