# Generate Images for D&D NPCS using a latent consistancy model

In addition to offering an option for regular text to image generation, this tool has a way to automagically generate semi-random descriptions of NPCs and then generate pictures based on those, for example, you might tell it you want a rogue, and it will first generate a detailed description like:

a watercolor image showing the entire body of of a D&D NPC in medieval clothing in a medieval city who is described as: petite extrodanarily attractive female gnome rogue  with sparkling grey eyes, an enchanting  mouth,  a snub nose, and straight  hair wearing a form-fitting black finely-tailored waistcoat, matching black sturdy leggings and brown fur-lined boots"

After creating these images, it will sort them into folders named gender_race_class.  For example the images created by the prompt above would be placed into the female_gnome_rogue folder.


# Run latent consistency models on your Mac/ PC or Linux

Latent consistency models (LCMs) are based on Stable Diffusion, but they can generate images much faster, needing only 4 to 8 steps for a good image (compared to 25 to 50 steps). [Simian Luo et al](https://arxiv.org/abs/2310.04378) released the first Stable Diffusion distilled model. It’s distilled from the Dreamshaper fine-tune by incorporating classifier-free guidance into the model’s input.

You can [run Latent Consistency Models in the cloud on Replicate](https://replicate.com/luosiallen/latent-consistency-model), but it's also possible to run it locally.

## Prerequisites

You’ll need:

- a Mac with an M1 or M2 chip
- 16GB RAM or more
- macOS 12.3 or higher
- Python 3.10 or above

## Install

Run this to clone the repo:

    git clone https://github.com/replicate/latent-consistency-model.git
    cd latent-consistency-model

Set up a virtualenv to install the dependencies:

    python3 -m pip install virtualenv
    python3 -m virtualenv venv

Activate the virtualenv:

    source venv/bin/activate

(You'll need to run this command again any time you want to run the script.)

Then, install the dependencies:

    pip install -r requirements.txt

## Run

The script will automatically download the [`SimianLuo/LCM_Dreamshaper_v7`](https://huggingface.co/SimianLuo/LCM_Dreamshaper_v7) (3.44 GB) and [safety checker](https://huggingface.co/CompVis/stable-diffusion-safety-checker) (1.22 GB) models from HuggingFace.

```sh
python main.py \
  "a beautiful apple floating in outer space, like a planet" \
  --steps 4 --width 512 --height 512
```

You’ll see an output like this:

```sh
Output image saved to: output/out-20231026-144506.png
Using seed: 48404
100%|███████████████████████████| 4/4 [00:00<00:00,  5.54it/s]
```

## Options

| Parameter     | Type  | Default | Description                                                   |
|---------------|-------|---------|---------------------------------------------------------------|
| prompt        | str   | N/A     | A text string for image generation.                           |
| --width       | int   | 512     | The width of the generated image.                             |
| --height      | int   | 512     | The height of the generated image.                            |
| --steps       | int   | 8       | The number of inference steps.                                |
| --seed        | int   | None    | Seed for random number generation.                            |
| --continuous  | flag  | False   | Enable continuous generation.                                 |
