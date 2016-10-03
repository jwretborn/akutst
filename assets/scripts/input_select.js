import React, { Component } from 'react';
import ApiStore from './stores/api-store.js';

export default class InputSelect extends Component {

	constructor(props) {
		super(props);
		this.state = {
			selectValue		: '',
			listItems		: []
		};

		this.handleSelect = this.handleSelect.bind(this);
		this.handleStoreChange = this.handleStoreChange.bind(this);
	}

	componentWillMount() {
		ApiStore.addChangeListener(this.handleStoreChange);
		this.loadData();
	}

	componentWillUnmount() {
		ApiStore.removeChangeListener(this.handleStoreChange);
	}

	componentWillReceiveProps(nextProps) {
		if (nextProps.url !== this.props.url) {
			this.loadData(nextProps.url);
		}
	}

	loadData(url) {
		if (url === undefined) {
			url = this.props.url;
		}
		var data = ApiStore.get(url);

		if (data !== 'loading') {
			this.setState({
				listItems : data.items
			});
		}
	}

	handleStoreChange() {
		this.loadData();
	}

	handleSelect(event) {
		var elem = (typeof event.selectedIndex === "undefined" ? event.target : event);
    	var value = elem.value || elem.options[elem.selectedIndex].value;

    	if (typeof this.props.onUpdate === 'function') {
    		for (var i=0; i<this.state.listItems.length; i++) {
    			if (this.state.listItems[i][this.props.mapKey] == value) {
    				this.props.onUpdate(value, this.state.listItems[i][this.props.mapValue], this.props.name);
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
					<label htmlFor={this.props.name} className="col-sm-2 control-label">{ this.props.label }</label>
					<div className="col-sm-4">
					    <select
					    	name={this.props.name}
					    	className="form-control"
					    	onChange={this.handleSelect}>
					    { items.map(function(item){
					    	return (
					            <option
					            	key 	= { item.id }
					            	value 	= { item[this.props.mapKey] } >
					            	{ item[this.props.mapValue] }
					            </option>
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
	label 		: 'Select',
	mapKey 		: 'id',
	mapValue	: 'name',
	url			: '',
	onUpdate	: ''
}
