import Particles from "react-tsparticles";
import React from 'react'
import './App.css';
import InputForm from './common_functions/InputForm'
import ChatDialogue from './chat_dialogue/ChatDialogue'
import switchActions from "./common_functions/action_switch";

const p_conf = require('./particleconfig.json')



class App extends React.Component {
  constructor(props) {
    super(props);

    let allText = [{
      "type": "text",
      "name": "Quanbot",
      "msg": "Tell me something",
      "id": 0,
      "action": [],
      "extra_info": []
    },
    ]

    this.state = { allText: allText }

    this.particlesInit = this.particlesInit.bind(this);
    this.particlesLoaded = this.particlesLoaded.bind(this);

    this.setIt = (data) => {
      this.setState(prev => ({
        allText: [data, ...prev.allText]
      }))

    
    }


  }

  particlesInit(main) {
    console.log(main);

    // you can initialize the tsParticles instance (main) here, adding custom shapes or presets
  }

  particlesLoaded(container) {
    console.log(container);
  }




  render() {
    return (
      <div className="App-header">
        <Particles
          id="tsparticles"
          init={this.particlesInit}
          loaded={this.particlesLoaded}
          options={p_conf}
        />
        <div className="bod">
          <h4>Quanbot </h4>
          <ChatDialogue dialogue={this.state.allText} ></ChatDialogue>
          <InputForm setIt={this.setIt} dialogue={this.state.allText} ></InputForm>
        </div>
      </div>
    );
  }


}




export default App



