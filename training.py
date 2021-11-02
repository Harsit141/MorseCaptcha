import os
import os.path
import cv2
import glob
import imutils


CAPTCHA_IMAGE_FOLDER = "generated_captcha_images"
OUTPUT_FOLDER = "extracted_letter_images"

captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER,"*"))   # Get a list of all the captcha images we need to process
counts = {}

for (i, captcha_image_file) in enumerate(captcha_image_files):    # loop over the image paths
 print("[INFO] processing image {}/{}".format(i + 1,len(captcha_image_files)))

  filename = os.path.basename(captcha_image_file)    # Since the filename contains the captcha text (i.e. "2A2X.png" has the text "2A2X"), grab the base filename as the text
  captcha_correct_text = os.path.splitext(filename)[0]
  image = cv2.imread(captcha_image_file)    # Load the image and convert it to grayscale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8,cv2.BORDER_REPLICATE)    # Add some extra padding around the image threshold the image (convert it to pure black and white)
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
  contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    # find the contours (continuous blobs of pixels) the image
  contours = contours[0] if imutils.is_cv2() else contours[1]    # Hack for compatibility with different OpenCV versions
  
  letter_image_regions = []
  for contour in contours:   # Now we can loop through each of the four contours and extract the letter inside of each one
    (x, y, w, h) = cv2.boundingRect(contour)   # Get the rectangle that contains the contour
    if w / h > 1.25:   # Compare the width and height of the contour to detect letters that are conjoined into one chunk
      half_width = int(w / 2)    # This contour is too wide to be a single letter! Split it in half into two letter regions!
      letter_image_regions.append((x, y, half_width, h))
      letter_image_regions.append((x + half_width, y, half_width, h))
    else:
      letter_image_regions.append((x, y, w, h))    # This is a normal letter by itself
    if len(letter_image_regions) != 4:   # If we found more or less than 4 letters in the captcha, our letter extraction didn't work correcly. Skip the image instead of saving bad training data!
      continue
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])    # Sort the detected letter images based on the x coordinate to make sure we are processing them from left-to-right so we match the right image with the right letter
    for letter_bounding_box, letter_text in zip(letter_image_regions, captcha_correct_text):   # Save out each letter as a single image
      x, y, w, h = letter_bounding_box   # Grab the coordinates of the letter in the image
      letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]    # Extract the letter from the original image with a 2-pixel margin around the edge
      save_path = os.path.join(OUTPUT_FOLDER, letter_text)    # Get the folder to save the image
      if not os.path.exists(save_path):    # if the output directory does not exist, create it
        os.makedirs(save_path)
      count = counts.get(letter_text, 1)   # write the letter image to a file
      p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
      cv2.imwrite(p, letter_image)
    counts[letter_text] = count + 1
 
