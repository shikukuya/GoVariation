class OnlineGame {
    /**
     * 
     * @param {Element} ele 
     * @param {Element} optionEle 
     * @param {boolean} create 是否创建房间
     */
    constructor(ele, optionEle, create) {
        this.create = !(typeof create === "undefined");
        this.url = optionEle.querySelector(".url").value || "127.0.0.1:34777";
        this.username = optionEle.querySelector(".username").value;
        this.room = optionEle.querySelector(".room").value.toString();
        if (!create) {
            if (this.username.length < 5) {
                alert("用户名至少需要5个字符");
                window.location.reload();
            }
            if (this.room.length !== 6) {
                alert("房间号必需为6个字符");
                window.location.reload();
            }
        }
        this.ws = new WebSocket("ws://" + this.url);
        this.ws.onopen = () => {
            console.log("ws open");
            if (this.create) {
                this.ws.send(
                    "create " + 
                    `${optionEle.querySelector(".width").value} ` +
                    `${optionEle.querySelector(".height").value} `
                );
            } else {
                this.ws.send(`join ${this.room} ${this.username}`);
                window.onbeforeunload = () => {
                    this.ws.close(1000);
                };
                this.game = new NormalGame(ele, optionEle);
                this.game.putBlockOriginal = this.game.putBlock;
                this.game.putBlock = (x, y) => {
                    this.ws.send(`put ${this.game.players[this.username][0]} ${x} ${y}`)
                    return this.game.putBlockOriginal(x, y);
                }
            }
        };
        this.ws.onmessage = (e) => {
            let data = JSON.parse(e.data);
            console.log("ws receive", data);
            if ("msg" in data) {
                if ("input" in data) {
                    prompt(data.msg, data.input);
                } else {
                    alert(data.msg);
                }
                window.location.reload();
            } else {
                switch (data.action) {
                    case "update":
                        this.game.width = data.options.width;
                        this.game.height = data.options.height;
                        this.game.arr = data.game;
                        this.game.players = data.players;
                        this.game.rend();
                        break;
                    default:
                        break;
                }
            }
        };
        this.ws.onclose = (e) => {
            (e.code === 1000 ? console.log : console.warn)("ws close", e);
        };
        this.ws.onerror = (e) => {
            console.warn("ws error", e);
        };
    }
}