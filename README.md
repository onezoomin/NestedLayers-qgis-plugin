# Nested Layers QGIS  Plugin

Roadmap for Features:
 - [x] Update all top level .qlr groups from matching files in the project folder
 - [x] Autosave all recursive .qlr files to matching files in the project folder
 - [ ] Options
 - [ ] Move Backup Save Files to ../Backup
 - [ ] Custom Layer Properties for Modification Date Sensitivity


## Why?

For a Git friendly QGIS project structure with external Layer Definition Files.

## How to use it?

1. Navigate to your qgis python plugin dir, e.g. <br>```cd ~/.qgis2/python/plugins/```
2. Clone this repo:<br> ```git clone https://github.com/onezoomin/NestedLayers-qgis-plugin.git NestedLayers```
3. Start QGIS and enable the plugin (menu Plugins > Manager and Install Plugins...)

Now you should see a "Go!" button in your "Plugins" toolbar (make sure it is enabled in menu Settings > Toolbars > Plugins).

4. Update via git pull
