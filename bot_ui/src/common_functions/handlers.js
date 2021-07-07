function handle_play(data) {
    console.log("IN PLAY",data)
    let nd = document.getElementById(data['last_media_id'])
    console.log(nd)
    nd.play() 
}

function handle_pause(data) {

    console.log("IN PAUSE",data)
    let nd = document.getElementById(data['last_media_id'])
    console.log(nd)
    nd.pause() 
}


module.exports = {handle_pause,handle_play}