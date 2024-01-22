import React from 'react';
import "./HeroSection.css";

const Hero = ({ name, vol }) => {
    const currentDate = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = currentDate.toLocaleDateString('en-US', options);

    return (
        <section className="hero">
            <div className="header-container">
                <h6 className="header-item left">100% AI Generated</h6>

                <section className="logo desktop-hidden">
                    <h1 className="theDailyByte">The Daily Byte</h1>
                </section>

                <h6 className="header-item right">
                    <a href="https://maximus-powers.com" 
                       target="_blank" 
                       rel="noopener noreferrer" 
                       style={{ color: 'black', textDecoration: 'overline' }}>
                        A Maximus Project
                    </a>
                </h6>
            </div>

            <section className="logo mobile-visible">
                <h1 className="theDailyByte">The Daily Byte</h1>
            </section>

            <section className="dateBar">
                <h5 className="vol">Vol. {vol}</h5>
                <h5 className="date">{formattedDate}</h5>
                <h5 className="price">$0.00</h5>
            </section>
        </section>
    );
};

export default Hero;
