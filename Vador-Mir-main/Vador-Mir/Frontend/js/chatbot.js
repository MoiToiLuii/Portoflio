// ===========================
// chatbot.js
// Gère le front du chatbot IA
// - récupération du message de l'utilisateur
// - envoi au backend (/api/chat)
// - affichage de la réponse dans l'historique
// ===========================

document.addEventListener("DOMContentLoaded", () => {
    // Récupération des éléments importants de la page chatbot
    const sendButton = document.getElementById("send-message-btn");
    const messageInput = document.getElementById("user-message");
    const historyContainer = document.getElementById("chat-history");

    if (!sendButton || !messageInput || !historyContainer) {
        // Si la page ne contient pas ces éléments, on ne fait rien
        return;
    }

    // Quand on clique sur le bouton "Envoyer"
    sendButton.addEventListener("click", () => {
        handleSendMessage(messageInput, historyContainer);
    });

    // Option : envoyer le message avec Ctrl+Enter dans la zone de texte
    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && event.ctrlKey) {
            event.preventDefault();
            handleSendMessage(messageInput, historyContainer);
        }
    });
});

// ---------------------------
// Gestion de l’envoi du message
// ---------------------------

/**
 * Récupère le message de l'utilisateur, fait des vérifications simples
 * puis l’envoie au backend. Affiche ensuite la réponse dans l’historique.
 *
 * @param {HTMLTextAreaElement} messageInput - zone de texte de l'utilisateur
 * @param {HTMLElement} historyContainer - conteneur de l'historique
 */
function handleSendMessage(messageInput, historyContainer) {
    const rawMessage = messageInput.value.trim();

    // Nettoyer d’abord d’éventuels anciens messages d’erreur
    window.appHelpers.clearError("chat-error");

    // Vérification basique : champ non vide
    if (!rawMessage) {
        window.appHelpers.showError("chat-error", "Veuillez saisir une question avant d'envoyer.");
        return;
    }

    // Vérification basique de longueur (doit être cohérente avec maxlength=500 dans le HTML)
    if (rawMessage.length > 500) {
        window.appHelpers.showError("chat-error", "Votre message est trop long (500 caractères max).");
        return;
    }

    // Ajouter le message de l'utilisateur à l'historique pour feedback immédiat
    appendMessage(historyContainer, "user", rawMessage);

    // Nettoyer la zone de saisie après envoi
    messageInput.value = "";

    // Appeler le backend (tu adapteras l’URL / méthode selon ton API réelle)
    fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include", // pour envoyer cookies de session si nécessaire
        body: JSON.stringify({ message: rawMessage })
    })
        .then(async (response) => {
            if (!response.ok) {
                // Si le serveur renvoie une erreur HTTP
                throw new Error("Erreur côté serveur (" + response.status + ")");
            }
            // On suppose que le backend renvoie { reply: "texte de la réponse" }
            return response.json();
        })
        .then((data) => {
            const reply = data.reply || "L'IA n'a pas pu fournir de réponse.";
            appendMessage(historyContainer, "bot", reply);
        })
        .catch((error) => {
            console.error(error);
            // Message d’erreur affiché à l’utilisateur
            window.appHelpers.showError(
                "chat-error",
                "Impossible de contacter l’IA pour le moment. Réessayez plus tard."
            );
            // On peut aussi ajouter un message d’erreur dans l’historique
            appendMessage(
                historyContainer,
                "bot",
                "Une erreur est survenue lors de l'appel à l’IA. Vérifiez votre connexion ou réessayez plus tard."
            );
        });
}

// ---------------------------
// Ajout de messages dans l’historique
// ---------------------------

/**
 * Ajoute un message (utilisateur ou bot) dans le conteneur d’historique.
 *
 * @param {HTMLElement} container - conteneur de l’historique (div#chat-history)
 * @param {"user"|"bot"} sender - origine du message
 * @param {string} text - contenu du message
 */
function appendMessage(container, sender, text) {
    const wrapper = document.createElement("div");

    // Ajoute les classes CSS pour le style (message-user / message-bot)
    wrapper.classList.add("message");
    if (sender === "user") {
        wrapper.classList.add("message-user");
    } else {
        wrapper.classList.add("message-bot");
    }

    // Crée un paragraphe avec le texte du message
    const p = document.createElement("p");

    // Préfixe pour indiquer qui parle (utile pour compréhension et accessibilité)
    const prefix = sender === "user" ? "Vous : " : "Assistant : ";
    p.textContent = prefix + text;

    wrapper.appendChild(p);
    container.appendChild(wrapper);

    // Faire défiler l'historique vers le bas pour voir le dernier message
    container.scrollTop = container.scrollHeight;
}
