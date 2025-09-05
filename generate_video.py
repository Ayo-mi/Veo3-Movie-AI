from google import genai
from google.genai import types
import time
import os



# Set your Gemini API key from an environment variable

client = genai.Client(api_key=os.environ["GEMINI_KEY"])



# Your story line broken down into scenes or prompts

story_script = [

    "A majestic dragon soars over a snow-capped mountain range, with the sun setting behind it.",

    "The dragon lands in a peaceful village, and a small child approaches it with a fruit.",

    "The dragon and the child share a laugh, and the dragon breathes a gentle puff of smoke.",

    "The child waves goodbye as the dragon takes off and flies into the night sky, its scales shimmering in the moonlight.",

]



def generate_video_from_prompt(prompt):

    """

    Generates an 8-second video from a text prompt using the Veo 3 model.

    """

    try:

        print(f"Generating video for scene: '{prompt[:50]}...'")

        operation = client.models.generate_videos(

            model="models/veo-3.0-generate-preview",

            prompt=prompt,

            config=types.GenerateVideosConfig(negative_prompt="barking, woofing"),

        )



        # Poll the operation status until the video is ready

        while not operation.done:

            print("Waiting for video generation to complete...")

            time.sleep(10)

            operation = client.operations.get(operation)



        if operation.response and operation.response.generated_videos:

            video = operation.response.generated_videos[0].video

            return video

        else:

            print(f"Failed to generate video for: '{prompt[:50]}...'")

            return None



    except Exception as e:

        print(f"An error occurred: {e}")

        return None



def save_video(video, filename):

    """

    Saves the generated video bytes to a file.

    """

    with open(filename, "wb") as f:

        f.write(video.video_bytes)

    print(f"Video saved to {filename}")



if __name__ == "__main__":

    generated_files = []

    output_dir = "movie_clips"

    os.makedirs(output_dir, exist_ok=True)



    for i, scene_prompt in enumerate(story_script):

        video_clip = generate_video_from_prompt(scene_prompt)

        if video_clip:

            filename = os.path.join(output_dir, f"scene_{i+1:02d}.mp4")

            save_video(video_clip, filename)

            generated_files.append(filename)



    print("\nAll video clips have been generated and saved.")

    print(f"Saved files: {generated_files}")