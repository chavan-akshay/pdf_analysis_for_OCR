Description:

I am working on a senario to parse medical documents within an archive. All documents of a single patient are appended in one file in a random order. The documents can have the following origins: scans of printed documents (e.g. doctor letters, medication plans, printed lab results), scans of medical images (e.g. sonography-images or electrocardiograms [ECG]), programatically generated PDF-documents (e.g. letters, reports, lab reports, ECGs,  etc.) which were sent to the archive. It is possible that documents appear as single files (one document, single file) but it can also appear that a collection of paper documents (e..g 3 letters, lab results, medication plans) were scanned into one file and uploaded into a single file (multiple documents, single file).

Tasks:
  - A function which takes a PDF file path as inputs and returns a dictionary which page has to be rotated by which angle to be upright (OCR-parsable). Documents can be generated PDFs (with embedded text) but are especially scanned pages. The documents may be landscape or portrait oriented.  The function is performant also for documents up to 200 pages.
  - A function which classifies pages of a 200 page document into 3 categories:
    1. machine-readable PDF / searchable PDF (e.g. internally generated discharge letter)
    2. Image-based PDF which may be OCR’d (e.g. discharge letters brought by the patient from an external hospital and then scanned)
    3. Image-based PDF which may not be OCR`d (e.g. ECG)
       
We are well aware that these tasks may require significant work. Aim to implement the best possible solution given the time and ressource constraints. 
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
