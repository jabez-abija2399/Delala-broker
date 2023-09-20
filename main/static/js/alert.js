// // Function to confirm deletion and show custom alert
// function confirmDelete(listingId) {
//     const result = confirm("Are you sure you want to delete this listing?");
    
//     if (result) {
//         // Form submission for deletion
//         const deleteForm = document.getElementById('delete-form-' + listingId);
//         if (deleteForm) {
//             deleteForm.submit();
//         }
//     } else {
//         // Show a custom alert for cancellation
//         showCustomAlert("Deletion canceled.");
//     }
//     return false;
// }

// Function to confirm update and show custom alert
function confirmUpdate() {
    const result = confirm("Are you sure you want to update this listing?");
    
    if (result) {
        // Proceed with the update action
        return true;
    } else {
        // Show a custom alert for cancellation
        showCustomAlert("Update canceled.");
        return false;
    }
}


function closeCustomAlert() {
    var customAlertContainer = document.getElementById("customAlertContainer");
    if (customAlertContainer) {
        customAlertContainer.style.display = "none";
    }
}


function showCustomAlert(message, type) {
    var customAlertContainer = document.getElementById("customAlertContainer");
    var customAlertMessage = document.getElementById("customAlertMessage");



        // Customize the alert box based on the type (e.g., 'success', 'error')
        if (type === 'success') {
            customAlertContainer.className = 'custom-alert-container success';
        } else if (type === 'error') {
            customAlertContainer.className = 'custom-alert-container error';
        }

        // Display the custom alert
        customAlertContainer.style.display = "block";

        // Automatically hide the alert after a few seconds (adjust as needed)
        setTimeout(function () {
            customAlertContainer.style.display = "none";
        }, 5000); // 5000 milliseconds (5 seconds)
    
}


var flashMessage = "{{ flash_message }}"; // Replace with the actual variable name
var flashMessageType = "{{ flash_message_type }}"; // Replace with the actual variable name

if (flashMessage) {
    showCustomAlert(flashMessage, flashMessageType);
}


