import React from 'react'
import switchActions from '../common_functions/action_switch';






class ChatDialogue extends React.Component {
    constructor(props) {
        super(props)
        this.state = { allText: props.dialogue }
        let all_data = {}


        this.r_text = (allText) =>
        
            allText.map(function (data) {
                let isAction = false
                const s = { color: "white", textAlign: "left", listStyle: 'none', backgroundColor: 'grey', margin: '5px', padding: '20px', fontSize: '10px',borderRadius:"5px" }
                if (data['name'] !== 'Quanbot') {
                    s.textAlign = 'right'
                    s.backgroundColor = 'pink'
                    s.color = 'black'
                }

                if(data['action'] && data['id']== allText.length-1){
                    switchActions(data['action'][0], all_data)
                }
                if (data['type'] == "text")    {
                    return <li key={data['id']} style={s}> {data['msg']}</li>
                }
                else if (data['type'] == "mp3") {
                    all_data['last_media_id'] = data['id']
                    return <div style={s} key={data['id']}><div style={{ paddingBottom: "20px", fontSize: "12px" }}>{data['extra_info']}</div><audio id={data['id']} controls autoPlay> <source ti src={data['msg']}></source></audio> </div>
                }


            })



    }
    componentWillReceiveProps(props) {
        let newData = props.dialogue
        this.setState({ allText: newData })
    }
    render() {
        return (<div style={{
            display: "flex",
            flexDirection: "column-reverse",
            overflowY: "auto",
            overflowX: "hidden",
            height: "80%"
        }}>{this.r_text(this.state.allText)}</div>)
    }
}


export default ChatDialogue

