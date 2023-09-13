import random
from time import time
import os
import sys
from PIL import Image
import concurrent.futures
from multiprocessing import Process, Queue, Lock, Value

IMG_SIZE = 224
SCALE = .5 * IMG_SIZE
DELETE = 1

# List of output directories (categories) for easy upload to Teachable Machine
output_dirs = ["right3", "left3", "up3", "down3"]  


'''
Saves images in the multiprocessing queue to disk.
These images contain the overlayed sign that will control the game
@ q: the queue shared between processes
'''
def save_composite_image(q: Queue):
    while(True):
        try:
            image = q.get(timeout=10)
            image[0].save(image[1])
            # print(f"Images saved: {image[1].split('/')[-2:]}")
        except TimeoutError as e:
            print(e)
            break

'''
Saves images in the multiprocessing queue to disk
These images DO NOT contain the overlayed sign
@ q: the queue shared between processes
'''
def save_nothing_image(n: Queue):
    while(True):
        try:
            image = n.get(timeout=10)
            image[0].save(image[1])
            # print(f"Images saved: {image[1].split('/')[-2:]}")
        except TimeoutError as e:
            print(e)
            break

def overlay_image_nothing(background):
    global nothing_lock, nothing_counter

    base_image = Image.open(background)

    composite_images = []

    # overlay_images_portrait = [Image.open(img) for img in overlay_portrait]

    # portrait_positions = [(0, 0),  # Top-left
    #                       ((base_image.width - overlay_images_portrait[0].width) // 2, 0),  # Top-center
    #                       (base_image.width - overlay_images_portrait[0].width, 0),  # Top-right
    #                       (0, (base_image.height - overlay_images_portrait[0].height) // 2),  # Middle-left
    #                       ((base_image.width - overlay_images_portrait[0].width) // 2, (base_image.height - overlay_images_portrait[0].height) // 2),  # Center
    #                       (base_image.width - overlay_images_portrait[0].width, (base_image.height - overlay_images_portrait[0].height) // 2),  # Middle-right
    #                       (0, base_image.height - overlay_images_portrait[0].height),  # Bottom-left
    #                       ((base_image.width - overlay_images_portrait[0].width) // 2, base_image.height - overlay_images_portrait[0].height),  # Bottom-center
    #                       (base_image.width - overlay_images_portrait[0].width, base_image.height - overlay_images_portrait[0].height)  # Bottom-right
    #                       ]

    # For each picture, I want to take 10 random croppings of it
    # for i in range(10):
    # for overlay_portrait in overlay_images_portrait:
        # for portrait_position in portrait_positions:
        #     for portrait_size_multiplier in [.25, .4, .6]:  # Vary the size of the hand image

    nothing_lock.acquire()
    output_filename = f"ml_model/base_images/image_dataset/nothing/composite_{nothing_counter}.png"
    nothing_counter += 1
    nothing_lock.release()

    if not os.path.isfile(output_filename):
        composite = base_image.copy()
        center = (random.randint(0, base_image.width - SCALE), random.randint(0, base_image.height - SCALE))
        composite = composite.crop((center[0] - SCALE, center[1] - SCALE, center[0] + SCALE, center[1] + SCALE))

        # original_x, original_y = base_image.size
        # start_x, start_y = portrait_position
        # mapped_x = int(start_x * IMG_SIZE / original_x)
        # mapped_y = int(start_y * IMG_SIZE / original_y)
        # portrait_position = (mapped_x, mapped_y)
        
        # overlay_portrait_resized = overlay_portrait.resize((int(overlay_portrait.width * portrait_size_multiplier), int(overlay_portrait.height * portrait_size_multiplier)))
        # rotated_overlay_portrait = overlay_portrait.rotate(random.randint(-10, 10), expand=True)
        # composite.paste(rotated_overlay_portrait, portrait_position, rotated_overlay_portrait)
        
        composite_images.append((composite, output_filename))
    
    else:
        print (f"SKIPPING {output_filename}")

    return composite_images 

def overlay_arrow(background: list, arrow: str, q: Queue, n: Queue, l: Lock, counter: Value):
    global filename_counter, counter_lock

    rotation = 0
    progress_counter = 0
    total_pics = len(background)

    for base_filename in background:
        if(progress_counter % 100 == 0):
            print(os.getpid(), f"progress: {progress_counter / total_pics}")
        progress_counter += 1

        base_image = Image.open(base_filename)
        arrow_image = Image.open(arrow)

        base_filename = base_filename.split('/')[-1][:-4]

        for arrow_size in [.5, .9]:
            # For each of the 3 directions.  
            for direction in output_dirs:
                if "right" in direction:
                    arrow_image1 = arrow_image.rotate(0, expand=True)
                elif "left" in direction:
                    arrow_image1 = arrow_image.rotate(180, expand=True)
                else:
                    arrow_image1 = arrow_image.rotate(90, expand=True)

                # if not os.path.isfile(output_filename):
                # For each position in the later-defined arrow_positions
                for i in range(4):

                    # Secure a unique filename with the counter variable
                    with counter.get_lock():
                        counter.value += 1
                        output_filename = f"ml_model/base_images/image_dataset/{direction}/{counter.value}_{base_filename}.png"
    
                    composite = base_image.copy()

                    # Some of these pictures have wonky dimensions, so I need to handle them appropriately
                    if(base_image.width - SCALE < SCALE):
                        x1 = base_image.width - SCALE
                        x2 = SCALE
                    else:
                        x2 = base_image.width - SCALE
                        x1 = SCALE
                    if(base_image.height - SCALE < SCALE):
                        y1 = base_image.height - SCALE
                        y2 = SCALE
                    else:
                        y2 = base_image.height - SCALE
                        y1 = SCALE

                    center = (random.randint(x1, x2), random.randint(y1, y2))
                    composite = composite.crop((center[0] - SCALE, center[1] - SCALE, center[0] + SCALE, center[1] + SCALE))
                    
                    # Make the arrow smaller and rotate it just a bit each time for some variation
                    arrow_image2 = arrow_image1.resize((int(arrow_image.width * arrow_size), int(arrow_image.height * arrow_size)))
                    arrow_image3 = arrow_image2.rotate(random.randint(-10, 10), expand=True)

                    arrow_positions = [(0, 0),  # Top-left
                                    # ((composite.width // 2) - (arrow_image.width // 2), 0),  # Top-center
                                    (composite.width - arrow_image.width, 0),  # Top-right
                                    # (0, (composite.height // 2) - (arrow_image.height // 2)),  # Middle-left
                                    ((composite.width // 2) - (arrow_image.width // 2), (composite.height // 2) - (arrow_image.height // 2)),  # Center
                                    # (composite.width - arrow_image.width, (composite.height // 2) - (arrow_image.height // 2)),  # Middle-right
                                    (0, composite.height - arrow_image.height),  # Bottom-left
                                    # ((composite.width // 2) - (arrow_image.width // 2), composite.height - arrow_image.height),  # Bottom-center
                                    (composite.width - arrow_image.width, composite.height - arrow_image.height)  # Bottom-right
                                    ]
                    
                    composite.paste(arrow_image3, arrow_positions[i], arrow_image3)

                    # TODO: add multiprocess queue
                    q.put_nowait((composite, output_filename))

        # Make a copy to serve as my "nothing" category

        # if(base_image.width - SCALE < SCALE):
        #     x1 = base_image.width - SCALE
        #     x2 = SCALE
        # else:
        #     x2 = base_image.width - SCALE
        #     x1 = SCALE
        # if(base_image.height - SCALE < SCALE):
        #     y1 = base_image.height - SCALE
        #     y2 = SCALE
        # else:
        #     y2 = base_image.height - SCALE
        #     y1 = SCALE

        # center = (random.randint(x1, x2), random.randint(y1, y2))
        # nothing_image = base_image.copy().crop((center[0] - SCALE, center[1] - SCALE, center[0] + SCALE, center[1] + SCALE))
        # n.put_nowait((nothing_image, f"ml_model/base_images/image_dataset/nothing/{base_filename}.png"))

def overlay_arrowv2(background: list, arrow: str, q: Queue, n: Queue, l: Lock, counter: Value, direction: str):
    global filename_counter, counter_lock

    progress_counter = 0
    total_pics = len(background)

    for base_filename in background:
        # Random arrow size for every background
        arrow_size = round(random.uniform(.4, 1), 2)

        if(progress_counter % 100 == 0):
            print(os.getpid(), f"progress: {progress_counter / total_pics}")
        progress_counter += 1

        base_image = Image.open(base_filename)
        arrow_image = Image.open(arrow)

        base_filename = base_filename.split('/')[-1][:-4]

        if "right" in direction:
            arrow_image1 = arrow_image.rotate(0, expand=True)
        elif "left" in direction:
            arrow_image1 = arrow_image.rotate(180, expand=True)
        else:
            arrow_image1 = arrow_image.rotate(90, expand=True)

        # Secure a unique filename with the counter variable
        with counter.get_lock():
            counter.value += 1
            output_filename = f"ml_model/base_images/image_dataset/{direction}/{counter.value}_{base_filename}.png"

        composite = base_image.copy()

        # Some of these pictures have wonky dimensions, so I need to handle them appropriately
        if(base_image.width - SCALE < SCALE):
            x1 = base_image.width - SCALE
            x2 = SCALE
        else:
            x2 = base_image.width - SCALE
            x1 = SCALE
        if(base_image.height - SCALE < SCALE):
            y1 = base_image.height - SCALE
            y2 = SCALE
        else:
            y2 = base_image.height - SCALE
            y1 = SCALE

        center = (random.randint(x1, x2), random.randint(y1, y2))
        composite = composite.crop((center[0] - SCALE, center[1] - SCALE, center[0] + SCALE, center[1] + SCALE))
        
        # Make the arrow smaller and rotate it just a bit each time for some variation
        arrow_image2 = arrow_image1.resize((int(arrow_image.width * arrow_size), int(arrow_image.height * arrow_size)))
        arrow_image3 = arrow_image2.rotate(random.randint(-10, 10), expand=True)

        arrow_positions = [(0, 0),  # Top-left
                        ((composite.width // 2) - (arrow_image.width // 2), 0),  # Top-center
                        (composite.width - arrow_image.width, 0),  # Top-right
                        (0, (composite.height // 2) - (arrow_image.height // 2)),  # Middle-left
                        ((composite.width // 2) - (arrow_image.width // 2), (composite.height // 2) - (arrow_image.height // 2)),  # Center
                        (composite.width - arrow_image.width, (composite.height // 2) - (arrow_image.height // 2)),  # Middle-right
                        (0, composite.height - arrow_image.height),  # Bottom-left
                        ((composite.width // 2) - (arrow_image.width // 2), composite.height - arrow_image.height),  # Bottom-center
                        (composite.width - arrow_image.width, composite.height - arrow_image.height)  # Bottom-right
                        ]
        
        composite.paste(arrow_image3, arrow_positions[random.randint(0,8)], arrow_image3)

        # TODO: add multiprocess queue
        q.put_nowait((composite, output_filename))

if __name__ == "__main__":
    background_path = 'ml_model/base_images/backgrounds/indoorCVPR_09/Images/'
    background_images = []

    arrow_path = 'ml_model/base_images/arrow2.png'

    # Load the images I want for my background from the selected sub paths
    for dir in os.listdir(background_path):
        # print(background_path + dir)
        for file in os.listdir(background_path + dir):
            background_images.append(background_path + dir + '/' + file)
            
    # A patch because I don't want to make my loop work with a wonky number of indices
    background_images = background_images[0:15000]

    # Remove all the old photos generated in the 4 categories\
    if(DELETE):
        for output_dir in output_dirs:
            output_path = f"ml_model/base_images/image_dataset/{output_dir}/"
            for file in os.listdir(output_path):
                if file.endswith(".png") or file.endswith(".jpg"):
                    os.remove(os.path.join(output_path, file))
        print("Successfully deleted all previously-generated images.\n")

    # progress = 0
    start = time()
    
    num_images = len(background_images)
    savingQueue = Queue()
    nothingQueue = Queue()
    counter_lock = Lock()
    filename_counter = Value('i', 0)

    procList = []

    # Making images with overlayed arrows
    # for x in range(5):
    #     proc = Process(target=overlay_arrowv2, args=(background_images[3000 * x:3000 * (x + 1)], arrow_path, savingQueue, nothingQueue, counter_lock, filename_counter, round(random.uniform(.4, 1), 2), output_dir[0]))
    #     proc.start()
    #     procList.append(proc)
    
    for i in range(5):
        # if(i < 3):
        proc = Process(target=overlay_arrow, args=(background_images[3000 * i:3000 * (i + 1)], arrow_path, savingQueue, nothingQueue, counter_lock, filename_counter))
        # else:
        #     proc = Process(target=overlay_image_nothing, args=(background_images[4000 * i:4000 * (i + 1) - 1500], savingQueue, counter_lock, filename_counter, output_dirs[i]))
        # proc = Process(target=overlay_arrowv2, args=(background_images[0:3000], arrow_path, savingQueue, nothingQueue, counter_lock, filename_counter, output_dirs[i]))
        proc.start()
        procList.append(proc)
    
    # To save the arrows and nothing images
    saveProcList = []

    # Saving images with overlayed arrows
    for x in range(5):
        saveProc = Process(target=save_composite_image, args=(savingQueue,))
        saveProc.start()
        saveProcList.append(saveProc)

    # Saving images with NO overlayed arrows
    # for x in range(5):
    #     saveProc2 = Process(target=save_nothing_image, args=(nothingQueue,))
    #     saveProc2.start()
    #     saveProcList.append(saveProc2)

    # Wait for all the processes to finish
    for proc in procList:
        proc.join()
    for proc in saveProcList:
        proc.join()

    print("All images generated and saved.")