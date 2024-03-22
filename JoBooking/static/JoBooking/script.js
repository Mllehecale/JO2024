console.log('hello');  // pour vérifier si affiche sur la console

// fonction pour récupérer panier dans localStorage
function getPanier(){
    let panier= localStorage.getItem('panier');

    if (panier===null){
        return [];
    }else{
        return JSON.parse(panier);
    }
}
// fonction enregistrement panier dans LocalStorage
function savePanier(panier){
    localStorage.setItem('panier',JSON.stringify(panier));
}

// fonction qui ajoute au panier + sauvegarde
function addOffre(offre){
    let panier=getPanier();
    let findOffre=panier.find(p =>p.id===offre.id);

    if(findOffre){
        findOffre.quantity+=1;
    }else{
        offre.quantity=1;
        panier.push(offre);
    }
    savePanier(panier);
}

// Récupérer du bouton de réservation
const boutonReserver= document.querySelector('.btn-reservation');
//Gestionnaire d'événement sur le clique
boutonReserver.addEventListener('click',function (){
    const offre = this.getAttribute('data-offre-id');
})