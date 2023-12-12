import { LineChart, Line, XAxis, YAxis, Tooltip, Label, ResponsiveContainer } from 'recharts';

// Domain calculation
// buffer % should be a float
// uses avg to center chart, then adds the range, buffer_perc is added after that
// this shows volatility in the data instead of stretching it to fill the domain
// range is a % as a float
export const calculateYDomain = (data, field, buffer_perc, range) => {
    if (data && data.length > 0) {
        const values = data.map(item => parseFloat(item[field]));

        // Calculate Mean (Average)
        const mean = values.reduce((acc, val) => acc + val, 0) / values.length;

        // calculate min and max
        const minBuffered = mean * (1 - range);
        const maxBuffered = mean * (1 + range);

        // calc and apply
        const rangeWithBuffer = maxBuffered - minBuffered;
        const bufferAmount = rangeWithBuffer * buffer_perc;
        return [minBuffered - bufferAmount, maxBuffered + bufferAmount];
    }
    return [0, 0];
};


export const calculateColorAndTimespan = (data) => {
    if (!data || data.length === 0) {
        return { color: 'grey', timespan: 'N/A' }; // Handle empty data
    }

    const parsedData = data.map(item => ({
        date: new Date(item.date),
        close_price: parseFloat(item.close_price)
    })).sort((a, b) => a.date - b.date);

    const startDate = parsedData[0].date;
    const endDate = parsedData[parsedData.length - 1].date;

    const diffTime = Math.abs(endDate - startDate) + 1;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    // Define thresholds for days to weeks and weeks to months conversions
    const daysInWeek = 7;
    const weeksInMonth = 4;
    const monthThreshold = daysInWeek * weeksInMonth;

    let timespan;
    if (diffDays >= monthThreshold - 5) {
        const diffMonths = Math.ceil(diffDays / monthThreshold);
        timespan = `${diffMonths} Month${diffMonths > 1 ? 's' : ''}`;
    } else if (diffDays > daysInWeek) {
        const diffWeeks = Math.floor(diffDays / daysInWeek);
        timespan = `${diffWeeks} Week${diffWeeks > 1 ? 's' : ''}`;
    } else {
        timespan = `${diffDays} Day${diffDays > 1 ? 's' : ''}`;
    }

    const startPrice = parsedData[0].close_price;
    const endPrice = parsedData[parsedData.length - 1].close_price;
    const color = endPrice > startPrice ? '#83C19A' : '#CC9595';

    return { color: color, timespan: timespan };
};




// Render chart
export const renderChart = (dataset, yDomain, title, caption, timeframeS, color, fieldToChart, setActivePopup) => {
    return (
        <div className="individual_chart">
            <ResponsiveContainer width="100%" height={100}>
                <h2 onClick={() => setActivePopup(caption)}>{title}</h2>
                <LineChart data={dataset} margin={{ top: 0, right: 10, bottom: 0, left: 10 }}>
                    <Line type="monotone" dataKey={fieldToChart} stroke={color} strokeWidth={5} dot={false} />
                    <XAxis dataKey="date" ticks={[]} tickLine={false} axisLine={false} tick={false}>
                        <Label value={timeframeS} offset={15} position="insideBottom" />
                    </XAxis>
                    <YAxis ticks={[]} tickLine={false} axisLine={false} tick={false} width={0} domain={yDomain} />
                    <Tooltip content={<CustomTooltip />}/>
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}


export const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
        return (
            <div className="custom-tooltip">
                <p className="label">{`${parseFloat(payload[0].value).toFixed(2)}`}</p>
                <p className="intro">{`${label}`}</p>
            </div>
        );
    }

    return null;
};


