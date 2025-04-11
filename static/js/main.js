// Main JavaScript file for FastAPI Web App

document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const fetchButton = document.getElementById('fetch-data');
    const itemsContainer = document.getElementById('items-container');

    // Function to fetch items from API
    async function fetchItems() {
        try {
            itemsContainer.innerHTML = '<p>Loading items...</p>';
            
            // Use authenticatedFetch if available, otherwise fall back to regular fetch
            const fetchFunction = window.authenticatedFetch || fetch;
            const response = await fetchFunction('/api/items');
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const items = await response.json();
            displayItems(items);
        } catch (error) {
            console.error('Error fetching items:', error);
            itemsContainer.innerHTML = `<p class="error">Error loading items: ${error.message}</p>`;
        }
    }

    // Function to display items in the UI
    function displayItems(items) {
        if (!items || items.length === 0) {
            itemsContainer.innerHTML = '<p>No items found.</p>';
            return;
        }

        // Check if user is authenticated to enable edit/delete actions
        const isAuthenticated = !!localStorage.getItem('auth_token');

        let html = '';
        items.forEach(item => {
            html += `
                <div class="item-card" data-id="${item.id}">
                    <h3>${item.name}</h3>
                    <p>${item.description || 'No description available'}</p>
                    <small>ID: ${item.id}</small>
                    ${isAuthenticated ? `
                        <div class="item-actions">
                            <button class="edit-item-btn">Edit</button>
                            <button class="delete-item-btn">Delete</button>
                        </div>
                    ` : ''}
                </div>
            `;
        });

        itemsContainer.innerHTML = html;

        // Add event listeners for edit/delete buttons if authenticated
        if (isAuthenticated) {
            document.querySelectorAll('.edit-item-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const itemCard = this.closest('.item-card');
                    const itemId = itemCard.dataset.id;
                    editItem(itemId);
                });
            });

            document.querySelectorAll('.delete-item-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const itemCard = this.closest('.item-card');
                    const itemId = itemCard.dataset.id;
                    deleteItem(itemId);
                });
            });
        }
    }

    // Function to edit an item (Placeholder - would show a form in a real app)
    function editItem(itemId) {
        alert(`Edit item functionality would appear here for item ${itemId}`);
        // In a real application, you would show a form and use PUT request to update
    }

    // Function to delete an item
    async function deleteItem(itemId) {
        if (!confirm('Are you sure you want to delete this item?')) {
            return;
        }

        try {
            const token = localStorage.getItem('auth_token');
            if (!token) {
                alert('You must be logged in to delete items');
                return;
            }

            const response = await fetch(`/api/items/${itemId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to delete item');
            }

            // Refresh items list after successful delete
            fetchItems();
        } catch (error) {
            console.error('Error deleting item:', error);
            alert(`Error deleting item: ${error.message}`);
        }
    }

    // Event listeners
    if (fetchButton) {
        fetchButton.addEventListener('click', fetchItems);
    }

    // Auto-load items on page load if container exists
    if (itemsContainer) {
        fetchItems();
    }
}); 