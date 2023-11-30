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

                        cell.id = i + "-" + j;

                        cell.appendChild(document.createElement("p"));

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
                var city = window.game.state.cities[i][j];
                if(city != null){
                    view_port.children[0].children[i].children[j].children[0].innerHTML = city;
                }
            }
        }

    }
};