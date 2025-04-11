// Items Management JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const itemsList = document.getElementById('items-list');
    const itemForm = document.getElementById('item-form');
    const formTitle = document.getElementById('form-title');
    const itemIdField = document.getElementById('item-id');
    const nameField = document.getElementById('item-name');
    const descriptionField = document.getElementById('item-description');
    const newItemBtn = document.getElementById('new-item-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const deleteModal = document.getElementById('delete-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
    
    // State
    let isEditing = false;
    let items = [];
    let itemToDelete = null;
    
    // Check authentication status and update UI
    const isAuthenticated = !!localStorage.getItem('auth_token');
    updateAuthUI(isAuthenticated);
    
    // Event listeners
    if (newItemBtn) {
        newItemBtn.addEventListener('click', showCreateForm);
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', hideForm);
    }
    
    if (itemForm) {
        itemForm.addEventListener('submit', handleFormSubmit);
    }
    
    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', hideDeleteModal);
    }
    
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', confirmDelete);
    }
    
    // Load items
    loadItems();
    
    // Functions
    function updateAuthUI(isAuthenticated) {
        const authContent = document.querySelectorAll('.auth-content');
        const nonAuthContent = document.querySelectorAll('.non-auth-content');
        
        authContent.forEach(element => {
            element.style.display = isAuthenticated ? 'block' : 'none';
        });
        
        nonAuthContent.forEach(element => {
            element.style.display = isAuthenticated ? 'none' : 'block';
        });
        
        // Update nav links based on auth status
        const loginLink = document.getElementById('login-link');
        const registerLink = document.getElementById('register-link');
        
        if (isAuthenticated && loginLink && registerLink) {
            loginLink.textContent = 'Profile';
            loginLink.href = '/profile';
            
            registerLink.textContent = 'Logout';
            registerLink.href = '#';
            registerLink.id = 'logout-btn';
            
            // Add logout functionality
            document.getElementById('logout-btn').addEventListener('click', function() {
                localStorage.removeItem('auth_token');
                localStorage.removeItem('user_data');
                window.location.reload();
            });
        }
    }
    
    async function loadItems() {
        try {
            itemsList.innerHTML = '<p id="loading-message">Loading items...</p>';
            
            const response = await fetch('/api/items');
            
            if (!response.ok) {
                throw new Error('Failed to load items');
            }
            
            items = await response.json();
            renderItems(items);
        } catch (error) {
            console.error('Error loading items:', error);
            itemsList.innerHTML = `<p class="error-message">Error loading items: ${error.message}</p>`;
        }
    }
    
    function renderItems(items) {
        if (!items || items.length === 0) {
            itemsList.innerHTML = '<p>No items found. Create one!</p>';
            return;
        }
        
        let html = '';
        items.forEach(item => {
            html += `
                <div class="item-card" data-id="${item.id}">
                    <div class="content">
                        <h3>${item.name}</h3>
                        <p>${item.description || 'No description'}</p>
                    </div>
                    ${isAuthenticated ? `
                        <div class="actions">
                            <button class="edit-btn" data-id="${item.id}">Edit</button>
                            <button class="delete-btn" data-id="${item.id}">Delete</button>
                        </div>
                    ` : ''}
                </div>
            `;
        });
        
        itemsList.innerHTML = html;
        
        // Add event listeners to the new buttons
        if (isAuthenticated) {
            document.querySelectorAll('.edit-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const itemId = this.getAttribute('data-id');
                    editItem(itemId);
                });
            });
            
            document.querySelectorAll('.delete-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const itemId = this.getAttribute('data-id');
                    showDeleteModal(itemId);
                });
            });
        }
    }
    
    function showCreateForm() {
        isEditing = false;
        formTitle.textContent = 'Create New Item';
        itemIdField.value = '';
        nameField.value = '';
        descriptionField.value = '';
        itemForm.reset();
        document.getElementById('item-form-container').style.display = 'block';
        nameField.focus();
    }
    
    function editItem(itemId) {
        const item = items.find(i => i.id === itemId);
        if (!item) return;
        
        isEditing = true;
        formTitle.textContent = 'Edit Item';
        itemIdField.value = item.id;
        nameField.value = item.name;
        descriptionField.value = item.description || '';
        
        document.getElementById('item-form-container').style.display = 'block';
        nameField.focus();
    }
    
    function hideForm() {
        document.getElementById('item-form-container').style.display = 'none';
    }
    
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        // Get form data
        const itemId = itemIdField.value;
        const name = nameField.value;
        const description = descriptionField.value;
        
        if (!name) {
            alert('Name is required');
            return;
        }
        
        const token = localStorage.getItem('auth_token');
        if (!token) {
            alert('You must be logged in to perform this action');
            return;
        }
        
        try {
            let response;
            
            if (isEditing) {
                // Update existing item
                response = await fetch(`/api/items/${itemId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        name,
                        description
                    })
                });
            } else {
                // Create new item
                response = await fetch('/api/items', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        name,
                        description
                    })
                });
            }
            
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to save item');
            }
            
            // Refresh items and hide form
            hideForm();
            loadItems();
        } catch (error) {
            console.error('Error saving item:', error);
            alert(`Error saving item: ${error.message}`);
        }
    }
    
    function showDeleteModal(itemId) {
        itemToDelete = itemId;
        deleteModal.style.display = 'flex';
    }
    
    function hideDeleteModal() {
        deleteModal.style.display = 'none';
        itemToDelete = null;
    }
    
    async function confirmDelete() {
        if (!itemToDelete) return;
        
        const token = localStorage.getItem('auth_token');
        if (!token) {
            alert('You must be logged in to delete items');
            hideDeleteModal();
            return;
        }
        
        try {
            const response = await fetch(`/api/items/${itemToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to delete item');
            }
            
            // Hide modal and refresh list
            hideDeleteModal();
            loadItems();
        } catch (error) {
            console.error('Error deleting item:', error);
            alert(`Error deleting item: ${error.message}`);
            hideDeleteModal();
        }
    }
}); 