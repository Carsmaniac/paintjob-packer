# Paintjob Packer
Paintjob mod maker for SCS trucksim games

Please note: I have no idea how GitHub works and I'm mostly making this to play around :)

## Functions (wishlist)

* Generate trucksim mods
    * Euro Truck Simulator 2 truck paintjobs
    * American Truck Simulator truck paintjobs
    * Player-owned trailer paintjobs
* Generate readymade paintjob packs with multiple paintjobs
    * Keep multiple sets of parameters (maybe you want to maintain an ETS 2 pack and an ATS pack)
* Quickly generate a single paintjob mod with set parameters (for quick in-game testing of a paintjob you're working on)

## How to Use

Paintjob Packer is just the last step in making a mod, it helps you turn a lovingly crafted image into a fully working .scs file. You'll first need to make your paintjob in a program such as Photoshop. You can find templates and tutorials all over the web.

### Making full paintjob packs
1. Run `configure.py`
2. Set up a truck list to your liking, following on-screen instructions
3. Save your paintjobs as `.dds` files, named after each paintjob's internal name
4. Place them in `input/<list name here>`
5. Add your modpack images
6. Run `auto.py`
7. Mod will be created and placed in the base folder

### Making single test mods
This is intended for when you are developing a paintjob. If you make a small tweak to your file, you can generate a new .scs file in one click without having to worry about piles of menus.

1. Save your paintjob as `test.dds`
2. Place it inside `input/manual`
3. Run `man.py`
4. Your mod will be saved as `test.scs` in the base folder

### Additional Tips
* When saving your `.dds` files, save them in the DXT5 format with mipmaps, otherwise you might run into problems ingame

## Files

* `single.py`: Generates a single paintjob
* `auto.py`: Generates a complete paintjob pack
* `man.py`: Generates a single paintjob with preset parameters
* `configure.py`: Configures parameters for paintjob packs and single manual paintjobs
* `paintjob.py`: Functions and other goodies used by everything else
* `config.ini`: Parameters for paintjob generation

TODO: Finish the readme
