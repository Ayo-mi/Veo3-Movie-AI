import subprocess

import os



def concatenate_videos(input_files, output_file):

    """

    Concatenates a list of video files into a single video file using FFmpeg.

    """

    if not input_files:

        print("No video files to concatenate.")

        return



    # Create a list file for FFmpeg

    list_file_path = "mylist.txt"

    with open(list_file_path, "w") as f:

        for file in input_files:

            f.write(f"file '{os.path.abspath(file)}'\n")



    # Construct the FFmpeg command

    command = [

        "ffmpeg",

        "-f", "concat",

        "-safe", "0",

        "-i", list_file_path,

        "-c", "copy",

        output_file

    ]



    print("Concatenating videos...")

    try:

        subprocess.run(command, check=True)

        print(f"Movie successfully created at {output_file}")

    except subprocess.CalledProcessError as e:

        print(f"An error occurred during concatenation: {e}")

    finally:

        os.remove(list_file_path)



if __name__ == "__main__":

    output_dir = "movie_clips"

    generated_files = [os.path.join(output_dir, f) for f in sorted(os.listdir(output_dir)) if f.endswith('.mp4')]

    final_movie_path = "final_movie.mp4"



    concatenate_videos(generated_files, final_movie_path)