import React, { Component } from 'react';

export default class DynamicSearch extends Component {

	// Constructor
	constructor(props) {
		super(props);
		this.state = { 
			searchString	: '', 
			display			: 'hide', 
			listItems		: [],
			value 			: ''
		};

		this.handleChange = this.handleChange.bind(this);
		this.handleSelect = this.handleSelect.bind(this);
	}

	// Do initial loading
	componentWillMount() {
		$.get(this.props.url, function(data) {
			this.setState({listItems : data.items});
		}.bind(this));
	}

	// sets state, triggers render method
	handleChange(event) {
		var str = event.target.value;
		// grab value form input box
		this.setState({searchString:str});

		if (this.state.display === 'hide' && str.length > 0) {
			this.setState({display : 'show'});
		}
		else {
			if (str.length === 0) {
				this.setState({display : 'hide'});
			}
		}
	}

	// Event to select a search item
	handleSelect(name, value) {
		// Will set the search item and close the list
		return function(event) {
			this.setState({
				searchString	: name, 
				display			: 'hide',
				value 			: value
			});
		}.bind(this); // bind to component
	}

	render() {
		var codes = this.state.listItems;
		var searchString = this.state.searchString.trim().toLowerCase();
		var value = this.state.value;

		// filter countries list by value from input box
		if(searchString.length > 0){
			codes = codes.filter(function(codes){
				return codes[this.props.mapName].toLowerCase().match( searchString );
			}.bind(this));	// bind to component
		}

		return (
			<div className="dynamic-search">
				<label for="retts" className="col-sm-2 control-label">{this.props.nameDisplay}</label>
				<div className="col-sm-4">
                	<input 
                		type="text" 
                		className="form-control" 
                		value={searchString} 
                		onChange={this.handleChange} 
                		placeholder="Search" />

                	<input type="hidden" name={this.props.name} value={value} />
				</div>
				<ul className={this.state.display + " list-group col-sm-6"}>
        			{ codes.map(function(code){ 
        				return (
        					<li 
        						className="list-group-item clickable" 
        						value={code[this.props.mapValue]} 
        						onClick={this.handleSelect(code[this.props.mapName], code[this.props.mapValue])}>
        						<span className="badge">{code[this.props.mapBadge]}</span>{code[this.props.mapName]} 
        					</li> 
        				);
        			}.bind(this)) }
        		</ul>
			</div>
		);
	}
}

DynamicSearch.defaultProps = {
	mapName			: 'name',
	mapBadge		: '',
	mapValue		: 'id',
	name 			: 'dynamic-search',
	nameDisplay		: 'Search',
}