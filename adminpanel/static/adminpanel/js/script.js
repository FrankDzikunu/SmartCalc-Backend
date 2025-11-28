/* ================================
   ADMIN PANEL JAVASCRIPT
================================ */

/* === Fade in page on load === */
document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("fade-in");
});

/* === MODAL HANDLING === */
function openModal(id) {
  const modal = document.getElementById(id);
  modal.classList.remove('hidden');
  modal.classList.add('flex');  // shows the modal
}

function closeModal(id) {
  const modal = document.getElementById(id);
  modal.classList.add('hidden'); // hides the modal
  modal.classList.remove('flex');
}


/* Close modal when clicking outside the modal box */
window.addEventListener("click", (e) => {
    document.querySelectorAll(".modal").forEach((modal) => {
        if (e.target === modal) {
            modal.classList.add("hidden");
        }
    });
});

/* === SOFT BUTTON CLICK ANIMATION === */
document.querySelectorAll("button, a").forEach((el) => {
    el.addEventListener("mousedown", () => {
        el.classList.add("pressed");
        setTimeout(() => el.classList.remove("pressed"), 150);
    });
});

/* === SEARCH BAR FILTER === */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filterValue = input.value.toLowerCase();
    const tableRows = document
        .getElementById(tableId)
        .getElementsByTagName("tr");

    Array.from(tableRows).forEach((row) => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(filterValue) ? "" : "none";
    });
}
