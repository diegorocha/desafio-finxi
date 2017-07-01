$(document).ready(function(){
    /*
        Remove o required apenas do input da foto
        Pois o usuário pode não enviar uma nova foto e a foto atual é mantida
     */
    $('input#id_foto').removeAttr('required');
});
