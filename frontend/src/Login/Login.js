import React, { useState } from 'react';
import { useAuth } from '../AuthContext/AuthContext.js'; // Ensure the path is correct

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const { login } = useAuth(); // Destructure the login function from the context

    const handleLogin = async () => {
        const response = await fetch('http://127.0.0.1:5000/auth_user', {
            method: 'POST',
            headers: {
                'Email': email,
                'Password': password
            }
        });
        const data = await response.json();

        if (response.status === 200) {
            login(email); // Invoke the login function after successful authentication
            alert(data.success); 
        } else {
            alert(data.error); 
        }
    }

    return (
        <div>
            <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <button onClick={handleLogin}>Login</button>
        </div>
    );
}

export default Login;
