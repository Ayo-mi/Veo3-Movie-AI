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

        # Generate video using the correct API call
        operation = client.models.generate_videos(

            model="models/veo-3.0-generate-preview",

            prompt=prompt,

            config=types.GenerateVideosConfig(negative_prompt="barking, woofing"),

        )

        print(f"Operation created: {operation}")

        # Poll the operation status until the video is ready
        max_attempts = 60  # 10 minutes max
        attempt = 0
        
        while not operation.done and attempt < max_attempts:

            print(f"Waiting for video generation to complete... (attempt {attempt + 1}/{max_attempts})")

            time.sleep(10)

            operation = client.operations.get(operation)
            attempt += 1

        if operation.done and operation.response and operation.response.generated_videos:

            video = operation.response.generated_videos[0].video

            print(f"Video generation successful for: '{prompt[:50]}...'")

            print(f"Video object type: {type(video)}")

            print(f"Video object attributes: {dir(video)}")

            # Check if video has the expected attributes
            if hasattr(video, 'video_bytes'):
                print(f"Video has video_bytes: {len(video.video_bytes) if video.video_bytes else 'None'}")
            elif hasattr(video, 'uri'):
                print(f"Video has URI: {video.uri}")
            elif hasattr(video, 'url'):
                print(f"Video has URL: {video.url}")
            else:
                print("Video object structure:")
                for attr in dir(video):
                    if not attr.startswith('_'):
                        try:
                            value = getattr(video, attr)
                            print(f"  {attr}: {type(value)} = {value}")
                        except:
                            print(f"  {attr}: <unable to access>")

            return video

        else:

            print(f"Failed to generate video for: '{prompt[:50]}...'")

            if operation.error:

                print(f"Operation error: {operation.error}")

            if operation.response:

                print(f"Operation response: {operation.response}")

            else:

                print("No response from operation")

            return None

    except Exception as e:

        print(f"An error occurred during video generation: {e}")

        import traceback

        traceback.print_exc()

        return None



def save_video(video, filename):

    """

    Saves the generated video to a file. Handles different video data formats.

    """

    if not video:

        print(f"Error: No video object provided for {filename}")

        return False

    

    try:

        # Try different ways to get video data
        video_data = None
        
        if hasattr(video, 'video_bytes') and video.video_bytes is not None:

            video_data = video.video_bytes

            print(f"Using video_bytes data (length: {len(video_data)})")

        elif hasattr(video, 'uri') and video.uri:

            print(f"Video has URI: {video.uri}")

            # If it's a URI, we might need to download it

            # For now, let's try to access the video data directly

            if hasattr(video, 'data') and video.data:

                video_data = video.data

                print(f"Using video.data (length: {len(video_data)})")

            else:

                print("Video has URI but no accessible data. You may need to download it separately.")

                return False

        elif hasattr(video, 'url') and video.url:

            print(f"Video has URL: {video.url}")

            # Similar to URI handling

            if hasattr(video, 'data') and video.data:

                video_data = video.data

                print(f"Using video.data (length: {len(video_data)})")

            else:

                print("Video has URL but no accessible data. You may need to download it separately.")

                return False

        else:

            print("Video object structure:")

            for attr in dir(video):

                if not attr.startswith('_'):

                    try:

                        value = getattr(video, attr)

                        if callable(value):

                            print(f"  {attr}: {type(value)} (method)")

                        else:

                            print(f"  {attr}: {type(value)} = {value}")

                    except:

                        print(f"  {attr}: <unable to access>")

            print(f"Error: Could not find video data in any expected format for {filename}")

            return False

        

        if video_data:

            with open(filename, "wb") as f:

                f.write(video_data)

            print(f"Video saved to {filename}")

            return True

        else:

            print(f"Error: No video data found for {filename}")

            return False

    except Exception as e:

        print(f"Error saving video to {filename}: {e}")

        import traceback

        traceback.print_exc()

        return False



if __name__ == "__main__":

    # Check if API key is set
    if "GEMINI_KEY" not in os.environ:
        print("Error: GEMINI_KEY environment variable is not set!")
        print("Please set your Gemini API key as an environment variable.")
        exit(1)

    generated_files = []

    output_dir = "movie_clips"

    os.makedirs(output_dir, exist_ok=True)

    print(f"Starting video generation for {len(story_script)} scenes...")

    print(f"Output directory: {os.path.abspath(output_dir)}")



    for i, scene_prompt in enumerate(story_script):

        print(f"\n{'='*60}")

        print(f"Processing scene {i+1}/{len(story_script)}")

        print(f"Prompt: {scene_prompt}")

        print(f"{'='*60}")

        

        video_clip = generate_video_from_prompt(scene_prompt)

        if video_clip:

            filename = os.path.join(output_dir, f"scene_{i+1:02d}.mp4")

            print(f"Attempting to save video to: {filename}")

            

            if save_video(video_clip, filename):

                generated_files.append(filename)

                print(f"✓ Successfully saved scene {i+1}")

            else:

                print(f"✗ Failed to save scene {i+1}")

        else:

            print(f"✗ Failed to generate video for scene {i+1}")



    print(f"\n{'='*60}")

    print("VIDEO GENERATION SUMMARY")

    print(f"{'='*60}")

    print(f"Total scenes processed: {len(story_script)}")

    print(f"Successfully generated and saved: {len(generated_files)}")

    print(f"Failed: {len(story_script) - len(generated_files)}")

    

    if generated_files:

        print(f"\nSaved files:")

        for file in generated_files:

            file_path = os.path.abspath(file)

            file_size = os.path.getsize(file) if os.path.exists(file) else 0

            print(f"  - {file_path} ({file_size} bytes)")

    else:

        print("\nNo videos were successfully generated and saved.")

        print("Check the error messages above for troubleshooting.")