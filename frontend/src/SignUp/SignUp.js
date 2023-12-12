import React, { useState } from 'react';
import { useAuth } from '../AuthContext/AuthContext.js';
import { Link } from 'react-router-dom';

function SignUpComponent() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [error, setError] = useState('');  // Add an error state

    const allCategories = ['General', 'Business', 'Entertainment', 'Health', 'Science', 'Polotics', 'Sports', 'Technology']; 

    const isValidEmail = (email) => {
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return emailRegex.test(email);
    }

    const handleCategorySelection = (category) => {
        if (!selectedCategories.includes(category)) {
            setSelectedCategories([...selectedCategories, category]);
        } else {
            setSelectedCategories(selectedCategories.filter(item => item !== category));
        }
    };

    const { login } = useAuth();

    const handleSignUp = async () => {
        // Validation
        if (!email || !password || !firstName || selectedCategories.length === 0) {
            setError("Please make sure you fill out all the fields");
            return;
        }

        if (!isValidEmail(email)) {
            setError("My friend... please use a real email address");
            return;
        }

        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: {
                'Email': email,
                'Password': password,
                'fName': firstName,
                'Categories': selectedCategories.join(',')
            }
        });
        const data = await response.json();
        if (data.success) {
            login(email);
        }
        setError('');  // Reset the error message
        alert(data.success);
    }
    return (
        <div>
            <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <input value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="First Name" />

            <div>
                {allCategories.map(category => (
                    <label key={category}>
                        <input type="checkbox" checked={selectedCategories.includes(category)} onChange={() => handleCategorySelection(category)} />
                        {category}
                    </label>
                ))}
            </div>

            <div>
                <strong>Order of Categories to Be Displayed:</strong>
                <ol>
                    {selectedCategories.map(category => (
                        <li key={category}>{category}</li>
                    ))}
                </ol>
            </div>
            {/* Display error message */}
            {error && <p style={{color: 'red'}}>{error}</p>}

            <button onClick={handleSignUp}>Sign Up</button>

            <div>
                <Link to="/login">Already have an accound? Login</Link>
            </div>
        </div>
    );
}

export default SignUpComponent;
