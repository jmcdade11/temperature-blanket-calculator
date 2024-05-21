# Overview

## What the heck is a temperature blanket?

A temperature blanket is a blanket where each row or section represents each day of a year using different yarn colours for different conditions. For more details, see [here](https://temperature-blanket.com/blog/what-is-a-temperature-blanket)

## What is this project?

My wife is a big fan of making temperature blankets, but she would screenshot her weather app each day and have to sort through historical screenshots when she wanted to do a stretch of days on the blanket. This project accomplishes a couple of things:

- Query the historical weather API at [worldweatheronline](https://www.worldweatheronline.com/) and cache the results from January 1st of the current year until yesterday inclusive
- Cross-reference a 'colour index' CSV file that maps colours to temperature ranges
- Generates a report for each month that shows the:
  - Daily high
  - Daily low
  - Selected temperature for the blanket (absolute highest wins)
  - Daily colour
  - A monthly total of each colour, to assist with yarn purchases
- Generated report will be generated here under 'temperature_blanket.html'

## Getting started

You will need a couple of things:

- API key for [worldweatheronline](https://www.worldweatheronline.com/)
  - Saved as environment variable `WEATHER_BLANKET_API_KEY`
- (Optional) path to colour index CSV file
  - Defaults to 'colour_index.csv'
  - Feel free to use the provided 'colour_index.csv' for the format of the CSV file you need to follow

## Potential future enhancements

- Right now the location for the weather API uses the public IP of the running machine, but a location string could be passed in instead
- Customizable year input (uses the current year now)
