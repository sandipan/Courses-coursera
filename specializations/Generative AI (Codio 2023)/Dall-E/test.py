import os
import openai
import secret
import requests
#openai.api_key='xxxxx'

# WRITE YOUR CODE HERE
response = openai.Image.create(
  prompt="a dog smoking a cigar in a poker room.",
  n=1,
  size="256x256"
)

print(response)
image_url = response['data'][0]['url']
print(image_url)


# WRITE YOUR CODE HERE
import os
import openai
import secret
import requests
#openai.api_key='xxxxxx'

def imageGen(txt):
  # WRITE YOUR CODE HERE
  response = openai.Image.create(
    prompt=txt,
    n=1,
    size="256x256"
  )

  #print(response)
  image_url = response['data'][0]['url']
  #print(image_url)

  img_data = requests.get(image_url).content
  with open('my_image.jpg', 'wb') as handler:
      handler.write(img_data)

imageGen("a dog smoking a cigar in a poker room.")


import os
import openai
import secret
import requests
#openai.api_key='xxxxx'
# Keep CODE ABOVE
# WRITE YOUR CODE HERE
response = openai.Image.create_variation(
  image=open("bunny.png", "rb"),
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
#using the url, we use the code below to save it as a file
img_data = requests.get(image_url).content
with open('image_name_var.png', 'wb') as handler:
    handler.write(img_data)
	

#this code generates a new image  from a prompt 
response = openai.Image.create(
  prompt="bunny and a cat",
  n=1,
  size="512x512"
)
#from the response generated this putS the url in a separate variable
image_url = response['data'][0]['url']

#using the url, we use the code below to save it as a file
img_data = requests.get(image_url).content
with open('bunny.png', 'wb') as handler:
    handler.write(img_data)
	
response = openai.Image.create_variation(
  image=open("bunny.png", "rb"),
  n=1,
  size="512x512"
)
image_url2= response['data'][0]['url']

img_data = requests.get(image_url2).content
with open('bunny_var.png', 'wb') as handler:
    handler.write(img_data)
	
#openai.api_key='xxxxxx'

# WRITE YOUR CODE HERE
def variationMaker(image_name):
	# WRITE YOUR CODE HERE
	response = openai.Image.create_variation(
	  image=open(image_name, "rb"),
	  n=1,
	  size="512x512"
	)
	image_url = response['data'][0]['url']

	img_data = requests.get(image_url).content
	with open('varTest.png', 'wb') as handler:
		handler.write(img_data)

variationMaker('test_image.png')


# WRITE YOUR CODE HERE
import os
import openai
import requests
import secret

#openai.api_key='xxxxxx'

# Set the prompts
prompts = ["robot dog in a lab", "robot dog exploring the city", "robot dog watching the sunset"]

# Generate and save the images
for i, prompt in enumerate(prompts):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="256x256"
    )

    # Get the image URL from the response
    image_url = response['data'][0]['url']

    # Download and save the image
    img_data = requests.get(image_url).content
    with open(f"robot_dog_journey_{i+1}.jpg", 'wb') as handler:
        handler.write(img_data)
		
import os
import openai
import requests
import secret

#openai.api_key='xxxxxx'

# Set the prompts
prompts = ["robot dog in a lab", "robot dog exploring the city", "robot dog watching the sunset"]

# Generate and save the images
for i, prompt in enumerate(prompts):
    try:
        response = openai.Image.create(
          prompt=prompt,
          n=1,
          size="256x256"
        )
        
        # Get the image URL from the response
        image_url = response['data'][0]['url']

        # Download and save the image
        img_data = requests.get(image_url).content
        with open(f"robot_dog_journey_{i+1}.jpg", 'wb') as handler:
            handler.write(img_data)

    except requests.exceptions.RequestException as e:
        # This will catch any general network error
        print(f"Network error: {e}")

    except openai.api_errors.APIError as e:
        # This will catch any error returned by the OpenAI API
        print(f"API error: {e}")

    except Exception as e:
        # This is a catch-all for any other exceptions
        print(f"Unexpected error: {e}")
		

import time

start_time = time.time()

# Your existing code here

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

import os
import openai
import requests
import secret
import time

# openai.api_key='xxxxx'

# Set the prompts
prompts = ["robot dog in a lab", "robot dog exploring the city", "robot dog watching the sunset"]

start_time = time.time()  # Start measuring execution time

# Generate and save the images
for i, prompt in enumerate(prompts):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256"
        )

        # Get the image URL from the response
        image_url = response['data'][0]['url']

        # Download and save the image
        img_data = requests.get(image_url).content
        with open(f"robot_dog_journey_{i+1}.jpg", 'wb') as handler:
            handler.write(img_data)

    except requests.exceptions.RequestException as e:
        # This will catch any general network error
        print(f"Network error: {e}")

    except openai.api_errors.APIError as e:
        # This will catch any error returned by the OpenAI API
        print(f"API error: {e}")

    except Exception as e:
        # This is a catch-all for any other exceptions
        print(f"Unexpected error: {e}")

end_time = time.time()  # End measuring execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

async def fetch_and_save_image(session, url, path):
    try:
        async with session.get(url) as resp:
            img_data = await resp.read()
            with open(path, 'wb') as handler:
                handler.write(img_data)
    except Exception as e:
        print(f"Unexpected error: {e}")
		
async def fetch_image(prompt, i):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256"
        )

        # Get the image URL from the response
        image_url = response['data'][0]['url']

        # Download and save the image
        async with aiohttp.ClientSession() as session:
            await fetch_and_save_image(session, image_url, f"robot_dog_journey_{i+1}.jpg")
    except openai.api_errors.APIError as e:
        # This will catch any error returned by the OpenAI API
        print(f"API error: {e}")

    except Exception as e:
        # This is a catch-all for any other exceptions
        print(f"Unexpected error: {e}")
		
async def main():
    start_time = time.time()  # Start measuring execution time

    tasks = []
    for i, prompt in enumerate(prompts):
        tasks.append(fetch_image(prompt, i))

    await asyncio.gather(*tasks)

    end_time = time.time()  # End measuring execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
	
import os
import openai
import aiohttp
import asyncio
import secret
import time

#openai.api_key='xxxxxx'

# Set the prompts
prompts = ["robot dog in a lab", "robot dog exploring the city", "robot dog watching the sunset"]

async def fetch_and_save_image(session, url, path):
    try:
        async with session.get(url) as resp:
            img_data = await resp.read()
            with open(path, 'wb') as handler:
                handler.write(img_data)
    except Exception as e:
        print(f"Unexpected error: {e}")

async def fetch_image(prompt, i):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256"
        )

        # Get the image URL from the response
        image_url = response['data'][0]['url']

        # Download and save the image
        async with aiohttp.ClientSession() as session:
            await fetch_and_save_image(session, image_url, f"robot_dog_journey_{i+1}.jpg")
    except openai.api_errors.APIError as e:
        # This will catch any error returned by the OpenAI API
        print(f"API error: {e}")

    except Exception as e:
        # This is a catch-all for any other exceptions
        print(f"Unexpected error: {e}")

async def main():
    start_time = time.time()  # Start measuring execution time

    tasks = []
    for i, prompt in enumerate(prompts):
        tasks.append(fetch_image(prompt, i))

    await asyncio.gather(*tasks)

    end_time = time.time()  # End measuring execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

# Run the main function
asyncio.run(main())


# WRITE YOUR CODE HERE
import os
import openai
import requests
import secret
import time

#openai.api_key='xxxxxx'

# Generate and save the images
def chain(prompts):
  for i, prompt in enumerate(prompts):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="256x256"
    )

    # Get the image URL from the response
    image_url = response['data'][0]['url']

    # Download and save the image
    img_data = requests.get(image_url).content
    with open(f"test{i+1}.jpg", 'wb') as handler:
        handler.write(img_data)

prompts = ["A cat", "A dog", "A bird"]
chain(prompts)


# WRITE YOUR CODE HERE
import os
import openai
import secret
from PIL import Image, ImageOps
from io import BytesIO
import requests

#openai.api_key='xxxxxx'

# Generate the base image
def generate_base_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

base_image_url = generate_base_image('red apple')
img_data = requests.get(base_image_url).content
with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)
	
# Manipulate the image properties
def manipulate_image(image, size, aspect_ratio, brightness, contrast, saturation, hue):
    # Resize the image
    new_size = (int(image.width * size), int(image.height * aspect_ratio * size))
    resized_image = image.resize(new_size, Image.ANTIALIAS)

    # Adjust the image properties
    from PIL import ImageEnhance, ImageOps
    enhanced_image = ImageEnhance.Brightness(resized_image).enhance(brightness)
    enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast)
    enhanced_image = ImageEnhance.Color(enhanced_image).enhance(saturation)
    
    # Adjust hue using ImageOps module
    # enhanced_image = ImageOps.colorize(enhanced_image.convert('L'), 'black', 'white', midpoint=128 - int(128 * hue))

    return enhanced_image
	
# Example of image manipulation
manipulated_image = manipulate_image(
  base_image, size=0.5, aspect_ratio=1, brightness=1.2,
  contrast=1.5, saturation=0.8, hue=0.1
)

# Save the manipulated image to a file
manipulated_image.save('manipulated_red_apple.jpg')


# Adjust hue only if hue is not 0
if hue != 0:
    # Convert image to HSV
    hsv_image = enhanced_image.convert('HSV')
    # Shift hue value
    hsv_image = hsv_image.point(lambda p: (p + int(256 * hue)) % 256 if p < 256 else p)
    # Convert back to RGB
    enhanced_image = hsv_image.convert('RGB')
	
# Example of image manipulation with only size change
size_changed_image = manipulate_image(
    base_image, size=0.8, aspect_ratio=1, brightness=1,
    contrast=1, saturation=1, hue=0
)

# Save the size-changed image to a file
size_changed_image.save('size_changed_red_apple.jpg')

# Example of image manipulation with a more purple hue
purple_image = manipulate_image(
    base_image, size=1, aspect_ratio=1, brightness=1,
    contrast=1, saturation=1, hue=0.8
)

# Save the purple image to a file
purple_image.save('purple_red_apple.jpg')


def generate_image(prompt):	
	response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
	image_url = response['data'][0]['url']
	img_data = requests.get(image_url).content
	with open('test_img.png', 'wb') as handler:
		handler.write(img_data)	
	image = Image.open('test_img.png')
	image = image.convert('L')
	image = image.resize((256, 256), Image.ANTIALIAS)
	image.save('test_img.png')
	
	
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url=response['data'][0]['url']

    # Download the image
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))
    # Apply transformations
    img = img.convert("L")  # Convert to grayscale
    img = img.resize((256, 256))  # Resize to 256x256 pixels
    # Save the image
    img.save("test_img.png")

import os
import openai
import secret
from PIL import Image, ImageFilter
from io import BytesIO
import requests
#openai.api_key='xxxxxx'
	
# Generate the base image
def generate_base_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

base_image_url = generate_base_image('plane')
img_data = requests.get(base_image_url).content
with open('plane.png', 'wb') as handler:
    handler.write(img_data)

image = Image.open('plane.png')
# Apply an edge enhance filter to the base image
edge_enhanced_image = image.filter(ImageFilter.EDGE_ENHANCE)

# Save the edge enhanced image to a file
edge_enhanced_image.save('enhanced_plane.png')

## PIL

# Flip the base image horizontally and vertically
flipped_both_image = ImageOps.mirror(ImageOps.flip(base_image))

# Save the horizontally and vertically flipped image to a file
flipped_both_image.save('flipped_both.jpg')

# Rotate the base image by 45 degrees with bilinear interpolation
rotated_image_45_bilinear = base_image.rotate(45, resample=Image.BILINEAR)

# Save the rotated image with bilinear interpolation to a file
rotated_image_45_bilinear.save('rotated_45_bilinear.jpg')

# Define custom center coordinates (x, y)
center_x = 100
center_y = 100

# Rotate the base image by 45 degrees around the custom center
rotated_image_custom_center = base_image.rotate(45, center=(center_x, center_y))

# Save the rotated image with custom center to a file
rotated_image_custom_center.save('rotated_custom_center.jpg')

# Rotate the base image by 120 degrees and expand the canvas
rotated_image_expanded = base_image.rotate(120, expand=True)

# Save the rotated image with expanded canvas to a file
rotated_image_expanded.save('rotated_expanded.jpg')

# Convert the base image to grayscale
grayscale_image = ImageOps.grayscale(base_image)

# Invert the grayscale image
inverted_grayscale_image = ImageOps.invert(grayscale_image)

# Save the inverted grayscale image to a file
inverted_grayscale_image.save('inverted_grayscale.jpg')

import os
import openai
import secret
from PIL import Image, ImageOps
from io import BytesIO
import requests
#openai.api_key='xxxxxx'
	
# Generate the base image
def generate_base_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

cool_prompt= "Reunion of man, team, squad with katanas, ninja ,background forest , abstract, full hd render + 3d octane render +4k UHD + immense detail + dramatic lighting + well lit + black, purple, blue, pink, cerulean, teal, metallic colours, + fine details + octane render + 8k"

base_image_url = generate_base_image(cool_prompt)
img_data = requests.get(base_image_url).content
with open('cool.png', 'wb') as handler:
    handler.write(img_data)

image = Image.open('cool.png')
image = image.rotate(45)
image.save('rotated_45_cool.png')
image = ImageOps.invert(image)
image.save('final_cool.png')


# CODIO SOLUTION BEGIN
import os
import openai
from PIL import Image,ImageOps
from io import BytesIO
import requests
import secret

# Set API key and prompt
#openai.api_key='xxxxxx'
user_input = "Create an image of a car"
"""
# Generate more descriptive text with GPT-3
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Create a more descriptive scene based on this user input: '{user_input}'.",
    max_tokens=50,
    n=1,
    stop=None,
    temperature=0.7,
)
"""
descriptive_text = "The car is a sleek, silver convertible with bright red leather seats. It's parked in front of a beautiful mansion with a fountain in the middle."
print(descriptive_text)

# Generate the base image
response = openai.Image.create(
    prompt=descriptive_text,
    n=1,
    size="512x512",
    temperature=1
)

image_url = response['data'][0]['url']

img_data = requests.get(image_url).content
with open('base_img.jpg', 'wb') as handler:
    handler.write(img_data)
# CODIO SOLUTION EMD

# WRITE YOUR CODE HERE
import os
import openai
from PIL import Image,ImageOps
from io import BytesIO
import requests
import secret

# Set API key and prompt
#openai.api_key='xxxxxx'


def generate_image(prompt):
  """
  This function accepts a user's prompt, enhances it using the GPT API, then generates an image from the enhanced prompt using the DALL-E API, and saves it as `my_img.png`.
  
  Parameters:
      prompt (str): The initial user's prompt.

  Returns:
      None
  """

  # Step 1: Pass the user's prompt to the GPT API to get a refined prompt.
  print(prompt)
  response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=prompt)
  prompt = response["choices"][0]["message"]["content"]
  print(prompt)
  # Step 2: Pass the refined prompt to the DALL-E API to get the generated image.
  # Generate the base image
  response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="512x512",
    temperature=1
  )

  image_url = response['data'][0]['url']

  # Step 3: Save the generated image as `my_img.png`.
  img_data = requests.get(image_url).content
  with open('my_img.png', 'wb') as handler:
    handler.write(img_data)

  return None
  
  
import os
import openai
from PIL import Image, ImageOps,ImageChops
from io import BytesIO
import requests

# Set environment variables
#openai.api_key =  os.getenv('OPENAI_KEY')
#openai.api_key='xxxxxx'

# Generate the base image
def generate_base_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

def download_image(image_url,x):
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    with open(x+'.jpg', 'wb') as handler:
      handler.write(img_data)
    return img
	
def generate_earth_image(angle):
    prompt = f"Realistic Earth from space at {angle} degrees angle"
    image_url = generate_base_image(prompt)
    image_filename = f"earth_{angle}_degrees"
    image = download_image(image_url, image_filename)
    return image

angles = range(0, 360, 10)
earth_images = [generate_earth_image(angle) for angle in angles]

angles = range(0, 360, 10)
image_filenames = [f"earth_{angle}_degrees.jpg" for angle in angles]

resized_earth_images = []
for filename in image_filenames:
    img = Image.open(filename)
    resized_img = img.resize((256, 256), Image.ANTIALIAS)
    resized_earth_images.append(resized_img)

output_gif = "rotating_earth.gif"
resized_earth_images[0].save(
    output_gif,
    save_all=True,
    append_images=resized_earth_images[1:],
    duration=100,
    loop=0
)

duration = 200 , # Adjust the frame duration to your preference
loop_count = 3  # Adjust the loop count to your preference
optimize = True  # Enable image optimization

output_gif = "optimized_rotating_earth.gif"
resized_earth_images[0].save(
    output_gif,
    save_all=True,
    append_images=resized_earth_images[1:],
    duration=duration,
    loop=loop_count,
    optimize=optimize
)

from PIL import ImageChops

def crossfade(image1, image2, alpha):
    return ImageChops.blend(image1, image2, alpha)

crossfade_frames = []
for i in range(len(resized_earth_images) - 1):
    for alpha in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        frame = crossfade(resized_earth_images[i], resized_earth_images[i + 1], alpha)
        crossfade_frames.append(frame)
		
from PIL import ImageEnhance

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

brightness_factor = 1.5
brightened_frames = [adjust_brightness(frame, brightness_factor) for frame in crossfade_frames]

output_gif = "enhanced_rotating_earth.gif"
brightened_frames[0].save(
    output_gif,
    save_all=True,
    append_images=brightened_frames[1:],
    duration=duration,
    loop=loop_count,
    optimize=optimize
)

output_gif = "enhanced_rotating_earth.gif"
brightened_frames[0].save(
    output_gif,
    save_all=True,
    append_images=brightened_frames[1:],
    duration=duration,
    loop=loop_count,
    optimize=optimize
)

def download_image(image_url,x):
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    with open(x+'.jpg', 'wb') as handler:
      handler.write(img_data)
    return img
	
# WRITE YOUR CODE HERE
import os
import openai
from PIL import Image, ImageOps,ImageChops
from io import BytesIO
import requests

# Set environment variables
#openai.api_key =  os.getenv('OPENAI_KEY')
#openai.api_key='xxxxxx'

# Generate the base image
def generate_base_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

moon_image_url = generate_base_image('moon')
night_sky_image_url = generate_base_image('night sky with stars')

img_data = requests.get(moon_image_url).content
with open('moon_image.jpg', 'wb') as handler:
    handler.write(img_data)
img_data = requests.get(night_sky_image_url).content
with open('night_sky.jpg', 'wb') as handler:
    handler.write(img_data)

#saving our images as variables.
moon_image=Image.open('moon_image.jpg')
night_sky_image=Image.open('night_sky.jpg')


# Resize the moon image to fit the composition
moon_image = moon_image.resize((200, 200), Image.ANTIALIAS)

# Ensure the moon image has the correct mode with an alpha channel
moon_image = moon_image.convert('RGBA')

# Overlay the moon image on top of the night sky image
night_sky_image.paste(moon_image, (150, 100), moon_image)

# Save the composed image to a file
night_sky_image.save('night_sky_with_moon.jpg')

# Download and open the generated images
image1 = download_image(image1_url,'image1')
image2 = download_image(image2_url,'image2')

# Create a custom mask (grayscale gradient)
width, height = image1.size
mask = Image.new('L', (width, height))
for y in range(height):
    for x in range(width):
        mask.putpixel((x, y), x)

# Composite the two images using the custom mask
result = Image.composite(image1, image2, mask)

# Save the composited image to a file
result.save('composite_custom_mask.jpg')

# Blend the images using the Multiply mode
image1 = Image.open('image1.jpg')
image2 = Image.open('image2.jpg')
multiply_blend = ImageChops.multiply(image1, image2)
multiply_blend.save('multiply_blend.jpg')

# Blend the images using the Multiply mode
image3 = Image.open('moon_image.jpg')
image4 = Image.open('night_sky.jpg')
multiply_blend = ImageChops.multiply(image3, image4)
multiply_blend.save('multiply_blend2.jpg')

from PIL import ImageChops

def average_blend(image1, image2):
    return ImageChops.add(image1, image2, scale=0.5)

# Use the custom blend mode to blend two images
image1 = Image.open('image1.jpg')
image2 = Image.open('image2.jpg')
average_blend_result = average_blend(image1, image2)
average_blend_result.save('average_blend.jpg')

# Create a custom gradient mask (grayscale gradient)
width, height = image1.size
mask = Image.new('L', (width, height))
for y in range(height):
    for x in range(width):
        mask.putpixel((x, y), x)

# Apply the custom gradient mask to the second image
masked_image2 = Image.composite(image2, Image.new('RGB', image2.size), mask)

# Blend the images using the custom blend mode
result = custom_blend(image1, masked_image2)

# Save the blended image to a file
result.save('custom_blend_gradient.jpg')

def filters(image_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Ask the user to choose a filter
        print("Choose a filter to apply on the image:")
        print("1. Contour")
        print("2. Edge Enhance")
        print("3. Find Edges")
        option = input("Enter your option: ")

        if option == "1":
            filtered_img = img.filter(ImageFilter.CONTOUR)
        elif option == "2":
            filtered_img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif option == "3":
            filtered_img = img.filter(ImageFilter.FIND_EDGES)
        else:
            print("Invalid option. Applying Contour filter by default.")
            filtered_img = img.filter(ImageFilter.CONTOUR)
        
        # Save the filtered image
        filtered_img.save('filtered_image.png')
        print("Filter applied successfully, 'filtered_image.png' created.")
