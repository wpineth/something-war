window.game = {
    state: null,
    initialize: function(){
        window.game.state = 'test';
    },
    move: function(serialization){
        fetch('/move');
    }
};