// TechHub JavaScript Enhancements
document.addEventListener("DOMContentLoaded", function () {
  // Auto-hide flash messages after 5 seconds
  const flashMessages = document.querySelectorAll(".alert");
  flashMessages.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Add loading states to forms
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function () {
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML =
          '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        submitBtn.disabled = true;
      }
    });
  });

  // Quantity input validation
  const quantityInputs = document.querySelectorAll('input[type="number"]');
  quantityInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const max = parseInt(this.max);
      const min = parseInt(this.min);
      let value = parseInt(this.value);

      if (value > max) {
        this.value = max;
        showToast("Maximum quantity reached", "warning");
      } else if (value < min) {
        this.value = min;
        showToast("Minimum quantity is 1", "warning");
      }
    });
  });

  // Product image error handling
  const productImages = document.querySelectorAll(".card-img-top, .img-fluid");
  productImages.forEach((img) => {
    img.addEventListener("error", function () {
      this.src = "https://via.placeholder.com/300x200?text=Image+Not+Found";
      this.alt = "Product image not available";
    });
  });

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Add to cart animation
  document.querySelectorAll('form[action*="add_to_cart"]').forEach((form) => {
    form.addEventListener("submit", function () {
      const cartBadge = document.querySelector(".navbar .badge");
      if (cartBadge) {
        cartBadge.style.transform = "scale(1.5)";
        setTimeout(() => {
          cartBadge.style.transform = "scale(1)";
        }, 300);
      }
    });
  });
});

// Toast notification function
function showToast(message, type = "info") {
  const toastContainer =
    document.getElementById("toast-container") || createToastContainer();

  const toast = document.createElement("div");
  toast.className = `toast align-items-center text-white bg-${type} border-0`;
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "assertive");
  toast.setAttribute("aria-atomic", "true");

  toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

  toastContainer.appendChild(toast);

  const bsToast = new bootstrap.Toast(toast);
  bsToast.show();

  // Remove toast after hide
  toast.addEventListener("hidden.bs.toast", () => {
    toast.remove();
  });
}

function createToastContainer() {
  const container = document.createElement("div");
  container.id = "toast-container";
  container.className = "toast-container position-fixed top-0 end-0 p-3";
  container.style.zIndex = "9999";
  document.body.appendChild(container);
  return container;
}

// Search enhancement
function enhanceSearch() {
  const searchInput = document.querySelector('input[name="search"]');
  if (searchInput) {
    let timeout;
    searchInput.addEventListener("input", function () {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        if (this.value.length >= 3 || this.value.length === 0) {
          this.form.submit();
        }
      }, 500);
    });
  }
}

// Price formatting
function formatPrice(price) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(price);
}

// Initialize enhancements
enhanceSearch();
