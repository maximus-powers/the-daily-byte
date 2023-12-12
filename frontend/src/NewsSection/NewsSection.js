import React, { useState } from 'react';
import './NewsSection.css';

function NewsSection({ category, articles }) {
    const [showSummaryIndex, setShowSummaryIndex] = useState(null); // This will store the index of the article whose summary is visible

    return (
        <div className="newsSectionContainer">
            <h4>{category}</h4>
                {articles.map(({ headline, summary, url }, index) => (
                    <div key={index}>
                        <h3 onClick={() => setShowSummaryIndex(index === showSummaryIndex ? null : index)}>
                            {headline}
                        </h3>
                        {index === showSummaryIndex && (
                            <div className="summaryPopup">
                                {summary}
                                <button onClick={() => window.open(url, '_blank')}>Source</button>
                                <button onClick={() => setShowSummaryIndex(null)}>Close</button>
                            </div>
                        )}
                    </div>
                ))}
        </div>
    );
}

export default NewsSection;
