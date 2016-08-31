import React, { Component } from 'react';
import ApiStore from '../stores/api-store.js';
import { Navbar, Nav, NavItem, NavDropdown, MenuItem, Table } from 'react-bootstrap'

export default class StatisticsTable extends Component {

	constructor(props) {
		super(props);

		this.state = {
            'listItems' : [],
			'groupBy'	: false
		}

        this.handleStoreChange = this.handleStoreChange.bind(this);
		this.handleGroupBySelectChange = this.handleGroupBySelectChange.bind(this);
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

    handleStoreChange() {
		this.loadData();
	}

	handleGroupBySelectChange(key, event) {
		this.setState({
			groupBy : key
		})
	}

	groupItems(items, groupKey) {
		var list = [];
		if (groupKey === false) {
			return items;
		}

		items.map(function(item) {
			var found = false;
			list.map(function(listItem) {
				if (listItem['name'] == item[groupKey]) {
					listItem['count'] += 1;
					found = true;
				}
			})
			if ( found === false) {
				list.push({'name':item[groupKey], 'count':1})
			}
		})

		return list;
	}

	render() {
		var list = this.groupItems(this.state.listItems, this.state.groupBy);
		var keys = (this.state.groupBy !== false) ? ['name', 'count'] : this.props.keys;

		return (
			<div>
				<Navbar>
    				<Navbar.Header>
        				<Navbar.Brand>
            				{ this.props.name }
            			</Navbar.Brand>
        			</Navbar.Header>
					<Nav>
     					<NavDropdown title="Gruppera efter" id="basic-nav-dropdown">
          					{ this.props.groupBy.map(key => (
								<MenuItem
									eventKey={key}
									onSelect={this.handleGroupBySelectChange}>{key}
									</MenuItem>
							))}
							<MenuItem divider />
							<MenuItem
								eventKey={false}
								onSelect={this.handleGroupBySelectChange}>Reset
								</MenuItem>
          				</NavDropdown>
     				</Nav>
    			</Navbar>
			<Table striped hover condensed>
				<thead>
    				<tr>
        				{ keys.map(key => (
							<th>{key}</th>
						))}
        			</tr>
    			</thead>
				<tbody>
            { list.map(function(item) {
            	return (
                	<tr>
						{ keys.map(key => (
							<td>{item[key]}</td>
						)) }
                	</tr>
                )
            }.bind(this))}
				</tbody>
			</Table>
			</div>
		);
	}
}

StatisticsTable.defaultProps = {
	name			: 'Table',
    url				: 'diagnostics/procedures',
	keys			: ['id', 'name'],
	groupBy			: ['Name']
}
