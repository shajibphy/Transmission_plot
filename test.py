import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the grayscale images for dark and light references
dark_image_path = r"C:\Users\Shafiul\Desktop\img\capture_img\dark_5K.png"
light_image_path = r"C:\Users\Shafiul\Desktop\img\capture_img\light_5K.png"
dark_image = cv2.imread(dark_image_path, cv2.IMREAD_GRAYSCALE)
light_image = cv2.imread(light_image_path, cv2.IMREAD_GRAYSCALE)

# Load the grayscale measurement image
measurement_image_path = r"C:\Users\Shafiul\Desktop\img\capture_img\measure_5K.png"
measurement_image = cv2.imread(measurement_image_path, cv2.IMREAD_GRAYSCALE)

# Resize the dark and light reference images to match the dimensions of the measurement image
dark_image = cv2.resize(dark_image, (measurement_image.shape[1], measurement_image.shape[0]))
light_image = cv2.resize(light_image, (measurement_image.shape[1], measurement_image.shape[0]))

# Define a threshold for identifying high and low-intensity regions
high_threshold = 50  # Adjust this threshold as needed
low_threshold = 40   # Adjust this threshold as needed

# Find vertical split positions based on high-intensity chunks in the measurement image
split_positions = []
is_inside_chunk = False

for col in range(measurement_image.shape[1]):
    column = measurement_image[:, col]

    if np.any(column >= high_threshold) and not is_inside_chunk:
        split_positions.append(col)
        is_inside_chunk = True
    elif np.all(column < low_threshold) and is_inside_chunk:
        split_positions.append(col)
        is_inside_chunk = False

# Add the leftmost and rightmost split positions if necessary
if is_inside_chunk:
    split_positions.append(measurement_image.shape[1] - 1)
if split_positions and split_positions[0] != 0:
    split_positions.insert(0, 0)

# Initialize y-axis limits to ensure consistent scaling
y_min = 0
y_max = 1  # Transmittance should be in the range [0, 1]

# Initialize lists to store start and end pixel positions for cropping
crop_start_pixels = []
crop_end_pixels = []

# Print the pixel range for each splitted part
for i in range(len(split_positions) - 1):
    left_col = split_positions[i]
    right_col = split_positions[i + 1]
    
    # Calculate the pixel range
    pixel_range = (0, right_col - left_col)
    print(f"Splitted part {i + 1} pixel range: {pixel_range}")

    # Prompt for the left and right pixel positions for cropping
    crop_start_pixel = int(input(f"Enter the start pixel for splitted part {i + 1} (left boundary): "))
    crop_end_pixel = int(input(f"Enter the end pixel for splitted part {i + 1} (right boundary): "))

    # Add the positions to the lists
    crop_start_pixels.append(crop_start_pixel)
    crop_end_pixels.append(crop_end_pixel)

# Split the measurement image based on the specified pixel positions
split_transmittance_images = []

for i in range(len(split_positions) - 1):
    left_col = split_positions[i]
    right_col = split_positions[i + 1]

    # Crop the region of interest from the measurement image based on the input pixel positions
    roi_measurement = measurement_image[:, left_col:right_col]
    roi_measurement = roi_measurement[:, crop_start_pixels[i]:crop_end_pixels[i]]

    # Resize the dark and light references to match the ROI dimensions
    dark_roi = cv2.resize(dark_image, (roi_measurement.shape[1], roi_measurement.shape[0]))
    light_roi = cv2.resize(light_image, (roi_measurement.shape[1], roi_measurement.shape[0]))

    # Calculate the transmittance based on the resized dark and light references
    transmittance = (roi_measurement - dark_roi) / (light_roi - dark_roi)
  
    # Clip values to ensure the range [0, 1]
    transmittance = np.clip(transmittance, 0, 1)

    # Calculate the mean transmittance for the region
    mean_transmittance = np.mean(transmittance, axis=1)
  
    # Plot transmittance curve for the region
    plt.plot(mean_transmittance, label=f"Region {i + 1}")

# Add labels and legend
plt.xlabel("Wavelength")
plt.ylabel("Transmittance")
plt.title("Transmittance Curves for Corrected Image")
plt.legend(loc="upper right")

# Show the combined plot
plt.show()
