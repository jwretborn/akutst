import React, { Component } from 'react';
import DynamicSearch from './dynamic_search.js';
import InputSelect from './input_select.js';

export default class PatientForm extends Component {

	constructor(props) {
		super(props);
		this.state = {
			searchFilter : ''
		}

		this.handleAgeChange = this.handleAgeChange.bind(this);
	}

	componentWillMount() {

	}

	handleAgeChange(key, value) {
		if (value != 'Vuxen') {
			this.setState({searchFilter : 'ped'});
		}
		else {
			this.setState({searchFilter : ''});
		}
	}

	render() {
		var searchFilter = this.state.searchFilter;

		return (
				<div>
					<div className="form-group">
						<InputSelect url={'/api/group/ages/items'} name={'age'} onUpdate={this.handleAgeChange} />
					</div>
					<div className="form-group">
						<DynamicSearch url={ '/api/codes' } mapBadge={'type'} name={'retts'} nameDisplay={'Sökorsak'} filterKey={'type'} filterValue={searchFilter} />
					</div>
				</div>
			);
	}
}

PatientForm.defaultProps = {

}