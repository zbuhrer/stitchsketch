# reconstruction_service.py

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import open3d as o3d
import numpy as np

app = Flask(__name__)
api = Api(app)
CORS(app)

class PointCloudGenerator:
    def generate_sparse_cloud(self, images):
        # Placeholder for sparse point cloud generation using COLMAP or similar
        # For simplicity, we'll return a dummy sparse cloud
        return o3d.geometry.PointCloud()

    def densify_cloud(self, sparse_cloud):
        # Placeholder for densifying the sparse cloud
        # For simplicity, we'll return the same cloud
        return sparse_cloud

class MeshGenerator:
    def create_mesh(self, dense_cloud):
        # Create a mesh from the dense point cloud using Open3D
        pcd = o3d.geometry.PointCloud(dense_cloud)
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha=0.03)
        return mesh

class ModelOptimizer:
    def simplify_mesh(self, mesh):
        # Simplify the mesh using Open3D
        mesh = mesh.simplify_quadric_decimation(100000)
        return mesh

    def smooth_mesh(self, mesh):
        # Smooth the mesh using Open3D
        mesh = mesh.filter_smooth_simple(number_of_iterations=10)
        return mesh

class ReconstructionService:
    def __init__(self):
        self.point_cloud_generator = PointCloudGenerator()
        self.mesh_generator = MeshGenerator()
        self.model_optimizer = ModelOptimizer()

    def create_point_cloud(self, images):
        sparse_cloud = self.point_cloud_generator.generate_sparse_cloud(images)
        dense_cloud = self.point_cloud_generator.densify_cloud(sparse_cloud)
        return dense_cloud

    def generate_mesh(self, point_cloud):
        mesh = self.mesh_generator.create_mesh(point_cloud)
        return mesh

    def optimize_model(self, mesh):
        mesh = self.model_optimizer.simplify_mesh(mesh)
        mesh = self.model_optimizer.smooth_mesh(mesh)
        return mesh

reconstruction_service = ReconstructionService()

class ReconstructionResource(Resource):
    def post(self):
        images = request.json.get('images')
        if not images:
            return jsonify({'error': 'No images provided'}), 400

        point_cloud = reconstruction_service.create_point_cloud(images)
        mesh = reconstruction_service.generate_mesh(point_cloud)
        optimized_mesh = reconstruction_service.optimize_model(mesh)

        # Convert the mesh to a format suitable for JSON response
        mesh_data = np.asarray(optimized_mesh.vertices).tolist()
        return jsonify({'mesh': mesh_data}), 200

api.add_resource(ReconstructionResource, '/reconstruct')

if __name__ == '__main__':
    app.run(debug=True)