from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2, os
import pandas as pd

df = pd.read_csv("Attendance.csv")
old_names = df.columns[2:]

all_names = os.listdir('./dataset')
new_employee = list(set(all_names) - set(old_names))
print(new_employee)
# our images are located in the dataset folder
print("[INFO] start processing faces...")
imagePaths = []
for emp_name in new_employee:
    imagePaths_temp  = list(paths.list_images(f"dataset\\{emp_name}"))
    imagePaths.extend(imagePaths_temp)

# print(imagePaths)

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	print(name)

# load the input image and convert it from RGB (OpenCV ordering)
 	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model="hog")

 	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

 	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)


print(knownEncodings)
print(knownNames)
# dump the facial encodings + names to disk
encodingsP = "encodings.pickle"
data = pickle.loads(open(encodingsP, "rb").read())
# print(data)
print("[INFO] serializing encodings...")
print(len(data.get("encodings")))
print(len(data.get("names")))
print(data["names"])
data["encodings"].extend(knownEncodings)
data["names"].extend(knownNames)
print(data["names"])
# data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()