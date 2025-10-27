# 代码生成时间: 2025-10-27 19:39:42
# career_planning_system.py
# A simple career planning system using Falcon framework.

from falcon import Falcon, Request, Response
import json

class CareerPlanningSystem:
    def __init__(self):
        # Initialize any necessary variables or services
        self.careers = [
            {'id': 1, 'name': 'Software Developer', 'description': 'Designs, codes, and maintains applications.'},
            {'id': 2, 'name': 'Data Scientist', 'description': 'Analyzes and interprets complex digital data.'},
            # Add more careers as needed
        ]

    def add_career(self, req: Request, resp: Response):
        """Add a new career to the system."""
        try:
            body = req.media or {}
            career = {
                'id': len(self.careers) + 1,  # Simple auto-incrementing ID
                'name': body.get('name'),
                'description': body.get('description')
            }
            if not career['name'] or not career['description']:
                raise ValueError('Name and description are required.')
            self.careers.append(career)
            resp.media = career
            resp.status = falcon.HTTP_201
        except ValueError as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_400
        except Exception as e:
            resp.media = {'error': 'An unexpected error occurred.'}
            resp.status = falcon.HTTP_500

    def get_careers(self, req: Request, resp: Response):
        """Get all careers from the system."""
        resp.media = self.careers
        resp.status = falcon.HTTP_200

    def get_career(self, req: Request, resp: Response, career_id):
        """Get a specific career by ID."""
        career = next((c for c in self.careers if c['id'] == int(career_id)), None)
        if career:
            resp.media = career
            resp.status = falcon.HTTP_200
        else:
            resp.media = {'error': 'Career not found.'}
            resp.status = falcon.HTTP_404

api = Falcon()

# Define the routes and resources
api.add_route('/careers', CareerPlanningSystem(), suffix=None)
api.add_route('/careers/{career_id}', CareerPlanningSystem(), suffix='get_career')

# Run the application
if __name__ == '__main__':
    api.run(port=8000, host='0.0.0.0')