import React, { Component } from 'react';


export default class InputSelect extends Component {

	constructor(props) {
		super(props);
		this.state = {
			selectValue		: '',
			listItems		: []
		};

		this.handleSelect = this.handleSelect.bind(this);
	}

	componentWillMount() {
		$.get(this.props.url, function(data) {
			this.setState({listItems : data.items});
		}.bind(this));
	}

	handleSelect(event) {
		var elem = (typeof event.selectedIndex === "undefined" ? window.event.srcElement : event);
    	var value = elem.value || elem.options[elem.selectedIndex].value;

    	if (typeof this.props.onUpdate === 'function') {
    		for (var i=0; i<this.state.listItems.length; i++) {
    			if (this.state.listItems[i][this.props.mapKey] == value) {
    				this.props.onUpdate(value, this.state.listItems[i][this.props.mapValue]);
    				break;
    			}
    		}
    	}

		this.setState({
			selectValue : value
		});
	}

	render() {
		var items = this.state.listItems;

		return (
				 <div className={this.props.name + "form-group"}>
					<label for={this.props.name} className="col-sm-2 control-label">Ålder</label>
					<div className="col-sm-4">
					    <select 
					    	name={this.props.name} 
					    	className="form-control" 
					    	onChange={this.handleSelect}>
					    { items.map(function(item){
					    	return (
					            <option value={ item[this.props.mapKey] }>{ item[this.props.mapValue] }</option>
					    	);
					    }.bind(this)) }
					    </select>
					</div>
				</div>
			);
	}
}

InputSelect.defaultProps = {
	name 		: '',
	mapKey 		: 'id',
	mapValue	: 'name',
	url			: '',
	onUpdate	: ''
}