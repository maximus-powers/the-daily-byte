# Frontend Architecture

## React Web App

### Sections: 

- Hero Section
- Landing Section
- Audio Section
- Stats Section
- News Section

*Mobile first layout, but the column of content breaks into three columns on desktop screens*


### /get_content API Call:
headers: {'Accept': 'application/json'}

API Response:
```    
{
    userID: int,
    firstName:  str,
    vol: int,
    landing: {
        memeTerm: str, 
        image: base64 str, 
        headline: str, 
        summary: str
        },
    audioFile: base64 str,
    statsData: {
        markets: {}, 
        economy: {}
        }, 
    categories: {
        category: [{
            headline: str, 
            summary: str, 
            url: str
            }, ...], 
        ...}
}
```

### Components
#### Hero Section:
Everything above and including the datebar. The component just destructures and maps data from the API response. 

#### Landing Section:
Displays the AI generated image next to it's headline and subheading. Has a base64 to blob function for the image. There are probably better ways to send it, but I did it through the JSON to keep it all on one endpoint.

#### Audio Section:
An audio player for an mp3. It first converts base64 to blob for the mp3, and creates a URL for it, which it passes into the audio player. The audio player toggles between play and pause when you press the button.

#### Statisitics Section:
Multiplie charts showing various economic indicators and their timeframe. Clicking on the titles opens a popup explaining the indicator. The colors of the markets graphs change between green and red depending on the trend. StatsUtils.js contains three functions: calculateYDomain, calculateColorAndTimespan, renderChart. There's also a custom tooltip. Plotted with recharts package, calculateYDomain allows for easy positioning of the window.

#### News Category Sections:
Just mapping data from the api. Click on the headlines for a popup explaining the news story, as well as a link to the source article.








