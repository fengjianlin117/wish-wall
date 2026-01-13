// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';
let authToken = localStorage.getItem('authToken');

// API Helper Functions
async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            authToken = null;
            localStorage.removeItem('authToken');
            showNotification('Session expired, please login again', 'error');
            showLoginForm();
            return null;
        }

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(error.message, 'error');
        return null;
    }
}

// Authentication Functions
async function register() {
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;

    if (!username || !email || !password || !confirmPassword) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }

    const response = await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
            username,
            email,
            password,
            display_name: username,
        }),
    });

    if (response) {
        authToken = response.access_token;
        localStorage.setItem('authToken', authToken);
        showNotification('Registration successful!', 'success');
        showMainApp();
        loadWishes();
    }
}

async function login() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    });

    if (response) {
        authToken = response.access_token;
        localStorage.setItem('authToken', authToken);
        showNotification('Login successful!', 'success');
        showMainApp();
        loadWishes();
    }
}

function logout() {
    authToken = null;
    localStorage.removeItem('authToken');
    showNotification('Logged out successfully', 'success');
    showLoginForm();
}

// Wish Functions
async function loadWishes() {
    const response = await apiRequest('/wishes?page=1&per_page=20');
    
    if (response) {
        displayWishes(response.wishes);
    }
}

function displayWishes(wishes) {
    const wishesList = document.getElementById('wishesList');
    
    if (!wishes || wishes.length === 0) {
        wishesList.innerHTML = '<p class="no-wishes">No wishes yet. Be the first to share!</p>';
        return;
    }

    wishesList.innerHTML = wishes.map(wish => `
        <div class="wish-card">
            <div class="wish-header">
                <h3>${escapeHtml(wish.title)}</h3>
                <span class="wish-category">${wish.category}</span>
            </div>
            <p class="wish-content">${escapeHtml(wish.content)}</p>
            <div class="wish-author">
                <strong>${wish.author.display_name || wish.author.username}</strong>
            </div>
            <div class="wish-stats">
                <span class="stat">❤️ ${wish.likes_count}</span>
                <span class="stat">💬 ${wish.comments_count}</span>
            </div>
            <div class="wish-actions">
                <button onclick="toggleLike(${wish.id})" class="action-btn">Like</button>
                <button onclick="showCommentForm(${wish.id})" class="action-btn">Comment</button>
                <button onclick="viewWishDetail(${wish.id})" class="action-btn">View</button>
            </div>
        </div>
    `).join('');
}

async function submitWish() {
    const title = document.getElementById('wishTitle').value;
    const content = document.getElementById('wishContent').value;
    const category = document.getElementById('wishCategory').value;

    if (!title || !content) {
        showNotification('Please fill in title and content', 'error');
        return;
    }

    if (!authToken) {
        showNotification('Please login first', 'error');
        return;
    }

    const response = await apiRequest('/wishes', {
        method: 'POST',
        body: JSON.stringify({
            title,
            content,
            category,
            is_public: true,
        }),
    });

    if (response) {
        showNotification('Wish posted successfully!', 'success');
        document.getElementById('wishTitle').value = '';
        document.getElementById('wishContent').value = '';
        loadWishes();
    }
}

async function toggleLike(wishId) {
    if (!authToken) {
        showNotification('Please login first', 'error');
        return;
    }

    const response = await apiRequest(`/wishes/${wishId}/like`, {
        method: 'POST',
    });

    if (response) {
        showNotification('Wish liked!', 'success');
        loadWishes();
    }
}

async function viewWishDetail(wishId) {
    const response = await apiRequest(`/wishes/${wishId}`);
    
    if (response) {
        displayWishDetail(response);
    }
}

function displayWishDetail(wish) {
    const detail = `
        <div class="wish-detail">
            <button onclick="goBack()" class="back-btn">← Back</button>
            <h2>${escapeHtml(wish.title)}</h2>
            <div class="detail-author">By ${wish.author.display_name || wish.author.username}</div>
            <p class="detail-content">${escapeHtml(wish.content)}</p>
            <div class="detail-stats">
                <span>❤️ ${wish.likes_count} likes</span>
                <span>💬 ${wish.comments_count} comments</span>
            </div>
            <div class="comments-section">
                <h3>Comments</h3>
                ${wish.comments ? wish.comments.map(comment => `
                    <div class="comment">
                        <strong>${comment.author.display_name}</strong>
                        <p>${escapeHtml(comment.content)}</p>
                    </div>
                `).join('') : ''}
            </div>
        </div>
    `;
    
    document.getElementById('wishesList').innerHTML = detail;
}

function goBack() {
    loadWishes();
}

function showCommentForm(wishId) {
    if (!authToken) {
        showNotification('Please login first', 'error');
        return;
    }
    alert('Comment feature coming soon');
}

// UI Helper Functions
function showLoginForm() {
    const mainContent = document.querySelector('main');
    mainContent.innerHTML = `
        <div class="auth-container">
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('login')">Login</button>
                <button class="tab-btn" onclick="switchTab('register')">Register</button>
            </div>
            
            <div id="login" class="tab-content active">
                <input type="text" id="loginUsername" placeholder="Username" class="input-field">
                <input type="password" id="loginPassword" placeholder="Password" class="input-field">
                <button onclick="login()" class="submit-btn">Login</button>
            </div>
            
            <div id="register" class="tab-content">
                <input type="text" id="regUsername" placeholder="Username" class="input-field">
                <input type="email" id="regEmail" placeholder="Email" class="input-field">
                <input type="password" id="regPassword" placeholder="Password" class="input-field">
                <input type="password" id="regConfirmPassword" placeholder="Confirm Password" class="input-field">
                <button onclick="register()" class="submit-btn">Register</button>
            </div>
        </div>
    `;
}

function showMainApp() {
    const mainContent = document.querySelector('main');
    mainContent.innerHTML = `
        <div class="app-header-nav">
            <button onclick="logout()" class="logout-btn">Logout</button>
        </div>
        
        <section class="wish-input-section">
            <h2>Share Your Wish</h2>
            <input type="text" id="wishTitle" placeholder="Wish Title" class="input-field">
            <select id="wishCategory" class="input-field">
                <option value="general">General</option>
                <option value="education">Education</option>
                <option value="career">Career</option>
                <option value="health">Health</option>
                <option value="travel">Travel</option>
                <option value="hobby">Hobby</option>
            </select>
            <textarea id="wishContent" placeholder="Describe your wish..." class="input-field" rows="4"></textarea>
            <button onclick="submitWish()" class="submit-btn">Post Wish</button>
        </section>
        
        <section class="wishes-display">
            <h2>Wishes</h2>
            <div id="wishesList" class="wishes-list"></div>
        </section>
    `;
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        showMainApp();
        loadWishes();
    } else {
        showLoginForm();
    }
});