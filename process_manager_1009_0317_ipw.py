# 代码生成时间: 2025-10-09 03:17:20
# process_manager.py
# A simple process manager using the FALCON framework.

import falcon
import os
import psutil
import subprocess
from falcon import API, Request, Response

# Exception handler for process-related errors
class ProcessManagerError(Exception):
    pass

# Resource class to handle process management
class ProcessManagerResource():
    def on_get(self, req, resp):
        """
        GET request handler to retrieve a list of all running processes.
        """
        try:
            processes = [proc.info for proc in psutil.process_iter(['pid', 'name', 'status'])]
            resp.media = processes
        except psutil.Error as e:
            raise ProcessManagerError(f"An error occurred while retrieving processes: {e}")
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        POST request handler to start a new process.
        """
        try:
            command = req.media.get('command')
            if not command:
                raise ProcessManagerError("No command provided to start a process.")
            result = subprocess.run(command, shell=True, check=True)
            resp.media = {'message': f'Process started successfully: {command}'}
        except subprocess.CalledProcessError as e:
            raise ProcessManagerError(f"Failed to start process: {e}")
        except KeyError:
            raise ProcessManagerError("Invalid data structure in request.")
        resp.status = falcon.HTTP_201

    def on_delete(self, req, resp, pid):
        """
        DELETE request handler to terminate a process by its PID.
        """
        try:
            process = psutil.Process(pid)
            process.terminate()
            resp.media = {'message': f'Process {pid} terminated successfully.'}
        except psutil.NoSuchProcess:
            raise ProcessManagerError(f"No process found with PID {pid}.")
        except psutil.Error as e:
            raise ProcessManagerError(f"An error occurred while terminating process: {e}")
        resp.status = falcon.HTTP_200

# Initialize the Falcon API
app = API()

# Add the process manager resource
process_manager = ProcessManagerResource()
app.add_route('/processes', process_manager)
app.add_route('/process/{pid}', process_manager, methods=['DELETE'], require={'pid': int})

# Run the API on port 8000
if __name__ == '__main__':
    app.run(port=8000)