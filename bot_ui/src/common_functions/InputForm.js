import React from 'react'
import switchActions from './action_switch'

let url = 'http://localhost:5000'

class InputForm extends React.Component {

  constructor(props) {
    super(props)


    this.state = { cb: props.setIt }

    this.getText = async (e) => {
      e.preventDefault()
      const data = document.getElementById('user_text').value
      if (data) {
        let t = { name: "Kelvin", msg: data, id: this.props.dialogue.length, "type": "text" }
        this.state.cb(t)
        document.getElementById('user_text').value = ""
        let d = await post_f(url + "/msg", t)
        this.state.cb({ name: "Quanbot", msg: d['message']['data'], "type": d['message']['type'], id: this.props.dialogue.length , "action":d['message']['action'],
        "extra_info":d['message']['extra_info']})

      }
    }

  }
  componentDidMount() {
    document.getElementById('user_text').focus()
  }

  render() {
    return (
      <div>
        <span >
          <form onSubmit={this.getText}>
            <input style={{ width: "70%" }} id="user_text"></input><button type="submit" style={{ width: "20%" }}>SEND</button>
          </form>
        </span>
      </div>
    );
  }
}

export default InputForm


async function post_f(ur, data) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  };
  let s = await (await fetch(ur, requestOptions)).json()
  return s
}