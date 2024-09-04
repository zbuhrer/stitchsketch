# UI Service

## Overview

The UI microservice for `StitchSketch` is an interactive interface built using Flet to manage photogrammetry-related tasks, enabling efficient job management, navigation between pages, and display of relevant data.

## Class Diagram

```markdown
graph TB
    subgraph Presentation Layer
        UIComponents[UI Components]
        MainController[Main Controller]
        PageController[Page Controller]
    end

    subgraph Business Logic Layer
        Job[Job Model]
    end

    MainController -->|uses| Job
    MainController -->|uses| UIComponents
    PageController -->|navigates to| UIComponents

    style MainController fill:#f9d7ff,stroke:#333,stroke-width:2px
    style PageController fill:#f9d7ff,stroke:#333,stroke-width:2px
    style Job fill:#f9d7ff,stroke:#333,stroke-width:2px
    style UIComponents fill:#f9d7ff,stroke:#333,stroke-width:2px
```

## Key Components

* `MainController`: Orchestrates the application flow by handling navigation and control-related tasks.
* `PageController`: Handles navigation between UI components and provides a clear separation from `MainController`.
* `Job Model`: Represents photogrammetry-related jobs, including attributes like job status, creation time, and associated data.

## Technology Used**

`StitchSketch`'s UI microservice utilizes Flet to create a user-friendly interface and manage photogrammetry-related tasks efficiently.

## Roadmap**

1. **Controller decoupling**: Investigate further ways to decouple `MainController` from both `Job` and `UIComponents`.
2. **UI component refinements**: Refine the separation of UI components, widgets, and modals for improved organization and maintainability.
3. **Testing**: Develop a testing strategy to ensure the stability and correctness of our application.
