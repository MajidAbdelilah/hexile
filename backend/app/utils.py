import docker
import requests
from django.conf import settings
import logging
import os
import time
from urllib.parse import urlparse
import stat

logger = logging.getLogger(__name__)

class InstanceManager:
    def __init__(self):
        self.client = None
        self._initialize_docker_client()

    def _check_socket_access(self, socket_path):
        try:
            # Try to access the socket
            with open(socket_path, 'r') as _:
                return True
        except (IOError, PermissionError) as e:
            logger.error(f"Cannot access Docker socket: {e}")
            return False

    def _find_docker_sock(self):
        # Try standard socket path first
        if os.path.exists('/var/run/docker.sock'):
            return '/var/run/docker.sock'
        
        # Try rootless socket path
        uid = os.getuid()
        rootless_sock = f'/run/user/{uid}/docker.sock'
        if os.path.exists(rootless_sock):
            return rootless_sock
            
        return None

    def _initialize_docker_client(self):
        try:
            self.client = docker.from_env()
            self.client.ping()
            logger.info("Successfully connected to Docker daemon using environment settings")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None

    def create_instance(self, instance_name, port):
        """
        Create a new Ghost instance Docker container
        """
        if not self.client:
            logger.warning("Docker client not available")
            return None
        try:
            container = self.client.containers.run(
                'ghost:latest',
                name=f'ghost_{instance_name}',
                ports={2368: port},
                environment={
                    'url': f'http://localhost:{port}'
                },
                detach=True
            )
            return container.id
        except Exception as e:
            logger.error(f"Error creating Ghost instance: {e}")
            raise

    def delete_instance(self, container_id):
        """
        Delete a Ghost instance Docker container
        """
        if not self.client:
            logger.warning("Docker client not available")
            return None
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            container.remove()
        except Exception as e:
            logger.error(f"Error deleting Ghost instance: {e}")
            raise

    def check_instance_status(self, container_id):
        """
        Check the status of a Ghost instance
        """
        if not self.client:
            logger.warning("Docker client not available")
            return None
        try:
            container = self.client.containers.get(container_id)
            return container.status
        except Exception as e:
            logger.error(f"Error checking Ghost instance status: {e}")
            raise

    def check_instance_health(self, port):
        """
        Check if the Ghost instance is responding
        """
        try:
            response = requests.get(f'http://localhost:{port}')
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error checking Ghost instance health: {e}")
            return False