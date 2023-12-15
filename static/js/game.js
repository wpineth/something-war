window.game = {
    state: null,
    selected: null,
    player: "white",
    other_player: "black",
    initialize: function(){
        return new Promise((resolve, reject) => {
            window.game.refresh().then(() => {
                var view_port = document.getElementById("game");

                var panel_titles = [
                    "Money:",
                    "Basic:",
                    "Runner:",
                    "Defender:",
                    "Swordsman:",
                    "Archer:",
                    "Support:",
                    "Berserker:"
                ];

                var black_panel = document.createElement("div");
                    black_panel.classList.add("black");
                    black_panel.classList.add("panel");
                    
                    var row = document.createElement("div");
                        row.classList.add("black");
                        row.classList.add("row");
                        var cell = document.createElement("div");
                            cell.classList.add("black");
                            cell.classList.add("cell");
                            cell.id = "black_phase";

                            var phase = document.createElement("p");
                                phase.classList.add("center");
                            cell.appendChild(phase);
                        row.appendChild(cell);
                    black_panel.appendChild(row);

                    for(var i = 0; i < 4; i++){
                        var row = document.createElement("div");
                        row.classList.add("black");
                        row.classList.add("row");
                            for(var j = 0; j < 2; j++){
                                var cell = document.createElement("div");
                                    cell.classList.add("black");
                                    cell.classList.add("cell");
                                    cell.id = "black_panel_" + ((i * 2) + j);

                                    var title = document.createElement("p");
                                        title.innerText = panel_titles[((i * 2) + j)];
                                    cell.appendChild(title);

                                    var research = document.createElement("p");
                                        research.classList.add("center");
                                    cell.appendChild(research);
                                row.appendChild(cell);
                            }

                        black_panel.appendChild(row);
                    }
                
                view_port.appendChild(black_panel);

                var board = document.createElement("div");
                    board.classList.add("board");

                    for(var i = 0; i < 8; i++){
                        var row = document.createElement("div");

                            row.classList.add("row");

                            for(var j = 0; j < 8; j++){
                                var cell = document.createElement("div");
                                    
                                    cell.classList.add("cell");

                                    cell.id = i + "-" + j;

                                row.appendChild(cell);
                            }

                        board.appendChild(row);
                    }

                view_port.appendChild(board);

                var white_panel = document.createElement("div");
                    white_panel.classList.add("white");
                    white_panel.classList.add("panel");
                    
                    var row = document.createElement("div");
                        row.classList.add("white");
                        row.classList.add("row");
                        var cell = document.createElement("div");
                            cell.classList.add("white");
                            cell.classList.add("cell");
                            cell.id = "white_phase";

                            var phase = document.createElement("p");
                                phase.classList.add("center");
                            cell.appendChild(phase);
                        row.appendChild(cell);
                    white_panel.appendChild(row);

                    for(var i = 0; i < 4; i++){
                        var row = document.createElement("div");
                            row.classList.add("white");
                            row.classList.add("row");
                            for(var j = 0; j < 2; j++){
                                var cell = document.createElement("div");
                                    cell.classList.add("white");
                                    cell.classList.add("cell");
                                    cell.id = "white_panel_" + ((i * 2) + j);

                                    var title = document.createElement("p");
                                        title.innerText = panel_titles[((i * 2) + j)];
                                    cell.appendChild(title);

                                    var research = document.createElement("p");
                                        research.classList.add("center");
                                    cell.appendChild(research);
                                row.appendChild(cell);
                            }

                        white_panel.appendChild(row);
                    }
                
                view_port.appendChild(white_panel);

                view_port.addEventListener("click", (event) => {
                    if((window.game.player == "black" && window.game.state.player_to_move == 1) || (window.game.player == "white" && window.game.state.player_to_move == -1)){
                        return;
                    }

                    var cell = event.target;
                    
                    while(!cell.id){
                        cell = cell.parentElement;
                    }

                    if(cell.id != "game" && !cell.id.startsWith(window.game.other_player)){
                        if(cell.id == window.game.player + "_phase"){
                            var research = null;
                            if(window.game.selected != null){
                                if(window.game.selected.startsWith(window.game.player)){
                                    research = parseInt(window.game.selected.split('_')[2]);
                                }

                                document.getElementById(window.game.selected).classList.remove("glow");
                                
                                window.game.selected = null;
                            }

                            if(research == null && !window.game.state.economy_phase){
                                fetch("/game/status", {
                                    method: "POST",
                                    headers: {
                                      "Content-Type": "application/json"
                                    },
                                    body: JSON.stringify({
                                        economy_phase: false
                                    })
                                }).then((response) => response.json()).then((data) => {
                                    window.game.state = data;
                                    
                                    window.game.render();
                                }).catch((err) => {
                                    console.log(err);
                                });
                            }else{
                                fetch("/game/status", {
                                    method: "POST",
                                    headers: {
                                      "Content-Type": "application/json"
                                    },
                                    body: JSON.stringify({
                                        research: research
                                    })
                                }).then((response) => response.json()).then((data) => {
                                    window.game.state = data;
                                    
                                    window.game.render();
                                }).catch((err) => {
                                    console.log(err);
                                });
                            }
                        }else{
                            if(cell.id != window.game.player + "_panel_0"){
                                if(window.game.selected == null){
                                    cell.classList.add("glow");
                                    window.game.start_action(cell.id);
                                }else if(!cell.id.startsWith(window.game.player)){
                                    cell.classList.add("glow");
                                    window.game.end_action(cell.id);
                                }
                            }
                        }
                    }
                });

                resolve();
            }).catch((err) => {
                reject(err);
            });
        });
    },
    render: function(){
        var view_port = document.getElementById("game");
        var board = view_port.children[1];

        if(window.game.state.player_to_move == 1){
            document.getElementById("black_phase").children[0].innerText = "It's White's turn...";

            if(window.game.state.economy_phase){
                document.getElementById("white_phase").children[0].innerText = "Economy";
            }else{
                document.getElementById("white_phase").children[0].innerText = "Command";
            }
        }else{
            document.getElementById("white_phase").children[0].innerText = "It's White's turn...";

            if(window.game.state.economy_phase){
                document.getElementById("black_phase").children[0].innerText = "Economy";
            }else{
                document.getElementById("black_phase").children[0].innerText = "Command";
            }
        }

        document.getElementById("black_panel_0").children[1].innerText = "$" + window.game.state.black_money;
        document.getElementById("white_panel_0").children[1].innerText = "$" + window.game.state.black_money;

        for(var i = 1; i < 8; i++){
            if(window.game.state.black_research[i]){
                document.getElementById("black_panel_" + i).children[1].innerText = "✅";
            }else{
                document.getElementById("black_panel_" + i).children[1].innerText = "❌";
            }
            
            if(window.game.state.white_research[i]){
                document.getElementById("white_panel_" + i).children[1].innerText = "✅";
            }else{
                document.getElementById("white_panel_" + i).children[1].innerText = "❌";
            }
        }

        for(var i = 0; i < 8; i++){
            for(var j = 0; j < 8; j++){
                board.children[i].children[j].innerHTML = "";

                var city = window.game.state.cities[i][j];
                var piece = window.game.state.pieces[i][j];
                
                if(city != null){
                    switch(city){
                        case -1:
                            var city = document.createElement("div");
                                city.classList.add("black");
                                city.classList.add("center");
                                city.classList.add("city");
                            board.children[i].children[j].appendChild(city);
                            break;
                        case 1:
                            var city = document.createElement("div");
                                city.classList.add("white");
                                city.classList.add("center");
                                city.classList.add("city");
                            board.children[i].children[j].appendChild(city);
                            break;
                        case 0:
                            var city = document.createElement("div");
                                city.classList.add("neutral");
                                city.classList.add("center");
                                city.classList.add("city");
                            board.children[i].children[j].appendChild(city);
                            break;
                    }
                }

                if(piece != 0){
                    switch(piece){
                        case -1:
                            var pieceElement = document.createElement("div");

                                pieceElement.classList.add("black");
                                pieceElement.classList.add("piece");
                                pieceElement.classList.add("center");

                            if(board.children[i].children[j].children.length > 0){
                                board.children[i].children[j].children[0].appendChild(pieceElement);
                            }else{
                                board.children[i].children[j].appendChild(pieceElement);
                            }
                            break;
                        case 1:
                            var pieceElement = document.createElement("div");

                                pieceElement.classList.add("white");
                                pieceElement.classList.add("piece");
                                pieceElement.classList.add("center");

                            if(board.children[i].children[j].children.length > 0){
                                board.children[i].children[j].children[0].appendChild(pieceElement);
                            }else{
                                board.children[i].children[j].appendChild(pieceElement);
                            }
                            break;
                    }

                    var is_city = Array.from(board.children[i].children[j].children[0].classList).includes("city");

                    var health = document.createElement("p");

                        health.innerHTML = window.game.state.piece_health[i][j] + "/" + window.game.state.max_health[Math.abs(piece).toString()];

                        health.classList.add("health");

                    var attack = document.createElement("p");

                        attack.innerHTML = window.game.state.attack[Math.abs(piece).toString()];

                        attack.classList.add("attack");

                    var retaliation = document.createElement("p");
                        retaliation.innerHTML = window.game.state.retaliation[Math.abs(piece).toString()];

                        retaliation.classList.add("retaliation");

                    if(is_city){
                        board.children[i].children[j].children[0].children[0].appendChild(health);
                        board.children[i].children[j].children[0].children[0].appendChild(attack);
                        board.children[i].children[j].children[0].children[0].appendChild(retaliation);
                    }else{
                        board.children[i].children[j].children[0].appendChild(health);
                        board.children[i].children[j].children[0].appendChild(attack);
                        board.children[i].children[j].children[0].appendChild(retaliation);
                    }
                }
            }
        }

    },
    start_action: function(value){
        window.game.selected = value;
    },
    end_action: function(value){
        var c1 = window.game.selected;
        var c2 = value;

        document.getElementById(c1).classList.remove("glow");
        document.getElementById(c2).classList.remove("glow");

        window.game.selected = null;

        window.game.act(c1, c2).then(() => {
            window.game.render();
            // window.game.refresh().then(() => {
            //     window.game.render();
            // });
        });
    },
    act: function(c1, c2){
        return new Promise((resolve, reject) => {
            var t1 = null;
            var t2 = null;
            if(c1.startsWith(window.game.player)){
                t1 = parseInt(c1.split("_")[2]);
                
                t2 = c2.split("-");
    
                t2[0] = parseInt(t2[0]);
                t2[1] = parseInt(t2[1]);
            }else{
                t1 = c1.split("-");
    
                t1[0] = parseInt(t1[0]);
                t1[1] = parseInt(t1[1]);
                
                t2 = c2.split("-");
    
                t2[0] = parseInt(t2[0]);
                t2[1] = parseInt(t2[1]);    
            }

            console.log(t1, t2);

            fetch("/game/status", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    t1: t1,
                    t2: t2
                })
            }).then((response) => response.json()).then((data) => {
                window.game.state = data;
                resolve();
            }).catch((err) => {
                reject(err);
            });
        });
    },
    refresh: function(){
        return new Promise((resolve, reject) => {
            fetch("/game/status").then((response) => response.json()).then((data) => {
                window.game.state = data;
                resolve();
            }).catch((err) => {
                reject(err);
            });
        });
    }
};