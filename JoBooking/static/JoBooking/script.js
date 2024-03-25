console.log('hello');  // pour vérifier si affiche sur la console

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
// fonction enregistrement panier dans LocalStorage
function savePanier(panier){
    localStorage.setItem('panier',JSON.stringify(panier));
}

// fonction qui ajoute au panier + sauvegarde
function addOffre(offre){
    let panier=getPanier();
    console.log('panier actuel;',panier)
    if (panier[offre.id]){
        console.log('déja dans panier',panier[offre.id] );
        panier[offre.id].quantity +=1;
    //let findOffre=panier.find(p =>p.id===offre.id);

    //if(findOffre){
        //findOffre.quantity+=1;
    //}else{
        //offre.quantity=1;
        //panier.push(offre);
    }else{
        panier[offre.id]={
            id:offre.id,
            quantity:1
        };

    }
    savePanier(panier);
}

// Récupérer  bouton de réservation
const boutonsReserver= document.querySelectorAll('.btn-reservation');
//Gestionnaire d'événement sur le clique
boutonsReserver.forEach(bouton=>{
    bouton.addEventListener('click',function (){
        console.log('bouton "réserver" fonctionne')

    const offreId = this.getAttribute('data-offre-id');
    const offre ={id:offreId};
    addOffre(offre);
});

    }

);
