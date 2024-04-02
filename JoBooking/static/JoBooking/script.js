console.log('hello');  // pour vérifier si script reconnu

// fonction pour récupérer panier dans localStorage
function getPanier(){
    let panier= localStorage.getItem('panier');
//  si le panier existe pas
    if (panier===null || panier===''){
        return {};
    }else{
        return JSON.parse(panier);
    }
}
// fonction pour enregistrer panier dans LocalStorage
function savePanier(panier){
    localStorage.setItem('panier',JSON.stringify(panier));
}


// fonction pour supprimer panier dans LocalStorage
function deletePanier(){
    localStorage.removeItem('panier');
}


// fonction pour afficher nombre éléments dans panier ( réservation )
function nombreReservation(){
    const panier = getPanier();
    const nombredeReservation=Object.keys(panier).length;
    console.log('nombre de réservations:',nombredeReservation);
    if (nombredeReservation!==null){
            document.getElementById('nombre-reservation').innerText=`🧺Réservation(${nombredeReservation})`;

    }
}

// fonction  pour s'assurer du chargement du DOM
document.addEventListener('DOMContentLoaded',function (){
    nombreReservation();
});



// fonction qui ajoute au panier + sauvegarde
    function addOffre(offre) {
        let panier = getPanier();
        console.log('panier actuel;', panier)
        if (panier[offre.id]) {
            console.log('déja dans panier', panier[offre.id]);
            panier[offre.id].quantity += 1;
        } else {
            panier[offre.id] = {
                id: offre.id,
                quantity :offre.quantity
            };

        }
        savePanier(panier);
        nombreReservation();
    }

// acquisition token    code source :django documentation
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


//envoie données panier de l'user  vers le back
function dataPanier(){
        const panier=getPanier()
        const csrftoken = getCookie('csrftoken');
        fetch('http://127.0.0.1:8000/reservation/',{
            method:'POST',
            headers:{
                'Content-type':'application/json',
                'X-CSRFToken':csrftoken
            },
            body:JSON.stringify({panier: panier})
        })
            .then(response=>response.json())
            .then(data=>{ console.log(data);
            })
            .catch(error=>{
                console.log('Erreur durant requête',error);
            });
}


// BOUTON DE RESERVATION
// Récupérer chaque bouton de réservation
    const boutonsReserver = document.querySelectorAll('.btn-reservation');
//Gestionnaire d'événement sur le clique
    boutonsReserver.forEach(bouton => {
            bouton.addEventListener('click', function () {
                console.log('bouton "réserver" fonctionne')

                const offreId = this.getAttribute('data-offre-id');
                const offre = {id: offreId};
                console.log(offre);
                addOffre(offre);

                dataPanier();
            });

        }
        );


// BOUTON D ANNULATION
const boutonAnnulation = document.querySelector('.btn-annuler');
boutonAnnulation.addEventListener('click',function (){
    console.log('bouton annuler opérationnel ! ')
    deletePanier();
    window.location.href='annulation';
})

//BOUTON PAIEMENT
const boutonPaiement = document.querySelector('.btn-valider');
boutonPaiement.addEventListener('click',function (){
    console.log('bouton valider opérationnel ! ')
    deletePanier();
    window.location.href='payer';
})