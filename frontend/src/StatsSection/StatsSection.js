import React, { useState } from 'react';
import { useSwipeable } from 'react-swipeable';
import { calculateColorAndTimespan, renderChart, calculateYDomain } from './StatsUtils.js';
import './StatsSection.css';

const EconSection = ({ markets_data , econ_data }) => {
    // pop up state
    const [activePopup, setActivePopup] = useState(null);
    const [currentChartIndex, setCurrentChartIndex] = useState(0);
    
    // swipeable handlers (has to be at the top level for some reason)
    const handlers = useSwipeable({
        onSwipedLeft: () => setCurrentChartIndex((prevIndex) => (prevIndex + 1) % totalCharts),
        onSwipedRight: () => setCurrentChartIndex((prevIndex) => (prevIndex - 1 + totalCharts) % totalCharts),
        preventDefaultTouchmoveEvent: true,
        trackMouse: true
    });

    // Only proceed if markets_data has keys
    if (!markets_data || !markets_data.fear_greed || !markets_data.sp500 || !markets_data.eth || !markets_data.itb) { return <div>Loading data...</div>; }
    const totalCharts = Object.keys(markets_data).length + Object.keys(econ_data).length;

    // Y DOMAIN CALCULATIONS
    // sort data, should already be sorted but just in case
    const sortedSPY = Array.isArray(markets_data.sp500) ? markets_data.sp500.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    const sortedETH = Array.isArray(markets_data.eth) ? markets_data.eth.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    const sortedITD = Array.isArray(markets_data.itb) ? markets_data.itb.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    const sortedGDP = Array.isArray(econ_data.gdp) ? econ_data.gdp.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    const sortedCPI = Array.isArray(econ_data.cpi) ? econ_data.cpi.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    const sortedFed = Array.isArray(econ_data.fed) ? econ_data.fed.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    const sortedUnemp = Array.isArray(econ_data.unemployment) ? econ_data.unemployment.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    const sortedOil = Array.isArray(econ_data.oil) ? econ_data.oil.sort((a, b) => new Date(a.date) - new Date(b.date)) : [];
    
    // Domain calculations
    const SPYYDomain = calculateYDomain(sortedSPY, 'close_price', 0.05, 0.02); // first float is top/bottom padding, second is threshold from avg to depict
    const ETHYDomain = calculateYDomain(sortedETH, 'close_price', 0.05, 0.1);
    const ITBYDomain = calculateYDomain(sortedITD, 'close_price', 0.1, 0.05);
    const GDPYDomain = calculateYDomain(sortedGDP, 'value', 0.05, 0.05);
    const CPIYDomain = calculateYDomain(sortedCPI, 'value', 0.05, 0.02);
    const FedYDomain = calculateYDomain(sortedFed, 'value', 0.05, 0.1);
    const UnempYDomain = calculateYDomain(sortedUnemp, 'value', 0.1, 0.2);
    const OilYDomain = calculateYDomain(sortedOil, 'value', 0.1, 0.3);

    // COlor and timeframe calculations
    const SPYColorAndTimespan = calculateColorAndTimespan(sortedSPY);
    const ETHColorAndTimespan = calculateColorAndTimespan(sortedETH);
    const ITBColorAndTimespan = calculateColorAndTimespan(sortedITD);
    const GDPColorAndTimespan = calculateColorAndTimespan(sortedGDP);
    const CPIColorAndTimespan = calculateColorAndTimespan(sortedCPI);
    const FedColorAndTimespan = calculateColorAndTimespan(sortedFed);
    const UnempColorAndTimespan = calculateColorAndTimespan(sortedUnemp);
    const OilColorAndTimespan = calculateColorAndTimespan(sortedOil);

    return (
        <div className="econ-section" {...handlers}>
            {/* Popup */}
            {activePopup && (
                <div className="popup">
                    <p>{activePopup}</p>
                    <button onClick={() => setActivePopup(null)}>Close</button>
                </div>
            )}

            <div className="charts-container">
                {renderChart(markets_data.sp500, SPYYDomain, "S&P 500", "The S&P 500, a barometer of U.S. economic health, reflects the stock performance of 500 leading American companies.", SPYColorAndTimespan['timespan'], SPYColorAndTimespan['color'], 'close_price', setActivePopup)}
                {renderChart(markets_data.eth, ETHYDomain, "Crypto", "Ethereum (ETH), the leading blockchain company, tracks the broader market, and isn't as convoluted with day-traders as Bitcoin.", ETHColorAndTimespan['timespan'], ETHColorAndTimespan['color'], 'close_price', setActivePopup)}
                {renderChart(markets_data.itb, ITBYDomain, "Real Estate", "The iShares U.S. Home Construction ETF (ITB) chart visualizes the performance of the U.S. housing construction sector, reflecting trends in residential building and real estate market health.", ITBColorAndTimespan['timespan'], ITBColorAndTimespan['color'], 'close_price', setActivePopup)}
                {renderChart(econ_data.gdp, GDPYDomain, "GDP", "The Gross Domestic Product (GDP) chart illustrates the total economic output of a country, indicating its economic health and growth trends.", GDPColorAndTimespan['timespan'], "#7990AD", 'value', setActivePopup)}
                {renderChart(econ_data.cpi, CPIYDomain, "Inflation", "The Consumer Price Index (CPI) chart tracks changes in the cost of goods and services, providing a measure of inflation and purchasing power over time.", CPIColorAndTimespan['timespan'], "#7990AD", 'value', setActivePopup)}
                {renderChart(econ_data.fed, FedYDomain, "Fed Rate", "Rising Federal Reserve rates typically signal efforts to curb inflation and cool the economy, while decreasing rates suggest attempts to stimulate economic growth and increase borrowing and spending.", FedColorAndTimespan['timespan'], "#7990AD", 'value', setActivePopup)}
                {renderChart(econ_data.unemployment, UnempYDomain, "Unemploy.", "The Unemployment chart tracks the percentage of the labor force that is jobless and actively seeking work, serving as a key indicator of labor market health and economic activity.", UnempColorAndTimespan['timespan'], "#7990AD", 'value', setActivePopup)}
                {renderChart(econ_data.oil, OilYDomain, "Crude Oil", "The Crude Oil chart shows the price fluctuations of crude oil, reflecting global supply and demand dynamics, geopolitical factors, and economic trends.", OilColorAndTimespan['timespan'], "#7990AD", 'value', setActivePopup)}
            </div>
        </div>
    );
}



export default EconSection;
