// Authentication JavaScript for FastAPI Web App

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    
    // Update UI based on authentication status
    updateAuthUI(!!token);
    
    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const messageElement = document.getElementById('login-message');
            
            try {
                messageElement.textContent = 'Logging in...';
                messageElement.className = 'message';
                
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Login failed');
                }
                
                // Store token and user info in localStorage
                localStorage.setItem('auth_token', data.access_token);
                
                // Get user info
                const userResponse = await fetch('/auth/users/me', {
                    headers: {
                        'Authorization': `Bearer ${data.access_token}`
                    }
                });
                
                if (userResponse.ok) {
                    const userData = await userResponse.json();
                    localStorage.setItem('user_data', JSON.stringify(userData));
                }
                
                messageElement.textContent = 'Login successful! Redirecting...';
                messageElement.className = 'message success-message';
                
                // Redirect to home page after successful login
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
                
            } catch (error) {
                messageElement.textContent = error.message;
                messageElement.className = 'message error-message';
                console.error('Login error:', error);
            }
        });
    }
    
    // Handle registration form submission
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const fullName = document.getElementById('full_name').value;
            const messageElement = document.getElementById('register-message');
            
            try {
                messageElement.textContent = 'Creating account...';
                messageElement.className = 'message';
                
                const response = await fetch('/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        username, 
                        email, 
                        password,
                        full_name: fullName || null
                    })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Registration failed');
                }
                
                messageElement.textContent = 'Registration successful! Redirecting to login...';
                messageElement.className = 'message success-message';
                
                // Redirect to login page after successful registration
                setTimeout(() => {
                    window.location.href = '/login';
                }, 1500);
                
            } catch (error) {
                messageElement.textContent = error.message;
                messageElement.className = 'message error-message';
                console.error('Registration error:', error);
            }
        });
    }
    
    // Handle logout button
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            // Clear authentication data
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_data');
            
            // Redirect to login page
            window.location.href = '/login';
        });
    }
});

// Update UI based on authentication status
function updateAuthUI(isAuthenticated) {
    // Get navigation links
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    
    // Find login and register links
    const loginLink = Array.from(navLinks.querySelectorAll('a')).find(link => link.getAttribute('href') === '/login');
    const registerLink = Array.from(navLinks.querySelectorAll('a')).find(link => link.getAttribute('href') === '/register');
    
    if (isAuthenticated) {
        // User is logged in
        if (loginLink) {
            const parentLi = loginLink.parentElement;
            parentLi.innerHTML = '<a href="/profile">Profile</a>';
        }
        
        if (registerLink) {
            const parentLi = registerLink.parentElement;
            parentLi.innerHTML = '<a href="#" id="logout-btn">Logout</a>';
            
            // Add event listener to the newly created logout button
            const logoutBtn = document.getElementById('logout-btn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', function() {
                    localStorage.removeItem('auth_token');
                    localStorage.removeItem('user_data');
                    window.location.href = '/login';
                });
            }
        }
        
        // Update authenticated content
        const authContent = document.querySelectorAll('.auth-content');
        authContent.forEach(element => {
            element.style.display = 'block';
        });
        
        // Update non-authenticated content
        const nonAuthContent = document.querySelectorAll('.non-auth-content');
        nonAuthContent.forEach(element => {
            element.style.display = 'none';
        });
    } else {
        // User is not logged in
        // Update authenticated content
        const authContent = document.querySelectorAll('.auth-content');
        authContent.forEach(element => {
            element.style.display = 'none';
        });
        
        // Update non-authenticated content
        const nonAuthContent = document.querySelectorAll('.non-auth-content');
        nonAuthContent.forEach(element => {
            element.style.display = 'block';
        });
    }
}

// Get the current user data from localStorage
function getCurrentUser() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

// Check if the user is authenticated
function isAuthenticated() {
    return !!localStorage.getItem('auth_token');
}

// Add authorization header to fetch requests
function authenticatedFetch(url, options = {}) {
    const token = localStorage.getItem('auth_token');
    if (!token) {
        return fetch(url, options);
    }
    
    // Create headers with authorization
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    
    return fetch(url, {
        ...options,
        headers
    });
} 