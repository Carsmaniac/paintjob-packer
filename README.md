# Paintjob Packer
Paintjob Packer is a lightweight mod making tool for Euro Truck Simulator 2 and American Truck Simulator. It allows you to generate simple paintjob mods, with a focus on mods that support multiple vehicles.

## Features

* Support for player-owned trailers, including those from DLCs
* Support for trucks using the newer accessory-based paintjob system, like the Scania S and MAN TGX Euro 6
* Support for as many vehicles as you like in a single mod
* Built-in support for >100 truck and trailer mods, full list [here](https://github.com/Carsmaniac/paintjob-packer/blob/master/library/mod%20links.md)
* Support for separate paintjobs for each cabin of a truck, in case a single texture doesn't work for all of them
* Optionally includes readymade 4k templates for each vehicle, which can be downloaded separately [here](https://forum.scssoft.com/viewtopic.php?f=33&t=272386) (ETS 2) and [here](https://forum.scssoft.com/viewtopic.php?f=199&t=288778) (ATS)

## Making a mod

Paintjob Packer doesn't make a completed mod when you click the *Generate mod* button. Instead, it makes what I call "custom example mods", giving you all the files you need for your mod, but with placeholders standing in for every image/texture. You then go through and replace all the placeholder images with your own to complete the mod. Since you usually have to test and tweak a paintjob many times before it's ready, generating paintjobs this way means you only have to run the program once.

**A more in-depth video version of this guide is [available on YouTube](https://www.youtube.com/watch?v=HJV8_X3P9k8)**

### Image editor requirements

Paintjob Packer requires an image editor that can save DDS files. DDS is a special image format used to save textures for many games, including both Trucksim games. You can use any of the following:

* Photoshop with its [DDS plugin](https://fnordware.blogspot.com/2014/09/dds-plug-in-for-after-effects-and.html)
* [GIMP](https://www.gimp.org/downloads/)
* [Paint.NET](https://www.getpaint.net/download.html)
* Or you could use any program you like and convert your images to DDS using [DXTBmp](https://www.mwgfx.co.uk/programs/dxtbmp.htm)

1. Generate base files using Paintjob Packer
    * Make a single paintjob for a single vehicle, or a pack with support for multiple vehicles
    * Support each truck's biggest cabin only or all of them, with a single paintjob per vehicle or separate ones for each cabin
    * Optionally use 4k/2k templates as placeholder files (if installed)

2. Replace mod manager files
    * `Mod_Manager_Description.txt` and `Mod_Manager_Image.jpg`
    * The description already contains a pre-generated list of vehicles supported by your mod
    * The image must be a 276 x 162 JPEG

3. Replace icon
    * `material/ui/accessory/<paintjob>_icon.dds`
    * Must be a 256 x 64 DDS
    * If you want your icon to match the vanilla paintjobs, use the placeholder image as a guide for size & shape

4. Replace vehicle textures
    * `vehicle/truck/upgrade/paintjob/<paintjob>/<vehicle>` and/or `vehicle/trailer_owned/upgrade/paintjob/<paintjob>/<vehicle>`
    * These are the main files of your mod, which determine what your paintjob will actually look like in-game
    * Save each DDS in DXT5 format with mipmaps, if possible
    * Ensure every file's height and width is a power of 2 (e.g. 16, 64, 2048, 4096 etc)
    * You can download template packs [here](https://forum.scssoft.com/viewtopic.php?f=33&t=272386) (ETS 2) and [here](https://forum.scssoft.com/viewtopic.php?f=199&t=288778) (ATS)
