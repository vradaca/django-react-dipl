// Confirm deletion of expense
function confirmDeleteExpense(expenseId) {
    const deleteForm = document.getElementById('deleteExpenseForm');
    deleteForm.action = `/expenses/delete-expense/${expenseId}`;
    openModal('deleteExpenseModal');
}

function confirmDeleteIncome(incomeId) {
    const deleteForm = document.getElementById('deleteIncomeForm');
    deleteForm.action = `/income/delete-income/${incomeId}`;
    openModal('deleteExpenseModal');
}

// Confirm deletion of user account
function confirmDeleteAccount() {
    return confirm("Are you sure you want to delete your account? This action cannot be undone.");
}

// Open modal
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}
