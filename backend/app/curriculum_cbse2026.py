# CBSE / NCERT Official Syllabus Database (Academic Session 2026-27)
# Dynamically loaded from persistent JSON seed files in app/seeds/cbse_2026_27/
import json
import os
import logging

logger = logging.getLogger(__name__)

SEEDS_DIR = os.path.join(os.path.dirname(__file__), "seeds", "cbse_2026_27")

def load_cbse_2026_syllabus():
    classes = []
    for class_num in [8, 9, 10, 11, 12]:
        file_path = os.path.join(SEEDS_DIR, f"class-{class_num}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    c_data = json.load(f)
                    classes.append(c_data)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        else:
            logger.warning(f"Seed file not found: {file_path}")

    return {
        "board": {
            "name": "Central Board of Secondary Education",
            "code": "CBSE",
            "country": "India",
            "description": "National level board of education in India for public and private schools"
        },
        "academic_year": {
            "year_code": "2026-27",
            "title": "CBSE Academic Session 2026-2027",
            "is_current": True
        },
        "classes": classes
    }

CBSE_2026_SYLLABUS = load_cbse_2026_syllabus()
