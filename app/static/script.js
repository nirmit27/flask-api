/* Flash Message Animation */

// Show flash messages with animation
document.addEventListener("DOMContentLoaded", function () {
  const messages = document.querySelectorAll(".message");

  messages.forEach((message, index) => {
    setTimeout(() => {
      message.classList.add("show");
    }, index * 500); // Staggered appearance

    // Auto-hide each message after 5 seconds
    setTimeout(() => {
      closeMessage(message.id);
    }, 5000 + index * 500);
  });
});

// Close message function
function closeMessage(messageId) {
  const message = document.getElementById(messageId);

  if (message) {
    message.classList.remove("show");
    setTimeout(() => {
      message.remove();
    }, 300); // Delay to allow animation to complete
  }
}

/* Deletion Operation */

function deleteTodo(todoId) {
  fetch("/delete-todo", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: todoId }),
  }).then((res) => {
    window.location.href = "/list";
  });
}
