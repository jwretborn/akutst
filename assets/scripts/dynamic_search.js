import React, { Component } from 'react';
import ApiStore from './stores/api-store.js';

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
		this.handleStoreChange = this.handleStoreChange.bind(this);
		this.filterItems = this.filterItems.bind(this);
	}

	// Do initial loading
	componentWillMount() {
		ApiStore.addChangeListener(this.handleStoreChange);
		this.loadData();
	}

	componentWillUnmount() {
		ApiStore.removeChangeListener(this.handleStoreChange);
	}

	loadData() {
		var data = ApiStore.get(this.props.url);
		if (data !== 'loading') {
			this.setState({
				listItems : data.items
			})
		}
	}

	filterItems(items) {
		if (this.props.filterKey !== '') {
			items = items.filter(function(items){
				if (items[this.props.filterKey] == null) {
					if (this.props.filterValue === '') {
						return true;
					}
					else {
						return false;
					}
				}
				return items[this.props.filterKey].toLowerCase().match(this.props.filterValue);
			}.bind(this));
		}
		return items;
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
			if (this.props.changeCallback !== false && typeof this.props.changeCallback == 'function') {
				this.props.changeCallback(value, this.props.name);
			}
		}.bind(this); // bind to component
	}

	handleStoreChange() {
		this.loadData();
	}

	render() {
		var codes = this.filterItems(this.state.listItems);
		var searchString = this.state.searchString.trim().toLowerCase();
		var value = this.state.value;

		// filter countries list by value from input box
		if(searchString.length > 0){
			codes = codes.filter(function(codes){
				return codes[this.props.mapValue].toLowerCase().match( searchString );
			}.bind(this));	// bind to component
		}

		return (
			<div className="dynamic-search">
				<label htmlFor="retts" className="col-sm-2 control-label">{this.props.nameDisplay}</label>
				<div className="col-sm-4">
                	<input
                		type 		= "text"
                		className 	= "form-control"
                		value 		= { searchString }
                		onChange 	= { this.handleChange }
                		placeholder = "Search" />

                	<input
                		type 		= "hidden"
                		name 		= { this.props.name }
                		value 		= { value } />
				</div>
				<ul className={this.state.display + " list-group col-sm-6"}>
        			{ codes.map(function(code){
        				return (
        					<li
        						key 		= { code.id }
        						className 	= "list-group-item clickable"
        						value 		= { code[this.props.mapKey] }
        						onClick 	= { this.handleSelect(code[this.props.mapValue], code[this.props.mapKey]) } >
        						<span className="badge">{code[this.props.mapBadge]}</span>{code[this.props.mapValue]}
        					</li>
        				);
        			}.bind(this)) }
        		</ul>
			</div>
		);
	}
}

DynamicSearch.defaultProps = {
	mapValue		: 'name',
	mapBadge		: '',
	mapKey			: 'id',
	name 			: 'dynamic-search',
	nameDisplay		: 'Search',
	filterKey		: '',
	filterValue		: '',
	url				: '',
	changeCallback	: false
}
