# Bazaraki cli scrapper

This is a simple python scrapper for [the bazaraki](https://www.bazaraki.com) marketplace web site.

## Arguments

- -a, --all-regions - By default, the utility will show ads only from Paphos region. If you wish to see ads from all regions on Cyprus, use this option.
- -f, --known-file - The utility stores previously inspected ads into a flat .txt file. This option shows the path to the file. The file needed to avoid inspecting the same ads each time.
- -i, --in-place - use this option to automatically update intormation in the known-file.
- -g, --goal - use it to choose one of the available filters: rent_house, buy_car or buy_house. Note that filters are hardcoded, if you want some new one just choose needed filters on the website, copy URL and past it into the new filter.

## Example
How I check for a new ads to bye some car:
```bash
./find_rent.py -f already_known_cars_paphos.txt -i -g buy_car
```