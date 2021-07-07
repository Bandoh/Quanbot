import { handle_pause, handle_play } from "./handlers";

function switchActions(action,args){
    console.log(action)
    switch (action) {
        case 'pause_music':
            handle_pause(args)
            break;
        case 'play_music':
            handle_play(args)
            break;
        default:
            console.log("In Hanlde ",args)
            break;
    }

    // if (action=='pause_music') handle_pause(args)
    // else if (action=='play_music') handle_play(args)
}

export default switchActions