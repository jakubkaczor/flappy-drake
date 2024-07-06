ASSETS_PATH := assets

.PHONY: graphics
graphics: $(ASSETS_PATH)/drake.png $(ASSETS_PATH)/pipe.png

.PHONY: clean
clean:
	@echo Cleaning graphics...
	rm -f $(ASSETS_PATH)/drake.png $(ASSETS_PATH)/pipe.png

$(ASSETS_PATH)/drake.png: $(ASSETS_PATH)/drake.svg 
	inkscape $(ASSETS_PATH)/drake.svg -o $(ASSETS_PATH)/drake.png -h 720

$(ASSETS_PATH)/pipe.png: $(ASSETS_PATH)/pipe.svg
	inkscape $(ASSETS_PATH)/pipe.svg -o $(ASSETS_PATH)/pipe.png -h 2160
