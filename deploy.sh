# Copy main.py and lib to an automounted device from adafruit

echo "Deployment began: " + `date`

cp ./main.py /Volumes/CIRCUITPY/
cp -r ./lib /Volumes/CIRCUITPY/
