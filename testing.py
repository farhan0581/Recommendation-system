import os
import time
base_path = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(base_path, "Recommendation-system","static")
print base_path
time.sleep(5)
print path
# if not os.path.exists(path):
# 	os.makedirs(path,0777)
