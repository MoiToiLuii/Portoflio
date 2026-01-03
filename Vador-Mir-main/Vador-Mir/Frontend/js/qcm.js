document.addEventListener("DOMContentLoaded", function() {
    // Affiche les champs "précise" si nécessaire
    const radioRestrictions = document.querySelector('input[name="visite_medicale"][value="oui_restrictions"]');
    const inputRestrictions = document.getElementById("restrictions");
    radioRestrictions.addEventListener("change", () => {
        inputRestrictions.style.display = radioRestrictions.checked ? "inline-block" : "none";
    });

    const radioBlessure = document.querySelector('input[name="reeducation"][value="oui_blessure"]');
    const inputBlessure = document.getElementById("blessure");
    radioBlessure.addEventListener("change", () => {
        inputBlessure.style.display = radioBlessure.checked ? "inline-block" : "none";
    });

    const radioOperation = document.querySelector('input[name="reeducation"][value="oui_operation"]');
    const inputOperation = document.getElementById("operation");
    radioOperation.addEventListener("change", () => {
        inputOperation.style.display = radioOperation.checked ? "inline-block" : "none";
    });

    const radioOperationAutre = document.querySelector('input[name="operation_impact"][value="oui_autre"]');
    const inputOperationAutre = document.getElementById("operation_autre");
    radioOperationAutre.addEventListener("change", () => {
        inputOperationAutre.style.display = radioOperationAutre.checked ? "inline-block" : "none";
    });

    const checkboxDouleursAutre = document.querySelector('input[name="douleurs"][value="autre"]');
    const inputDouleursAutre = document.getElementById("douleurs_autre");
    checkboxDouleursAutre.addEventListener("change", () => {
        inputDouleursAutre.style.display = checkboxDouleursAutre.checked ? "inline-block" : "none";
    });

    // Affiche les détails pour "chez moi" et "extérieur"
    const checkboxChezMoi = document.querySelector('input[name="endroit_sport"][value="chez_moi"]');
    const divChezMoiDetails = document.getElementById("chez_moi_details");
    checkboxChezMoi.addEventListener("change", () => {
        divChezMoiDetails.style.display = checkboxChezMoi.checked ? "block" : "none";
    });

    const checkboxExterieur = document.querySelector('input[name="endroit_sport"][value="exterieur"]');
    const divExterieurDetails = document.getElementById("exterieur_details");
    checkboxExterieur.addEventListener("change", () => {
        divExterieurDetails.style.display = checkboxExterieur.checked ? "block" : "none";
    });

    // Gestion de la soumission du formulaire
    document.getElementById("qcmForm").addEventListener("submit", function(event) {
        event.preventDefault();

        // Récupère toutes les réponses
        const reponses = {
            visite_medicale: document.querySelector('input[name="visite_medicale"]:checked').value,
            restrictions: document.getElementById("restrictions").value,
            reeducation: document.querySelector('input[name="reeducation"]:checked').value,
            blessure: document.getElementById("blessure").value,
            operation: document.getElementById("operation").value,
            operation_impact: document.querySelector('input[name="operation_impact"]:checked').value,
            operation_autre: document.getElementById("operation_autre").value,
            douleurs: Array.from(document.querySelectorAll('input[name="douleurs"]:checked')).map(el => el.value),
            douleurs_autre: document.getElementById("douleurs_autre").value,
            endurance: document.querySelector('input[name="endurance"]:checked').value,
            budget: document.querySelector('input[name="budget"]:checked').value,
            investissement_materiel: document.querySelector('input[name="investissement_materiel"]:checked').value,
            endroit_sport: Array.from(document.querySelectorAll('input[name="endroit_sport"]:checked')).map(el => el.value),
            chez_moi_equipement: Array.from(document.querySelectorAll('input[name="chez_moi_equipement"]:checked')).map(el => el.value),
            exterieur_equipement: Array.from(document.querySelectorAll('input[name="exterieur_equipement"]:checked')).map(el => el.value),
            frequence: document.querySelector('input[name="frequence"]:checked').value,
            moment_journee: document.querySelector('input[name="moment_journee"]:checked').value,
            type_seance: document.querySelector('input[name="type_seance"]:checked').value,
            exercices_specifices: Array.from(document.querySelectorAll('input[name="exercices_specifices"]:checked')).map(el => el.value),
            suivi_progres: document.querySelector('input[name="suivi_progres"]:checked').value,
        };

        // Sauvegarde dans localStorage
        localStorage.setItem("reponsesQCM", JSON.stringify(reponses));

        // Redirige vers la page des exercices
        window.location.href = "exercices.html";
    });
});
