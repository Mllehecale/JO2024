console.log('hello');  // pour vérifier si script reconnu

document.addEventListener('DOMContentLoaded',function (){
   console.log('Le DOM est chargé')
})

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
            document.getElementById('nombre-reservation').innerText=`🧺Panier(${nombredeReservation})`;

    }
}

//fonction  pour s'assurer du chargement du DOM
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
            quantity: 1
        };

    }
    savePanier(panier);
    nombreReservation();
}

// function supprime une offre dans le panier
//function supprimerOffre(offre){
  //  let panier=getPanier();
    //delete panier[offre.id];
    //savePanier(panier);
   // const OffrePanier=document.querySelector(`.offre[data-offre-id="${offre.id}"]`);
    //if (OffrePanier){
      //  OffrePanier.parentElement.remove();
    //}

    //nombreReservation();
//}

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

function dataPanier(){
    const panier=getPanier();
    const csrftoken=getCookie('csrftoken');
    const url='http://127.0.0.1:8000/commande/';
    fetch(url,{
        method:'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({panier:panier})
    })
        .then(response=>response.json())
        .then(data=>{console.log(data)})
        .catch(error=>{console.log('erreur durant requête',error)});

}

//function pour supprimer une offre du panier
function supprimerOffre(offreId) {
    const csrftoken = getCookie('csrftoken');
    const url = 'http://127.0.0.1:8000/commande/supprimer_offre';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({offre_id: offreId})
    })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    const offrePanier = document.querySelector(`.offre[data-offre-id="${offreId}"]`);
                    if (offrePanier) {
                        offrePanier.remove();
                    } else {
                        console.error('offre panier pas trouvé sur page');
                    }
                });
            } else {
                console.error('error durant suppression de offre dans panier')
            }
        })
        .catch(error => {
            console.error('voici lerreur:', error);

        });
}


// BOUTON DE RESERVATION
// Récupérer chaque bouton de réservation
const boutonsReserver = document.querySelectorAll('.btn-reservation');
boutonsReserver.forEach(bouton => {
    bouton.addEventListener('click', function () {
        console.log('bouton "réserver" fonctionne')

        const offreId = this.getAttribute('data-offre-id');
        const offre = {id: offreId};
        console.log(offre);
        addOffre(offre);

        dataPanier();
    });

});


//BOUTON ANNULATION DE LA COMMANDE ENTIERE
const boutonannulation=document.getElementById('btn-annulation')
function declencherannulation(){
    console.log('bouton annuler opérationnel');
    window.location.href='annulation';
    deletePanier();

}
boutonannulation.addEventListener("click",declencherannulation)


// BOUTON SUPPRIMER UNE OFFRE DE LA COMMANDE
const boutonsupprimeroffre = document.querySelectorAll('.btn-supprimer');
boutonsupprimeroffre.forEach(boutonsupp=>{
boutonsupp.addEventListener('click',function (){

    console.log("btn supprimer fonctionne");
        const offreId = this.getAttribute('data-offre-id');
    supprimerOffre(offreId);

    });
});



//BOUTON PAIEMENT
const boutonpaiement=document.getElementById('btnpayer');
function declencherpaiement (){
    console.log('bouton payer opérationnel');
    window.location.href='payer';
    deletePanier();

}
boutonpaiement.addEventListener("click",declencherpaiement);



