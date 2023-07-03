import cv2
import os
from datetime import datetime


image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "img", "id.studentBibash.png"))
output_filename = f"newImage_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
output_image_path = os.path.join(os.path.dirname(__file__), output_filename)


scale_d_percent =50
scale_i_percent =200


image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
resize_option = input("Choose resize option (d: decrease, i: increase): ")


#if increase is choosen
if resize_option.lower() == "i":
    width = int(image.shape[1]* scale_i_percent /100)
    height = int(image.shape[0]* scale_i_percent /100)
    isize = (width, height)
    output = cv2.resize(image, isize)


#if decrease is chhoosen
elif resize_option.lower() == "d":
    width = int(image.shape[1]* scale_d_percent /100)
    height = int(image.shape[0]* scale_d_percent /100)
    dsize = (width, height)
    output = cv2.resize(image, dsize)

else:
    print("Invalid option. Please choose 'd' or 'i'.")



try:
    #cv2.imshow("title", output)
    cv2.imwrite(output_image_path, output)
    #cv2.waitKey(0)
    print(f"Output image saved successfully at: {output_image_path}")
except Exception as e:
    print(f"An error occurs: {e}")