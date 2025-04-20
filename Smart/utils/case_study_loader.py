import os
from django.conf import settings
from datetime import datetime

def get_case_studies():
    base_dir = os.path.join(settings.BASE_DIR, 'case_studies_data')
    studies = []
    
    for study_dir in sorted(os.listdir(base_dir)):
        study_path = os.path.join(base_dir, study_dir)
        if os.path.isdir(study_path):
            study = {
                'slug': study_dir,
                'title': ' '.join([word.capitalize() for word in study_dir.split('-')]),
                'description': '',
                'pdf': None,
                'screenshots': [],
                'thumbnail': None,
                'modified': datetime.fromtimestamp(os.path.getmtime(study_path))
            }
            
            # Read description
            desc_path = os.path.join(study_path, 'description.txt')
            if os.path.exists(desc_path):
                with open(desc_path, 'r') as f:
                    study['description'] = f.read().strip()
            
            # Find PDF and images
            for file in os.listdir(study_path):
                file_lower = file.lower()
                file_path = os.path.join(study_path, file)
                
                if file_lower.endswith('.pdf'):
                    study['pdf'] = file
                elif file_lower.startswith(('screenshot', 'app-screen', 'screen')) and \
                     file_lower.endswith(('.png', '.jpg', '.jpeg')):
                    study['screenshots'].append(file)
                elif file_lower.startswith('thumbnail') and \
                     file_lower.endswith(('.png', '.jpg', '.jpeg')):
                    study['thumbnail'] = file
            
            studies.append(study)
    
    # Sort by modification date (newest first)
    studies.sort(key=lambda x: x['modified'], reverse=True)
    return studies