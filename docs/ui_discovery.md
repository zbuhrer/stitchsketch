## UI Discovery: Refactoring Container Endpoints

### Introduction

As we continue to develop StitchSketch, it's essential to refactor our container endpoints to utilize the most suitable web frameworks for each service. This document outlines the recommended frameworks and a roadmap for refactoring our existing codebase.

### Framework Recommendations

Based on the analysis of each service's requirements and characteristics, we recommend the following frameworks:

* **API Gateway**: Flask
	+ Lightweight, flexible, and well-suited for building API gateways.
	+ Key features:
		- Support for web sockets
		- Simple routing mechanism
		- Integration with authentication mechanisms (e.g., OAuth)
* **Image Processing Service** and **3D Reconstruction Service**: Pyramid or Quart (for async processing)
	+ Ideal frameworks for handling complex computations and asynchronous processing required for these services.
	+ Key features:
		- Built-in support for asynchronous processing
		- Robust caching mechanisms
		- Integration with job queues (e.g., Celery, RQ)
* **Upholstery Service**: Flask
	+ Simple, flexible, and well-suited for this service's traditional web application requirements.
	+ Key features:
		- Built-in support for templates
		- Easy integration with authentication mechanisms (e.g., OAuth)
		- Support for static file serving
* **Visualization Service**: Dash (for interactive visualizations)
	+ Excellent choice for building interactive, web-based visualizations.
	+ Key features:
		- Robust support for interactive visualizations
		- Integration with data sources (e.g., databases, APIs)
		- Easy deployment to cloud platforms (e.g., Heroku)
* **User and Project Management Service**: Django
	+ Robust, structured approach to handling user accounts and project metadata.
	+ Key features:
		- Built-in support for user authentication and authorization
		- Robust model-based data management
		- Integration with job queues (e.g., Celery, RQ)

### Roadmap

#### Phase 1: Research and Planning

1. Conduct in-depth research on each recommended framework, focusing on their strengths, weaknesses, and integration capabilities.
2. Identify potential risks and challenges associated with refactoring the existing codebase.


#### Phase 2: Refactor API Gateway

1. Migrate the API Gateway to Flask, following best practices and guidelines for secure and efficient API development.
2. Integrate the new API Gateway with other services, ensuring seamless communication and data flow.
3. Update dependencies and ensure compatibility with other services.

#### Phase 3: Refactor Image Processing Service and 3D Reconstruction Service

1. Migrate these services to Pyramid or Quart, leveraging their capabilities for asynchronous processing.
2. Update dependencies and ensure compatibility with other services.
3. Integrate the new services with job queues (e.g., Celery, RQ) for efficient processing.

#### Phase 4: Refactor Upholstery Service

1. Upgrade the Upholstery Service to Flask, following best practices for web application development.
2. Update dependencies and ensure compatibility with other services.
3. Integrate the new service with authentication mechanisms (e.g., OAuth).

#### Phase 5: Refactor Visualization Service

1. Migrate the Visualization Service to Dash, taking advantage of its capabilities for interactive visualizations.
2. Update dependencies and ensure compatibility with other services.
3. Deploy the new service to cloud platforms (e.g., Heroku).

#### Phase 6: Refactor User and Project Management Service

1. Upgrade the User and Project Management Service to Django, utilizing its robust features for user account management and project metadata handling.
2. Update dependencies and ensure compatibility with other services.
3. Integrate the new service with job queues (e.g., Celery, RQ) for efficient processing.

### Conclusion

Refactoring our container endpoints to utilize the recommended frameworks will improve the overall efficiency, scalability, and maintainability of StitchSketch. By following this roadmap, we can ensure a smooth transition while minimizing potential risks and challenges.
