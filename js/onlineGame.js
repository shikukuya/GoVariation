class OnlineGame {
    constructor(url) {
        this.ws = new WebSocket(url || "ws://127.0.0.1:34777");
        this.ws.onopen = function () {
            alert("ws连接成功");
            this.ws.send("test");
        };
        this.ws.onmessage = function (e) {
            alert(e.data)
        };
    }
}
new OnlineGame()