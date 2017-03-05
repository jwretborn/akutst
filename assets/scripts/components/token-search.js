import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import ApiStore from '../stores/api-store.js';
import _ from 'underscore';

export default class TokenSearch extends Component {

  // Constructor
  constructor(props) {
    super(props);
    this.state = {
      searchString	: '',
      display			: 'hide',
      listItems		: [],
      value 			: '',
        selectedItems   : [],
        listIndexSel    : 0
    };

    // Bind functions
    this.handleChange = this.handleChange.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
    this.handleDeleteToken = this.handleDeleteToken.bind(this);
    this.handleKeyEvent = this.handleKeyEvent.bind(this);
    this.handleStoreChange = this.handleStoreChange.bind(this);
    this.applyFilter = this.applyFilter.bind(this);
    this.getSearchList = this.getSearchList.bind(this);
	}

	// Do initial loading
	componentWillMount() {
		ApiStore.addChangeListener(this.handleStoreChange);
		this.loadData();

        // Keys

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

  // Filter items based on the props filter key and on already selected items
  applyFilter(items) {
    items = items.filter(function(item){
      if (this.props.filterKey !== '') {
        // Check pre-specified filter-key
        if (item[this.props.filterKey] == null) {
          if (this.props.filterValue === '') {
            return true;
          }
          else {
            return false;
          }
        }
        // Check for match of the search-string
        return item[this.props.filterKey].toLowerCase().match(this.props.filterValue);
      }

      // Remove selected values
      return ! _.contains(_.pluck(this.state.selectedItems, this.props.mapValue), item[this.props.mapValue].toLowerCase());
    }.bind(this));

    return items;
  }

  getSearchList(items) {
    var codes = this.applyFilter(this.state.listItems);
    var searchString = this.state.searchString.trim().toLowerCase();

    // filter items list by value from input box
    if(searchString.length > 0){
      codes = codes.filter(function(codes){
        return codes[this.props.mapValue].toLowerCase().match( searchString );
      }.bind(this));	// bind to component
    }

    return codes;
  }

	// sets state, triggers render method
	handleChange(event) {
		var str = event.target.value;
		// grab value form input box
		this.setState({searchString:str});

		if (this.state.display === 'hide' && str.length > 0) {
			this.setState({
                display : 'show',
                listIndexSel : 0
            });
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
      // Add value
      var selected = this.state.selectedItems;
      selected.push({'name' : name.toLowerCase(), 'id' : value});

            // Update date
			this.setState({
				searchString	: '',
				display			: 'hide',
				value 			: _.pluck(selected, 'id'),
        selectedItems   : selected
			});

      // Check if we have a callback function to run
			if (this.props.changeCallback !== false && typeof this.props.changeCallback == 'function') {
				this.props.changeCallback(value, this.props.name);
			}

      // Return focus to the input
      ReactDOM.findDOMNode(this.refs.tokenInput).focus();
		}.bind(this); // bind to component
	}

    // Handles removal of tokens
    handleDeleteToken(id) {
      return function(event) {
        // Remove value
        var selected = this.state.selectedItems.filter((x) => x.id !== id);
        var value = _.pluck(selected, 'id');

        // Update state
        this.setState({
          'selectedItems' : selected,
          'value' : value
        });

        // Check if we have a callback function to run
        if (this.props.changeCallback !== false && typeof this.props.changeCallback == 'function') {
          this.props.changeCallback(value, this.props.name);
        }
      }.bind(this);
    }

    // Key handler
    handleKeyEvent(event) {
      if (event.key == 'ArrowDown') {
          // Key Down - move selector down, if not bottom
          if (this.state.listIndexSel < (this.getSearchList().length - this.state.selectedItems.length - 1)) {
              this.setState({
                  'listIndexSel' : this.state.listIndexSel+1
              });
          }
      }
      else if (event.key == 'ArrowUp') {
        // Key Up - move selector up, if not to
        if (this.state.listIndexSel > 0) {
          this.setState({
            'listIndexSel' : this.state.listIndexSel-1
          });
        }
      }
      else if (event.key == 'Enter') {
        // Enter - select item
        var selected = this.state.selectedItems;

        var list = this.getSearchList();
        if (list.length > 0) {
          var item = list[this.state.listIndexSel];
          var name = item[this.props.mapValue];
          var value = item[this.props.mapKey];
          // Add value
          selected.push({'name' : name.toLowerCase(), 'id' : value});
        }
        else if (this.props.canAdd === true) {
          // add value
          var elem = (typeof event.selectedIndex === "undefined" ? event.target : event);
          var value = elem.value || elem.options[elem.selectedIndex].value;
          console.log('add value');
          selected.push({'name' : value.toLowerCase(), 'id' : value.toLowerCase()});
        }
        else {
          // error
          console.log('hepp');
        }

        // Update date
        this.setState({
          searchString	: '',
          display			: 'hide',
          value 			: _.pluck(selected, 'id'),
          selectedItems : selected
        });


        // Check if we have a callback function to run
        if (this.props.changeCallback !== false && typeof this.props.changeCallback == 'function') {
          this.props.changeCallback(value, this.props.name);
        }
      }
      else if (event.key == 'Backspace') {
        // Backspace - If no search string, remove token
        if (this.state.searchString == '') {
        // Remove last
        this.state.selectedItems.pop();

        // Update state
        this.setState({
          'selectedItems' : this.state.selectedItems,
          'value' : _.pluck(selected, 'id')
        });

        // Check if we have a callback function to run
        if (this.props.changeCallback !== false && typeof this.props.changeCallback == 'function') {
          this.props.changeCallback(value, this.props.name);
        }
      }
    }
  }

    // Dummy callback
	handleStoreChange() {
		this.loadData();
	}

    // Render function
	render() {
		var codes = this.getSearchList();
		var searchString = this.state.searchString.trim().toLowerCase();
		var value = this.state.value;
    var selected = this.state.selectedItems;

		return (
			<div
				className="token-search form-group"
				onKeyUp= {this.handleKeyEvent}>
				<label htmlFor="retts" className="col-sm-2 control-label">{this.props.nameDisplay}</label>
				<div className="input-area col-sm-6">
					{ selected.map(function(item) {
						return (
					<div
						key 		= { item.id }
						className 	= "token">
						<div className="token-name">
						{item.name}
						</div>
						<div
							className="token-close"
							onClick= { this.handleDeleteToken(item.id)}>
							x
						</div>
					</div>)
					}.bind(this)) }
					<input
						type 		= "text"
						ref         = "tokenInput"
						className 	= "token-input"
						value 		= { searchString }
						onChange 	= { this.handleChange }
						disabled	= { this.props.singleValue && selected.length > 0 }
                        placeholder = "Search" />

                    <input
                        type 		= "hidden"
                        name 		= { this.props.name }
                        value 		= { value } />
                </div>
                <div
                    className   =   {this.state.display + " list-area list-group col-sm-6"}
                    ref         =   "filteredList">
        			{ codes.map(function(code, index){
        				return (
        					<div
        						key 		= { code.id }
        						className 	= { "list-group-item clickable" + (index == this.state.listIndexSel ? ' selected' : '')}
        						value 		= { code[this.props.mapKey] }
        						onClick 	= { this.handleSelect(code[this.props.mapValue], code[this.props.mapKey]) } >
        						<span className="badge">{code[this.props.mapBadge]}</span>{code[this.props.mapValue]}
        					</div>
        				);
        			}.bind(this)) }
        		</div>
			</div>
		);
	}
}

TokenSearch.defaultProps = {
	mapValue		: 'name',
	mapBadge		: '',
	mapKey			: 'id',
	name 			: 'dynamic-search',
	nameDisplay		: 'Search',
	singleValue		: false,
	filterKey		: '',
	filterValue		: '',
  canAdd        : false,
	url				: '',
	changeCallback	: false
}
