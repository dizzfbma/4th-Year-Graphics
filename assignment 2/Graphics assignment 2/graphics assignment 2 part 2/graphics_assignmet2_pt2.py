import cv2
import numpy as np
from matplotlib import pyplot as plt

# Function to process and display the image smoothing in both domains
def process_image(img, img_title):
    # Apply Gaussian smoothing
    kernel_size = (15, 15)
    sigma = 10
    smoothed_spatial = cv2.GaussianBlur(img, kernel_size, sigma)

    # Display the smoothed image
    plt.figure(figsize=(10, 5))
    plt.imshow(cv2.cvtColor(smoothed_spatial, cv2.COLOR_BGR2RGB))
    plt.title(f'{img_title} - Spatial Domain Gaussian Blurred Image')
    plt.axis('off')
    plt.show()

    # Generate Gaussian kernel and compute its FFT
    gaussian_kernel = cv2.getGaussianKernel(ksize=kernel_size[0], sigma=sigma)
    gaussian_kernel_2d = gaussian_kernel @ gaussian_kernel.T
    fft_gaussian = np.fft.fftshift(np.fft.fft2(gaussian_kernel_2d, s=img.shape[:2]))

    # Plot the FFT of the Gaussian kernel
    plt.figure(figsize=(10, 5))
    plt.imshow(np.log(np.abs(fft_gaussian) + 1), cmap='gray')
    plt.title(f'{img_title} - 2D FFT of Gaussian Kernel (Low-Pass Filter)')
    plt.axis('off')
    plt.show()

    # Convert the image to grayscale for frequency domain filtering
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Compute the 2D FFT of the grayscale image
    f = np.fft.fft2(img_gray)
    fshift = np.fft.fftshift(f)

    # Create a low-pass filter mask
    rows, cols = img_gray.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), np.float32)
    radius = 50
    cv2.circle(mask, (ccol, crow), radius, 1, thickness=-1)

    # Apply the low-pass filter in the frequency domain
    fshift_filtered = fshift * mask

    # Perform inverse FFT to return to the spatial domain
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_filtered_frequency = np.fft.ifft2(f_ishift)
    img_filtered_frequency = np.abs(img_filtered_frequency)

    # Display the frequency domain filtered image
    plt.figure(figsize=(10, 5))
    plt.imshow(img_filtered_frequency, cmap='gray')
    plt.title(f'{img_title} - Frequency Domain Low-Pass Filtered Image')
    plt.axis('off')
    plt.show()

    # Side-by-side comparison of spatial and frequency domain smoothed images
    plt.figure(figsize=(15, 7))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(smoothed_spatial, cv2.COLOR_BGR2RGB))
    plt.title(f'{img_title} - Spatial Domain Smoothing')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(img_filtered_frequency, cmap='gray')
    plt.title(f'{img_title} - Frequency Domain Smoothing')
    plt.axis('off')

    plt.show()


img1 = cv2.imread('Task2.jpg')
process_image(img1, "Task2 Image")


img2 = cv2.imread('2nd_Image.png')
process_image(img2, "2nd Image")
