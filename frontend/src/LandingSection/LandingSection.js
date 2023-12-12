import React, { useEffect, useState } from 'react';
import './LandingSection.css'; // Make sure to import your CSS file

function LandingComponent({ landingData }) {
    const [imageURL, setImageURL] = useState(null);

    useEffect(() => {
        // Check if landingData exists and has an image property
        if (landingData && landingData.image) {
            try {
                const imageBlob = b64toBlob(landingData.image, 'image/png');
                const url = URL.createObjectURL(imageBlob);
                setImageURL(url);
            } catch (error) {
                console.error('Error converting base64 to image:', error);
            }
        }
    }, [landingData]);

    function b64toBlob(b64Data, contentType = '', sliceSize = 512) {
        const byteCharacters = atob(b64Data);
        const byteArrays = [];

        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize);

            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }

        return new Blob(byteArrays, { type: contentType });
    }

    return (
        <div className="landing">
            {imageURL && (
                <div className="imageContainer">
                    <img src={imageURL} alt={landingData.memeTerm || 'Landing Image'} />
                </div>
            )}

            <div className="landingTextContainer">
                {landingData && landingData.headline && (
                    <h2 className="landingHeadline">{landingData.headline}</h2>
                )}
                {landingData && landingData.summary && (
                    <h4 className="landingText">{landingData.summary}</h4>
                )}
            </div>
        </div>
    );
}

export default LandingComponent;
