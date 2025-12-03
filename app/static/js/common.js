/**
 * Common JavaScript Functions
 * Used across all pages
 */

// Check authentication on page load
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token) {
        window.location.href = '/';
        return false;
    }

    // Display username
    if (user.full_name) {
        $('#username-display').text(user.full_name);
    }

    return true;
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}

// Show toast notification
function showToast(title, message, type = 'info') {
    const toast = $('#toast');
    const toastTitle = $('#toast-title');
    const toastBody = $('#toast-body');

    // Set colors based on type
    toast.removeClass('bg-success bg-danger bg-warning bg-info');
    if (type === 'success') {
        toast.addClass('bg-success text-white');
    } else if (type === 'error') {
        toast.addClass('bg-danger text-white');
    } else if (type === 'warning') {
        toast.addClass('bg-warning');
    } else {
        toast.addClass('bg-info text-white');
    }

    toastTitle.text(title);
    toastBody.text(message);

    const bsToast = new bootstrap.Toast(toast[0]);
    bsToast.show();
}

// Format number with commas
function formatNumber(num) {
    return parseFloat(num || 0).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Format date/time
function formatDateTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format date only
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Confirm delete action
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// AJAX Error Handler
function handleAjaxError(xhr, message = 'An error occurred') {
    const response = xhr.responseJSON;
    const errorMsg = response?.error || message;
    showToast('Error', errorMsg, 'error');
    console.error('Ajax Error:', xhr);
}

// Get auth headers for AJAX requests
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    };
}

// Highlight active nav link
$(document).ready(function() {
    const currentPath = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        const href = $(this).attr('href');
        if (href === currentPath) {
            $(this).addClass('active');
        }
    });
});

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in other files
window.checkAuth = checkAuth;
window.logout = logout;
window.showToast = showToast;
window.formatNumber = formatNumber;
window.formatDateTime = formatDateTime;
window.formatDate = formatDate;
window.confirmDelete = confirmDelete;
window.handleAjaxError = handleAjaxError;
window.getAuthHeaders = getAuthHeaders;
window.debounce = debounce;
