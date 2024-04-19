import pandas as pd
from numpy import random
from colormap import rgb2hex

def random_faces():
    # Generating random values for face attributes
    df = pd.DataFrame(columns=['Angry', 'Joy', 'Sorrow','Surprised','Headwear','Exposed','Blurred','Confidence'])
    new_row = {
        'Angry': random.randint(0, 100),
        'Joy': random.randint(0, 100),
        'Sorrow': random.randint(0, 100),
        'Surprised': random.randint(0, 100),
        'Headwear': random.randint(0, 100),
        'Exposed': random.randint(0, 100),
        'Blurred': random.randint(0, 100),
        'Confidence': random.randint(0, 100)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

def random_labels():
    # Generating random labels
    labels = ['Label1', 'Label2', 'Label3', 'Label4', 'Label5']
    scores = [random.randint(0, 100) for _ in range(5)]
    df = pd.DataFrame({'description': labels, 'score': scores})
    return df

def random_objects():
    # Generating random objects
    objects = ['Object1', 'Object2', 'Object3', 'Object4', 'Object5']
    scores = [random.randint(0, 100) for _ in range(5)]
    df = pd.DataFrame({'name': objects, 'score': scores})
    return df

def random_safesearch():
    # Generating random safe search results
    df = pd.DataFrame(columns=['Adult', 'Spoof', 'Medical','Violence','Racy'])
    new_row = {
        'Adult': random.randint(0, 100),
        'Spoof': random.randint(0, 100),
        'Medical': random.randint(0, 100),
        'Violence': random.randint(0, 100),
        'Racy': random.randint(0, 100)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

import random
import pandas as pd

def common_cctv_colors():
    colors = colors = ['#000000', '#2E8B57', '#8B4513', '#00008B', '#483D8B']
    return colors

def random_properties():
    # Generating random color properties
    colors = common_cctv_colors()
    scores = [random.randint(0, 100) for _ in range(len(colors))]
    df = pd.DataFrame({'color': colors, 'score': scores})
    return df



def get_gvision(image_path):
    # Simulating Google Vision API calls with random data
    face_df = random_faces()
    label_df = random_labels()
    object_df = random_objects()
    safe_df = random_safesearch()
    cloth_color_df = random_properties()

    return face_df, label_df, object_df, safe_df, cloth_color_df

# Example usage:
# image_path = 'path_to_your_image.jpg'
# face_df, label_df, object_df, safe_df, cloth_color_df = get_gvision(image_path)
# print("Random Faces:")
# print(face_df)
# print("\nRandom Labels:")
# print(label_df)
# print("\nRandom Objects:")
# print(object_df)
# print("\nRandom Safe Search:")
# print(safe_df)
# print("\nRandom Color Properties:")
# print(cloth_color_df)
