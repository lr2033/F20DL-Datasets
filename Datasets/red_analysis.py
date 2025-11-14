import cv2
import numpy as np
import os
import csv
import random


#Function to analyse the number of red pixels in an image.
def analyse_red(image_path, red_threshold=200, tolerance=50):
    
    #Read the image using OpenCV.
    image = cv2.imread(image_path)

    #Check if the image was loaded successfully.
    if image is None:
        #If not... raise an error indicating the image was not found.
        raise FileNotFoundError(f"Image not found: {image_path}")

    #Convert the image into RGB format.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #Split the image into its RGB components.
    R = image_rgb[:, :, 0]
    G = image_rgb[:, :, 1]
    B = image_rgb[:, :, 2]

    #Identify red pixels based on the defined thresholds.
    red_pixels = (R > red_threshold) & (R - G > tolerance) & (R - B > tolerance)

    #Calculate the red pixel percentage by (summing the red pixels) and (dividing by total pixels in the image) then multiplying by 100.
    red_percentage = (np.sum(red_pixels) / (image.shape[0] * image.shape[1])) * 100
    
    #Return the calculated red pixel percentage.
    return red_percentage

#Function to assign a magnitude based on red percentage.
#Wanted to randomise the magnitude within a range for each red percentage bracket.
def red_magnitude(red_percentage):
    if red_percentage > 2: #Highest red percentage... highest magnitude.
        return round(random.uniform(8, 8.50), 1)
    elif red_percentage > 1.4:
        return round(random.uniform(7.5, 7.99), 1) 
    elif red_percentage > 1.25:
        return round(random.uniform(7, 7.49), 1)
    elif red_percentage > 1:
        return round(random.uniform(6, 6.99), 1)
    elif red_percentage > 0.75:
        return round(random.uniform(5.76, 5.99), 1)
    elif red_percentage <= 0.75:
        return round(random.uniform(5.5, 5.75), 1)


if __name__ == "__main__":

    #Dataset directory containing images.
    dataset_dir = "EQ_Plots"

    #List to store results.
    results = []

    #Loop through all JPG, JPEG and PNG images in the dataset.
    for file in sorted(os.listdir(dataset_dir)):
        #Check if the file is an image.
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            #Full path to the image.
            image_path = os.path.join(dataset_dir, file)
            try:
                #Analyse the red content in the image.
                red_pct = analyse_red(image_path)

                #Set magnitude based on red percentage.
                magnitude = red_magnitude(red_pct)

                #Append the results to the list.
                results.append((file, red_pct, magnitude))

            #Catch any exceptions during processing.
            except Exception as e:
                #Print debug message.
                print(f"Error processing {file}: {e}")

    #Sort results by red percentage (descending)
    results.sort(key=lambda x: x[1], reverse=True)

    #Write to CSV.
    csv_path = "red_analysis3.csv"
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Image", "Red Percentage", "Magnitude"])
        for file, red_pct, magnitude in results:
            writer.writerow([file, f"{red_pct:.2f}", magnitude])

    #Print summary to console.
    for file, red_pct, magnitude in results:
        print(f"{file:25s} -> {red_pct:6.2f}% red | Magnitude: {magnitude}")

    print(f"\nResults saved to '{csv_path}'")
