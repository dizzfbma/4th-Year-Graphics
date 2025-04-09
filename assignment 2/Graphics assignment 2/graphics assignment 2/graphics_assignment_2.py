import cv2
import numpy as np
from matplotlib import pyplot as plt

# Step 1: Load Image and Convert to Grayscale
# Load the image
image = cv2.imread('Task1.jpg')

# Convert to Grayscale using the Green channel for better contrast
grayscale_image = image[:, :, 1]  # Green channel

# Display Grayscale Image
plt.imshow(grayscale_image, cmap='gray')
plt.title('Grayscale Image')
plt.axis('off')
plt.show()

# Step 2: Image Enhancement (Histogram Equalization)
# Apply histogram equalization
enhanced_image = cv2.equalizeHist(grayscale_image)

# Display Equalized Image
plt.imshow(enhanced_image, cmap='gray')
plt.title('Histogram Equalized Image')
plt.axis('off')
plt.show()

# Step 3: Thresholding
# Apply binary thresholding (try different threshold values if needed)
_, binary_image = cv2.threshold(enhanced_image, 200, 255, cv2.THRESH_BINARY)

# Display Binary Thresholded Image
plt.imshow(binary_image, cmap='gray')
plt.title('Binary Thresholded Image')
plt.axis('off')
plt.show()

# Step 4: Noise Removal with Morphological Opening
# Define a disk-shaped structuring element for morphological operations
structuring_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# Apply morphological opening to remove small noise
opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, structuring_element)

# Display Noise Removed Image
plt.imshow(opened_image, cmap='gray')
plt.title('Noise Removed Image')
plt.axis('off')
plt.show()

# Step 5: Connected Components Labeling
# Label connected components
num_labels, label_image = cv2.connectedComponents(opened_image)

# Map component labels to image for visualization
label_hue = np.uint8(179 * label_image / np.max(label_image))
blank_channel = 255 * np.ones_like(label_hue)
labeled_image = cv2.merge([label_hue, blank_channel, blank_channel])
labeled_image = cv2.cvtColor(labeled_image, cv2.COLOR_HSV2BGR)
labeled_image[label_hue == 0] = 0  # Background color

# Display Connected Components
plt.imshow(labeled_image)
plt.title('Connected Components')
plt.axis('off')
plt.show()

# Step 6: Filtering of Fat Globules Based on Region Properties
# Analyze connected components to filter globules by size and shape
filtered_image = np.zeros_like(opened_image)

# Loop through each connected component to filter by area and shape
for label in range(1, num_labels):
    # Create a mask for each component
    component_mask = (label_image == label).astype("uint8") * 255

    # Calculate contour properties
    contours, _ = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        contour = contours[0]
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # Compute compactness as (4 * pi * Area) / (Perimeter^2)
        compactness = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0

        # Filter based on area and compactness
        if area > 190 and 0.7 <= compactness <= 1.3:  # Adjust values if needed
            filtered_image[label_image == label] = 255

# Display Filtered Fat Globules
plt.imshow(filtered_image, cmap='gray')
plt.title('Filtered Fat Globules')
plt.axis('off')
plt.show()

# Step 7: Calculate Total Fat Area Percentage
# Calculate the percentage of area covered by fat globules
fat_area = np.sum(filtered_image == 255)
total_area = filtered_image.size
fat_area_percentage = (fat_area / total_area) * 100

# Print the fat area percentage
print(f"Total Fat Area (%): {fat_area_percentage:.2f}")

# Step 8: Count the Number of Filtered Fat Globules
# Count the number of connected components (fat globules)
num_fat_globules, _ = cv2.connectedComponents(filtered_image)

# The first component is the background, so subtract 1 to get the number of fat globules
num_fat_globules -= 1

# Print the number of filtered fat globules
print(f"Number of Filtered Fat Globules: {num_fat_globules}")
