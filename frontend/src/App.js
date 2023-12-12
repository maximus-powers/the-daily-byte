import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import NewsSection from './NewsSection/NewsSection';
import LandingSection from './LandingSection/LandingSection';
import Hero from './HeroSection/HeroSection';
import SignUp from './SignUp/SignUp';
import Login from './Login/Login';
import AudioPlayer from './AudioSection/AudioSection';
import StatsSection from './StatsSection/StatsSection.js'
import { useAuth } from './AuthContext/AuthContext.js';

function App() {
    const [firstName, setFirstName] = useState("");
    const [landing, setLanding] = useState(null);
    const [categories, setCategories] = useState({});
    const [vol, setVol] = useState(0); 
    const [error, setError] = useState(null);
    const [audioFileBase64, setAudioFileBase64] = useState(null);
    const [marketsData, setMarketsData] = useState(null);
    const [econData, setEconData] = useState(null);

    const { isAuthenticated, userEmail } = useAuth();

    useEffect(() => {
        const emailToSend = isAuthenticated ? userEmail : 'powersms@clarkson.edu';

        fetch('http://tdb-api.maximus-powers.com/get_content', {
            headers: {
                'Accept': 'application/json',
                'Email': emailToSend
            }
        })
        .then(resp => {
            if (!resp.ok) {
                throw new Error('Failed to fetch data from API.');
            }
            return resp.json();
        })
        .then(dataResponse => {
            console.log(dataResponse);
            const { firstName, vol, landing, audioFile, statsData, categories } = dataResponse;

            setFirstName(firstName);
            setLanding(landing);
            setCategories(categories);
            setVol(vol);
            setAudioFileBase64(audioFile);
            setMarketsData(statsData.markets);
            setEconData(statsData.economy);
        })
        .catch(err => {
            setError(err.message);
        });
    }, [isAuthenticated, userEmail]);

    console.log('Markets Data:', marketsData);


    // for when we distribute them on layout
    let categoriesEntries = [];
    if (categories) {
        categoriesEntries = Object.entries(categories);
    }

    // etc
    if (error) {return <div>Error: {error}</div>;}
    if (!categories) {return <div>Loading...</div>;}

    return (
        <Router>
            <div className="App">
                <Hero name={isAuthenticated ? firstName : null} vol={vol} />
    
                <Routes>
                    <Route path="/signup" element={<SignUp />} />
                    <Route path="/login" element={<Login />} />
    
                    <Route path="/" element={
                        <div className="container">
                            <div className="row">
                                {/* Leftmost Column */}
                                <div className="col-md-4">
                                    <LandingSection landingData={landing} />
                                    <AudioPlayer base64Audio={audioFileBase64} />
                                    <StatsSection markets_data={marketsData} econ_data={econData} />
                                    {categoriesEntries.length > 0 &&
                                        <NewsSection key={categoriesEntries[0][0]} category={categoriesEntries[0][0]} articles={categoriesEntries[0][1]} />
                                    }
                                </div>
    
                                {/* Middle Column */}
                                <div className="col-md-4">
                                    {categoriesEntries.slice(1, 4).map(([category, articles]) => (
                                        <NewsSection key={category} category={category} articles={articles} />
                                    ))}
                                </div>
    
                                {/* Rightmost Column */}
                                <div className="col-md-4">
                                    {categoriesEntries.slice(4).map(([category, articles]) => (
                                        <NewsSection key={category} category={category} articles={articles} />
                                    ))}
                                </div>
                            </div>
                        </div>
                    } />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
