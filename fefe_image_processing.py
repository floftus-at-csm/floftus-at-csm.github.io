

# from skimage.util import compare_images
from PIL import ImageFile, Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import os
import cv2
import imutils
import inspect
from os import path, listdir
ImageFile.LOAD_TRUNCATED_IMAGES = True # used to stop errors with file size

# class fefe_image_processes:
class scikit:
    from skimage import io, util
    from skimage import data, transform, exposure, filters
    from skimage.filters import threshold_otsu, threshold_local
    def resize_image_for_screen(starter_img, width, height, dir_path):
        new_img = starter_img.resize((width, height), Image.ANTIALIAS)
        return new_img

    # dir_path tells the function where to look for images
    # img1/2_path are the paths of the images that will be compared 
    # in the first loop both will be from the contoured folder
    # after the first loop the first will be from the frame differenced folder and the second will be from the contoured folder
    # the output path argument tells the function where to save the image
    def frame_difference_paths(dir_path, img1_path, img2_path, input_position, image_counter, image_counter2, output_path):
        image1_path = os.path.join(dir_path, img1_path, str(input_position), str(image_counter)+'.png')
        image2_path = os.path.join(dir_path, img2_path, str(input_position), str(image_counter2)+'.png')
        img1 = io.imread(image1_path, as_gray=True)
        img2 = io.imread(image2_path, as_gray=True)
        diff_photo = util.compare_images(img1, img2, method='diff')
        frameDiff_directory = os.path.join(dir_path, 'frameDiff')
        output_path=os.path.join(frameDiff_directory, str(input_position), str(output_path)+'.png')
        io.imsave(output_path, diff_photo)

    # ================================= #
    # Scikit processes 
    def difference_images(img1, img2):
        # images need to be numpy arrays 
        diff_photo = compare_images(img1, img2, method='diff')
        return diff_photo


    def blend_images(img1, img2):
        # images need to be numpy arrays 
        diff_photo = compare_images(img1, img2, method='blend')
        return diff_photo

    def edge_detection_standard(img1):
        edged_img = filters.roberts(img1)
        return edged_img

    def edge_detection_sobel(img):
        edged_img = filters.roberts(img)
        return edged_img

    def edge_detection_scharr(img):
        edged_img = filters.scharr(img)
        return edged_img

    def edge_detection_farid_h(img):
        edged_img = filters.farid_h(img)
        return edged_img

    def edge_detection_farid_v(img):
        edged_img = filters.farid_v(img)
        return edged_img
    # meijering, sato, frangi, hessian, roberts, sobel, scharr, prewitt 
    def edge_detection_meijering(img):
        edged_img = filters.meijering(img)
        return edged_img

    def edge_detection_sato(img):
        edged_img = filters.sato(img)
        return edged_img

    def edge_detection_frangi(img):
        edged_img = filters.frangi(img)
        return edged_img

    def contrast_stretch(img):
        p2, p98 = np.percentile(img, (2, 98))
        # Contrast stretching
        img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98)) # rescale image based on contrast stretching - this draws the detail in images
        return img_rescale

    def invert_numpy_array(img):
        contrasted_inverted = util.invert(img) # invert image
        return contrasted_inverted

    # dithering

    # image separations 

    def local_threshold_image(img):
        # does a better job than standard thresholding but is slower
        # requires a scikit image input
        block_size = 35
        local_thresh = threshold_local(img, block_size, offset=10)
        return local_thresh

class PIL_processes:
    # ================================= #
    # PIL processes
    def threshold_image(img, threshold_value):
        # standard method of thresholding - requires a PIL image 
        im = img.point( lambda p: 255 if p>threshold_value else 0)
        return im 

    # cv2 processes 
    def find_largest_contour(image, min_area):
        """
        This function finds all the contours in an image and return the largest
        contour area.
        :param image: a binary image
        """
        # add min area here
        image = image.astype(np.uint8)
        # contours, hierarchy
        (_, cnts, _) = cv2.findContours(
            image,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            # areaMin = cv2.getTrackbarPos("Area", "Parameters")
            if area > min_area:
                largest_contour = max(cnts, key=cv2.contourArea)
        return largest_contour

    def extract_foreground_from_frame(img, threshold1, threshold2, min_area, output_folder_path):

        image = img
        # show('Input image', image)
        # blur the image to smmooth out the edges a bit, also reduces a bit of noise
        # imgBlur = cv2.blur(image,(3, 3))
        imgBlur = cv2.GaussianBlur(image, (5, 5), 0)
        # convert the image to grayscale 
        gray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

        # optional switch up
        imgCanny = cv2.Canny(gray, threshold1, threshold2)
        kernel = np.ones((5,5))

        imgDil = cv2.dilate(imgCanny, kernel, iterations = 1)
        contour = self.find_largest_contour(imgDil, min_area)

        # apply thresholding to conver the image to binary format
        # after this operation all the pixels below 200 value will be 0...
        # and all th pixels above 200 will be 255
        # I think I should change these values to threshold1 and 2
        #ret, gray = cv2.threshold(gray, 200 , 255, cv2.CHAIN_APPROX_NONE)

        # find the largest contour area in the image
        # contour = find_largest_contour(gray)
        image_contour = np.copy(image)
        cv2.drawContours(image_contour, [contour], 0, (0, 255, 0), 2, cv2.LINE_AA, maxLevel=1)
        # show('Contour', image_contour)

        # create a black `mask` the same size as the original grayscale image 
        mask = np.zeros_like(gray)
        # fill the new mask with the shape of the largest contour
        # all the pixels inside that area will be white 
        cv2.fillPoly(mask, [contour], 255)
        # create a copy of the current mask
        res_mask = np.copy(mask)
        res_mask[mask == 0] = cv2.GC_BGD # obvious background pixels
        res_mask[mask == 255] = cv2.GC_PR_BGD # probable background pixels
        res_mask[mask == 255] = cv2.GC_FGD # obvious foreground pixels

        # create a mask for obvious and probable foreground pixels
        # all the obvious foreground pixels will be white and...
        # ... all the probable foreground pixels will be black
        mask2 = np.where(
            (res_mask == cv2.GC_FGD) | (res_mask == cv2.GC_PR_FGD),
            255,
            0
        ).astype('uint8')


        # create `new_mask3d` from `mask2` but with 3 dimensions instead of 2
        new_mask3d = np.repeat(mask2[:, :, np.newaxis], 3, axis=2)
        mask3d = new_mask3d
        mask3d[new_mask3d > 0] = 255.0
        mask3d[mask3d > 255] = 255.0
        # apply Gaussian blurring to smoothen out the edges a bit
        # `mask3d` is the final foreground mask (not extracted foreground image)
        mask3d = cv2.GaussianBlur(mask3d, (5, 5), 0)
        # show('Foreground mask', mask3d)

        # create the foreground image by zeroing out the pixels where `mask2`...
        # ... has black pixels
        foreground = np.copy(image).astype(float)
        foreground[mask2 == 0] = 0
        # cv2.imshow('Foreground', foreground.astype(np.uint8))

        # TO DO - save the images to disk - TO DO!
        # save_name = os.path.basename(input_file_path).strip(".png")

        # cv2.imwrite(os.path.join(output_folder_path, f"{save_name}_foreground.png"), foreground)
        # cv2.imwrite(os.path.join(output_folder_path, f"{save_name}_foreground_mask.png"), mask3d)
        return foreground
    
    # def extract_foreground_real_python(img)

    def grayscale(img):
        grayscale_img = img.convert('L')
        return grayscale_img

    def solarize(img, threshold_val):
        # threshold 0 - 255  (start with 130 e.g)
        solarized_img = ImageOps.solarize(img, threshold = threshold_val)
        return solarized_img

    def resize_image(img, w, h):
        newsize = (w, h)
        im1 = img.resize(newsize)
        return im1

    def PIL_edges(img):
        img_gray = img.convert("L")
        edged = img_gray.filter(ImageFilter.FIND_EDGES)
        return edged    

    def PIL_edges_smooth(img):
        img_gray = img.convert("L")
        img_smooth = img_gray.filter(ImageFilter.SMOOTH)
        edged = img_smooth.filter(ImageFilter.FIND_EDGES)
        return edged
    
    def PIL_enhance_edges(img):
        img_gray = img.convert("L")
        edge_enhance = img_gray.filter(ImageFilter.EDGE_ENHANCE)
        return edge_enhance
    
    def PIL_contour(img, threshold):
        img_l = img.convert("L")
        img_l = img_l.point(lambda x: 255 if x > threshold else 0)
        img_l = img_l.filter(ImageFilter.CONTOUR)
        return img_l

    def PIL_invert(img):
        img = img.point(lambda x: 0 if x == 255 else 255)
        return img
    
    def PIL_contrast(img, contrast_amount):
        # contrast between 0 and 2
        enhancer = ImageEnhance.Contrast(img)
        im_output = enhancer.enhance(contrast_amount)
        return im_output


class general:
    # ================================= #
    # General Processes

    def PIL_to_scikit_or_openCV(pil_image):
        # Make Numpy array for scikit-image from "PIL Image"
        numpy_array_image = np.array(pil_image)
        return numpy_array_image

    def numpy_array_to_PIL(numpy_array):
        # Make "PIL Image" from Numpy array
        pil_image = Image.fromarray(numpy_array)
        return pil_image

    def print_functions(self):
        print(inspect.getmembers(predicate=inspect.isfunction))

    def load_images_in_folder(path):
        # return array of images

        imagesList = listdir(path)
        loadedImages = []
        for image in imagesList:
            img = Image.open(path + image)
            loadedImages.append(img)

        return loadedImages
