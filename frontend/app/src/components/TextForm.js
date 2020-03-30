import React from 'react'

class TextForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      value: ''
    }
  }

  handleChange = (event) => {
    this.setState({value: event.target.value});
  }

  handleSubmit = (event) => {
    event.preventDefault();
    this.props.callback(this.state.value);
  }

  render(){
    return (
      <form onSubmit={this.handleSubmit} className="input-form">
        <label>
          <h4>{this.props.label}:</h4>
          <input type="text" value={this.state.value} onChange={this.handleChange} />
        </label>
        <input className="new-input" type="submit" value="Submit" />
      </form>
    );
  }
}

export default TextForm;
