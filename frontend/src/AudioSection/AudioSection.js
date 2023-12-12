import React, { useState, useEffect, useRef } from 'react';
import './AudioSection.css';

function AudioPlayer({ base64Audio }) {
    const [audioURL, setAudioURL] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef(null);

    useEffect(() => {
        if (base64Audio) {
            const audioBlob = b64toBlob(base64Audio, 'audio/mpeg');
            const url = URL.createObjectURL(audioBlob);
            setAudioURL(url);

            return () => {
                URL.revokeObjectURL(url);
            };
        }
    }, [base64Audio]);

    const togglePlayPause = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

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

        return new Blob(byteArrays, {type: contentType});
    }

    return (
        <div className="audioPlayerContainer">
            {audioURL && (
                <>
                    <audio ref={audioRef} className="audioElement" src={audioURL} />
                    <button onClick={togglePlayPause} className="audioControlButton">
                        <h2>{isPlaying ? 'Pause' : 'Listen to Your News'}</h2>
                    </button>
                </>
            )}
        </div>
    );
}

export default AudioPlayer;
