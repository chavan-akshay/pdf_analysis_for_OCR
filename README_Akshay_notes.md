Here are the few insights regarding the implemented solutions.

Task 1:
To detect orientation of the text within a file, I have used a unique approach.
Usually if we observe some text then it contains "zebra patters" or a clear pattern of alternating light and dark rows.
Hence, to make the text OCR parsable we first preprocess the image to identify and highlight the text itself and then
compare the variance or spread of a distribution of the image variants obtained by rotating the image through 360 degrees
within an increment of 1 degree each. 

Finally, the instance of angle with higher resemblance to zebra strips is consider as required orientation angle.
Although the method works almost 90 % of time to get proper orientation, the detected orientation could also be upside down.
To avoid this it is possible to pass the detected angle through OCR detector and analyse the output to decide
whether to continue with the obtained angle or invert the image to get the OCR parsable angle.

    We compare the processed image to exhibit "Zebra Pattern".
    By this method we are able to achieve the rotation angle.

I have also tried using cv2 library minAreaReact for orientation detection,
but it failed to identify the orientation for many instances. The method itself is quite promising and can be explored further.
I have attached the code implemented with that approach under contour_detection.py file.

Task 2:
The pdf generator file produces header and footer which makes each file machine-readable.
Hence, I have trimmed the pdf before passing for classification task. I have used pytesseract method to identify
if the file is OCR parsable or not.

I have attached additional google images on which I tried my code for better analysis.

Due to limited time restrictions and my current ongoing work, I was unable to implement "cherry on the cake task".
