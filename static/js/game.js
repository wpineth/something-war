window.game = {
    state: null,
    initialize: function(){
        return new Promise((resolve, reject) => {
            fetch('/game/status').then((response) => response.json()).then((data) => {
                window.game.state = data;

                var view_port = document.getElementById("game");

                var table = document.createElement("table");

                for(var i = 0; i < 8; i++){
                    var row = document.createElement("tr");

                    for(var j = 0; j < 8; j++){
                        var cell = document.createElement("td");

                        var info_box = document.createElement("div");

                        info_box.id = i + "-" + j;

                        cell.appendChild(info_box);

                        row.appendChild(cell);
                    }

                    table.appendChild(row);
                }

                view_port.appendChild(table);

                resolve();
            }).catch(() => {
                reject();
            });
        });
    },
    render: function(){
        var view_port = document.getElementById("game");

        for(var i = 0; i < 8; i++){
            for(var j = 0; j < 8; j++){
                var info_box = view_port.children[0].children[i].children[j].children[0];

                info_box.innerHTML = '';

                var city = window.game.state.cities[i][j];
                var piece = window.game.state.pieces[i][j];
                
                if(city != null){
                    switch(city){
                        case -1:
                            view_port.children[0].children[i].children[j].children[0].classList = 'black';
                            break;
                        case 1:
                            view_port.children[0].children[i].children[j].children[0].classList = 'white';
                            break;
                        case 0:
                            view_port.children[0].children[i].children[j].children[0].classList = 'neutral';
                            break;
                    }
                }

                if(piece != 0){
                    switch(piece){
                        case -1:
                            var pieceElement = document.createElement('div');

                            pieceElement.classList = 'black';

                            view_port.children[0].children[i].children[j].children[0].appendChild(pieceElement);
                            break;
                        case 1:
                            var pieceElement = document.createElement('div');

                            pieceElement.classList = 'white';

                            view_port.children[0].children[i].children[j].children[0].appendChild(pieceElement);
                            break;
                    }

                    var health = document.createElement('p');

                    health.innerHTML = window.game.state.piece_health[i][j] + '/' + window.game.state.max_health[Math.abs(piece).toString()];

                    health.classList = 'health';

                    view_port.children[0].children[i].children[j].children[0].children[0].appendChild(health);

                    var attack = document.createElement('p');

                    attack.innerHTML = window.game.state.attack[Math.abs(piece).toString()];

                    attack.classList = 'attack';

                    view_port.children[0].children[i].children[j].children[0].children[0].appendChild(attack);

                    var retaliation = document.createElement('p');

                    retaliation.innerHTML = window.game.state.retaliation[Math.abs(piece).toString()];

                    retaliation.classList = 'retaliation';

                    view_port.children[0].children[i].children[j].children[0].children[0].appendChild(retaliation);
                }
            }
        }

    }
};