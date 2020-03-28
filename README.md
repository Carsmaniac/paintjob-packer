# Paintjob Packer
Paintjob Packer is a lightweight mod making tool for Euro Truck Simulator 2 and American Truck Simulator. It allows you to generate simple paintjob mods, with a focus on mods that support multiple vehicles.

## Features

* Support for player-owned trailers, including those from DLCs
* Support for trucks using the newer accessory-based paintjob system, like the Scania S and MAN TGX Euro 6
* Support for as many vehicles as you like in a single mod
* Built-in support for 40 modded trucks, full list [here](https://github.com/Carsmaniac/paintjob-packer/blob/master/library/mod%20links.md)
* Support for separate paintjobs for each cabin of a truck, in case a single texture doesn't work for all of them

## Making a mod

Paintjob Packer doesn't make a completed mod when you click the *Generate mod* button. Instead, it makes what I call "custom example mods", giving you all the files you need for your mod, but with placeholders standing in for every image/texture. You then go through and replace all the placeholder images with your own to complete the mod. Since you usually have to test and tweak a paintjob many times before it's ready, this setup means you only have to run the program once.

### Required programs

* An **image manipulator** that can save as DDS. I use Photoshop with the [DDS plugin](https://fnordware.blogspot.com/2014/09/dds-plug-in-for-after-effects-and.html), but you can also use [GIMP](https://www.gimp.org/downloads/) (free) with its [DDS plugin](https://code.google.com/archive/p/gimp-dds/downloads)
* If you're using the cabin unifier, a **hex editor**. I use [HxD](https://mh-nexus.de/en/hxd/) on Windows and [Hex Fiend](https://ridiculousfish.com/hexfiend/) on macOS

1. Generate base files using Paintjob Packer
    * Paintjob Packer is made for paintjob packs, but you can also make a single paintjob
    * Choose between separate paintjobs for each cabin, or a single combined paintjob per vehicle
      * Combined paintjobs cut down on mod size by only needing one file per truck, but your design might not work perfectly across all the cabin sizes
  	  * Separate paintjobs let you tweak your design for each cab size, but your mod will be bigger due to multiple (usually 3) files per truck
  	  * The optional cabin unifier system gives you the best of both worlds, but is more complex to use (only available when using separate paintjobs)
    * Internal name must consist of only lowercase letters, numbers and underscores. It must be 12 characters or fewer (10 if using separate paintjobs) and **unique** - two different mods that use the same internal name are incompatible with each other

2. Replace mod manager files
    * `mod_manager_description.txt` and `mod_manager_image.jpg`
    * The description already contains a pre-generated list of vehicles supported by your mod
    * The image must be a 276 x 162 JPEG

3. Replace icon
    * `material/ui/accessory/<internal name>_icon.dds`
    * Must be a 256 x 64 DDS
    * If you want your icon to match the vanilla paintjobs, use the placeholder image as a guide for size & shape

4. Make main vehicle files
    * `vehicle/truck/upgrade/paintjob/<internal name>/<vehicle>` (each "cabin" DDS) and/or `vehicle/trailer_owned/upgrade/paintjob/<internal name>/<vehicle>` (each "body" DDS)
    * Using templates is recommended, I have [a pack you can download](https://forum.scssoft.com/viewtopic.php?f=33&t=272386)
    * Save each DDS as DXT 5 *with mipmaps*
    * For consistency's sake, Cabin A is always the biggest cabin size, then Cabin B is smaller, then Cabin C is the smallest. If the 8x4 chassis uses a separate cabin, it's called Cabin 8
    * Some trucks have fewer than 3 cabins, and some mods have more than 3
    * You'll need to replace every cabin DDS there

5. Make accessory files
    * Every DDS not replaced in the last step
    * Only necessary for trailers and some trucks
    * Not all accessories need templates, if you just want to change the colour of a part simply re-colour the placeholder file that's already there

### If using the cabin unifier system

6. Make additional DDS files if needed
    * Each truck will only generate with `cabin_a.dds` by default, if you need additional sizes you'll need to make additional DDS files
    * You only need to make additional files if your design doesn't work on a certain-sized cabin, most paintjobs will work fine with just the one DDS
    * Make sure additional DDS file names match an existing TOBJ, e.g. `cabin_b.dds` is okay, but `cabin_small.dds` is not

7. Edit existing TOBJ files to point to your new DDS
    * Open the TOBJ using a hex editor and edit only a single letter near the end, e.g. turning `cabin_a` into `cabin_b`
    * Multiple TOBJ files can point to the same DDS, so you could have one DDS for cabins A & 8, and a second for cabins B & C, for example

8. Run the cabin unifier
    * If any files are missing or named incorrectly, the unifier will let you know
    * Don't edit `unifier.ini`, it might cause the unifier to work incorrectly
    * The unifier looks at your TOBJ files to see which cabins you need and which you don't, then edits some files in the def folder
    * You can only unify once, so delete `Cabin Unifier.exe` (or `unifier.py`) and `unifier.ini` afterwards
