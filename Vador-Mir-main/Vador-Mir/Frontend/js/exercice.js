document.addEventListener("DOMContentLoaded", function() {
    // Récupère les réponses du QCM
    const reponses = JSON.parse(localStorage.getItem("reponsesQCM"));
    const exercicesDiv = document.getElementById("exercices");

    if (!reponses) {
        exercicesDiv.innerHTML = "<p>Tu n’as pas encore répondu au QCM. <a href='qcm.html'>Commence ici</a>.</p>";
        return;
    }

    // Fonction pour générer les exercices
    function genererExercices(reponses) {
        let html = `<h2>Voici ta routine personnalisée :</h2>`;

        // 1. Adaptation en fonction de la condition physique
        if (reponses.reeducation === "oui_blessure" || reponses.reeducation === "oui_operation" ||
            reponses.operation_impact !== "non" || reponses.douleurs.includes("genoux") ||
            reponses.douleurs.includes("dos") || reponses.douleurs.includes("epaules")) {
            html += `<div class="recommandation">
                <p>⚠️ <strong>Attention</strong> : En raison de tes antécédents médicaux ou douleurs, nous te proposons des exercices <strong>doux et adaptés</strong>. Consulte un professionnel de santé si nécessaire.</p>
            </div>`;
        }

        // 2. Exercices en fonction de l'endurance
        if (reponses.endurance === "essouffle_1_etage") {
            html += `
                <div class="exercice">
                    <h3>Marche active</h3>
                    <p>Commence par des séances de marche rapide de 10 à 15 min, 3 fois par semaine.</p>
                    <img src="docs/photos/marche.jpg" alt="Marche active" width="300">
                    <p class="materiel">Matériel : Aucune (extérieur ou tapis à la maison).</p>
                </div>
            `;
        } else if (reponses.endurance === "marcher_30_min") {
            html += `
                <div class="exercice">
                    <h3>Marche + Renforcement léger</h3>
                    <p>30 min de marche + 10 min d’exercices au poids du corps (squats muraux, élévations de mollets).</p>
                    <img src="docs/photos/squat_mural.jpg" alt="Squat mural" width="300">
                    <p class="materiel">Matériel : Mur pour les squats.</p>
                </div>
            `;
        } else {
            html += `
                <div class="exercice">
                    <h3>Circuit complet</h3>
                    <p>Enchaîne 3 tours de :</p>
                    <ul>
                        <li>20 squats</li>
                        <li>10 pompes (sur les genoux si besoin)</li>
                        <li>30 secondes de gainage</li>
                        <li>1 min de marche sur place</li>
                    </ul>
                    <img src="docs/photos/circuit.jpg" alt="Circuit complet" width="300">
                    <p class="materiel">Matériel : Tapis de sol (optionnel).</p>
                </div>
            `;
        }

        // 3. Adaptation en fonction des douleurs
        if (reponses.douleurs.includes("genoux")) {
            html += `
                <div class="exercice">
                    <h3>Renforcement des genoux</h3>
                    <p>Assis·e sur une chaise, lève une jambe tendue et maintient 5 secondes. Répète 10 fois par jambe.</p>
                    <img src="docs/photos/renforcement_genoux.jpg" alt="Renforcement genoux" width="300">
                </div>
            `;
        }

        if (reponses.douleurs.includes("dos")) {
            html += `
                <div class="exercice">
                    <h3>Étirements du dos</h3>
                    <p>Allongé·e sur le dos, ramène tes genoux vers ta poitrine et tiens 20 secondes. Répète 5 fois.</p>
                    <img src="docs/photos/etirement_dos.jpg" alt="Étirement dos" width="300">
                </div>
            `;
        }

        // 4. Adaptation en fonction du budget et de l'endroit
        if (reponses.budget === "0_euro" || reponses.investissement_materiel === "non") {
            html += `
                <div class="recommandation">
                    <p>💡 <strong>Conseil</strong> : Voici des exercices <strong>sans matériel</strong> :</p>
                    <ul>
                        <li>Squats</li>
                        <li>Fentes statiques</li>
                        <li>Gainage ventral</li>
                    </ul>
                </div>
            `;
        } else if (reponses.budget === "20_50_euro" || reponses.investissement_materiel === "oui_basique") {
            html += `
                <div class="recommandation">
                    <p>💡 <strong>Conseil</strong> : Avec un petit budget, tu peux acheter des <strong>élastiques de résistance</strong> pour varier tes exercices (ex. : rowing, extensions de jambe).</p>
                    <img src="docs/photos/elastique.jpg" alt="Élastique de résistance" width="300">
                </div>
            `;
        }

        // 5. Adaptation en fonction de la fréquence
        if (reponses.frequence === "1_seance") {
            html += `
                <div class="recommandation">
                    <p>📅 <strong>Pour 1 séance/semaine</strong> : Privilégie un <strong>full-body</strong> (tout le corps) pour maximiser les résultats.</p>
                </div>
            `;
        } else if (reponses.frequence === "4_seances_plus") {
            html += `
                <div class="recommandation">
                    <p>📅 <strong>Pour 4 séances/semaine</strong> : Alterne haut du corps, bas du corps, cardio et étirements.</p>
                </div>
            `;
        }

        // 6. Adaptation en fonction des objectifs complémentaires
        if (reponses.exercices_specifices.includes("respiration")) {
            html += `
                <div class="exercice">
                    <h3>Respiration et relaxation</h3>
                    <p>5 min de cohérence cardiaque (inspire 5 sec, expire 5 sec).</p>
                    <img src="docs/photos/respiration.jpg" alt="Respiration" width="300">
                </div>
            `;
        }

        if (reponses.exercices_specifices.includes("mobilite")) {
            html += `
                <div class="exercice">
                    <h3>Mobilité des épaules</h3>
                    <p>Fais des cercles avec tes bras, 10 fois dans chaque sens.</p>
                    <img src="docs/photos/mobilite_epaules.jpg" alt="Mobilité épaules" width="300">
                </div>
            `;
        }

        // 7. Recommandations de matériel si budget
        if (reponses.budget === "50_100_euro" || reponses.budget === "plus_100_euro") {
            html += `
                <div class="recommandation">
                    <p>🛒 <strong>Matériel recommandé</strong> :</p>
                    <ul>
                        <li>Tapis de yoga (20–40 €)</li>
                        <li>Haltères ajustables (50–100 €)</li>
                        <li>Abonnement à une appli de coaching (ex. : Nike Training Club)</li>
                    </ul>
                </div>
            `;
        }

        // 8. Message de motivation
        html += `
            <div class="recommandation">
                <p>🌟 <strong>Conseil</strong> : Écoute ton corps et progresse à ton rythme. Tu peux ajuster les exercices en fonction de tes sensations !</p>
            </div>
        `;

        return html;
    }

    // Affiche les exercices
    exercicesDiv.innerHTML = genererExercices(reponses);

    // Gestion du bouton "Recommencer le QCM"
    document.getElementById("recommencer").addEventListener("click", function() {
        localStorage.removeItem("reponsesQCM");
        window.location.href = "qcm.html";
    });

    // Gestion du bouton "Imprimer ma routine"
    document.getElementById("imprimer").addEventListener("click", function() {
        window.print();
    });
});
