// ===========================
// main.js
// Script global pour le front
// - gestion du bouton "Déconnexion"
// - helpers pour afficher les erreurs sur les formulaires
// - validation formulaire inscription
// ===========================

// ---------------------------
// Déconnexion
// ---------------------------

function handleLogout() {
  fetch("/logout", {
    method: "GET",
    credentials: "include"
  }).finally(() => {
    window.location.href = "login.html";
  });
}

// ---------------------------
// Helpers erreurs
// ---------------------------

function showError(elementId, message) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent = message;
  }
}

function clearError(elementId) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent = "";
  }
}

window.appHelpers = {
  showError,
  clearError
};

// ---------------------------
// DOMContentLoaded global
// ---------------------------

document.addEventListener("DOMContentLoaded", () => {
  // Bouton déconnexion (présent sur plusieurs pages)
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", handleLogout);
  }

  // Validation formulaire d'inscription (signup.html)
  const signupForm = document.querySelector('form[action="/signup"]');
  if (!signupForm) return; // si on n'est pas sur signup.html, on s'arrête là

  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const passwordConfirm = document.getElementById("password-confirm");
  const errorEl = document.getElementById("signup-error");

  signupForm.addEventListener("submit", (event) => {
    // Nettoyage
    if (errorEl) errorEl.textContent = "";
    email?.removeAttribute("aria-invalid");
    password?.removeAttribute("aria-invalid");
    passwordConfirm?.removeAttribute("aria-invalid");
    passwordConfirm?.removeAttribute("aria-describedby");

    // 0) Champs vides
    if (!email.value || !password.value || !passwordConfirm.value) {
      event.preventDefault();
      if (errorEl) {
        errorEl.textContent = "Veuillez remplir tous les champs.";
      }
      if (!email.value) {
        email.setAttribute("aria-invalid", "true");
        email.focus();
      } else if (!password.value) {
        password.setAttribute("aria-invalid", "true");
        password.focus();
      } else {
        passwordConfirm.setAttribute("aria-invalid", "true");
        passwordConfirm.focus();
      }
      return;
    }

    // 1) Vérif e-mail (HTML5 : required + type="email")
    if (email && !email.checkValidity()) {
      event.preventDefault();
      if (errorEl) {
        errorEl.textContent = "Veuillez saisir une adresse e-mail valide.";
      }
      email.setAttribute("aria-invalid", "true");
      email.focus();
      return;
    }

    // 2) Vérif mots de passe identiques
    if (password && passwordConfirm && password.value !== passwordConfirm.value) {
      event.preventDefault();
      if (errorEl) {
        errorEl.textContent = "Les mots de passe ne correspondent pas.";
      }
      passwordConfirm.setAttribute("aria-invalid", "true");
      passwordConfirm.setAttribute("aria-describedby", "signup-error");
      passwordConfirm.focus();
    }
  });
});
