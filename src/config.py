import os
import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data", "hinhanh")

COLUMNS = ['Id_imgs', 'Types', 'ppm', 'Phones', 'Num_of_photos', 'Date']
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
META_COLORS = f"metadata_colors_{datetime.date.today()}.csv"

SIZE_IMG = 224
SIZE_CUT = (300, 400)
RATIO = 0.75
HSV_KITS = {
    "1.1.1.1.0":[(35, 102, 76), (95, 255, 255)],    # Hue, Saturation, Value of 4 types of phones (mi8 lite, nokia, oppo, poco f3)
    "1.1.1.0.1":[(35, 100, 70), (100, 255, 255)]    # Hue, Saturation, Value of a phone (samsung)
    }
